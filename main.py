from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from mesh_terrain import MeshTerrain

app = Ursina()

window.color = color.rgb(0,200,255)
indra = Sky()
indra.color = window.color

player = FirstPersonController()
player.gravity = 0.0
player.cursor.visible = False
window.fullscreen = False

terrain = MeshTerrain()

px = player.x
pz = player.z

count = 1
def update():
    global count, px, pz
    count+= 1
    if count == 2: 
        terrain.genTerrain()
        count = 0
    
    if abs(player.x - px) > 4 or abs(player.z - pz) > 4:
        px = player.x
        pz = player.z
        terrain.swirlengine.reset(px,pz)
    blockFound = False
    step = 2
    height = 1.86
    x = str(floor(player.x+.5))
    z = str(floor(player.z+.5))
    y = floor(player.y+.5)

    for i in range(-step,step):
        if terrain.td.get("x"+x+"y"+str(y+i)+"z"+z) == "t":
            target = y+i+height
            blockFound = True
            break
    if blockFound == True:
        # go up / down depending on position
        player.y = lerp(player.y,target,6* time.dt)
    else:
        # Gravity lol 
        player.y -= 9.8 * time.dt    
   

app.run()