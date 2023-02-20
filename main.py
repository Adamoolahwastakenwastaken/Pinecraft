from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from mesh_terrain import MeshTerrain
from pypresence import Presence
from datetime import datetime
from flake import Flake
from random import randint

app = Ursina()



window.color = color.rgb(0,200,255)
indra = Sky()
indra.color = window.color

player = FirstPersonController()
player.gravity = 0.0
player.cursor.visible = False
window.fullscreen = False



terrain = MeshTerrain()
flakes = []

for i in range(64):
    e = Flake(player.position) # works cuz our Flake is an entity with a Vector3
    flakes.append(e)
grass_audio = Audio('step.ogg',autoplay=False,loop=False)
snow_audio = Audio('snowStep.mp3',autoplay=False,loop=False)    


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


count = 0
def update():  
    global count, px, pz

    terrain.genTerrain()

    count+= 1
    if count == 4: 
        count = 0

        terrain.update(player.position,camera)    
    
    if abs(player.x - px) > 4 or abs(player.z - pz) > 4:
        px = player.x
        pz = player.z
        terrain.swirlEngine.reset(px,pz)
        if player.y > 4:
            if snow_audio.playing==False:
                snow_audio.pitch=randint(1,10)
                snow_audio.play()
        elif grass_audio.playing==False:
            grass_audio.pitch=randint(1,10)
            grass_audio.play()

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