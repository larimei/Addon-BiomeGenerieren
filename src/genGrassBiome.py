import bmesh
import math
import mathutils
import random
import bpy

# Grass ------------------------
WIDTH_MAX = 0.6
WIDTH_MIN = 0.03

HEIGHT_MIN = 4
HEIGHT_MAX = 12

ROT_BASE_MIN = 3
ROT_BASE_MAX = 25
ROT_TIP_MIN = 30
ROT_TIP_MAX = 90
ROT_FALLOFF = 5
# Grass ------------------------

# Materials ------------------------
GRASSMATERIAL: bpy.types.Material
BUSHMATERIAL: bpy.types.Material
STEMMATERIAL: bpy.types.Material
BLOSSOMMATERIAL: bpy.types.Material
LEAVESMATERIALS = [None] * 4
# Materials ------------------------


class GenerateGrassBiome ():
    def createMaterials(self):
        self.GRASSMATERIAL = bpy.data.materials.new(
            name="grassMaterial")
        self.GRASSMATERIAL.use_nodes = True
        self.GRASSMATERIAL.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (
            0, 0.4, 0.1, 1)
        self.BUSHMATERIAL = bpy.data.materials.new(
            name="bushMaterial")
        self.BUSHMATERIAL.use_nodes = True
        self.BUSHMATERIAL.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (
            0, 0.3, 0.2, 1)
        self.STEMMATERIAL = bpy.data.materials.new(
            name="stemMaterial")
        self.STEMMATERIAL.use_nodes = True
        self.STEMMATERIAL.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (
            0.4, 0.1, 0, 1)
        self.BLOSSOMMATERIAL = bpy.data.materials.new(
            name="blossomMaterial")
        self.BLOSSOMMATERIAL.use_nodes = True
        self.BLOSSOMMATERIAL.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (
            1, 1, 0.6, 1)

        for i in range(len(self.LEAVESMATERIALS)-1):
            self.LEAVESMATERIALS[i] = bpy.data.materials.new(
                name="blossomMaterial")
            self.LEAVESMATERIALS[i].use_nodes = True
            self.LEAVESMATERIALS[i].node_tree.nodes["Principled BSDF"].inputs[0].default_value = (
                random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1), 1)

    def createGrassArray(self):
        collection = bpy.data.collections.new("GrassCollection")
        bpy.context.scene.collection.children.link(collection)
        for grassIncrement in range(10):
            grass_mesh = bpy.data.meshes.new("grass_shrub_mesh")
            grass_object = bpy.data.objects.new("grass shrub", grass_mesh)
            rndOffsetNeg = random.uniform(-25, 0)
            rndOffsetPos = random.uniform(0, 25)
            grass_object.location = (random.uniform(rndOffsetPos,  rndOffsetNeg), random.uniform(
                rndOffsetPos,  rndOffsetNeg), 0)

            bm = bmesh.new()
            bm.from_mesh(grass_mesh)

            def map_range(v, from_min, from_max, to_min, to_max):
                """Bringt einen Wert v von einer Skala (from_min, from_max) auf eine neue Skala (to_min, to_max)"""
                return to_min + (v - from_min) * (to_max - to_min) / (from_max - from_min)
            blades = grassIncrement + 1
            for i in range(blades):
                c_height = random.randrange(HEIGHT_MIN, HEIGHT_MAX)
                c_blade = []

                c_rot_base = random.uniform(ROT_BASE_MIN, ROT_BASE_MAX)
                c_rot_tip = random.uniform(ROT_TIP_MIN, ROT_TIP_MAX)

                last_vert_1 = None
                last_vert_2 = None

                for i in range(c_height):
                    progress = i / c_height

                    v = math.pow(progress, 0.8)

                    pos_x = map_range(v, 0, 1, WIDTH_MAX, WIDTH_MIN)

                    vert_1 = bm.verts.new((-pos_x, 0, i))
                    vert_2 = bm.verts.new((pos_x, 0, i))
                    rot_angle = map_range(
                        math.pow(progress, ROT_FALLOFF), 0, 1, c_rot_base, c_rot_tip)
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
            grass_object.data.materials.append(self.GRASSMATERIAL)
            collection.objects.link(grass_object)

    def createFlowersArray(self):
        collection = bpy.data.collections.new("FlowerCollection")
        bpy.context.scene.collection.children.link(collection)
        for flowerIncrement in range(3):
            bpy.ops.mesh.primitive_cube_add(
                location=(0, 0, 6), scale=(0.5, 0.5, 0.15))

            paddelData = bpy.context.active_object.data
            paddelRoot: bpy.types.Object = bpy.context.active_object
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_mode(type="FACE")
            bm = bmesh.from_edit_mesh(paddelData)

            if hasattr(bm.faces, "ensure_lookup_table"):
                bm.faces.ensure_lookup_table()

            bmesh.ops.translate(
                bm, verts=bm.faces[1].verts, vec=bm.faces[1].normal * 3)
            c = bm.faces[1].calc_center_median()
            for v in bm.faces[1].verts:
                v.co = c + 2 * (v.co - c)
                #
            # Show the updates in the viewport
            bmesh.update_edit_mesh(paddelData, True)
            bpy.ops.object.mode_set(mode='OBJECT')

            num = 8
            rad = 2
            paddelsContainer = bpy.data.objects.new("paddelsContainer", None)
            collection.objects.link(paddelsContainer)
            flowerParent = bpy.data.objects.new("flowerParent", None)

            rndScale = random.uniform(0.5, 1.25)
            flowerParent.scale = (rndScale, rndScale, rndScale)
            for i in range(num):
                y = math.sin(i/num * math.pi * 2) * rad
                x = math.cos(i / num * math.pi*2) * rad
                angle = i/num * 2 * math.pi - math.pi/2

                paddel = bpy.data.objects.new('onePaddel', paddelData)

                collection.objects.link(paddel)
                paddel.location = (x, y, 6)
                paddel.rotation_euler.z = angle
                paddel.parent = paddelsContainer

            paddel.data.materials.append(self.LEAVESMATERIALS[flowerIncrement])
            bpy.data.objects.remove(paddelRoot)
            paddelsContainer.parent = flowerParent
            bpy.ops.mesh.primitive_ico_sphere_add(
                location=(0, 0, 6), scale=(1.75, 1.75, 0.5))

            bpy.context.active_object.data.materials.append(
                self.BLOSSOMMATERIAL)
            bpy.context.active_object.name = "blossom"
            bpy.context.active_object.parent = flowerParent
            collection.objects.link(bpy.context.active_object)
            bpy.ops.mesh.primitive_cube_add(
                location=(0, 0, 2), scale=(0.75, 0.75, 4))
            bpy.context.active_object.data.materials.append(self.STEMMATERIAL)
            bpy.context.active_object.name = "steam"
            collection.objects.link(bpy.context.active_object)
            bpy.context.active_object.parent = flowerParent
            rndOffsetNeg = random.uniform(-100, 0)
            rndOffsetPos = random.uniform(0, 100)
            flowerParent.location = (random.uniform(rndOffsetPos,  rndOffsetNeg), random.uniform(
                rndOffsetPos,  rndOffsetNeg), 0)
            collection.objects.link(flowerParent)

    def genBushes(self):
        collection = bpy.data.collections.new("BushCollection")
        bpy.context.scene.collection.children.link(collection)
        for bushesIncrement in range(2):
            bpy.ops.mesh.primitive_ico_sphere_add(
                subdivisions=1, enter_editmode=True, location=(0, 0, 5), scale=(10, 10, 10))
            bpy.context.active_object.name = "bush" + str(bushesIncrement)

            bushData = bpy.context.active_object.data
            bushObject: bpy.types.Object = bpy.context.active_object

            bushObject.data.materials.append(self.BUSHMATERIAL)
            bpy.ops.mesh.select_mode(type="VERT")
            bm = bmesh.from_edit_mesh(bushData)

            if hasattr(bm.verts, "ensure_lookup_table"):
                bm.verts.ensure_lookup_table()

            bm.verts[0].co += bm.verts[0].normal * -5
            bpy.ops.object.mode_set(mode='OBJECT')
            if(bushesIncrement % 1 == 0):
                bpy.ops.object.duplicate()
                duplicatedBush: bpy.types.Object = bpy.context.active_object
                duplicatedBush.location = (10, 10, -1)
                duplicatedBush.scale = (0.75, 0.75, 0.75)
                duplicatedBush.parent = bushObject
                bpy.ops.object.duplicate()
                duplicatedBush: bpy.types.Object = bpy.context.active_object
                duplicatedBush.location = (-8, -9, -3)
                duplicatedBush.scale = (0.5, 0.5, 0.5)
                duplicatedBush.parent = bushObject
                bpy.ops.object.duplicate()
                duplicatedBush: bpy.types.Object = bpy.context.active_object
                duplicatedBush.location = (5,  -10, -1.67)
                duplicatedBush.scale = (0.6, 0.6, 0.6)
                duplicatedBush.parent = bushObject
                bpy.ops.object.duplicate()
                duplicatedBush: bpy.types.Object = bpy.context.active_object
                duplicatedBush.location = (-8,  9, -3)
                duplicatedBush.scale = (0.5, 0.5, 0.5)
                duplicatedBush.parent = bushObject
            else:
                bpy.ops.object.duplicate()
                duplicatedBush: bpy.types.Object = bpy.context.active_object
                duplicatedBush.location = (10, 6, -4)
                duplicatedBush.scale = (0.35, 0.35, 0.35)
                duplicatedBush.parent = bushObject
                bpy.ops.object.duplicate()
                duplicatedBush: bpy.types.Object = bpy.context.active_object
                duplicatedBush.location = (-8, -9, -3.35)
                duplicatedBush.scale = (0.45, 0.45, 0.45)
                duplicatedBush.parent = bushObject
            bushObject.rotation_euler = (0, 0, random.randrange(0, 360))
            bushObject.location = (0,
                                   0, 0)
            rndScale = random.uniform(0.045, 0.085)
            bushObject.scale = (rndScale, rndScale, rndScale)
            collection.objects.link(bushObject)
