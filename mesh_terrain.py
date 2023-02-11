from ursina import *
from random import randrange
from perlin import Perlin
class MeshTerrain:
    def __init__(this):

        this.block = load_model('block.obj')
        this.textureAtlas = 'texture_atlas_3.png'
        this.subsets = []
        this.numSubsets = 1
        this.subWidth = 32
        # terrain dictionary :O
        this.td = {}
        this.perlin = Perlin()

        for i in range(0,this.numSubsets):
            e = Entity(model = Mesh(), 
            texture=this.textureAtlas)
            e.texture_scale*=64/e.texture.width
            this.subsets.append(e)

    def genBlock(this,x,y,z):
        # Add to the verticies of our subset
        model = this.subsets[0].model
        model.vertices.extend([Vec3(x,y,z) + v for v in this.block.vertices])  
        uu = 8
        uv = 7
        if y > 2 :
            uu = 8
            uv = 6
        model.uvs.extend([Vec2(uu,uv) + u for u in this.block.uvs])
        # Record The terrain in a dictionary :<
        this.td ["x"+str(floor(x))+
                 "y"+str(floor(y))+
                 "z"+str(floor(z))] = "t" # Rounds down the values for x,y,z so that they dont become 7.8948

    def genTerrain(this):
        x = 0
        z = 0

        d = int(this.subWidth * 0.5)

        for k in range(-d,d):
            for j in range(-d,d):
                y = floor(this.perlin.get_height(x+k,z+j))
                this.genBlock(x+k,y,z+j)
        this.subsets[0].model.generate()        