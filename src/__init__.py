
import math
import random
from . import ground
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
        GenerateGrass().execute()
        return {'FINISHED'}


class GenerateGrass():

    def execute(GenerateGrass,):

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

        leavesMaterials = [None] * 4
        grassArray = genGrass.GenerateGrass.createGrassArray(
            genGrass, grassMat)

        for i in range(len(leavesMaterials)-1):
            leavesMaterials[i] = bpy.data.materials.new(
                name="blossomMaterial")
            leavesMaterials[i].use_nodes = True
            leavesMaterials[i].node_tree.nodes["Principled BSDF"].inputs[0].default_value = (
                random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1), 1)

        for i in range(len(ground.Ground.grass_faces)):
            rnd = random.randint(5, 25)
            if i % rnd == 0:
                genGrass.GenerateGrass.genGrass(
                    genGrass, grassArray, grassContainer, ground.Ground.grass_faces[i])

            # genGrass.GenerateGrass.genFlowers(
            #    genGrass,  flowerContainer, stemMat, blossomMat, leavesMaterials, ground.Ground.grass_faces)
            # rand bushes creation
            # genGrass.GenerateGrass.genBushes(
            # genGrass, bushesContainer, bushMat, ground.Ground.grass_faces)
            # rand grass creation


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
