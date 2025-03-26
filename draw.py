import pyMeow as pm
import math
def drawBox(pos2d, center, width, head, color):
    pm.draw_rectangle_lines(
        posX=pos2d["x"] - center,
        posY=pos2d["y"] - center / 2,
        width=width,
        height=head + center / 2,
        color=color,
        lineThick=1.2,
    )
        
def drawShadow(pos2d, center, width, head, color):
    pm.draw_rectangle(
        posX=pos2d["x"] - center,
        posY=pos2d["y"] - center / 2,
        width=width,
        height=head + center / 2,
        color=pm.fade_color(color, 0.7),
    )
    
def drawName(pos2d, center, width, head, name, color):
    textSize = pm.measure_text(name, 15) / 2
    pm.draw_text(
        text=name,
        posX=pos2d["x"] - textSize,
        posY=pos2d["y"] - 24,
        fontSize=15,
        color=color,
    )

def snapLine(pos2d, center, width, head, name, color):
    dark_color = pm.get_color("black")
    pm.draw_line(
        pm.get_screen_width() / 2,
        1,
        pos2d["x"] - center,
        pos2d["y"] - center / 2,
        dark_color,
        3
    )
    pm.draw_line(
        pm.get_screen_width() / 2,
        1,
        pos2d["x"] - center,
        pos2d["y"] - center / 2,
        color,
    )
    
def corner(pos2d, center, width, head, color):
    corner_length = 10  
    thickness = 2       

    pm.draw_line(
        pos2d["x"] - center,
        pos2d["y"] - center / 2,
        pos2d["x"] - center + corner_length,
        pos2d["y"] - center / 2,
        color,
        thickness
    )
    pm.draw_line(
        pos2d["x"] - center,
        pos2d["y"] - center / 2,
        pos2d["x"] - center,
        pos2d["y"] - center / 2 + corner_length,
        color,
        thickness
    )                     
    pm.draw_line(
        pos2d["x"] - center + width,
        pos2d["y"] - center / 2,
        pos2d["x"] - center + width - corner_length,
        pos2d["y"] - center / 2,
        color,
        thickness
    )
    pm.draw_line(
        pos2d["x"] - center + width,
        pos2d["y"] - center / 2,
        pos2d["x"] - center + width,
        pos2d["y"] - center / 2 + corner_length,
        color,
        thickness
    )                          
    pm.draw_line(
        pos2d["x"] - center,
        pos2d["y"] - center / 2 + head + center / 2,
        pos2d["x"] - center + corner_length,
        pos2d["y"] - center / 2 + head + center / 2,
        color,
        thickness
    )
    pm.draw_line(
        pos2d["x"] - center,
        pos2d["y"] - center / 2 + head + center / 2,
        pos2d["x"] - center,
        pos2d["y"] - center / 2 + head + center / 2 - corner_length,
        color,
        thickness
    )                      
    pm.draw_line(
        pos2d["x"] - center + width,
        pos2d["y"] - center / 2 + head + center / 2,
        pos2d["x"] - center + width - corner_length,
        pos2d["y"] - center / 2 + head + center / 2,
        color,
        thickness
    )
    pm.draw_line(
        pos2d["x"] - center + width,
        pos2d["y"] - center / 2 + head + center / 2,
        pos2d["x"] - center + width,
        pos2d["y"] - center / 2 + head + center / 2 - corner_length,
        color,
        thickness
    )

def drawHealthBar(pos2d, center, width, head, health, max_health=100):
    bar_width = 5
    bar_height = head + center / 2
    health_percent = health / max_health
    
    pm.draw_rectangle(
        posX=pos2d["x"] - center - bar_width - 3,
        posY=pos2d["y"] - center / 2,
        width=bar_width,
        height=bar_height,
        color=pm.get_color("black"),
    )

    pm.draw_rectangle(
        posX=pos2d["x"] - center - bar_width - 3,
        posY=pos2d["y"] - center / 2 + bar_height * (1 - health_percent),
        width=bar_width,
        height=bar_height * health_percent,
        color=pm.get_color("green") if health > 50 else pm.get_color("yellow") if health > 25 else pm.get_color("red"),
    )

