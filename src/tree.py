import bpy
import random
import bmesh
import mathutils
import math

def create_leave_material() -> bpy.types.Material:
        mat_leave: bpy.types.Material = bpy.data.materials.new("Leave Material")
        mat_leave.use_nodes = True
        nodes_leave: typing.List[bpy.types.Node] = mat_leave.node_tree.nodes
        nodes_leave["Principled BSDF"].inputs[0].default_value = [0.038, 0.7, 0.05, 1.000000]

        return mat_leave

def create_trunk_material() -> bpy.types.Material:
        mat_trunk: bpy.types.Material = bpy.data.materials.new("Trunk Material")
        mat_trunk.use_nodes = True
        nodes_leave: typing.List[bpy.types.Node] = mat_trunk.node_tree.nodes
        nodes_leave["Principled BSDF"].inputs[0].default_value = [0.3, 0.152, 0.02, 1.000000]

        return mat_trunk


def generateTree():

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
        posY = 1 * random.uniform(MIN_SHIFT, MAX_SHIFT)
        posX = 1 * random.uniform(MIN_SHIFT, MAX_SHIFT)
        vert = (posX, posY, posZ)
        verts.append(vert)
        if i is not 0:
            edge = (i-1, i)
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
        random_angle = random.randrange(0, 120)
        # rotate??
        rot_matrix_blade = mathutils.Matrix.Rotation(
            math.radians(random_angle), 3, 'Z')
        bmesh.ops.rotate(bm, cent=verts[i].co,
                         matrix=rot_matrix_blade, verts=[verts[i]])
        bm.verts.ensure_lookup_table()

    bmesh.update_edit_mesh(me, True)

    bpy.ops.object.editmode_toggle()

    skin: bpy.types.SkinModifier = bpy.ops.object.modifier_add(type='SKIN')

    rad_x = 1.5
    rad_y = 1.5

    i = 0

    for v in me.skin_vertices[0].data:
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
    bpy.context.object.data.materials.append(create_trunk_material())

    leaves = bpy.ops.mesh.primitive_ico_sphere_add(radius=random.uniform(1, 1.2), enter_editmode=False, align='WORLD', location=(
    posX, posY, posZ + 2), scale=(random.uniform(2.5, 5), random.uniform(2.5, 5), random.uniform(6, 8)))
    bpy.context.object.data.materials.append(create_leave_material())


class Tree(bpy.types.Operator):
    """Insert a Tree"""
    bl_idname = "object.generate_tree"
    bl_label = "Generate a Tree"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        generateTree()
        return {'FINISHED'}

generateTree()


