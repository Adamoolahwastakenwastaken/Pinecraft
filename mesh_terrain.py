from ursina import *
from random import randrange, random
from perlin import Perlin
from swirl_engine import SwirlEngine

class MeshTerrain:
    def __init__(this):

        this.block = load_model('block.obj',use_deepcopy=True)
        this.textureAtlas = 'texture_atlas_3.png'
        this.numVertices = len(this.block.vertices)
        print(this.numVertices)
        this.subsets = []
        this.numSubsets = 128
        this.subWidth = 6 # should be even or we die of broken code !
        this.swirlengine = SwirlEngine(this.subWidth)
        this.currentSubset = 0
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
        model = this.subsets[this.currentSubset].model
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
        
        # 40-42 Chooses a random tint for the color of a block :yay:
        c = random()-.5
        model.colors.extend((Vec4(1-c,1-c,1-c,1),)*
                            this.numVertices)

    def genTerrain(this):
        x = this.swirlengine.pos.x
        z = this.swirlengine.pos.y

        d = int(this.subWidth * 0.5)

        for k in range(-d,d):
            for j in range(-d,d):
                y = floor(this.perlin.get_height(x+k,z+j))
                if this.td.get("x"+str(floor(x))+
                                "y"+str(floor(y))+
                                "z"+str(floor(z))) != "t":
                    this.genBlock(x+k,y,z+j)
        this.subsets[this.currentSubset].model.generate()
        # fix for "1: RecursionError: maximum recursion depth exceeded in comparison"
        if this.currentSubset<this.numSubsets-1:
            this.currentSubset+=1
        else: this.currentSubset=0
        this.swirlengine.move()       