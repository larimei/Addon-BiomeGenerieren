import bpy
import random
import mathutils
import math
import typing


class Stone:

    WIDTH = random.uniform(2, 5)
    DEPTH = random.uniform(2, 5)

    if WIDTH > DEPTH:
        HEIGHT = WIDTH / DEPTH + random.uniform(0, 2)
    elif WIDTH == DEPTH:
        HEIGHT = abs(WIDTH + DEPTH - 4)
    else:
        HEIGHT = DEPTH / WIDTH + random.uniform(0, 2)

    def __init__(self):
        pass

    def createMaterial(self) -> bpy.types.Material:

        GREYTONE = random.uniform(0.25, 0.75)

        stoneMaterial: bpy.types.Material = bpy.data.materials.new(
            "Stone Material")
        stoneMaterial.use_nodes = True

        stoneNodes: typing.List[bpy.types.Node] = stoneMaterial.node_tree.nodes
        stoneNodes["Principled BSDF"].inputs[0].default_value = (
            GREYTONE, GREYTONE, GREYTONE, 1)

     #   noiseTex: bpy.types.Node = stoneNodes.new("ShaderNodeTexNoise")
      #  voronoiTex: bpy.types.Node = stoneNodes.new("ShaderNodeTexVoronoi")

    #    noiseTex.inputs[2].default_value = 15.000
  #      noiseTex.inputs[3].default_value = 0.592
   #
 #       voronoiTex.inputs[1].default_value = 0
#        voronoiTex.inputs[2].default_value = 1.000

    #    stoneMaterial.node_tree.links.new(voronoiTex.outputs[1],noiseTex.inputs[1])
     #   stoneMaterial.node_tree.links.new(noiseTex.outputs[1], stoneNodes["Material Output"].inputs[0])

        return stoneMaterial

    def generateStone(self):
        collection = bpy.data.collections.new("StoneCollection")
        bpy.context.scene.collection.children.link(collection)

        # stoneMesh = bpy.ops.meshes.new("stone")  # add the new mesh
        #    obj = bpy.ops.objects.new(stoneMesh.name, stoneMesh)

        #   obj.primitive_uv_sphere_add(radius=1, enter_editmode=False, location=(0, 0, 0), scale=(1, 1, 1))

        bpy.ops.mesh.primitive_ico_sphere_add(
            enter_editmode=False, location=(0, 0, 0), scale=(self.WIDTH, self.DEPTH, self.HEIGHT)
        )
        bpy.ops.object.shade_flat()

        bpy.context.object.data.materials.append(self.createMaterial())

    # bpy.ops.mesh.primitive_uv_sphere_add(enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))

    #frequency = random.uniform(5, 25)
    #amplitude = random.uniform(0.1, 0.2)

        currentmesh = bpy.context.object.data

        for vert in currentmesh.vertices:
            # vert.co.x += abs(random.uniform(2, 5)/HEIGHT)
            vert.co.x += random.uniform(-0.5, 0.5)
            vert.co.y += random.uniform(-0.5, 0.5)
            vert.co.z += random.uniform(-0.5, 0.5)
            #  vert.co.x += amplitude * math.cos(frequency * vert.co.z)
            # vert.co.z += amplitude * math.sin(frequency * vert.co.y)
            # vert.co.y += amplitude * math.sin(frequency * vert.co.x)

        currentmesh.update()
        collection.objects.link(bpy.context.object)
