import typing
import bmesh
from bmesh.types import BMFaceSeq
import bpy
import random


AMOUNT = 5
HEIGHT = AMOUNT / 2.2  # 0A2E1E


def create_leave_material() -> bpy.types.Material:
    mat_leave: bpy.types.Material = bpy.data.materials.new("Leave Material")
    mat_leave.use_nodes = True
    nodes_leave: typing.List[bpy.types.Node] = mat_leave.node_tree.nodes
    nodes_leave["Principled BSDF"].inputs[0].default_value = [
        0.009, 0.141, 0.058, 1.000000]

    return mat_leave


def create_trunk_material() -> bpy.types.Material:
    mat_trunk: bpy.types.Material = bpy.data.materials.new("Trunk Material")
    mat_trunk.use_nodes = True
    nodes_leave: typing.List[bpy.types.Node] = mat_trunk.node_tree.nodes
    nodes_leave["Principled BSDF"].inputs[0].default_value = [
        0.051, 0.010, 0.00, 1.000000]

    return mat_trunk


def generateCylinder(location, scale, width_scale_top, width_scale_bottom, trunk):
    mesh = bpy.ops.mesh.primitive_cylinder_add(
        vertices=6, enter_editmode=False, align='WORLD', location=location, scale=scale)
    # rotate

    if not trunk:
        bpy.ops.transform.rotate(value=random.uniform(-1, 1), orient_axis='Z', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(
            False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
        bpy.ops.transform.rotate(value=random.uniform(-0.08, 0.08), orient_axis='Y', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(
            False, True, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
        bpy.ops.transform.rotate(value=random.uniform(-0.08, 0.08), orient_axis='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(
            True, False, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)

    col = bpy.data.collections.get("Collection")
    # Get the active mesh
    mesh = bpy.context.object

    # Get a BMesh representation
    bm = bmesh.new()   # create an empty BMesh
    bm.from_mesh(mesh.data)   # fill it in from a Mesh

    bpy.context.view_layer.objects.active = mesh

    bpy.ops.object.editmode_toggle()

    bm = bmesh.from_edit_mesh(mesh.data)

    bm.faces.ensure_lookup_table()

    for i in range(0, 8):
        face: BMFaceSeq = bm.faces[i]
        if i is 4:
            scale = width_scale_top
        elif i is 7:
            scale = width_scale_bottom
        else:
            scale = random.uniform(0.9, 1.1)

        if isinstance(face, bmesh.types.BMFace):
            c = face.calc_center_median()
            for v in face.verts:
                v.co = c + scale * (v.co - c)

        #face.select = True
        #bpy.ops.mesh.knife_tool(use_occlude_geometry=True, only_selected=False)

    bmesh.update_edit_mesh(mesh.data)

    bpy.ops.object.editmode_toggle()


top = AMOUNT * 0.2
bottom = AMOUNT * 0.55

for i in range(0, AMOUNT + 1):
    if i is 0:
        generateCylinder((0, 0, 0), (1, 1, 0.75), 0.6, 1, True)
        bpy.context.object.data.materials.append(create_trunk_material())
    else:
        if i is AMOUNT:
            generateCylinder((0, 0, HEIGHT * i / AMOUNT),
                             (1, 1, 0.8), 0.07, bottom, False)
        else:
            generateCylinder((0, 0, HEIGHT * i / AMOUNT),
                             (1, 1, 0.8), top, bottom, False)
            top = top - 0.2
            bottom = bottom-0.4
        bpy.context.object.data.materials.append(create_leave_material())
