
from src.ground import Ground
from src.genGrassBiome import GenerateGrassBiome
from src.generateTree import Tree
from src.cactus import Cactus
from src.stone import Stone
from src.utility import CleanCollectionsUtils, ParticleUtils
from src.ui import *
import bpy


bl_info = {
    "name": "Generate Biomes",
    "author": "Valentin, Fabian, Viktor, Lara",
    "version": (1, 0),
    "blender": (2, 90, 0),
    "location": "View3D > Toolbar > Generate Biomes",
    "description": "Adds different biomes, where you can set different parameters",
    "warning": "",
    "wiki_url": "",
    "category": "Add Mesh",
}

# from .  import ui
# This is the Main Panel in 3DView


class DeleteAll(bpy.types.Operator):
    bl_idname = "delete.all"
    bl_label = "Button text"

    def execute(self, context):
        # Szene leeren
        bpy.ops.object.select_all(action='SELECT')  # selektiert alle Objekte
        # löscht selektierte objekte
        bpy.ops.object.delete(use_global=False, confirm=False)
        bpy.ops.outliner.orphans_purge()  # löscht überbleibende Meshdaten etc.
        for collection in bpy.data.collections:
            if collection.name != "Collection":
                bpy.data.collections.remove(collection)

        return {'FINISHED'}


class GenerateGround(bpy.types.Operator):
    bl_idname = "gen.landscape"
    bl_label = "Button text"

    def execute(self, context):
        DeleteAll.execute(DeleteAll, context)
        # ground--------------------------
        weights = [float(context.scene.grassWeight), float(context.scene.forestWeight), float(
            context.scene.desertWeight), float(context.scene.mountainWeight)]
        colors = [context.scene.grassColor, context.scene.forestColor,
                  context.scene.desertColor, context.scene.mountainColor, context.scene.snowColor]
        ground = Ground(int(context.scene.size), float(context.scene.groundEdgeSize), int(context.scene.offsetX), int(
            context.scene.offsetY), float(context.scene.biomeScale), float(context.scene.snowBorder), weights=weights, colors=colors)

        ground.generate_ground(context)
        # grass--------------------------
        GenerateBiomeContent.generateGrassBiome(int(context.scene.grassCount),
                                                int(context.scene.flowerCount), int(context.scene.bushCount))
        # forest--------------------------
        GenerateBiomeContent.generateForestBiome(
            int(context.scene.treeCount), int(context.scene.pineCount), int(context.scene.branchCount))

        # desert--------------------------
        GenerateBiomeContent.generateDesertBiome(
            int(context.scene.cactusCount), int(context.scene.stoneCount))

        bpy.context.space_data.shading.type = 'MATERIAL'

        CleanCollectionsUtils.cleanSystem()

        return {'FINISHED'}


class GenerateBiomeContent():

    def generateGrassBiome(grassCount, flowerCount, bushCount):
        GenerateGrassBiome.createGrassArray()
        GenerateGrassBiome.createFlowersArray()
        GenerateGrassBiome.genBushes()
        ParticleUtils.createParticleSystem(
            bpy.data.objects["Plane"], "grassParticles", "grass", "GrassCollection", grassCount, 1.0, 0.01, 1)
        ParticleUtils.createParticleSystem(
            bpy.data.objects["Plane"], "flowerParticles", "grass", "FlowerCollection", flowerCount, 1.0, 0.01, 1)
        ParticleUtils.createParticleSystem(
            bpy.data.objects["Plane"], "bushParticles", "grass", "BushCollection", bushCount, 1.0, 0.25, 1)

    def generateForestBiome(treeCount, pineCount, branchCount):
        Tree.generateTree(0, 0, 0)
        ParticleUtils.createParticleSystem(
            bpy.data.objects["Plane"], "treeParticles", "forest", "TreeCollection", treeCount, 1.0, 0.03, 1)

        Tree.generatePineTree(0, 0, 0.7)
        ParticleUtils.createParticleSystem(
            bpy.data.objects["Plane"], "pineParticles", "forest", "PineCollection", pineCount, 1.0, 0.06, 2)

        Tree.generateTreeWithBranches()
        ParticleUtils.createParticleSystem(
            bpy.data.objects["Plane"], "branchParticles", "forest", "TreeWithBranchesCollection", branchCount, 1.0, 0.06, 3)

    def generateDesertBiome(cactusCount, stoneCount):
        # generate Desert content here
        Cactus.generateCactus()
        ParticleUtils.createParticleSystem(
            bpy.data.objects["Plane"], "cactusParticles", "desert", "CactusCollection", cactusCount, 1.0, 0.03, 1)

        stone = Stone()
        stone.generateStone()
        ParticleUtils.createParticleSystem(
            bpy.data.objects["Plane"], "stoneParticles", "desert", "StoneCollection", stoneCount, 1.0, 0.025, 1)


