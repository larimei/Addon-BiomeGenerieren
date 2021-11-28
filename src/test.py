import bpy

# bpy.ops.object.select_all(action='SELECT')
# bpy.ops.object.delete(use_global=False, confirm=False)
# bpy.ops.outliner.orphans_purge()


class SimpleOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.simple_operator"
    bl_label = "Simple Object Operator"

    ground_size = 20
    subdivision_levels = ground_size - 1

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        bpy.ops.mesh.primitive_plane_add(
            size=self.ground_size, location=(0, 0, 0))

        ground = bpy.context.object
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.subdivide(number_cuts=self.subdivision_levels)
        bpy.ops.object.editmode_toggle()

        return {'FINISHED'}


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
