import bpy
import random
import mathutils
import math
import typing
from src import utility


class Stone:

    def __init__(self):
        pass

    def generateStone(self):

        for stone_version in range(3):
            collection = bpy.data.collections.new(
                "StoneCollection" + str(stone_version))
            bpy.context.scene.collection.children.link(collection)
            WIDTH = random.uniform(2, 5)
            DEPTH = random.uniform(2, 5)
            HEIGHT = DEPTH / WIDTH + random.uniform(0, 2)

            if WIDTH > DEPTH:
                HEIGHT = WIDTH / DEPTH + random.uniform(0, 2)
            elif WIDTH == DEPTH:
                HEIGHT = abs(WIDTH + DEPTH - 4)

            GREYTONE = random.uniform(0.25, 0.75)
            bpy.ops.mesh.primitive_ico_sphere_add(
                enter_editmode=False, location=(0, 0,  0), scale=(WIDTH, DEPTH, HEIGHT)
            )
            #bpy.ops.mesh.name = "stone"
            bpy.ops.object.shade_flat()

            bpy.context.object.data.materials.append(utility.MaterialUtils.create_material(
                "stone_material", (GREYTONE, GREYTONE, GREYTONE, 1)))

            currentmesh = bpy.context.object.data

            for vert in currentmesh.vertices:
                vert.co.x += random.uniform(-0.5, 1)
                vert.co.y += random.uniform(-0.5, 1)
                vert.co.z += random.uniform(-0.5, 1)

            currentmesh.update()
            rndScale = random.uniform(1, 1.5)
            bpy.context.object.scale = (rndScale, rndScale, rndScale)
            collection.objects.link(bpy.context.object)