def drawArmorBar(pos2d, center, width, head, armor, max_armor=100):
    bar_width = 5
    bar_height = head + center / 2
    armor_percent = armor / max_armor
    
    pm.draw_rectangle(
        posX=pos2d["x"] - center - bar_width - 8,
        posY=pos2d["y"] - center / 2,
        width=bar_width,
        height=bar_height,
        color=pm.get_color("black"),
    )
    
    pm.draw_rectangle(
        posX=pos2d["x"] - center - bar_width - 8,
        posY=pos2d["y"] - center / 2 + bar_height * (1 - armor_percent),
        width=bar_width,
        height=bar_height * armor_percent,
        color=pm.get_color("cyan"),
    )

def drawDistance(pos2d, center, width, head, pos3d, player_pos3d, color):
    distance = calculate_distance(player_pos3d, pos3d)
    
    text = f"{distance:.1f}m"
    textSize = pm.measure_text(text, 15) / 2
    
    pm.draw_text(
        text=text,
        posX=pos2d["x"] - textSize,
        posY=pos2d["y"] + head + center / 2 + 5,
        fontSize=15,
        color=color,
    )

def drawRadar(radar_x, radar_y, radar_size, radar_zoom, local_pos, local_angle, entities, background_color, border_color, player_color, team_color, enemy_color):

    pm.draw_rectangle(
        posX=radar_x,
        posY=radar_y,
        width=radar_size,
        height=radar_size,
        color=background_color
    )

    pm.draw_rectangle_lines(
        posX=radar_x,
        posY=radar_y,
        width=radar_size,
        height=radar_size,
        color=border_color,
        lineThick=2
    )
    
    center_x = radar_x + radar_size / 2
    center_y = radar_y + radar_size / 2
    
    pm.draw_circle(
        center_x,
        center_y,
        5,
        player_color
    )
    
    direction_length = 10
    direction_x = center_x
    direction_y = center_y - direction_length
    
    pm.draw_line(
        startPosX=center_x,
        startPosY=center_y,
        endPosX=direction_x,
        endPosY=direction_y,
        color=player_color,
        thick=2
    )
    
    for entity in entities:
        if entity.health <= 0:
            continue

        rel_x = entity.pos3d["x"] - local_pos["x"]
        rel_y = entity.pos3d["y"] - local_pos["y"]
        
        angle_rad = math.radians(local_angle)
        rot_x = rel_x * math.cos(angle_rad) - rel_y * math.sin(angle_rad)
        rot_y = rel_x * math.sin(angle_rad) + rel_y * math.cos(angle_rad)
        
        scaled_x = rot_x * (40 / radar_zoom)
        scaled_y = rot_y * (40 / radar_zoom)
        
        radar_pos_x = center_x + scaled_x
        radar_pos_y = center_y - scaled_y 
        
       
        if (radar_pos_x >= radar_x and radar_pos_x <= radar_x + radar_size and
            radar_pos_y >= radar_y and radar_pos_y <= radar_y + radar_size):

            entity_color = team_color if entity.team else enemy_color
            pm.draw_circle(
                radar_pos_x,
                radar_pos_y,
                4,
                entity_color
            )

def drawFov(fov, color):
    pm.draw_circle(
        posX=pm.get_screen_width() / 2,
        posY=pm.get_screen_height() / 2,
        radius=fov,
        color=color
    )

def calculate_distance(pos1, pos2):
    
    dx = pos2["x"] - pos1["x"]
    dy = pos2["y"] - pos1["y"]
    dz = pos2["z"] - pos1["z"]
    
    return (dx**2 + dy**2 + dz**2)**0.5




