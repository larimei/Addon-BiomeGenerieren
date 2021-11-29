
import bmesh
import math
import mathutils
import random
import bpy

WIDTH_MAX = 0.6
WIDTH_MIN = 0.03

HEIGHT_MIN = 4
HEIGHT_MAX = 12

ROT_BASE_MIN = 3
ROT_BASE_MAX = 25
ROT_TIP_MIN = 30
ROT_TIP_MAX = 90
ROT_FALLOFF = 5
# Szene leeren
bpy.ops.object.select_all(action='SELECT')  # selektiert alle Objekte
# löscht selektierte objekte
bpy.ops.object.delete(use_global=False, confirm=False)
bpy.ops.outliner.orphans_purge()  # löscht überbleibende Meshdaten etc.


class generateGrass():

    def genGrass(self, x, y):
        object_color = (
            random.uniform(0, 1),
            random.uniform(0, 1),
            random.uniform(0, 1),
            1  # Alpha-Wert der Farbe (Intransparenz) - soll hier immer 1 sein
        )
        grass_mesh = bpy.data.meshes.new("grass_shrub_mesh")
        grass_object = bpy.data.objects.new("grass shrub", grass_mesh)
        grass_object.color = object_color
        grass_object.location = (x, y, 0)
        # Mesh in aktuelle Collection der Szene verlinken
        bpy.context.collection.objects.link(grass_object)

        #
        bm = bmesh.new()
        bm.from_mesh(grass_mesh)

        def map_range(v, from_min, from_max, to_min, to_max):
            """Bringt einen Wert v von einer Skala (from_min, from_max) auf eine neue Skala (to_min, to_max)"""
            return to_min + (v - from_min) * (to_max - to_min) / (from_max - from_min)
        blades = random.randrange(0, 5)

        for i in range(blades):

            # Zufällige Werte für jedes Blatt generieren
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

                # Halm immer weiter biegen desto weiter oben wir uns im Mesh/Loop befinden
                rot_angle = map_range(
                    math.pow(progress, ROT_FALLOFF), 0, 1, c_rot_base, c_rot_tip)
                rot_matrix = mathutils.Matrix.Rotation(
                    math.radians(rot_angle), 4, 'X')
                bmesh.ops.rotate(bm, cent=(0, 0, 0), matrix=rot_matrix,
                                 verts=[vert_1, vert_2])

                # Generierung des Polygons in erster Stufe überspringen (weil bisher nur 2 Verices bestehen)
                if i is not 0:
                    bm.faces.new((last_vert_1, last_vert_2, vert_2, vert_1))

                # Vertices der Vertices-Liste des aktuellen Halms hinzufügen
                c_blade.append(vert_1)
                c_blade.append(vert_2)

                # Letzte Vertices speichern, um sie für die generierung des nächsten Polygons zu verwenden
                last_vert_1 = vert_1
                last_vert_2 = vert_2

            # Jeden Halm zufällig auf Z Achse rotieren
            random_angle = random.randrange(0, 360)
            rot_matrix_blade = mathutils.Matrix.Rotation(
                math.radians(random_angle), 4, 'Z')

            # Dabei jeden Vertex des aktuellen Halms rotieren
            for v in c_blade:
                bmesh.ops.rotate(bm, cent=(0, 0, 0),
                                 matrix=rot_matrix_blade, verts=[v])

        # BMesh auf Mesh anwenden und abschließen
        bm.to_mesh(grass_mesh)
        bm.free()

    def genFlower(self, _x, _y):
        object_color = (
            random.uniform(0, 1),
            random.uniform(0, 1),
            random.uniform(0, 1),
            1  # Alpha-Wert der Farbe (Intransparenz) - soll hier immer 1 sein
        )

        bpy.ops.mesh.primitive_cube_add(
            location=(_x, _y, 6), scale=(0.5, 0.5, 0.15))

        paddelData = bpy.context.active_object.data
        paddel: bpy.types.Object = bpy.context.active_object
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_mode(type="FACE")
        bm = bmesh.from_edit_mesh(paddelData)

        if hasattr(bm.faces, "ensure_lookup_table"):
            bm.faces.ensure_lookup_table()

        for i in range(len(bm.faces)):
            bm.faces[i].select = False
        bm.faces[1].select = True
        bmesh.ops.translate(
            bm, verts=bm.faces[1].verts, vec=bm.faces[1].normal * 3)
        c = bm.faces[1].calc_center_median()
        for v in bm.faces[1].verts:
            v.co = c + 2 * (v.co - c)
        # Show the updates in the viewport
        bmesh.update_edit_mesh(paddelData, True)
        bpy.ops.object.mode_set(mode='OBJECT')

        num = 8
        rad = 2
        for i in range(num):
            y = math.sin(i/num * math.pi * 2) * rad
            x = math.cos(i / num * math.pi*2) * rad
            angle = i/num * 2 * math.pi - math.pi/2

            ob = bpy.data.objects.new('ob', paddelData)
            ob.color = object_color
            bpy.context.collection.objects.link(ob)
            ob.location = (_x + x, _y + y, 6)
            ob.rotation_euler.z = angle

        bpy.data.objects.remove(paddel)
        bpy.ops.mesh.primitive_ico_sphere_add(
            location=(_x, _y, 6), scale=(1.75, 1.75, 0.5))
        bpy.context.active_object.color = object_color
        bpy.ops.mesh.primitive_cube_add(
            location=(_x, _y, 2), scale=(0.75, 0.75, 4))
        bpy.context.active_object.color = object_color


gen = generateGrass()

for i in range(2000):
    x = random.randrange(-400, 400)
    y = random.randrange(-400, 400)
    if(x % 20 == 0):
        gen.genFlower(x, y)
    gen.genGrass(x, y)
