import bpy
import random
import bmesh
import mathutils
import math


mesh = bpy.data.meshes.new("tree")  # add the new mesh
obj = bpy.data.objects.new(mesh.name, mesh)
col = bpy.data.collections.get("Collection")
col.objects.link(obj)
bpy.context.view_layer.objects.active = obj

VERTICES = 10
MIN_SHIFT = 0.9
MAX_SHIFT = 1.1
verts = []
edges = []

for i in range(VERTICES):
    posZ = i * 0.6
    posY = 1 * random.uniform(MIN_SHIFT,MAX_SHIFT)
    posX = 1 * random.uniform(MIN_SHIFT,MAX_SHIFT)
    vert = (posX,posY,posZ)
    verts.append(vert)
    if i is not 0:
        edge = (i-1,i)
        edges.append(edge)
    
faces = []

trunk = mesh.from_pydata(verts, edges, faces)


me = obj.data

bpy.ops.object.editmode_toggle()


# Get a BMesh representation
bm = bmesh.from_edit_mesh(me)



verts = bm.verts
num_verts = len(verts)
for i in range(0, num_verts):
    bm.verts.ensure_lookup_table()
    #bmesh.ops.scale(bm, vec=(0, 0, 0), space=(mathutils.Matrix.Scale(2,2,2)), verts=[verts[i]]) #????
    random_angle = random.randrange(0, 20)
    rot_matrix_blade = mathutils.Matrix.Rotation(math.radians(random_angle),4, 'Z')
    bmesh.ops.rotate(bm, cent=(0, 0, 0), matrix=rot_matrix_blade, verts=[verts[i]])
    bm.verts.ensure_lookup_table()

bmesh.update_edit_mesh(me, True)

bpy.ops.object.editmode_toggle()

bpy.ops.object.modifier_add(type='SKIN')

leaves = bpy.ops.mesh.primitive_ico_sphere_add(radius=random.uniform(1,1.2), enter_editmode=False, align='WORLD', location=(posX, posY, posZ + 2), scale=(random.uniform(2.5,5), random.uniform(2.5,5), random.uniform(6,8)))