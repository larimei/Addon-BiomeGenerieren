import bpy
import bmesh
import math
# Szene leeren
bpy.ops.object.select_all(action='SELECT')  # selektiert alle Objekte
# löscht selektierte objekte
bpy.ops.object.delete(use_global=False, confirm=False)
bpy.ops.outliner.orphans_purge()  # löscht überbleibende Meshdaten etc.


bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0), scale=(0.5, 0.5, 0.15))
paddelData = bpy.data.objects["Cube"].data
paddel: bpy.types.Object = bpy.data.objects["Cube"]
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_mode(type="FACE")
bm = bmesh.from_edit_mesh(paddelData)

if hasattr(bm.faces, "ensure_lookup_table"):
    bm.faces.ensure_lookup_table()

for i in range(len(bm.faces)):
    bm.faces[i].select = False
bm.faces[1].select = True
bmesh.ops.translate(bm, verts=bm.faces[1].verts, vec=bm.faces[1].normal * 3)
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
    bpy.context.collection.objects.link(ob)
    ob.location = (x, y, 0)
    ob.rotation_euler.z = angle

bpy.data.objects.remove(paddel)
bpy.ops.mesh.primitive_ico_sphere_add(
    location=(0, 0, 0), scale=(1.75, 1.75, 0.5))
