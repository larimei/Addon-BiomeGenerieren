import typing
from bmesh.types import BMFaceSeq
import bpy
import random
import bmesh
import mathutils
import math
from src import utility

LEAVEMATERIAL: bpy.types.Material
TRUNKMATERIAL: bpy.types.Material
PINEMATERIAL: bpy.types.Material

TREECONTAINER: bpy.types.Object
PINETREECONTAINER: bpy.types.Object
BRANCHTREECONTAINER: bpy.types.Object

VERTICES = 10
MIN_SHIFT = 0.9
MAX_SHIFT = 1.1

AMOUNT = 5
HEIGHT = AMOUNT / 4

leave_positions = []


class Tree():

    def generate_tree(_x, _y, _z):

        mesh = bpy.data.meshes.new("tree")  # add the new mesh
        obj = bpy.data.objects.new(mesh.name, mesh)
        collection = bpy.data.collections.new("TreeCollection")
        bpy.context.scene.collection.children.link(collection)
        collection.objects.link(obj)
        bpy.context.view_layer.objects.active = obj

        verts = []
        edges = []

        for i in range(VERTICES):
            pos_z = i * 0.6 + _x
            pos_y = 1 * random.uniform(MIN_SHIFT, MAX_SHIFT) + _y
            pos_x = 1 * random.uniform(MIN_SHIFT, MAX_SHIFT) + _z
            vert = (pos_x, pos_y, pos_z)
            verts.append(vert)
            if i != 0:
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
            if i == 0:
                rad_x = random.uniform(0.65, 0.85)
                rad_y = random.uniform(0.65, 0.85)
            else:
                rad_x = rad_x - random.uniform(0.02, 0.05)
                rad_y = rad_y - random.uniform(0.025, 0.055)
            i = i + 1

        bpy.ops.object.modifier_add(type='SUBSURF')
        bpy.context.object.modifiers["Subdivision"].render_levels = 1
        bpy.context.object.data.materials.append(
            utility.MaterialUtils.create_material("trunkMaterial", (0.3, 0.152, 0.02, 1.000000)))

        leaves = bpy.ops.mesh.primitive_ico_sphere_add(radius=random.uniform(1, 1.2), enter_editmode=False, align='WORLD', location=(
            pos_x, pos_y, pos_z + 4), scale=(random.uniform(2.5, 4), random.uniform(2.5, 4), random.uniform(4, 6)))
        collection.objects.link(bpy.context.object)
        bpy.ops.collection.objects_remove(collection='Collection')

        bpy.context.object.parent = obj

        bpy.context.object.data.materials.append(
            utility.MaterialUtils.create_material("leaveMaterial", (0.038, 0.7, 0.05, 1.000000)))

    def generate_cylinder(_location, _scale, _width_scale_top, _width_scale_bottom, _trunk):
        mesh = bpy.ops.mesh.primitive_cylinder_add(
            vertices=6, enter_editmode=False, align='WORLD', location=_location, scale=_scale)
        # rotate

        if not _trunk:
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
            if i == 4:
                _scale = _width_scale_top
            elif i == 7:
                _scale = _width_scale_bottom
            else:
                _scale = random.uniform(0.9, 1.1)

            if isinstance(face, bmesh.types.BMFace):
                c = face.calc_center_median()
                for v in face.verts:
                    v.co = c + _scale * (v.co - c)

        bmesh.update_edit_mesh(mesh.data)

        bpy.ops.object.editmode_toggle()

    def generate_pine_tree(_x, _y, _z):
        collection = bpy.data.collections.new("PineCollection")
        bpy.context.scene.collection.children.link(collection)
        top = AMOUNT * 0.2
        bottom = AMOUNT * 0.55
        height = 0

        for i in range(0, AMOUNT + 1):
            if i == 0:
                Tree.generate_cylinder(
                    (_x, _y, _z), (1, 1, 0.75), 0.6, 1, True)

                active = bpy.context.object
                collection.objects.link(active)
                bpy.context.object.data.materials.append(utility.MaterialUtils.create_material(
                    "pineTrunkMaterial", (0.051, 0.010, 0.00, 1.000000)))
                bpy.ops.collection.objects_remove(collection='Collection')

            else:
                if i == AMOUNT:
                    Tree.generate_cylinder(
                        (_x, _y, _z + height), (1, 1, 0.8), 0.07, bottom, False)
                else:
                    Tree.generate_cylinder(
                        (_x, _y, _z + height), (1, 1, 0.8), top, bottom, False)
                    top = top - 0.2
                    bottom = bottom-0.4

                height = height + 0.09
                bpy.context.object.parent = active
                active = bpy.context.object
                collection.objects.link(active)
                bpy.context.object.data.materials.append(utility.MaterialUtils.create_material(
                    "pineMaterial", (0.009, 0.141, 0.058, 1.000000)))
                bpy.ops.collection.objects_remove(collection='Collection')

    def generate_branches(_edges, _verts, _vert, _branch, _last_index):
        bool = False
        for i in range(random.randrange(3, 5)):
            if _branch:
                branchvert = (_vert[0] + random.uniform(0.2, 0.8), _vert[1] +
                              random.uniform(0.2, 0.8), _vert[2] + random.uniform(0.2, 0.8))
            elif _branch is False:
                branchvert = (_vert[0] + random.uniform(-0.8, -0.2), _vert[1] +
                              random.uniform(-0.8, -0.2), _vert[2] + random.uniform(0.2, 0.8))

            _vert = branchvert
            _verts.append(branchvert)
            if i == 0:
                edge = (_last_index - 1, len(_verts) - 1)
            else:
                if bool:
                    edge = (_last_index, len(_verts) - 1)
                    bool = False
                else:
                    edge = (len(_verts) - 2, len(_verts) - 1)

            _edges.append(edge)
        leave_positions.append(branchvert)

    def generate_leaves(_collection, _radius, _position, _scale):

        mesh = bpy.data.meshes.new("LeaveBranches")  # add the new mesh
        obj = bpy.data.objects.new(mesh.name, mesh)
        _collection.objects.link(obj)
        bpy.context.view_layer.objects.active = obj

        # Select the newly created object
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)

        # Construct the bmesh sphere and assign it to the blender mesh.
        bm = bmesh.new()
        bmesh.ops.create_icosphere(
            bm, subdivisions=2, diameter=_radius)
        bm.to_mesh(mesh)
        bm.free()

        bpy.context.object.scale = _scale
        bpy.context.object.location = _position
        bpy.context.object.data.materials.append(utility.MaterialUtils.create_material(
            "branchLeaveMaterial", (0.03, 0.6, 0.04, 1.000000)))

    def generate_more_trunk(_edges, _verts, _vert):
        for i in range(0, 3):
            pos_z = _vert[2] + 0.6
            pos_y = 1 * random.uniform(MIN_SHIFT, MAX_SHIFT)
            pos_x = 1 * random.uniform(MIN_SHIFT, MAX_SHIFT)
            _vert = (pos_x, pos_y, pos_z)
            _verts.append(_vert)
            if i != 0:
                edge = (len(_verts)-2, len(_verts)-1)
                _edges.append(edge)
            else:
                edge = (VERTICES - 1, len(_verts) - 1)
                _edges.append(edge)
        leave_positions.append(_vert)

    def generate_tree_with_branches():

        mesh = bpy.data.meshes.new("treeWithBranches")  # add the new mesh
        obj = bpy.data.objects.new(mesh.name, mesh)
        collection = bpy.data.collections.new("TreeWithBranchesCollection")
        bpy.context.scene.collection.children.link(collection)
        collection.objects.link(obj)
        bpy.context.view_layer.objects.active = obj

        verts = []
        edges = []
        verts_trunk = []

        for i in range(VERTICES):
            pos_z = i * 0.6
            pos_y = 1 * random.uniform(MIN_SHIFT, MAX_SHIFT)
            pos_x = 1 * random.uniform(MIN_SHIFT, MAX_SHIFT)
            vert = (pos_x, pos_y, pos_z)
            verts.append(vert)
            verts_trunk.append(vert)
            if i != 0:
                edge = (i-1, i)
                edges.append(edge)

        Tree.generate_branches(edges, verts, vert, True, VERTICES)
        Tree.generate_branches(edges, verts, vert, False,  VERTICES)
        Tree.generate_more_trunk(edges, verts, vert)

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
                if i == 0:
                    rad_x = random.uniform(0.65, 0.85)
                    rad_y = random.uniform(0.65, 0.85)
                else:
                    rad_x = rad_x - random.uniform(0.02, 0.05)
                    rad_y = rad_y - random.uniform(0.025, 0.055)
                i = i + 1

        bpy.ops.object.modifier_add(type='SUBSURF')
        bpy.context.object.modifiers["Subdivision"].render_levels = 1

        bpy.context.object.data.materials.append(utility.MaterialUtils.create_material(
            "branchTrunkMaterial", (0.279, 0.122, 0.01, 1.000000)))

        for modifier in obj.modifiers:
            bpy.ops.object.modifier_apply(modifier=modifier.name)

        for pos in leave_positions:
            if pos is leave_positions[len(leave_positions) - 1]:
                Tree.generate_leaves(collection, random.uniform(
                    1, 1.7), (pos[0], pos[1], pos[2] + 1.6), (random.uniform(2, 2.3), random.uniform(2, 2.3), random.uniform(1.2, 2)))

            else:
                Tree.generate_leaves(collection, random.uniform(1, 1.2), (pos[0], pos[1], pos[2]), (
                    random.uniform(1.3, 1.9), random.uniform(1.3, 1.9), random.uniform(1, 1.1)))
