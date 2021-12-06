import bpy
import bmesh
import random
import numpy.linalg
import numpy as np
# bpy.ops.object.select_all(action='SELECT')
# bpy.ops.object.delete(use_global=False, confirm=False)
# bpy.ops.outliner.orphans_purge()


class SimpleOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.simple_operator"
    bl_label = "Simple Object Operator"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        ground = Ground()
        ground.generate_ground(context)

        return {'FINISHED'}


class Ground:
    # these should be initialized with input
    ground_size = 20
    face_edge_size = 0.5
    biome_total = 4

    # constants
    SUBDIVISION_LEVELS = ground_size / face_edge_size - 1
    VERTCOUNT_EDGE = round(SUBDIVISION_LEVELS + 2)
    BIOME_AMOUNT = 4

    def generate_ground(self, context):
        bpy.ops.mesh.primitive_plane_add(
            size=self.ground_size, location=(0, 0, 0))

        ground = bpy.context.object
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.subdivide(number_cuts=self.SUBDIVISION_LEVELS)
        bpy.ops.object.editmode_toggle()

        ground_mesh = bmesh.new()
        ground_mesh.from_mesh(ground.data)
        ground_mesh.verts.ensure_lookup_table()

        ground_mesh.to_mesh(ground.data)
        ground_mesh.free()
        bpy.ops.texture.new()
        tex_clr = bpy.data.textures["Texture"]
        tex_clr.name = "Voronoi"
        tex_clr.type = 'VORONOI'
        voronoi_clr: bpy.types.VoronoiTexture = bpy.data.textures["Voronoi"]
        voronoi_clr.distance_metric = 'DISTANCE_SQUARED'
        voronoi_clr.color_mode = 'POSITION'
        voronoi_clr.noise_scale = 1
        bpy.ops.texture.new()
        tex_int = bpy.data.textures["Texture"]
        tex_int.name = "Voronoi2"
        tex_int.type = 'VORONOI'
        voronoi_int: bpy.types.VoronoiTexture = bpy.data.textures["Voronoi2"]
        voronoi_int.distance_metric = 'DISTANCE_SQUARED'
        voronoi_int.color_mode = 'INTENSITY'
        voronoi_int.noise_scale = 1

        for i in range(20):
            for val in voronoi_clr.evaluate([i, i, 0]):
                print(val)


class Biome:
    def __init__(self, type):
        self.type = type
        # self.material


class BiomeVertex:
    def __init__(self, x, y, biome):
        self.biome = biome
        self.x = x
        self.y = y


classes = [SimpleOperator]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.object.simple_operator()
