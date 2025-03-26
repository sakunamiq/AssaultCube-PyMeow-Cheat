import pyMeow as pm
from memory import AccessGame, rMemory
from draw import *
from colorama import Fore
import offsets
import time
import os
import math

proc, base = AccessGame()

class Colors:
    cyan = pm.get_color("cyan")
    orange = pm.get_color("orange")
    purple = pm.get_color("purple")
    white = pm.get_color("white")
    black = pm.get_color("black")
    green = pm.get_color("green")
    yellow = pm.get_color("yellow")
    red = pm.get_color("red")
    
class entityList:
    def __init__(self, addr):
        self.addr = addr
        health, name, armor, team, pos3d, fpos3d, pos2d, fpos2d, head, width, center = rMemory(proc, addr)

        self.health = health
        self.name = name
        self.armor = armor
        self.team = team
        self.pos3d = pos3d
        self.fpos3d = fpos3d
        self.pos2d = pos2d
        self.fpos2d = fpos2d
        self.head = head
        self.width = width
        self.center = center
        self.color = Colors.cyan if self.team else Colors.purple
    
    def wts(self, vm):
        try:
            self.pos2d = pm.world_to_screen(vm, self.pos3d)
            self.fpos2d = pm.world_to_screen(vm, self.fpos3d)
            self.head = self.fpos2d["y"] - self.pos2d["y"]
            self.width = self.head / 2
            self.center = self.width / 2
            return True
        except:
            return False
