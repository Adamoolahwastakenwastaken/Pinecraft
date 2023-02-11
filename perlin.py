from perlin_module import PerlinNoise

class Perlin:
    def __init__(this):
        this.seed = 23
        this.octaves = 3
        this.freq = 54
        this.amp = 12

        this.pNoise = PerlinNoise(seed = this.seed, 
                                  octaves = this.octaves)
    def get_height(this,x,z):
        y = 0
        y = this.pNoise([x/this.freq,z/this.freq])*this.amp
        return y    