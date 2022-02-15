import bpy
from src.utility import TextureUtils


class GlobalNoise:

    def __init__(self, _scale: float):
        bpy.ops.texture.new()
        tex_clr = TextureUtils.get_texture_if_exists("GlobalNoise")
        tex_clr.name = "GlobalNoise"
        tex_clr.type = 'CLOUDS'
        self.cloud: bpy.types.CloudsTexture = bpy.data.textures["GlobalNoise"]
        self.cloud.noise_basis = 'BLENDER_ORIGINAL'
        self.cloud.cloud_type = 'GRAYSCALE'
        self.cloud.noise_scale = _scale

    def get_height(self, _x, _y):
        return self.cloud.evaluate([_x, _y, 0])[3] * 3
