import bpy
from src.utility import TextureUtils
class DesertNoise:

    def __init__(self, scale: float, turbulence: float):
        bpy.ops.texture.new()
        tex_clr = TextureUtils.get_texture_if_exists("Desert")
        tex_clr.name = "Desert"
        tex_clr.type = 'STUCCI'
        self.desert: bpy.types.StucciTexture = bpy.data.textures["Desert"]
        self.desert.stucci_type = 'PLASTIC'
        self.desert.noise_scale = scale
        self.desert.turbulence = turbulence

    def get_height(self, x, y):
        return self.desert.evaluate([x, y, 0])[3]
