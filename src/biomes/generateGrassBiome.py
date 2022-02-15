import bmesh
import math
import mathutils
import random
import bpy

from src import utility


class GenerateGrassBiome ():
    # Grass ------------------------
    width_max: float
    width_min: float

    height_min: int
    height_max: int

    rot_base_min: float
    rot_base_max: int
    rot_tip_min: int
    rot_tip_max: int
    rot_falloff: int
    # Grass ------------------------

    def __init__(self, _width_max, _width_min, _height_min, _height_max, _rot_base_min, _rot_base_max, _rot_tip_min, _rot_tip_max, _rot_falloff):
        self.width_max = _width_max
        self.width_min = _width_min

        self.height_min = _height_min
        self.height_max = _height_max

        self.rot_base_min = _rot_base_min
        self.rot_base_max = _rot_base_max
        self.rot_tip_min = _rot_tip_min
        self.rot_tip_max = _rot_tip_max
        self.rot_falloff = _rot_falloff

    def create_grass_array(self):
        collection = bpy.data.collections.new("GrassCollection")
        bpy.context.scene.collection.children.link(collection)
        for grass_increment in range(10):
            grass_mesh = bpy.data.meshes.new("grass_shrub_mesh")
            grass_object = bpy.data.objects.new("grass shrub", grass_mesh)
            random_offset_neg = random.uniform(-25, 0)
            random_offset_pos = random.uniform(0, 25)
            grass_object.location = (random.uniform(random_offset_pos,  random_offset_neg), random.uniform(
                random_offset_pos,  random_offset_neg), 0)

            bm = bmesh.new()
            bm.from_mesh(grass_mesh)

            def map_range(v, from_min, from_max, to_min, to_max):
                return to_min + (v - from_min) * (to_max - to_min) / (from_max - from_min)

            blades = grass_increment + 1
            for i in range(blades):
                c_height = random.randrange(self.height_min, self.height_max)
                c_blade = []

                c_rot_base = random.uniform(
                    self.rot_base_min, self.rot_base_max)
                c_rot_tip = random.uniform(self.rot_tip_min, self.rot_tip_max)

                last_vert_1 = None
                last_vert_2 = None

                for i in range(c_height):
                    progress = i / c_height

                    v = math.pow(progress, 0.8)

                    pos_x = map_range(v, 0, 1, self.width_max, self.width_min)

                    vert_1 = bm.verts.new((-pos_x, 0, i))
                    vert_2 = bm.verts.new((pos_x, 0, i))
                    rot_angle = map_range(
                        math.pow(progress, self.rot_falloff), 0, 1, c_rot_base, c_rot_tip)
                    rot_matrix = mathutils.Matrix.Rotation(
                        math.radians(rot_angle), 4, 'X')
                    bmesh.ops.rotate(bm, cent=(0, 0, 0), matrix=rot_matrix,
                                     verts=[vert_1, vert_2])
                    if i != 0:
                        bm.faces.new(
                            (last_vert_1, last_vert_2, vert_2, vert_1))
                    c_blade.append(vert_1)
                    c_blade.append(vert_2)

                    last_vert_1 = vert_1
                    last_vert_2 = vert_2

                random_angle = random.randrange(0, 360)
                rot_matrix_blade = mathutils.Matrix.Rotation(
                    math.radians(random_angle), 4, 'Z')

                for v in c_blade:
                    bmesh.ops.rotate(bm, cent=(0, 0, 0),
                                     matrix=rot_matrix_blade, verts=[v])

            bm.to_mesh(grass_mesh)
            bm.free()
            grass_object.data.materials.append(utility.MaterialUtils.create_material(
                "grassMaterial", (0, 0.4, 0.1, 1)))
            collection.objects.link(grass_object)

    def create_flowers_array(self):
        collection = bpy.data.collections.new("FlowerCollection")
        bpy.context.scene.collection.children.link(collection)
        for flower_increment in range(5):
            bpy.ops.mesh.primitive_cube_add(
                location=(0, 0, 6), scale=(0.5, 0.5, 0.15))

            paddel_data = bpy.context.active_object.data
            paddel_root: bpy.types.Object = bpy.context.active_object
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_mode(type="FACE")
            bm = bmesh.from_edit_mesh(paddel_data)

            if hasattr(bm.faces, "ensure_lookup_table"):
                bm.faces.ensure_lookup_table()

            bmesh.ops.translate(
                bm, verts=bm.faces[1].verts, vec=bm.faces[1].normal * 3)
            c = bm.faces[1].calc_center_median()
            for v in bm.faces[1].verts:
                v.co = c + 2 * (v.co - c)

            bmesh.update_edit_mesh(paddel_data, True)
            bpy.ops.object.mode_set(mode='OBJECT')

            num = 8
            rad = 2
            paddels_container = bpy.data.objects.new("paddelsContainer", None)
            collection.objects.link(paddels_container)
            flower_parent = bpy.data.objects.new(
                "flowerParent" + str(flower_increment), None)
            for i in range(num):
                y = math.sin(i/num * math.pi * 2) * rad
                x = math.cos(i / num * math.pi*2) * rad
                angle = i/num * 2 * math.pi - math.pi/2

                paddel = bpy.data.objects.new('onePaddel', paddel_data)

                collection.objects.link(paddel)
                paddel.location = (x, y, 6)
                paddel.rotation_euler.z = angle
                paddel.parent = paddels_container

            paddel.data.materials.append(utility.MaterialUtils.create_material(
                "leaveMaterial", (random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1), 1)))
            bpy.data.objects.remove(paddel_root)
            paddels_container.parent = flower_parent
            bpy.ops.mesh.primitive_ico_sphere_add(
                location=(0, 0, 6), scale=(1.75, 1.75, 0.5))

            bpy.context.active_object.data.materials.append(utility.MaterialUtils.create_material(
                "blossomMaterial", (1, 1, 0.6, 1)))
            bpy.context.active_object.name = "blossom"
            bpy.context.active_object.parent = flower_parent
            collection.objects.link(bpy.context.active_object)
            bpy.ops.mesh.primitive_cube_add(
                location=(0, 0, 2), scale=(0.75, 0.75, 4))
            bpy.context.active_object.data.materials.append(utility.MaterialUtils.create_material(
                "stemMaterial", (0.4, 0.1, 0, 1)))
            bpy.context.active_object.name = "steam"
            collection.objects.link(bpy.context.active_object)
            bpy.context.active_object.parent = flower_parent
            random_offset_neg = random.uniform(-100, 0)
            random_offset_pos = random.uniform(0, 100)
            flower_parent.location = (random.uniform(random_offset_pos,  random_offset_neg), random.uniform(
                random_offset_pos,  random_offset_neg), 0)
            collection.objects.link(flower_parent)

    def create_bushes_array(self):

        for bushes_increment in range(3):
            collection = bpy.data.collections.new(
                "BushCollection" + str(bushes_increment))
            bpy.context.scene.collection.children.link(collection)
            bpy.ops.mesh.primitive_ico_sphere_add(
                subdivisions=1, enter_editmode=True, location=(0, 0, 0), scale=(10, 10, 10))
            bpy.context.active_object.name = "bush" + str(bushes_increment)

            bush_data = bpy.context.active_object.data
            bush_object: bpy.types.Object = bpy.context.active_object

            bush_object.data.materials.append(utility.MaterialUtils.create_material(
                "bushMaterial", (0, 0.3, 0.2, 1)))
            bpy.ops.mesh.select_mode(type="VERT")
            bm = bmesh.from_edit_mesh(bush_data)

            if hasattr(bm.verts, "ensure_lookup_table"):
                bm.verts.ensure_lookup_table()

            bm.verts[0].co += bm.verts[0].normal * -5
            bpy.ops.object.mode_set(mode='OBJECT')
            if(bushes_increment == 0):
                bpy.ops.object.duplicate()
                duplicated_bush: bpy.types.Object = bpy.context.active_object
                duplicated_bush.location = (10, 10, -1)
                duplicated_bush.scale = (0.75, 0.75, 0.75)
                collection.objects.link(duplicated_bush)
                duplicated_bush.parent = bush_object
                bpy.ops.object.duplicate()
                duplicated_bush: bpy.types.Object = bpy.context.active_object
                duplicated_bush.location = (-8, -9, -3)
                duplicated_bush.scale = (0.5, 0.5, 0.5)
                duplicated_bush.parent = bush_object
                bpy.ops.object.duplicate()
                duplicated_bush: bpy.types.Object = bpy.context.active_object
                duplicated_bush.location = (5,  -10, -1.67)
                duplicated_bush.scale = (0.6, 0.6, 0.6)
                duplicated_bush.parent = bush_object
                bpy.ops.object.duplicate()
                duplicated_bush: bpy.types.Object = bpy.context.active_object
                duplicated_bush.location = (-8,  9, -3)
                duplicated_bush.scale = (0.5, 0.5, 0.5)
                duplicated_bush.parent = bush_object
            if(bushes_increment == 1):
                bpy.ops.object.duplicate()
                duplicated_bush: bpy.types.Object = bpy.context.active_object
                duplicated_bush.location = (10, 6, -4)
                duplicated_bush.scale = (0.35, 0.35, 0.35)
                collection.objects.link(duplicated_bush)
                duplicated_bush.parent = bush_object
                bpy.ops.object.duplicate()
                duplicated_bush: bpy.types.Object = bpy.context.active_object
                duplicated_bush.location = (-8, -9, -3.35)
                duplicated_bush.scale = (0.45, 0.45, 0.45)
                duplicated_bush.parent = bush_object

            bush_object.rotation_euler = (0, 0, random.randrange(0, 360))
            collection.objects.link(bush_object)
