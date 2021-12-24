
import bpy
import bmesh
import random


# class SimpleOperator(bpy.types.Operator):
#   """Tooltip"""
#  bl_idname = "object.simple_operator"
# bl_label = "Simple Object Operator"
#
#   @classmethod
#  def poll(cls, context):
#     return True
#
#   def execute(self, context):
#      ground = Ground()
#     ground.generate_ground(context)
#
#       return {'FINISHED'}


class Ground():
    # these should be initialized with input

    # int
    ground_size: int  # 80
    biome_offset_x: int  # 10
    biome_offset_y: int  # 10
    # float
    face_edge_size = 0.5
    biome_scale = 20

    # constants that are effected by input
    SUBDIVISION_LEVELS: float
    VERTCOUNT_EDGE: int
    BIOME_AMOUNT = 4
    # others
    faces = []
    grass_faces = []
    forest_faces = []
    desert_faces = []
    mountain_faces = []

    def initializeVariable(self, _groundSize, _biome_offset_y, _biome_offset_x):
        self.ground_size = _groundSize
        self.biome_offset_x = _biome_offset_x
        self.biome_offset_y = _biome_offset_y
        self.SUBDIVISION_LEVELS = self.ground_size / self.face_edge_size - 1
        self.VERTCOUNT_EDGE = round(self.SUBDIVISION_LEVELS + 2)

    def generate_ground(self, context):
        bpy.ops.mesh.primitive_plane_add(
            size=self.ground_size, location=(0, 0, 0))

        ground = bpy.context.object
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.subdivide(number_cuts=self.SUBDIVISION_LEVELS)
        bpy.ops.object.editmode_toggle()

        ground_mesh = bmesh.new()
        ground_mesh.from_mesh(ground.data)
        ground_mesh.verts.ensure_lookup_table()

        v = VoronoiNoise(scale=self.biome_scale)
        hn = GlobalNoise(scale=2)
        mn = MountainNoise(scale=0.4, distortion=1.2)
        for i in range(len(ground_mesh.verts)):
            vert = ground_mesh.verts[i].co
            info = v.get_biome_and_weight(
                vert.x + self.biome_offset_x, vert.y + self.biome_offset_y)
            biome = info[0]
            weight = info[1]
            global_height = hn.get_height(vert.x, vert.y)
            # grass
            if biome == 0:
                vert.z = 2 * global_height + 3 * weight * global_height
            # forest
            elif biome == 1:
                vert.z = 2 * global_height + 3 * weight * global_height
            # desert
            elif biome == 2:
                vert.z = 2 * global_height + 3 * weight * global_height
            # mountains
            else:
                mtn_height = mn.get_height(vert.x, vert.y)
                #vert.z = 2 * global_height + 3 * weight * mtn_height
                vert.z = weight * weight
            linked_faces = ground_mesh.verts[i].link_faces
            for j in range(len(linked_faces)):
                current_face = linked_faces[j]
                face: BiomeFace = next(
                    (x for x in self.faces if x.index == current_face.index), None)
                if(face is not None):
                    face.biomes.append(biome)
                else:
                    new_face: BiomeFace = BiomeFace(index=current_face.index, biomes=[
                        biome], center=current_face.calc_center_median(), normal=current_face.normal)
                    self.faces.append(new_face)

        ground_mesh.to_mesh(ground.data)
        ground_mesh.free()
        self.allocate_biomes(Ground)

    def allocate_biomes(self):
        for face in self.faces:
            for biome in face.biomes:
                if biome == 0:
                    self.grass_faces.append(face)
                if biome == 1:
                    self.forest_faces.append(face)
                if biome == 2:
                    self.desert_faces.append(face)
                if biome == 3:
                    self.mountain_faces.append(face)


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
        tex_clr = bpy.data.textures["Texture"]
        tex_clr.name = "Voronoi"
        tex_clr.type = 'VORONOI'
        self.voronoi_clr: bpy.types.VoronoiTexture = bpy.data.textures["Voronoi"]
        self.voronoi_clr.distance_metric = 'MINKOVSKY_FOUR'
        self.voronoi_clr.color_mode = 'POSITION'
        self.voronoi_clr.noise_scale = scale

        bpy.ops.texture.new()
        tex_weight = bpy.data.textures["Texture"]
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
        tex_clr = bpy.data.textures["Texture"]
        tex_clr.name = "Cloud"
        tex_clr.type = 'CLOUDS'
        self.cloud: bpy.types.CloudsTexture = bpy.data.textures["Cloud"]
        self.cloud.noise_basis = 'BLENDER_ORIGINAL'
        self.cloud.cloud_type = 'GRAYSCALE'
        self.cloud.noise_scale = scale

    def get_height(self, x, y):
        return self.cloud.evaluate([x, y, 0])[3]


class MountainNoise:

    def __init__(self, scale: float, distortion: float):
        bpy.ops.texture.new()
        tex_clr = bpy.data.textures["Texture"]
        tex_clr.name = "Mountain"
        tex_clr.type = 'DISTORTED_NOISE'
        self.mountain: bpy.types.DistortedNoiseTexture = bpy.data.textures["Mountain"]
        self.mountain.noise_distortion = 'IMPROVED_PERLIN'
        self.mountain.noise_scale = scale
        self.mountain.distortion = distortion

    def get_height(self, x, y):
        return self.mountain.evaluate([x, y, 0])[3]


#classes = [SimpleOperator]


# def register():
 #   for cls in classes:
  #      bpy.utils.register_class(cls)


# def unregister():
 #   for cls in classes:
  #      bpy.utils.unregister_class(cls)


# if __name__ == "__main__":
 #   register()

    # test call
  #  bpy.ops.object.simple_operator()
