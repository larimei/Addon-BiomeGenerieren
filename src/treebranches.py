import bpy
import random
import bmesh
import mathutils
import math

VERTICES = 7
MIN_SHIFT = 0.9
MAX_SHIFT = 1.1

leavePositions = []


def generateBranches(edges, verts, vert, branch, newBranch, lastIndex):
    bool = False
    for i in range(random.randrange(3, 5)):
        if branch:
            branchvert = (vert[0] + random.uniform(0.2, 0.8), vert[1] +
                          random.uniform(0.2, 0.8), vert[2] + random.uniform(0.2, 0.8))
        elif branch is False:
            branchvert = (vert[0] + random.uniform(-0.8, -0.2), vert[1] +
                          random.uniform(-0.8, -0.2), vert[2] + random.uniform(0.2, 0.8))
        """ elif branch is 3:
            branchVert = (vert[0] + random.uniform(-1,0), vert[1] + random.uniform(0,1), vert[2] + random.uniform(0,1))
        elif branch is 4:
            branchVert = (vert[0] + random.uniform(0,1), vert[1] + random.uniform(-1,0), vert[2] + random.uniform(0,1)) """

        vert = branchvert
        verts.append(branchvert)
        if i is 0:
            edge = (lastIndex - 1, len(verts) - 1)
        else:
            if bool:
                edge = (lastIndex, len(verts) -1)   
                bool = False
            else:
                edge = (len(verts) - 2, len(verts) -1)

        edges.append(edge)
        """ if i is 2 and newBranch:
                lastIndex = len(verts) - 1
                generateBranches(edges, verts, vert, not branch, False, lastIndex)
                bool = True """

        """  if newBranch and i is not 0:
             generateBranches(edges, verts, branchvert, not branch, False, len(verts) -1 )
             newBranch = False """
    leavePositions.append(branchvert)

def generateLeaves(): 
    for pos in leavePositions:
        if pos is leavePositions[len(leavePositions) - 1]:
            leaves = bpy.ops.mesh.primitive_ico_sphere_add(radius=random.uniform(2, 2.7), enter_editmode=False, align='WORLD', location=(
            pos[0], pos[1], pos[2] + 1.2), scale=(random.uniform(2, 3), random.uniform(2, 3), random.uniform(1.7, 2.5)))
        else:
            leaves = bpy.ops.mesh.primitive_ico_sphere_add(radius=random.uniform(1, 1.2), enter_editmode=False, align='WORLD', location=(
            pos[0], pos[1], pos[2]), scale=(random.uniform(2, 3), random.uniform(2, 3), random.uniform(2, 3)))

def generateMoreTrunk(edges, verts, vert):
    for i in range(0,3):
        posZ = vert[2] + 0.6
        posY = 1 * random.uniform(MIN_SHIFT, MAX_SHIFT)
        posX = 1 * random.uniform(MIN_SHIFT, MAX_SHIFT)
        vert = (posX, posY, posZ)
        verts.append(vert)
        if i is not 0:
            edge = (len(verts)-2, len(verts)-1)
            edges.append(edge)
        else:
            edge = (VERTICES - 1, len(verts) - 1)
            edges.append(edge)
    leavePositions.append(vert)


   


def generateTreeWithBranches():

    mesh = bpy.data.meshes.new("tree")  # add the new mesh
    obj = bpy.data.objects.new(mesh.name, mesh)
    col = bpy.data.collections.get("Collection")
    col.objects.link(obj)
    bpy.context.view_layer.objects.active = obj

    verts = []
    edges = []
    verts_trunk = []

    for i in range(VERTICES):
        posZ = i * 0.6
        posY = 1 * random.uniform(MIN_SHIFT, MAX_SHIFT)
        posX = 1 * random.uniform(MIN_SHIFT, MAX_SHIFT)
        vert = (posX, posY, posZ)
        verts.append(vert)
        verts_trunk.append(vert)
        if i is not 0:
            edge = (i-1, i)
            edges.append(edge)

    generateBranches(edges, verts, vert, True, True, VERTICES)
    generateBranches(edges, verts, vert, False, False, VERTICES)
    generateMoreTrunk(edges, verts, vert)

    faces = []

    trunk = mesh.from_pydata(verts, edges, faces)

    me = obj.data

    obj.select_set(True)

    bpy.ops.object.mode_set(mode='EDIT')

    # Get a BMesh representation
    bm = bmesh.from_edit_mesh(me)

    verts = bm.verts
    num_verts = len(verts)
    for i in range(0, num_verts):
        bm.verts.ensure_lookup_table()
        random_angle = random.randrange(0, 120)
        # rotate??
        rot_matrix_blade = mathutils.Matrix.Rotation(
            math.radians(random_angle), 3, 'Z')
        bmesh.ops.rotate(bm, cent=verts[i].co,
                         matrix=rot_matrix_blade, verts=[verts[i]])
        bm.verts.ensure_lookup_table()

    bmesh.update_edit_mesh(me, True)

    bpy.ops.object.mode_set(mode='OBJECT')

    skin: bpy.types.SkinModifier = bpy.ops.object.modifier_add(type='SKIN')

        
    rad_x = 1.5
    rad_y = 1.5

    i = 0

    for v in me.skin_vertices[0].data:
        if i < len(verts_trunk) - 1:
            v.radius = rad_x, rad_y
            if i is 0:
                rad_x = random.uniform(0.65, 0.85)
                rad_y = random.uniform(0.65, 0.85)
            else:
                rad_x = rad_x - random.uniform(0.02, 0.05)
                rad_y = rad_y - random.uniform(0.025, 0.055)
            i = i + 1

    bpy.ops.object.modifier_add(type='SUBSURF')
    bpy.context.object.modifiers["Subdivision"].render_levels = 1
    
    #for modifier in obj.modifiers:
        #bpy.ops.object.modifier_apply(modifier=modifier.name)


    generateLeaves()

    #bpy.ops.object.select_all(action='SELECT')
    #bpy.ops.object.join()




class TreeBranches(bpy.types.Operator):
    """Insert a Tree"""
    bl_idname = "object.generate_tree_branches"
    bl_label = "Generate a Tree"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        generateTreeWithBranches()
        return {'FINISHED'}


generateTreeWithBranches()
