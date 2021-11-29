import bpy
import bmesh
import math
import mathutils
import random


def map_range(v, from_min, from_max, to_min, to_max):
    """Bringt einen Wert v von einer Skala (from_min, from_max) auf eine neue Skala (to_min, to_max)"""
    return to_min + (v - from_min) * (to_max - to_min) / (from_max - from_min)

AMOUNT = 8

WIDTH_MAX = 0.6
WIDTH_MIN = 0.03

HEIGHT_MIN = 4
HEIGHT_MAX = 12

ROT_BASE_MIN = 1
ROT_BASE_MAX = 4
ROT_TIP_MIN = 5
ROT_TIP_MAX = 20
ROT_FALLOFF = 5

# Szene leeren
bpy.ops.object.select_all(action='SELECT')  # selektiert alle Objekte
# löscht selektierte objekte
bpy.ops.object.delete(use_global=False, confirm=False)
bpy.ops.outliner.orphans_purge()  # löscht überbleibende Meshdaten etc.

# Mesh und Objekt erstellen
trunk_mesh = bpy.data.meshes.new("trunk_shrub_mesh")
trunk_object = bpy.data.objects.new("trunk shrub", trunk_mesh)

# Mesh in aktuelle Collection der Szene verlinken
bpy.context.collection.objects.link(trunk_object)

#
bm = bmesh.new()
bm.from_mesh(trunk_mesh)
c_height = random.randrange(HEIGHT_MIN, HEIGHT_MAX)

rot = random.uniform(ROT_BASE_MIN, ROT_BASE_MAX)
rot_tip = random.uniform(ROT_TIP_MIN, ROT_TIP_MAX)

vertices = []
last_vert = bm.verts.new((0,0,0))
    
vertices.append(last_vert)



for i in range(AMOUNT):

    vert = bm.verts.new((0, 0, i))
    progress = i / c_height

    v = math.pow(progress, 0.8)

    pos_x = map_range(v, 0, 1, WIDTH_MAX, WIDTH_MIN)
    """ 
    # Halm immer weiter biegen desto weiter oben wir uns im Mesh/Loop befinden
    rot_angle = map_range(math.pow(progress, ROT_FALLOFF), 0, 1, rot, rot_tip)
    rot_matrix = mathutils.Matrix.Rotation(math.radians(rot_angle), 4, 'X')
    bmesh.ops.rotate(bm, cent=(0, 0, 0), matrix=rot_matrix, verts=[vert]) """
        
    # Jeden Halm zufällig auf Z Achse rotieren
    random_angle = random.randrange(0, 1)
    rot_matrix_blade = mathutils.Matrix.Rotation(math.radians(0), 4, 'Z')

    # Dabei jeden Vertex des aktuellen Halms rotieren
    for v in vertices:
        bmesh.ops.rotate(bm, cent=(0, 0, 0), matrix=rot_matrix_blade, verts=[v])


    bm.edges.new((vert, last_vert))

        # Vertices der Vertices-Liste des aktuellen Halms hinzufügen
    vertices.append(vert)
        # Letzte Vertices speichern, um sie für die generierung des nächsten Polygons zu verwenden
    last_vert = vert
    

# BMesh auf Mesh anwenden und abschließen
bm.to_mesh(trunk_mesh)
bm.free()