classes = [MainPanel, DistributionPanel, DesertPanel, ForestPanel, GrassPanel, MountainPanel,
           GenerateGround, DeleteAll]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.size = bpy.props.IntProperty(
        name="Ground Mesh Size",
        default=80
    )
    bpy.types.Scene.offsetX = bpy.props.IntProperty(
        name="Biome offset X",
        default=10
    )
    bpy.types.Scene.offsetY = bpy.props.IntProperty(
        name="Biome offset Y",
        default=10
    )
    bpy.types.Scene.biomeScale = bpy.props.FloatProperty(
        name="Biome Scale",
        default=20.0
    )
    bpy.types.Scene.groundEdgeSize = bpy.props.FloatProperty(
        name="Ground Edge Size",
        default=0.5,
        min=0.1,
        step=10
    )
    bpy.types.Scene.cactusCount = bpy.props.IntProperty(
        name="Cactus Count",
        default=50
    )
    bpy.types.Scene.stoneCount = bpy.props.IntProperty(
        name="Stone Count",
        default=10
    )
    bpy.types.Scene.grassCount = bpy.props.IntProperty(
        name="Grass Count",
        default=500
    )
    bpy.types.Scene.flowerCount = bpy.props.IntProperty(
        name="Flower Count",
        default=50
    )
    bpy.types.Scene.bushCount = bpy.props.IntProperty(
        name="Bush Count",
        default=10
    )
    bpy.types.Scene.treeCount = bpy.props.IntProperty(
        name="Tree Count",
        default=12
    )
    bpy.types.Scene.pineCount = bpy.props.IntProperty(
        name="Pine Count",
        default=16
    )
    bpy.types.Scene.branchCount = bpy.props.IntProperty(
        name="Tree With Branches Count",
        default=12
    )
    bpy.types.Scene.snowBorder = bpy.props.FloatProperty(
        name="Snow Border Height",
        default=6.5,
        soft_min=0.0,
        soft_max=1.0,
        step=10
    )
    bpy.types.Scene.grassWeight = bpy.props.FloatProperty(
        name="Grass Biome Weight",
        default=1.0,
        min=0.0,
        max=1.0,
        soft_min=0.0,
        soft_max=1.0,
        step=10
    )
    bpy.types.Scene.forestWeight = bpy.props.FloatProperty(
        name="Forest Biome Weight",
        default=1.0,
        min=0.0,
        max=1.0,
        soft_min=0.0,
        soft_max=1.0,
        step=10
    )
    bpy.types.Scene.desertWeight = bpy.props.FloatProperty(
        name="Desert Biome Weight",
        default=1.0,
        min=0.0,
        max=1.0,
        soft_min=0.0,
        soft_max=1.0,
        step=10
    )
    bpy.types.Scene.mountainWeight = bpy.props.FloatProperty(
        name="Mountain Biome Weight",
        default=1.0,
        min=0.0,
        max=1.0,
        soft_min=0.0,
        soft_max=1.0,
        step=10
    )

    bpy.types.Scene.grassColor = bpy.props.FloatVectorProperty(
        name="Grass Color",
        subtype="COLOR",
        default=(0.09, 0.9, 0.1, 1.000000),
        size=4,
        min=0.0,
        max=1.0,
    )
    bpy.types.Scene.forestColor = bpy.props.FloatVectorProperty(
        name="Forest Color",
        subtype="COLOR",
        default=(0.038, 0.7, 0.05, 1.000000),
        size=4,
        min=0.0,
        max=1.0,
    )
    bpy.types.Scene.desertColor = bpy.props.FloatVectorProperty(
        name="Desert Color",
        subtype="COLOR",
        default=(0.77, 0.65, 0.39, 1.000000),
        size=4,
        min=0.0,
        max=1.0,
    )
    bpy.types.Scene.mountainColor = bpy.props.FloatVectorProperty(
        name="Mountain Color",
        subtype="COLOR",
        default=(0.4, 0.4, 0.4, 1.000000),
        size=4,
        min=0.0,
        max=1.0,
    )
    bpy.types.Scene.snowColor = bpy.props.FloatVectorProperty(
        name="Snow Color",
        subtype="COLOR",
        default=(0.95, 0.95, 0.95, 1.000000),
        size=4,
        min=0.0,
        max=1.0,
    )


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.size
    del bpy.types.Scene.offsetX
    del bpy.types.Scene.offsetY
    del bpy.types.Scene.biomeScale
    del bpy.types.Scene.cactusCount
    del bpy.types.Scene.stoneCount
    del bpy.types.Scene.grassCount
    del bpy.types.Scene.flowerCount
    del bpy.types.Scene.bushCount
    del bpy.types.Scene.treeCount
    del bpy.types.Scene.pineCount
    del bpy.types.Scene.grassWeight
    del bpy.types.Scene.forestWeight
    del bpy.types.Scene.desertWeight
    del bpy.types.Scene.mountainWeight
    del bpy.types.Scene.grassColor
    del bpy.types.Scene.forestColor
    del bpy.types.Scene.desertColor
    del bpy.types.Scene.mountainColor
    del bpy.types.Scene.snowColor
    del bpy.types.Scene.groundEdgeSize


if __name__ == "__main__":
    register()
