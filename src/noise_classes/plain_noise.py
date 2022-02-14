import bpy
from src.utility import TextureUtils
class PlainNoise:

    def __init__(self, scale: float, depth: float):
        bpy.ops.texture.new()
        tex_clr = TextureUtils.get_texture_if_exists("Plain")
        tex_clr.name = "Plain"
        tex_clr.type = 'CLOUDS'
        self.plain: bpy.types.StucciTexture = bpy.data.textures["Plain"]
        self.plain.noise_basis = 'ORIGINAL_PERLIN'
        self.plain.noise_type = 'SOFT_NOISE'
        self.plain.noise_scale = scale
        self.plain.noise_depth = depth

    def get_height(self, x, y):
        return self.plain.evaluate([x, y, 0])[3]

