from perlin import Perlin
from ursina import *
from random import random
from mining_sys import *
from swirl_engine import SwirlEngine

class MeshTerrain:
    def __init__(this):

        this.block = load_model('block.obj')
        this.textureAtlas = 'texture_atlas_3.png'

        this.subsets = []
        this.numSubsets = 256
        this.subWidth = 12
        # ***
        this.currentSubset=0
        this.count=0
        this.swirlEngine = SwirlEngine(this.subWidth)

        # Our terrain dictionary :D
        this.td = {}
        # Our vertex dictionary # mining system
        this.vd = {}

        this.perlin = Perlin()

        for i in range(this.numSubsets):
            e = Entity( model=Mesh(),
                        texture=this.textureAtlas)
            e.texture_scale*=64/e.texture.width
            this.subsets.append(e)

    def update(this,pos,cam):
        highlight(pos,cam,this.td)

    def input(this,key):
        if key=='left mouse up' and bte.visible:
            epi = mine(this.td,this.vd,this.subsets)
            if epi != None:
                this.genWalls(epi[0], epi[1])
                this.subsets[epi[1]].model.generate()
    
    # I.e. after mining, to create illusion of depth.
    def genWalls(this,epi,subset):
        if epi==None: return
        # Refactor this -- place in mining_system 
        # except for cal to genBlock?
        wp =    [   Vec3(0,1,0),
                    Vec3(0,-1,0),
                    Vec3(-1,0,0),
                    Vec3(1,0,0),
                    Vec3(0,0,-1),
                    Vec3(0,0,1)]
        for i in range(0,6):
            np = epi + wp[i]
            if this.td.get( 'x'+str(floor(np.x))+
                            'y'+str(floor(np.y))+
                            'z'+str(floor(np.z)))==None:
                this.genBlock(np.x,np.y,np.z,subset,gap=False,blockType='soil')
    def genBlock(this,x,y,z,subset=-1,gap=True,blockType='grass'):
        if subset == -1 : subset=this.currentSubset
        model = this.subsets[subset].model
        # Extend or add to the vertices of our model.
        model.vertices.extend([ Vec3(x,y,z) + v for v in 
                                this.block.vertices])
        # Record terrain in dictionary :)
        this.td["x"+str(floor(x))+
                "y"+str(floor(y))+
                "z"+str(floor(z))] = "t"
        if gap==True:
            key = ("x"+str(floor(x))+
            "y"+str(floor(y+1))+
            "z"+str(floor(z)))  
            if this.td.get(key)==None:
                this.td[key] = "g"  

        # Rec Subset index
        vob = (subset,len(model.vertices)-37)
        this.vd["x"+str(floor(x))+
                "y"+str(floor(y))+
                "z"+str(floor(z))] = vob
        # ***
        cc = random()*0.5
        model.colors.extend((   Vec4(1-cc,1-cc,1-cc,1),) * 
                                len(this.block.vertices))

        # This is the texture atlas co-ord for grass :)
        uu = 8
        uv = 7
        if blockType == 'soil':
            uu = 10
            uv = 7
        elif blockType == 'stone':
            uu = 8
            uv = 5
        elif blockType == 'ice':
            uu =9
            uv =7
        elif random() > .86:
            uu = 8
            uv = 5     
        if y > 2:
            uu = 8
            uv = 6
        model.uvs.extend([Vec2(uu,uv) + u for u in this.block.uvs])


    def genTerrain(this):

        x = 0
        z = 0
        # ***
        x = this.swirlEngine.pos.x
        z = this.swirlEngine.pos.y

        d = int(this.subWidth*0.5)

        for k in range(-d,d):
            for j in range(-d,d):

                y = floor(this.perlin.get_height(x+k,z+j))
                # ***
                if this.td.get( "x"+str(floor(x+k))+
                                "y"+str(floor(y))+
                                "z"+str(floor(z+j)))==None:
                    this.genBlock(x+k,y,z+j,blockType='grass')
                    this.count+=1
                    # ***
                    if this.count==this.subWidth*this.subWidth:
                        this.subsets[this.currentSubset].model.generate()
                        this.currentSubset+=1
                        this.count=0

        # if madeNew==True:
            # this.subsets[this.currentSubset].model.generate()

        # *** Swirl to next position.
        this.swirlEngine.move()
        if this.currentSubset==this.numSubsets-1:
            this.currentSubset=0