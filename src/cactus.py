import bpy
import random
import bmesh
import mathutils
import math

VERTICES = 9
MIN_SHIFT = 0.5
MAX_SHIFT = 1.5
HEIGHT = 1.5

leavePositions = []

def generateBranches(edges, verts, vert, branch, lastIndex):
    for i in range(random.randrange(3, 5)):
        if branch:
            branchvert = (vert[0] + random.uniform(0.2, 0.75), vert[1] +
                          random.uniform(0.2, 0.75), vert[2] - random.uniform(0.1, 0.75))
        elif branch is False:
            branchvert = (vert[0] + random.uniform(-0.75, -0.2), vert[1] +
                          random.uniform(-0.75, -0.2), vert[2] - random.uniform(0.2, 0.75))

        vert = branchvert
        verts.append(branchvert)
        if i is 0:
            edge = (lastIndex - (VERTICES/2), len(verts) - 1)
        else:
            edge = (len(verts) - 2, len(verts) - 1) 

        edges.append(edge)

    leavePositions.append(branchvert)

def generateCactus():

    mesh = bpy.data.meshes.new("cactus")  # add the new mesh
    obj = bpy.data.objects.new(mesh.name, mesh)
    col = bpy.data.collections.get("Collection")
    col.objects.link(obj)
    bpy.context.view_layer.objects.active = obj

    verts = []
    edges = []

    for i in range(VERTICES):
        posZ = i * HEIGHT
        posY = 1 * random.uniform(MIN_SHIFT, MAX_SHIFT)
        posX = 1 * random.uniform(MIN_SHIFT, MAX_SHIFT)
        vert = (posX, posY, posZ)
        verts.append(vert)
        if i is not 0:
            edge = (i-1, i)
            edges.append(edge)

    generateBranches(edges, verts, vert, True, (VERTICES/2))
    generateBranches(edges, verts, vert, False, (VERTICES/2))

    faces = []

    trunk = mesh.from_pydata(verts, edges, faces)

    me = obj.data

    obj.select_set(True)

  # bpy.ops.object.mode_set(mode='EDIT')

  # bpy.ops.object.mode_set(mode='OBJECT')

    skin: bpy.types.SkinModifier = bpy.ops.object.modifier_add(type='SKIN')

    rad_x = random.uniform(0.65, 0.75)
    rad_y = random.uniform(0.65, 0.75)

    i = 0

    for v in me.skin_vertices[0].data:
        v.radius = rad_x, rad_y
        if i is 0:
            rad_x = random.uniform(0.75, 2.0)
            rad_y = random.uniform(0.75, 2.0)
        else:
            rad_x = rad_x - random.uniform(0.01, 0.05)
            rad_y = rad_y - random.uniform(0.01, 0.05)
        i = i + 1

    bpy.ops.object.modifier_add(type='SUBSURF')
    bpy.context.object.modifiers["Subdivision"].render_levels = 1
    
    for modifier in obj.modifiers:
        bpy.ops.object.modifier_apply(modifier=modifier.name)


    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.join()




class CactusBranches(bpy.types.Operator):
    bl_idname = "object.generate_cactus_branches"
    bl_label = "Generate a Cactus"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        generateCactus()
        return {'FINISHED'}

generateCactus()