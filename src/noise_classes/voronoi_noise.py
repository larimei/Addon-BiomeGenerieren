import bpy
from ...src.utility import TextureUtils


class VoronoiNoise:
    distribution = []
    biome_allowed = []

    def __init__(self, _scale: float, _grass_weight, _forest_weight, _desert_weight, _mountain_weight):
        self.distribution, self.biome_allowed = self.calc_distributions(
            _grass_weight, _forest_weight, _desert_weight, _mountain_weight)
        bpy.ops.texture.new()
        tex_color = TextureUtils.get_texture_if_exists("Voronoi")
        tex_color.name = "Voronoi"
        tex_color.type = 'VORONOI'
        self.voronoi_color: bpy.types.VoronoiTexture = bpy.data.textures["Voronoi"]
        self.voronoi_color.distance_metric = 'MINKOVSKY_FOUR'
        self.voronoi_color.color_mode = 'POSITION'
        self.voronoi_color.noise_scale = _scale

        bpy.ops.texture.new()
        tex_weight = TextureUtils.get_texture_if_exists("Weight")
        tex_weight.name = "Weight"
        tex_weight.type = 'VORONOI'
        self.voronoi_weight: bpy.types.VoronoiTexture = bpy.data.textures["Weight"]
        self.voronoi_weight.distance_metric = 'DISTANCE_SQUARED'
        self.voronoi_weight.color_mode = 'POSITION'
        self.voronoi_weight.noise_scale = _scale

    def get_biome_and_weight(self, _x, _y):
        colors = self.voronoi_color.evaluate([_x, _y, 0])
        weights = self.voronoi_weight.evaluate([_x, _y, 0])
        color = colors[1]
        weight = 0
        biome = 0
        # mountain
        if color >= self.distribution[3] and self.biome_allowed[3]:
            biome = 3
            weight = (weights[3] - 1) * (-1)
            weight = (weight * weight) * 2
        # desert
        elif color >= self.distribution[2] and self.biome_allowed[2]:
            biome = 2
        # forest
        elif color >= self.distribution[1] and self.biome_allowed[1]:
            biome = 1
        # grass
        elif color >= self.distribution[0] and self.biome_allowed[0]:
            biome = 0
        return biome, weight

    def calc_distributions(self, _grass_weight, _forest_weight, _desert_weight, _mountain_weight):
        # biomes are generated based on the green color value of a voronoi diagram
        # the default steps are a different biome every 0.25 green value,
        # they have to be remapped when the weights change
        total = _grass_weight + _forest_weight + _desert_weight + _mountain_weight
        mtnDist = total - _mountain_weight
        desertDist = mtnDist - _desert_weight
        forestDist = desertDist - _forest_weight
        grassDist = 0
        flags = [bool(_grass_weight), bool(_forest_weight),
                 bool(_desert_weight), bool(_mountain_weight)]
        if bool(total):
            distribution = [grassDist, (forestDist/total),
                            (desertDist/total), (mtnDist/total)]
            return distribution, flags
        else:
            distribution = [0, 0, 0, 0]
            return distribution, flags
