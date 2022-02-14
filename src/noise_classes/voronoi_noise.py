import bpy 
from src.utility import TextureUtils
class VoronoiNoise:
    distribution = []
    biome_allowed = []

    def __init__(self, scale: float, grassWeight, forestWeight, desertWeight, mountainWeight):
        self.distribution, self.biome_allowed = self.calcDistributions(
            grassWeight, forestWeight, desertWeight, mountainWeight)
        bpy.ops.texture.new()
        tex_clr = TextureUtils.get_texture_if_exists("Voronoi")
        tex_clr.name = "Voronoi"
        tex_clr.type = 'VORONOI'
        self.voronoi_clr: bpy.types.VoronoiTexture = bpy.data.textures["Voronoi"]
        self.voronoi_clr.distance_metric = 'MINKOVSKY_FOUR'
        self.voronoi_clr.color_mode = 'POSITION'
        self.voronoi_clr.noise_scale = scale

        bpy.ops.texture.new()
        tex_weight = TextureUtils.get_texture_if_exists("Weight")
        tex_weight.name = "Weight"
        tex_weight.type = 'VORONOI'
        self.voronoi_weight: bpy.types.VoronoiTexture = bpy.data.textures["Weight"]
        self.voronoi_weight.distance_metric = 'DISTANCE_SQUARED'
        self.voronoi_weight.color_mode = 'POSITION'
        self.voronoi_weight.noise_scale = scale

    def get_biome_and_weight(self, x, y):
        colors = self.voronoi_clr.evaluate([x, y, 0])
        weights = self.voronoi_weight.evaluate([x, y, 0])
        color = colors[1]
        weight = 0
        biome = 0
        if color >= self.distribution[3] and self.biome_allowed[3]:
            biome = 3
            weight = (weights[3] - 1) * (-1)
            weight = (weight * weight) * 2
        elif color >= self.distribution[2] and self.biome_allowed[2]:
            biome = 2
        elif color >= self.distribution[1] and self.biome_allowed[1]:
            biome = 1
        elif color >= self.distribution[0] and self.biome_allowed[0]:
            biome = 0
        return biome, weight

    def calcDistributions(self, grassW, forestW, desertW, mountainW):
        total = grassW + forestW + desertW + mountainW
        mtnDist = total - mountainW
        desertDist = mtnDist - desertW
        forestDist = desertDist - forestW
        grassDist = 0
        flags = [bool(grassW), bool(forestW), bool(desertW), bool(mountainW)]
        if bool(total):
            distribution = [grassDist, (forestDist/total),
                            (desertDist/total), (mtnDist/total)]
            return distribution, flags
        else:
            distribution = [0, 0, 0, 0]
            return distribution, flags