class Menu:
    def __init__(self):
        self.draw = False
        self.current_tab = "Visual"
        self.visual_subtab = "Enemy"  
        self.menu_key = 0x24  # Home key
        self.use_alt_combo = False  # No longer using Alt combination
        if os.name == "posix":
            self.menu_key = 0xff63
            self.use_alt_combo = False
        
        ## AIMBOT
        self.aimbot = False
        self.show_fov = False
        self.aimbot_fov = 250   
        self.fov_color = Colors.red
        self.triggerbot = False
        
        ## ENEMY
        self.box = False
        self.namedisplay = False
        self.snapline = False
        self.cornerbox = False
        self.shadow = False
        self.healthbar = False
        self.armorbar = False
        self.distancedisplay = False
        
        self.box_color = Colors.red
        self.cornerbox_color = Colors.cyan
        self.snapline_color = Colors.white
        self.name_color = Colors.white
        self.shadow_color = Colors.black
        self.distance_color = Colors.white
        
        ## TEAM
        self.team_box = False
        self.team_namedisplay = False
        self.team_snapline = False
        self.team_cornerbox = False
        self.team_shadow = False
        self.team_healthbar = False
        self.team_armorbar = False
        self.team_distancedisplay = False
        
        self.team_box_color = Colors.green
        self.team_cornerbox_color = Colors.cyan
        self.team_snapline_color = Colors.white
        self.team_name_color = Colors.white
        self.team_shadow_color = Colors.black
        self.team_distance_color = Colors.white
        
        ## RADAR
        self.radar = False
        self.radar_size = 200
        self.radar_zoom = 40  
        self.radar_position_x = 20
        self.radar_position_y = 20
        self.radar_background_color = pm.fade_color(Colors.black, 0.7)
        self.radar_border_color = Colors.white
        self.radar_enemy_color = Colors.red
        self.radar_team_color = Colors.green
        self.radar_player_color = Colors.cyan
        
        ## MEMORY
        self.infhealth = False
        self.infarmor = False
        self.infammo = False
        self.fovchanger = False
        self.dfov = 90
        self.show_info = False
        
    def draw_menu(self):
        window_box = pm.gui_window_box(
            posX=200,
            posY=200,
            width=400,
            height=430,
            title="Pidoras Cheat"
        )
        if window_box:
            draw = False
            pm.toggle_mouse()
        
        if pm.gui_button(200+10, 200+20, 80, 30, "Aim"):
            self.current_tab = "Aim"
        if pm.gui_button(200+150, 200+ 20, 80, 30, "Visual"):
            self.current_tab = "Visual"
        if pm.gui_button(200+300, 200+20, 80, 30, "Misc"):  
            self.current_tab = "Misc"
        
        if self.current_tab == "Aim":
            self.aimbot = pm.gui_check_box(posX=210, posY=270, width=20, height=20, text="Aimbot", checked=self.aimbot)
            self.show_fov = pm.gui_check_box(posX=210, posY=300, width=20, height=20, text="Show Fov", checked=self.show_fov)
            self.triggerbot = pm.gui_check_box(posX=210, posY=360, width=20, height=20, text="Triggerbot", checked=self.triggerbot)
            
            self.aimbot_fov_slider = pm.gui_slider(posX=220, posY=330, width=100, height=20, textLeft="50", textRight="800", value=self.aimbot_fov, minValue=50, maxValue=800)

            self.fov_color = pm.gui_color_picker(posX=340, posY=300, width=30, height=20, id=1)
            
            if self.aimbot_fov_slider != self.aimbot_fov:
                self.aimbot_fov = self.aimbot_fov_slider
                
        elif self.current_tab == "Visual":
            pm.draw_text("Red ESP", 210, 270, 16, Colors.black)
            pm.draw_text("Blue ESP", 390, 270, 16, Colors.black)
            
            self.box = pm.gui_check_box(posX=210, posY=300, width=20, height=20, text="Box", checked=self.box)
            self.box_color = pm.gui_color_picker(posX=320, posY=300, width=30, height=20, id=1)
            
            self.cornerbox = pm.gui_check_box(posX=210, posY=330, width=20, height=20, text="Corner Box", checked=self.cornerbox)
            self.cornerbox_color = pm.gui_color_picker(posX=320, posY=330, width=30, height=20, id=2)
            
            self.snapline = pm.gui_check_box(posX=210, posY=360, width=20, height=20, text="SnapLine", checked=self.snapline)
            self.snapline_color = pm.gui_color_picker(posX=320, posY=360, width=30, height=20, id=3)
            
            self.namedisplay = pm.gui_check_box(posX=210, posY=390, width=20, height=20, text="Name", checked=self.namedisplay)
            self.name_color = pm.gui_color_picker(posX=320, posY=390, width=30, height=20, id=4)
            
            self.shadow = pm.gui_check_box(posX=210, posY=420, width=20, height=20, text="Filled Box", checked=self.shadow)
            self.shadow_color = pm.gui_color_picker(posX=320, posY=420, width=30, height=20, id=5)
            
            self.distancedisplay = pm.gui_check_box(posX=210, posY=450, width=20, height=20, text="Distance", checked=self.distancedisplay)
            self.distance_color = pm.gui_color_picker(posX=320, posY=450, width=30, height=20, id=6)
            
            self.armorbar = pm.gui_check_box(posX=210, posY=480, width=20, height=20, text="Armor Bar", checked=self.armorbar)
            self.healthbar = pm.gui_check_box(posX=210, posY=510, width=20, height=20, text="Health Bar", checked=self.healthbar)
            
            self.team_box = pm.gui_check_box(posX=390, posY=300, width=20, height=20, text="Box", checked=self.team_box)
            self.team_box_color = pm.gui_color_picker(posX=500, posY=300, width=30, height=20, id=7)
            
            self.team_cornerbox = pm.gui_check_box(posX=390, posY=330, width=20, height=20, text="Corner Box", checked=self.team_cornerbox)
            self.team_cornerbox_color = pm.gui_color_picker(posX=500, posY=330, width=30, height=20, id=8)
            
            self.team_snapline = pm.gui_check_box(posX=390, posY=360, width=20, height=20, text="SnapLine", checked=self.team_snapline)
            self.team_snapline_color = pm.gui_color_picker(posX=500, posY=360, width=30, height=20, id=9)
            
            self.team_namedisplay = pm.gui_check_box(posX=390, posY=390, width=20, height=20, text="Name", checked=self.team_namedisplay)
            self.team_name_color = pm.gui_color_picker(posX=500, posY=390, width=30, height=20, id=10)
            
            self.team_shadow = pm.gui_check_box(posX=390, posY=420, width=20, height=20, text="Filled Box", checked=self.team_shadow)
            self.team_shadow_color = pm.gui_color_picker(posX=500, posY=420, width=30, height=20, id=11)
            
            self.team_distancedisplay = pm.gui_check_box(posX=390, posY=450, width=20, height=20, text="Distance", checked=self.team_distancedisplay)
            self.team_distance_color = pm.gui_color_picker(posX=500, posY=450, width=30, height=20, id=12)
            
            self.team_armorbar = pm.gui_check_box(posX=390, posY=480, width=20, height=20, text="Armor Bar", checked=self.team_armorbar)
            self.team_healthbar = pm.gui_check_box(posX=390, posY=510, width=20, height=20, text="Health Bar", checked=self.team_healthbar)
                

                
        elif self.current_tab == "Misc":
            # Memory options
            self.infhealth = pm.gui_check_box(posX=210, posY=270, width=20, height=20, text="God Mode", checked=self.infhealth)
            self.infarmor = pm.gui_check_box(posX=210, posY=300, width=20, height=20, text="Infinite Armor", checked=self.infarmor)
            self.infammo = pm.gui_check_box(posX=210, posY=330, width=20, height=20, text="Infinite Ammo", checked=self.infammo)
            self.fovchanger = pm.gui_check_box(posX=210, posY=360, width=20, height=20, text="Fov Changer", checked=self.fovchanger)
            self.fovslider = pm.gui_slider(posX=230, posY=390, width=100, height=20, textLeft="80", textRight="180", value=self.dfov, minValue=80, maxValue=180)
            self.show_info = pm.gui_check_box(posX=210, posY=420, width=20, height=20, text="Show Info", checked=self.show_info)
            
            if self.fovslider != self.dfov:
                self.dfov = self.fovslider
                
            self.radar = pm.gui_check_box(posX=390, posY=270, width=20, height=20, text="Radar", checked=self.radar)
            
            if self.radar:
                
                self.radar_size_slider = pm.gui_slider(posX=390, posY=300, width=100, height=20, textLeft="100", textRight="300", value=self.radar_size, minValue=100, maxValue=300)
                if self.radar_size_slider != self.radar_size:
                    self.radar_size = self.radar_size_slider
                
                
                self.radar_zoom_slider = pm.gui_slider(posX=390, posY=330, width=100, height=20, textLeft="5", textRight="50", value=self.radar_zoom, minValue=5, maxValue=50)
                if self.radar_zoom_slider != self.radar_zoom:
                    self.radar_zoom = self.radar_zoom_slider
                
                
                self.radar_position_x_slider = pm.gui_slider(posX=390, posY=360, width=100, height=20, textLeft="10", textRight="500", value=self.radar_position_x, minValue=10, maxValue=500)
                if self.radar_position_x_slider != self.radar_position_x:
                    self.radar_position_x = self.radar_position_x_slider
                
                
                self.radar_position_y_slider = pm.gui_slider(posX=390, posY=390, width=100, height=20, textLeft="10", textRight="500", value=self.radar_position_y, minValue=10, maxValue=500)
                
                if self.radar_position_y_slider != self.radar_position_y:
                    self.radar_position_y = self.radar_position_y_slider
                
                
                self.radar_enemy_color = pm.gui_color_picker(posX=390, posY=420, width=30, height=20, id=13)
                pm.draw_text("Blue Color", 490, 420, 12, Colors.black)
                
                self.radar_team_color = pm.gui_color_picker(posX=390, posY=450, width=30, height=20, id=14)
                pm.draw_text("Red Color", 490, 450, 12, Colors.black)

