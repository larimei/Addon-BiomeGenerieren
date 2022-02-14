import bpy
from src.utility import TextureUtils


class MountainNoise:

    def __init__(self, scale: float, distortion: float):
        bpy.ops.texture.new()
        tex_clr = TextureUtils.get_texture_if_exists("Mountain")
        tex_clr.name = "Mountain"
        tex_clr.type = 'DISTORTED_NOISE'
        self.mountain: bpy.types.DistortedNoiseTexture = bpy.data.textures["Mountain"]
        self.mountain.noise_distortion = 'IMPROVED_PERLIN'
        self.mountain.noise_scale = scale
        self.mountain.distortion = distortion

    def get_height(self, x, y):
        return self.mountain.evaluate([x, y, 0])[3]

