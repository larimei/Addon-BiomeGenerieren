
import bpy
import bmesh
import math
# bpy.ops.object.select_all(action='SELECT')
# bpy.ops.object.delete(use_global=False, confirm=False)
# bpy.ops.outliner.orphans_purge()


class SimpleOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.simple_operator"
    bl_label = "Simple Object Operator"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        ground = Ground()
        ground.generate_ground(context)

        return {'FINISHED'}


class Ground:
    # these should be initialized with input

    # int
    ground_size = 80
    biome_offset_x = 10
    biome_offset_y = 10
    # float
    face_edge_size = 0.5
    biome_scale = 20

    # constants that are effected by input
    SUBDIVISION_LEVELS = ground_size / face_edge_size - 1
    VERTCOUNT_EDGE = round(SUBDIVISION_LEVELS + 2)
    BIOME_AMOUNT = 4

    def generate_ground(self, context):
        bpy.ops.mesh.primitive_plane_add(
            size=self.ground_size, location=(0, 0, 0))

        ground = bpy.context.object
        ground.name = "Ground"
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.subdivide(number_cuts=self.SUBDIVISION_LEVELS)
        bpy.ops.object.editmode_toggle()

        ground_mesh = bmesh.new()
        ground_mesh.from_mesh(ground.data)
        ground_mesh.verts.ensure_lookup_table()

        v = VoronoiNoise(scale=self.biome_scale)
        hn = GlobalNoise(scale=6)
        mn = MountainNoise(scale=0.4, distortion=0.3)
        dn = DesertNoise(scale=4, turbulence=200)
        pn = PlainNoise(scale=10, depth=0)
        for i in range(len(ground_mesh.verts)):
            vert = ground_mesh.verts[i].co
            biome, weight = v.get_biome_and_weight(
                vert.x + self.biome_offset_x, vert.y + self.biome_offset_y)

            global_height = hn.get_height(vert.x, vert.y)
            # grass
            if biome == 0:
                vert.z = pn.get_height(vert.x, vert.y) * \
                    3 + global_height - 1

            # forest
            elif biome == 1:
                vert.z = global_height

            # desert
            elif biome == 2:
                canyon_height = dn.get_height(vert.x, vert.y)
                vert.z = math.pow(canyon_height, 2) * 3 + \
                    0.5 * global_height - 0.5
            # mountains
            else:
                mtn_height = mn.get_height(vert.x, vert.y)
                vert.z = global_height + \
                    math.pow(weight, 3) + math.pow(weight, 2) * mtn_height

        ground_mesh.to_mesh(ground.data)
        ground_mesh.free()
        # Select object:
        bpy.ops.object.select_pattern(
            pattern="Ground", case_sensitive=True, extend=False)
        # Add modifier:
        bpy.ops.object.modifier_add(type='DECIMATE')
        bpy.context.object.modifiers["Decimate"].use_collapse_triangulate = True
        bpy.context.object.modifiers["Decimate"].ratio = 0.95


class Biome:
    def __init__(self, type):
        self.type = type
        # self.material


class BiomeFace:
    def __init__(self, index, biomes, center, normal):
        self.biomes = biomes
        self.index = index
        self.center = center
        self.normal = normal


class VoronoiNoise:

    def __init__(self, scale: float):
        bpy.ops.texture.new()
        tex_clr = TextureUtils.getTextureIfExists("Voronoi")
        tex_clr.name = "Voronoi"
        tex_clr.type = 'VORONOI'
        self.voronoi_clr: bpy.types.VoronoiTexture = bpy.data.textures["Voronoi"]
        self.voronoi_clr.distance_metric = 'MINKOVSKY_FOUR'
        self.voronoi_clr.color_mode = 'POSITION'
        self.voronoi_clr.noise_scale = scale

        bpy.ops.texture.new()
        tex_weight = TextureUtils.getTextureIfExists("Weight")
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
        if color >= 0.75:
            biome = 3
            weight = (weights[3] - 1) * (-1)
            weight = (weight * weight) * 2
        elif color >= 0.5:
            biome = 2
        elif color >= 0.25:
            biome = 1
        return biome, weight


class GlobalNoise:

    def __init__(self, scale: float):
        bpy.ops.texture.new()
        tex_clr = TextureUtils.getTextureIfExists("GlobalNoise")
        tex_clr.name = "GlobalNoise"
        tex_clr.type = 'CLOUDS'
        self.cloud: bpy.types.CloudsTexture = bpy.data.textures["GlobalNoise"]
        self.cloud.noise_basis = 'BLENDER_ORIGINAL'
        self.cloud.cloud_type = 'GRAYSCALE'
        self.cloud.noise_scale = scale

    def get_height(self, x, y):
        return self.cloud.evaluate([x, y, 0])[3] * 3


class MountainNoise:

    def __init__(self, scale: float, distortion: float):
        bpy.ops.texture.new()
        tex_clr = TextureUtils.getTextureIfExists("Mountain")
        tex_clr.name = "Mountain"
        tex_clr.type = 'DISTORTED_NOISE'
        self.mountain: bpy.types.DistortedNoiseTexture = bpy.data.textures["Mountain"]
        self.mountain.noise_distortion = 'IMPROVED_PERLIN'
        self.mountain.noise_scale = scale
        self.mountain.distortion = distortion

    def get_height(self, x, y):
        return self.mountain.evaluate([x, y, 0])[3]


class DesertNoise:

    def __init__(self, scale: float, turbulence: float):
        bpy.ops.texture.new()
        tex_clr = TextureUtils.getTextureIfExists("Desert")
        tex_clr.name = "Desert"
        tex_clr.type = 'STUCCI'
        self.desert: bpy.types.StucciTexture = bpy.data.textures["Desert"]
        self.desert.stucci_type = 'PLASTIC'
        self.desert.noise_scale = scale
        self.desert.turbulence = turbulence

    def get_height(self, x, y):
        return self.desert.evaluate([x, y, 0])[3]


class PlainNoise:

    def __init__(self, scale: float, depth: float):
        bpy.ops.texture.new()
        tex_clr = TextureUtils.getTextureIfExists("Plain")
        tex_clr.name = "Plain"
        tex_clr.type = 'CLOUDS'
        self.plain: bpy.types.StucciTexture = bpy.data.textures["Plain"]
        self.plain.noise_basis = 'ORIGINAL_PERLIN'
        self.plain.noise_type = 'SOFT_NOISE'
        self.plain.noise_scale = scale
        self.plain.noise_depth = depth

    def get_height(self, x, y):
        return self.plain.evaluate([x, y, 0])[3]


class TextureUtils:
    def getTextureIfExists(name: str):
        try:
            tex = bpy.data.textures[name]
            bpy.data.textures.remove(bpy.data.textures["Texture"])
        except KeyError:
            tex = bpy.data.textures["Texture"]
        return tex


classes = [SimpleOperator]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.object.simple_operator()
