import bpy
import random
from . src.ground import Ground
from .src.biomes.generate_grass_biome import GenerateGrassBiome
from .src.biomes.generate_tree_biome import Tree
from .src.biomes.generate_desert_biome import Cactus
from .src.biomes.generate_desert_biome import Stone
from . src.utility import CleanCollectionsUtils, ParticleUtils
from . src.ui import *


bl_info = {
    "name": "Generate Biomes",
    "author": "Valentin, Fabian, Viktor, Lara",
    "version": (1, 0),
    "blender": (2, 90, 0),
    "location": "View3D > Toolbar > Generate Biomes",
    "description": "Adds different biomes based different parameters",
    "warning": "",
    "wiki_url": "",
    "category": "Add Mesh",
}

class GENERATEBIOMES_OT_reset_scene(bpy.types.Operator):
    bl_idname = "generatebiomes.reset_scene"
    bl_label = "Reset Scene"

    def execute(self, context):
        for collection in bpy.data.collections:
            if collection.name != "Collection":
                bpy.data.collections.remove(collection)
            else:
                for object in collection.objects:
                    bpy.data.objects.remove(object)

        return {'FINISHED'}


class GENERATEBIOMES_OT_generate_ground(bpy.types.Operator):
    bl_idname = "generatebiomes.generate_ground"
    bl_label = "Generate Ground"

    def execute(self, context):
        GENERATEBIOMES_OT_reset_scene.execute(
            GENERATEBIOMES_OT_reset_scene, context)
        # ground--------------------------
        weights = [float(context.scene.grassWeight), float(context.scene.forestWeight), float(
            context.scene.desertWeight), float(context.scene.mountainWeight)]
        colors = [context.scene.grassColor, context.scene.forestColor,
                  context.scene.desertColor, context.scene.mountainColor, context.scene.snowColor]
        ground = Ground(int(context.scene.size), float(context.scene.groundEdgeSize), int(context.scene.offsetX), int(
            context.scene.offsetY), float(context.scene.biomeScale), float(context.scene.snowBorder), weights=weights, colors=colors)

        ground.generate_ground()
        # grass--------------------------
        GenerateBiomeContent.generate_grass_biome(int(context.scene.grassCount),
                                                  int(context.scene.flowerCount), int(context.scene.bushCount))
        # forest--------------------------
        GenerateBiomeContent.generate_forest_biome(
            int(context.scene.treeCount), int(context.scene.pineCount), int(context.scene.branchCount))

        # desert--------------------------
        GenerateBiomeContent.generate_desert_biome(
            int(context.scene.cactusCount), int(context.scene.stoneCount))

        bpy.context.space_data.shading.type = 'MATERIAL'

        CleanCollectionsUtils.clean_system()

        return {'FINISHED'}


class GenerateBiomeContent():

    def generate_grass_biome(_grass_count, _flower_count, _bush_count):
        grass_biome = GenerateGrassBiome(0.6, 0.3, 4, 12, 0.3, 25, 30, 90, 5)
        grass_biome.create_grass_array()
        grass_biome.create_flowers_array()
        grass_biome.create_bushes_array()

        ParticleUtils.create_particle_system(
            bpy.data.objects["Plane"], "grassParticles", "grass", "GrassCollection", _grass_count, 0, random.uniform(0.0075, 0.0085), random.randint(0, 10))
        ParticleUtils.create_particle_system(
            bpy.data.objects["Plane"], "flowerParticles", "grass", "FlowerCollection", _flower_count, 1.0, random.uniform(0.009, 0.0125), random.randint(0, 5))
        ParticleUtils.create_particle_system(
            bpy.data.objects["Plane"], "bushParticles", "grass", "BushCollection0", int(_bush_count/3.0), 1.0, random.uniform(0.015, 0.025), random.randint(0, 2))
        ParticleUtils.create_particle_system(
            bpy.data.objects["Plane"], "bushParticles.001", "grass", "BushCollection1", int(_bush_count/3.0), 1.0, random.uniform(0.015, 0.025), random.randint(2, 4))
        ParticleUtils.create_particle_system(
            bpy.data.objects["Plane"], "bushParticles.002", "grass", "BushCollection2", int(_bush_count/3.0), 1.0, random.uniform(0.015, 0.025), random.randint(4, 6))

    def generate_forest_biome(_tree_count, _pine_count, _branch_count):
        Tree.generate_tree(0, 0, 0)
        ParticleUtils.create_particle_system(
            bpy.data.objects["Plane"], "treeParticles", "forest", "TreeCollection", _tree_count, 0, random.uniform(0.025, 0.03), random.randint(0, 2))

        Tree.generate_pine_tree(0, 0, 0.7)
        ParticleUtils.create_particle_system(
            bpy.data.objects["Plane"], "pineParticles", "forest", "PineCollection", _pine_count, 0, random.uniform(0.06, 0.07), random.randint(2, 4))

        Tree.generate_tree_with_branches()
        ParticleUtils.create_particle_system(
            bpy.data.objects["Plane"], "branchParticles", "forest", "TreeWithBranchesCollection", _branch_count, 0, random.uniform(0.06, 0.07), random.randint(4, 6))

    def generate_desert_biome(_cactus_count, _stone_count):
        Cactus.generate_cactus()
        ParticleUtils.create_particle_system(
            bpy.data.objects["Plane"], "cactusParticles", "desert", "CactusCollection0", int(_cactus_count/3.0), 1.0, random.uniform(0.02, 0.03), random.randint(0, 2))
        ParticleUtils.create_particle_system(
            bpy.data.objects["Plane"], "cactusParticles.001", "desert", "CactusCollection1", int(_cactus_count/3.0), 1.0, random.uniform(0.02, 0.03), random.randint(2, 4))
        ParticleUtils.create_particle_system(
            bpy.data.objects["Plane"], "cactusParticles.002", "desert", "CactusCollection2", int(_cactus_count/3.0), 1.0, random.uniform(0.02, 0.03), random.randint(4, 6))

        Stone.generate_stone()
        ParticleUtils.create_particle_system(
            bpy.data.objects["Plane"], "stoneParticles", "desert", "StoneCollection0", int(_stone_count/3), 1.0, random.uniform(0.02, 0.03), random.randint(6, 8))
        ParticleUtils.create_particle_system(
            bpy.data.objects["Plane"], "stoneParticles.001", "desert", "StoneCollection1", int(_stone_count/3), 1.0, random.uniform(0.02, 0.03), random.randint(10, 12))
        ParticleUtils.create_particle_system(
            bpy.data.objects["Plane"], "stoneParticles.002", "desert", "StoneCollection2", int(_stone_count/3), 1.0, random.uniform(0.02, 0.03), random.randint(12, 14))


classes = [GENERATEBIOMES_PT_MainPanel, GENERATEBIOMES_PT_DistributionPanel, GENERATEBIOMES_PT_DesertPanel, GENERATEBIOMES_PT_ForestPanel, GENERATEBIOMES_PT_GrassPanel, GENERATEBIOMES_PT_MountainPanel,
           GENERATEBIOMES_OT_generate_ground, GENERATEBIOMES_OT_reset_scene]


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
        default=30
    )
    bpy.types.Scene.stoneCount = bpy.props.IntProperty(
        name="Stone Count",
        default=30
    )
    bpy.types.Scene.grassCount = bpy.props.IntProperty(
        name="Grass Count",
        default=500
    )
    bpy.types.Scene.flowerCount = bpy.props.IntProperty(
        name="Flower Count",
        default=25
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
        default=(0.0712, 0.287, 0.068, 1.000000),
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