def overlay():
    pm.overlay_init(target="AssaultCube", fps=144, trackTarget=True)
    print(Fore.GREEN + "[+] Оверлей загружен.")
    screen_x = pm.get_screen_height()
    f_screen_x = screen_x / 2
    menu = Menu()
    
    # Initialize variables to prevent UnboundLocalError
    local_player_addr = None
    player_count = 0
    local_player_pos = {"x": 0, "y": 0, "z": 0}
    
    while pm.overlay_loop():
        pm.begin_drawing()
        
        if (menu.use_alt_combo and pm.key_pressed(menu.menu_key) and pm.key_pressed(0x12)) or (not menu.use_alt_combo and pm.key_pressed(menu.menu_key)):
            menu.draw = not menu.draw
            pm.toggle_mouse()
            time.sleep(0.15)
        
        if menu.draw:
            menu.draw_menu()
        
        # Update player_count at the beginning to ensure it's always defined
        player_count = pm.r_int(proc, base + offsets.player_count)
        
        if menu.show_info:
            pm.draw_text("Pidoras Cheat", 10, 300, 20, Colors.green)
            pm.draw_fps(10, 325)
            if player_count > 1:
                enemy_count = player_count - 1
                pm.draw_text(f"Enemies: {enemy_count}", 10, 350, 20, Colors.green)
            if local_player_addr:
                camera_x = pm.r_float(proc, local_player_addr + offsets.PlayerCameraX)
                camera_y = pm.r_float(proc, local_player_addr + offsets.PlayerCameraY)
                pm.draw_text(f"View Angles: X:{camera_x:.2f} Y:{camera_y:.2f}", 10, 375, 20, Colors.green)
        
        if menu.show_fov:
            pm.draw_circle_lines(
                pm.get_screen_width() / 2,
                pm.get_screen_height() / 2,
                menu.aimbot_fov,
                menu.fov_color
            )
        
        if player_count > 1:
            ent_buffer = pm.r_ints(
                proc, pm.r_int(proc, base + offsets.entity_list), player_count
            )[1:]
            v_matrix = pm.r_floats(proc, base + offsets.view_matrix, 16)
            
            local_player_addr = pm.r_int(proc, base + offsets.local_player)
            local_player_pos = pm.r_vec3(proc, local_player_addr + offsets.pos)
            
            if menu.fovchanger:
                pm.w_float(proc, base + offsets.FOV, menu.dfov)
            
            if local_player_addr:
                try:
                    local_player = entityList(local_player_addr)
                    if menu.infhealth:
                        pm.w_int(proc, local_player_addr + offsets.health, 999)
                    if menu.infarmor:
                        pm.w_int(proc, local_player_addr + offsets.armor, 999)
                    if menu.infammo:
                        pm.w_int(proc, local_player_addr + offsets.AssaultAmmo, 999)
                        pm.w_int(proc, local_player_addr + offsets.SniperAmmo, 999)
                        pm.w_int(proc, local_player_addr + offsets.PistolAmmo, 999)
                        pm.w_int(proc, local_player_addr + offsets.GrenadeAmmo, 999)
                        pm.w_int(proc, local_player_addr + offsets.SubmachineAmmo, 999)
                        pm.w_int(proc, local_player_addr + offsets.Shotgun, 999)
                        
                except Exception as e:
                    print(Fore.RED + f"[!] Error: {e}")
                    pass
 
            is_enemy_in_crosshair = False
            screen_center_x = pm.get_screen_width() / 2
            screen_center_y = pm.get_screen_height() / 2
            
            for addr in ent_buffer:
                try:
                    ent = entityList(addr)
                    if ent.wts(v_matrix) and ent.health >= 1:
                        
                        if ent.team != local_player.team and menu.triggerbot:
                            
                            if (abs(ent.pos2d["x"] - screen_center_x) < ent.width / 2 and 
                                abs(ent.pos2d["y"] - screen_center_y) < ent.head / 2):
                                is_enemy_in_crosshair = True
                        
                        if ent.team:
                            if menu.team_box:
                                drawBox(ent.pos2d, ent.center, ent.width, ent.head, menu.team_box_color)
                            if menu.team_namedisplay:
                                drawName(ent.pos2d, ent.center, ent.width, ent.head, ent.name, menu.team_name_color)
                            
                            if menu.team_snapline:
                                snapLine(ent.pos2d, ent.center, ent.width, ent.head, ent.name, menu.team_snapline_color)
                            
                            if menu.team_cornerbox:
                                corner(ent.pos2d, ent.center, ent.width, ent.head, menu.team_cornerbox_color)
                                
                            if menu.team_shadow:
                                drawShadow(ent.pos2d, ent.center, ent.width, ent.head, menu.team_shadow_color)
                            
                            if menu.team_healthbar:
                                drawHealthBar(ent.pos2d, ent.center, ent.width, ent.head, ent.health)
                            
                            if menu.team_armorbar:
                                drawArmorBar(ent.pos2d, ent.center, ent.width, ent.head, ent.armor)
                            
                            if menu.team_distancedisplay:
                                drawDistance(ent.pos2d, ent.center, ent.width, ent.head, ent.pos3d, local_player_pos, menu.team_distance_color)
                            
                        
                        else:  
                                
                            if menu.box:
                                drawBox(ent.pos2d, ent.center, ent.width, ent.head, menu.box_color)
                            
                            if menu.namedisplay:
                                drawName(ent.pos2d, ent.center, ent.width, ent.head, ent.name, menu.name_color)
                            
                            if menu.snapline:
                                snapLine(ent.pos2d, ent.center, ent.width, ent.head, ent.name, menu.snapline_color)
                            
                            if menu.cornerbox:
                                corner(ent.pos2d, ent.center, ent.width, ent.head, menu.cornerbox_color)
                                
                            if menu.shadow:
                                drawShadow(ent.pos2d, ent.center, ent.width, ent.head, menu.shadow_color)
                            
                            if menu.healthbar:
                                drawHealthBar(ent.pos2d, ent.center, ent.width, ent.head, ent.health)
                            
                            if menu.armorbar:
                                drawArmorBar(ent.pos2d, ent.center, ent.width, ent.head, ent.armor)
                            
                            if menu.distancedisplay:
                                drawDistance(ent.pos2d, ent.center, ent.width, ent.head, ent.pos3d, local_player_pos, menu.distance_color)
                            
                except:
                    continue
            
            if menu.triggerbot:
                if is_enemy_in_crosshair:
                    pm.w_int(proc, local_player_addr + offsets.autoShoot, 1)
                else:
                    pm.w_int(proc, local_player_addr + offsets.autoShoot, 0)
                
            if menu.radar:
                local_angle = 0
                if local_player_addr:
                    local_angle = pm.r_float(proc, local_player_addr + offsets.PlayerCameraY)
                
                radar_entities = []
                for addr in ent_buffer:
                    try:
                        ent = entityList(addr)
                        if ent.health >= 1:
                            radar_entities.append(ent)
                    except:
                        continue
                
                drawRadar(
                    radar_x=menu.radar_position_x,
                    radar_y=menu.radar_position_y,
                    radar_size=menu.radar_size,
                    radar_zoom=menu.radar_zoom,
                    local_pos=local_player_pos,
                    local_angle=local_angle,
                    entities=radar_entities,
                    background_color=menu.radar_background_color,
                    border_color=menu.radar_border_color,
                    player_color=menu.radar_player_color,
                    enemy_color=menu.radar_team_color,
                    team_color=menu.radar_enemy_color
                )
                
        pm.end_drawing()
    
