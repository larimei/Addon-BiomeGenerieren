import bpy
import random

from src.utility import MaterialUtils


class Stone:

    def generate_stone():

        for stone_version in range(3):
            collection = bpy.data.collections.new(
                "StoneCollection" + str(stone_version))
            bpy.context.scene.collection.children.link(collection)
            width = random.uniform(2, 5)
            depth = random.uniform(2, 5)
            height = depth / width + random.uniform(0, 2)

            if width > depth:
                height = width / depth + random.uniform(0, 2)
            elif width == depth:
                height = abs(width + depth - 4)

            greytone = random.uniform(0.25, 0.75)
            bpy.ops.mesh.primitive_ico_sphere_add(
                enter_editmode=False, location=(0, 0,  0), scale=(width, depth, height)
            )
            #bpy.ops.mesh.name = "stone"
            bpy.ops.object.shade_flat()

            bpy.context.object.data.materials.append(MaterialUtils.create_material(
                "stone_material", (greytone, greytone, greytone, 1)))

            current_mesh = bpy.context.object.data

            for vert in current_mesh.vertices:
                vert.co.x += random.uniform(-0.5, 1)
                vert.co.y += random.uniform(-0.5, 1)
                vert.co.z += random.uniform(-0.5, 1)

            current_mesh.update()
            rnd_scale = random.uniform(1, 1.5)
            bpy.context.object.scale = (rnd_scale, rnd_scale, rnd_scale)
            collection.objects.link(bpy.context.object)
