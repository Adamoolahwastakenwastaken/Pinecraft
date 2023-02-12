from perlin_module import PerlinNoise
from random import randint

class Perlin:
    def __init__(this):
        this.seed = 23
        print(this.seed)
        this.octaves = 8
        this.freq = 256
        this.amp = 18

        this.pNoise_continental = PerlinNoise( seed=this.seed,
                                    octaves=1)

        this.pNoise_details = PerlinNoise(  seed=this.seed,
                                    octaves=this.octaves)
        

    def get_height(this,x,z):
        from math import sin
        y = 0
        y = this.pNoise_continental([x/512,z/512])*128
        y += this.pNoise_details([x/this.freq,z/this.freq])*this.amp
        
        # Apply some predictable surface variation.
        sAmp=0.33
        y+=sin(z)*sAmp
        y+=sin(x*0.5)*sAmp
        return y