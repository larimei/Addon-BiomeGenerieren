import bmesh
import bpy



def generateCylinder(location, scale, width_scale_top, width_scale_bottom):
    mesh = bpy.ops.mesh.primitive_cylinder_add(vertices=6, enter_editmode=False, align='WORLD', location=location, scale=scale)
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
    face_top = bm.faces[4]
    if isinstance(face_top, bmesh.types.BMFace):
        c = face_top.calc_center_median()
        for v in face_top.verts:
            v.co = c + width_scale_top * (v.co - c)
    face_bottom = bm.faces[7]
    if isinstance(face_top, bmesh.types.BMFace):
        c = face_bottom.calc_center_median()
        for v in face_bottom.verts:
            v.co = c + width_scale_bottom * (v.co - c)

    bmesh.update_edit_mesh(mesh.data)
    
    bpy.ops.object.editmode_toggle()


generateCylinder((0,0,0), (1,1,0.75), 0.6, 1)
generateCylinder((0,0,0.5), (1,1,0.8), 0.6, 2.3)
generateCylinder((0,0,1), (1,1,0.8), 0.5, 2)
generateCylinder((0,0,1.5), (1,1,0.8), 0.4, 1.5)
generateCylinder((0,0,2), (1,1,0.8), 0.1, 1)