import bpy
import random
from mathutils import Vector
import bmesh

def get_average(vert_range):
    med = Vector()
    for vert in vert_range:
        vec = vert.co
        med = med + vec
    return med / len(vert_range)

mesh = bpy.data.meshes.new("tree")  # add the new mesh
obj = bpy.data.objects.new(mesh.name, mesh)
col = bpy.data.collections.get("Collection")
col.objects.link(obj)
bpy.context.view_layer.objects.active = obj

VERTICES = 10
MIN_SHIFT = 0.8
MAX_SHIFT = 1.2
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
scale = 1 / (num_verts / 4)
j = 0
for i in range(0, num_verts):
    bm.verts.ensure_lookup_table()
    bmesh.ops.scale(bm, vec=(2, 2, 1), verts=[verts[i]]) #????
    bm.verts.ensure_lookup_table()

bmesh.update_edit_mesh(me, True)

bpy.ops.object.modifier_add(type='SKIN')

leaves = bpy.ops.mesh.primitive_ico_sphere_add(radius=1, enter_editmode=False, align='WORLD', location=(posX, posY, posZ + 1), scale=(random.uniform(2,4), random.uniform(2,4), random.uniform(6,8)))
