import typing
from bmesh.types import BMFaceSeq
import bpy
import random
import bmesh
import mathutils
import math

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
HEIGHT = AMOUNT / 2.2




def createMaterial(name, value):


    material = bpy.data.materials.new(
        name=name)
    material.use_nodes = True
    material.node_tree.nodes["Principled BSDF"].inputs[0].default_value = value

    return material


class Tree():
    """Insert a Tree"""
    bl_idname = "object.generate_tree"
    bl_label = "Generate a Tree"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        Tree.generateTree()
        return {'FINISHED'}

    def generateTree(location):

        mesh = bpy.data.meshes.new("tree")  # add the new mesh
        obj = bpy.data.objects.new(mesh.name, mesh)
        col = bpy.data.collections.get("Collection")
        col.objects.link(obj)
        bpy.context.view_layer.objects.active = obj

        verts = []
        edges = []

        for i in range(VERTICES):
            posZ = i * 0.6 + location.center.z
            posY = 1 * random.uniform(MIN_SHIFT, MAX_SHIFT) + location.center.y
            posX = 1 * random.uniform(MIN_SHIFT, MAX_SHIFT) + location.center.x
            vert = (posX, posY, posZ)
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
        bpy.context.object.data.materials.append(createMaterial("trunkMaterial", (0.038, 0.7, 0.05, 1.000000)))

        leaves = bpy.ops.mesh.primitive_ico_sphere_add(radius=random.uniform(1, 1.2), enter_editmode=False, align='WORLD', location=(
            posX, posY, posZ), scale=(random.uniform(2.5, 5), random.uniform(2.5, 5), random.uniform(6, 8)))
        bpy.context.object.data.materials.append(createMaterial("leaveMaterial", (0.3, 0.152, 0.02, 1.000000)))

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
    
        bmesh.update_edit_mesh(mesh.data)
    
        bpy.ops.object.editmode_toggle()

    def generatePineTree(location):
        top = AMOUNT * 0.2
        bottom = AMOUNT * 0.55

        for i in range(0, AMOUNT + 1):
            if i is 0:
                Tree.generateCylinder((location.center.x,location.center.y,location.center.z), (1,1,0.75), 0.6, 1, True)
                bpy.context.object.data.materials.append(createMaterial("pineTrunkMaterial", (0.051, 0.010, 0.00, 1.000000))) 
            else:
                if i is AMOUNT:
                    Tree.generateCylinder((location.center.x,location.center.y,location.center.z + HEIGHT * i / AMOUNT), (1,1,0.8), 0.07, bottom, False)
                else:
                    Tree.generateCylinder((location.center.x,location.center.y,location.center.z + HEIGHT * i / AMOUNT), (1,1,0.8), top, bottom, False)
                    top = top - 0.2
                    bottom = bottom-0.4
                bpy.context.object.data.materials.append(createMaterial("pineMaterial", (0.009, 0.141, 0.058, 1.000000))) 
                    
                
                
            