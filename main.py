from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from mesh_terrain import MeshTerrain
from pypresence import Presence
from datetime import datetime
import pygame
from flake import Flake

app = Ursina()


window.color = color.rgb(0,200,255)
indra = Sky()
indra.color = window.color

player = FirstPersonController()
player.gravity = 0.0
player.cursor.visible = False
window.fullscreen = False

date_string = '2023-12-25'


terrain = MeshTerrain()
# run only if its christmas see line 21
if datetime.now() == date_string:
    flakes = []

    for i in range(32):
        e = Flake(player.position) # works cuz our Flake is an entity with a Vector3
        flakes.append(e)
FPS = 60


px = player.x
pz = player.z

def input(key):
    terrain.input(key)

# RPC STUFF
#def rpc():
   # CLIENT_ID = 1074326950493036584
   # RPC = Presence(CLIENT_ID) # initialize client class
   # RPC.connect() # handshake loop start
   # print(RPC.update(state="Playing", details="Definetely not a minecraft rip-off", start = time.time() - start_time, end = 2+2 ))  # Set the presence    


count = 1
def update():  
    global count, px, pz
    count+= 1
    if count == 2: 
        terrain.genTerrain()
        count = 0

    terrain.update(player.position,camera)    
    
    if abs(player.x - px) > 4 or abs(player.z - pz) > 4:
        px = player.x
        pz = player.z
        terrain.swirlEngine.reset(px,pz)
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
app.step()
app.run()