
import random
from . import genGrass
import bpy


bl_info = {
    "name": "Generate Biomes",
    "author": "Valentin, Fabian, Viktor, Lara",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Toolbar > Generate Biomes",
    "description": "Adds different biomes, where you can set different parameters",
    "warning": "",
    "wiki_url": "",
    "category": "Add Mesh",
}

#from .  import ui
# This is the Main Panel in 3DView


class MainPanel(bpy.types.Panel):
    bl_label = "Generate Biomes"
    bl_idname = "script.execute_preset"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Generate Biomes'

    def draw(self, context):
        layout = self.layout
        layout.scale_x = 4
        layout.scale_y = 2

        row = layout.row()
        row.label(text="Add a biome", icon='WORLD')
        row = layout.row()
        # insert operator
        row.operator("object.text_add", text="Add Desert")
        # insert operator
        row.operator("object.text_add", text="Add Forest")
        row = layout.row()
        # insert operator
        row.operator("object.text_add", text="Add Ocean")
        # insert operator
        row.operator("object.text_add", text="Add Mountains")
        row = layout.row()
        # insert operator
        row.operator("grass.gen", text="Add Grass")
        # insert operator
        row.operator("delete.all", text="Delete all")


class DeleteAll(bpy.types.Operator):
    bl_idname = "delete.all"
    bl_label = "Button text"

    def execute(self, context):
        # Szene leeren
        bpy.ops.object.select_all(action='SELECT')  # selektiert alle Objekte
        # löscht selektierte objekte
        bpy.ops.object.delete(use_global=False, confirm=False)
        bpy.ops.outliner.orphans_purge()  # löscht überbleibende Meshdaten etc.
        return {'FINISHED'}


class GenerateGrass(bpy.types.Operator):
    bl_idname = "grass.gen"
    bl_label = "Button text"

    def execute(self, context):
        grassContainer = bpy.data.objects.new("grassContainer", None)
        bpy.context.collection.objects.link(grassContainer)
        flowerContainer = bpy.data.objects.new("flowerContainer", None)
        bpy.context.collection.objects.link(flowerContainer)
        for i in range(2000):
            x = random.randrange(-200, 200)
            y = random.randrange(-200, 200)
            randMod = random.randrange(100, 150)
            if(i % randMod == 0):
                genGrass.GenerateGrass.genFlowers(
                    genGrass, x, y, grassContainer)
            genGrass.GenerateGrass.genGrass(genGrass, x, y, flowerContainer)
        return {'FINISHED'}


class SimpleOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.simple_operator"
    bl_label = "Simple Object Operator"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        main(context)
        return {'FINISHED'}


def main(context):
    for ob in context.scene.objects:
        print(ob)


classes = [MainPanel, SimpleOperator, GenerateGrass, DeleteAll]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
