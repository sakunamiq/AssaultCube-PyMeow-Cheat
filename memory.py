import pyMeow as pm
import offsets

def AccessGame():
    proc = pm.open_process("ac_client.exe")
    base = pm.get_module(proc, "ac_client.exe")["base"]
    return proc, base

def rMemory(proc, addr):
    
    health = pm.r_int(proc, addr + offsets.health)
    name = pm.r_string(proc, addr + offsets.name)
    armor = pm.r_int(proc, addr + offsets.armor)
    team = pm.r_int(proc, addr + offsets.team)
        
    pos3d = pm.r_vec3(proc, addr + offsets.pos)
    fpos3d = pm.r_vec3(proc, addr + offsets.fpos)
    pos2d = fpos2d = None
    head = width = center = None
    
    return health, name, armor, team, pos3d, fpos3d, pos2d, fpos2d, head, width, center

def view_matrix(mem):
    matrix = list()
    offset = 0
    for _ in range(16):
        matrix.append(mem.read_float(Pointer.view_matrix + offset))
        offset += 4
    return matrix

