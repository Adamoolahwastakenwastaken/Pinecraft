from ursina import Entity,Vec3
from random import random

class Flake(Entity):
    def __init__(this,origin):
        super().__init__(
            model='quad',
            texture = 'assets/flake_1.png',
            position=origin,
            double_sided = True,
            scale=1
        )
        this.x+=random()*20-10
        this.y+=random()*10
        this.z+=random()*20-10