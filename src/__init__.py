
import math
import random
from . import ground
from . import genGrassBiome
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
        layout.scale_x = 8
        layout.scale_y = 4

        row = layout.row()
        row.label(text="Add a biome", icon='WORLD')

        col = self.layout.column(align=True)
        col.prop(context.scene, "size")
        col.prop(context.scene, "offsetX")
        col.prop(context.scene, "offsetY")
        row = layout.row()
        # insert operator
        row.operator("gen.landscape", text="Generate")
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


class GenerateGround(bpy.types.Operator):
    bl_idname = "gen.landscape"
    bl_label = "Button text"

    def execute(self, context):
        # ground--------------------------
        ground.Ground.initializeVariable(ground.Ground,
                                         int(context.scene.size), int(context.scene.offsetX), int(context.scene.offsetY))
        ground.Ground.generate_ground(ground.Ground, context)
        # ground--------------------------
        GenerateBiomeContent().generateGrassBiome()
        return {'FINISHED'}


class GenerateBiomeContent():

    def generateGrassBiome(GenerateGrass):
        genGrassBiome.GenerateGrassBiome.createMaterials(genGrassBiome)
        grassArray = genGrassBiome.GenerateGrassBiome.createGrassArray(
            genGrassBiome)
        for i in range(len(ground.Ground.grass_faces)):
            rndGrass = random.randint(50, 75)
            if i % rndGrass == 0:
                genGrassBiome.GenerateGrassBiome.genGrass(
                    genGrassBiome, grassArray, ground.Ground.grass_faces[i])
            rndFlowers = random.randint(200, 400)
            if i % rndFlowers == 0:
                genGrassBiome.GenerateGrassBiome.genFlowers(
                    genGrassBiome, ground.Ground.grass_faces[i])
            rndBushes = random.randint(400, 700)
            if i % rndBushes == 0:
                genGrassBiome.GenerateGrassBiome.genBushes(
                    genGrassBiome, ground.Ground.grass_faces[i])

    def generateForestBiome(GenerateGrass):
        # generate Forrest content here
        for i in range(len(ground.Ground.forest_faces)):
            print(ground.Ground.forest_faces[i])

    def generateDesertBiome(GenerateGrass):
        # generate Desert content here
        for i in range(len(ground.Ground.desert_faces)):
            print(ground.Ground.desert_faces[i])

    def generateMountainBiome(GenerateGrass):
        # generate Mountain content here
        for i in range(len(ground.Ground.mountain_faces)):
            print(ground.Ground.mountain_faces[i])


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


classes = [MainPanel, SimpleOperator,
           GenerateGround, DeleteAll]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.size = bpy.props.StringProperty(
        name="Ground Size",
        description="My description",
        default="80"
    )
    bpy.types.Scene.offsetX = bpy.props.StringProperty(
        name="Biom offset X",
        description="My description",
        default="10"
    )
    bpy.types.Scene.offsetY = bpy.props.StringProperty(
        name="Biom offset Y",
        description="My description",
        default="10"
    )


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.size
    del bpy.types.Scene.offsetX
    del bpy.types.Scene.offsetY


if __name__ == "__main__":
    register()
