from ursina import Entity,Vec3,time
from random import random

class Flake(Entity):
    def __init__(this,origin):
        super().__init__(
            model='quad',
            texture = 'assets/flake_1.png',
            position=origin,
            double_sided = True,
            scale=.3
        )
        this.x+=random()*20-10
        this.y+=random()*10+5
        this.z+=random()*20-10
        this.minSpeed = .6
        this.fallSpeed = random()*4.5+this.minSpeed
        this.spinSpeed = random()*4

    def pyhsics(this,pPos):
       this.y-=this.fallSpeed*time.dt

       this.rotation_y += this.spinSpeed * time.dt
       if this.y<0:
        this.x=pPos.x+random()*40-20
        this.y+=pPos.y+random()*40-20
        this.z+=pPos.z+random()*10+5
