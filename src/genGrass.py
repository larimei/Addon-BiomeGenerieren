
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


class generateGrass():

    def genGrass(self, x, y):

        grass_mesh = bpy.data.meshes.new("grass_shrub_mesh")
        grass_object = bpy.data.objects.new("grass shrub", grass_mesh)
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


gen = generateGrass()

for i in range(1000):
    x = random.randrange(-100, 100)
    y = random.randrange(-100, 100)
    gen.genGrass(x, y)
