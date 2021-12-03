
import math
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

# from .  import ui
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
        layout.scale_y = 4

        row = layout.row()
        row.label(text="Add a biome", icon='WORLD')

        col = self.layout.column(align=True)
        col.prop(context.scene, "range")

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
        bushesContainer = bpy.data.objects.new("bushesContainer", None)
        bpy.context.collection.objects.link(bushesContainer)

        grassMat: bpy.types.Material = bpy.data.materials.new(
            name="grassMaterial")
        grassMat.use_nodes = True
        grassMat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (
            0, 0.4, 0.1, 1)
        bushMat: bpy.types.Material = bpy.data.materials.new(
            name="bushMaterial")
        bushMat.use_nodes = True
        bushMat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (
            0, 0.3, 0.2, 1)
        stemMat: bpy.types.Material = bpy.data.materials.new(
            name="stemMaterial")
        stemMat.use_nodes = True
        stemMat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (
            0.4, 0.1, 0, 1)
        blossomMat: bpy.types.Material = bpy.data.materials.new(
            name="blossomMaterial")
        blossomMat.use_nodes = True
        blossomMat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (
            1, 1, 0.6, 1)

        terrainRange: int = int(context.scene.range) * int(context.scene.range)
        for i in range(terrainRange):
            x = random.randrange(round(-terrainRange/20),
                                 round(terrainRange/20))
            y = random.randrange(round(-terrainRange/20),
                                 round(terrainRange/20))

            randFlow = random.randrange(
                round(terrainRange/16), round(terrainRange/8))
            if(i % randFlow == 0):
                genGrass.GenerateGrass.genFlowers(
                    genGrass, x, y, flowerContainer, stemMat, blossomMat)
            randBushes = random.randrange(
                round(terrainRange/8), round(terrainRange/4))

            if(i % randBushes == 0):
                genGrass.GenerateGrass.genBushes(
                    genGrass, x, y, bushesContainer, bushMat)
            genGrass.GenerateGrass.genGrass(
                genGrass, x, y, grassContainer, grassMat)
        return {'FINISHED'}


class SimpleOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.simple_operator"
    bl_label = "Simple Object Operator"

    @ classmethod
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
    bpy.types.Scene.range = bpy.props.StringProperty(
        name="Quadratmeters",
        description="My description",
        default="40"
    )


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.range


if __name__ == "__main__":
    register()
