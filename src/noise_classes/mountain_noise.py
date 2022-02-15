import bpy
from ...src.utility import TextureUtils


class MountainNoise:

    def __init__(self, _scale: float, _distortion: float):
        bpy.ops.texture.new()
        tex_clr = TextureUtils.get_texture_if_exists("Mountain")
        tex_clr.name = "Mountain"
        tex_clr.type = 'DISTORTED_NOISE'
        self.mountain: bpy.types.DistortedNoiseTexture = bpy.data.textures["Mountain"]
        self.mountain.noise_distortion = 'IMPROVED_PERLIN'
        self.mountain.noise_scale = _scale
        self.mountain.distortion = _distortion

    def get_height(self, _x, _y):
        return self.mountain.evaluate([_x, _y, 0])[3]
