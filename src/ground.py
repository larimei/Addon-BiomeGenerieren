
import random
import bpy
import bmesh
import math

from src.utility import GroundUtils, MaterialUtils
from src.noise_classes.desert_noise import DesertNoise
from src.noise_classes.mountain_noise import MountainNoise
from src.noise_classes.plain_noise import PlainNoise
from src.noise_classes.global_noise import GlobalNoise
from src.noise_classes.voronoi_noise import VoronoiNoise


class Ground():

    def __init__(self, _ground_size, _edge_size, _biome_offset_y, _biome_offset_x, _biome_scale, _snow_border, weights, colors):
        self.ground_size: int = _ground_size
        self.biome_offset_x: int = _biome_offset_x
        self.biome_offset_y: int = _biome_offset_y
        self.biome_scale: float = _biome_scale
        self.subdivision_levels: int = int(self.ground_size / _edge_size - 1)
        self.grass_weight: float = weights[0]
        self.forest_weight: float = weights[1]
        self.desert_weight: float = weights[2]
        self.mountain_weight: float = weights[3]
        self.snowfall_border: float = _snow_border
        self.colors = colors
        self.grass_faces = {}
        self.forest_faces = {}
        self.desert_faces = {}
        self.mountain_faces = {}
        self.snow_faces = {}

    def generate_ground(self):
        bpy.ops.mesh.primitive_plane_add(
            size=self.ground_size, location=(0, 0, 0))

        ground = bpy.context.object
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.subdivide(number_cuts=self.subdivision_levels)
        bpy.ops.object.editmode_toggle()

        ground_mesh = bmesh.new()
        ground_mesh.from_mesh(ground.data)
        ground_mesh.verts.ensure_lookup_table()

        v = VoronoiNoise(self.biome_scale, self.grass_weight,
                         self.forest_weight, self.desert_weight, self.mountain_weight)
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
                self.add_face_to_grass(
                    _linked_faces=ground_mesh.verts[i].link_faces)
            # forest
            elif biome == 1:
                vert.z = global_height
                self.add_face_to_forest(
                    _linked_faces=ground_mesh.verts[i].link_faces)

            # desert
            elif biome == 2:
                canyon_height = dn.get_height(vert.x, vert.y)
                vert.z = math.pow(canyon_height, 2) * 3 + \
                    0.5 * global_height - 0.5
                self.add_face_to_desert(
                    _linked_faces=ground_mesh.verts[i].link_faces)
            # mountains
            else:
                mtn_height = mn.get_height(vert.x, vert.y)
                vert.z = global_height + \
                    math.pow(weight, 3) + math.pow(weight, 2) * mtn_height
                if(vert.z >= (self.snowfall_border + random.uniform(0, 1))):
                    self.add_face_to_snow(
                        _linked_faces=ground_mesh.verts[i].link_faces)
                else:
                    self.add_to_mountain(
                        _linked_faces=ground_mesh.verts[i].link_faces)

        ground_mesh.to_mesh(ground.data)
        ground_mesh.free()

        self.add_materials(_ground=ground)

        # Add Decimate Modifier for Tris:
        bpy.ops.object.select_pattern(
            pattern="Ground", case_sensitive=True, extend=False)
        bpy.ops.object.modifier_add(type='DECIMATE')
        bpy.context.object.modifiers["Decimate"].use_collapse_triangulate = True
        bpy.context.object.modifiers["Decimate"].ratio = 0.95

    def add_face_to_grass(self, _linked_faces):
        for i in range(len(_linked_faces)):
            current_face: bmesh.types.BMFace = _linked_faces[i]
            self.grass_faces[current_face.index] = BiomeFace(
                _index=current_face.index)

    def add_face_to_forest(self, _linked_faces):
        for i in range(len(_linked_faces)):
            current_face: bmesh.types.BMFace = _linked_faces[i]
            self.forest_faces[current_face.index] = BiomeFace(
                _index=current_face.index)

    def add_face_to_desert(self, _linked_faces):
        for i in range(len(_linked_faces)):
            current_face: bmesh.types.BMFace = _linked_faces[i]
            self.desert_faces[current_face.index] = BiomeFace(
                _index=current_face.index)

    def add_to_mountain(self, _linked_faces):
        for i in range(len(_linked_faces)):
            current_face: bmesh.types.BMFace = _linked_faces[i]
            self.mountain_faces[current_face.index] = BiomeFace(
                _index=current_face.index)

    def add_face_to_snow(self, _linked_faces):
        for i in range(len(_linked_faces)):
            current_face: bmesh.types.BMFace = _linked_faces[i]
            self.snow_faces[current_face.index] = BiomeFace(
                _index=current_face.index)

    def add_materials(self, _ground):
        GroundUtils.create_facemask(_object=_ground, _nameGroup="grass", _indexes=list(self.grass_faces.keys()), _material=MaterialUtils.create_material(
            "grass", self.colors[0]))
        GroundUtils.create_facemask(_object=_ground, _nameGroup="forest", _indexes=list(self.forest_faces.keys()), _material=MaterialUtils.create_material(
            "forest", self.colors[1]))

        GroundUtils.create_facemask(_object=_ground, _nameGroup="desert", _indexes=list(self.desert_faces.keys()), _material=MaterialUtils.create_material(
            "desert", self.colors[2]))
        GroundUtils.create_facemask(_object=_ground, _nameGroup="mountain", _indexes=list(self.mountain_faces.keys()), _material=MaterialUtils.create_material(
            "mountain", self.colors[3]))
        GroundUtils.create_facemask(_object=_ground, _nameGroup="snow", _indexes=list(self.snow_faces.keys()), _material=MaterialUtils.create_material(
            "snow", self.colors[4]))

        GroundUtils.create_gradient(_object=_ground, _name='desert', _otherName='forest', _material=MaterialUtils.create_material_between(
            "desert-forest", self.colors[2], self.colors[1]))
        GroundUtils.create_gradient(_object=_ground, _name='desert', _otherName='grass', _material=MaterialUtils.create_material_between(
            "desert-grass", self.colors[2], self.colors[1]))
        GroundUtils.create_gradient(_object=_ground, _name='forest', _otherName='grass', _material=MaterialUtils.create_material_between(
            "forest-grass", self.colors[1], self.colors[0]))
        GroundUtils.create_gradient(_object=_ground, _name='mountain', _otherName='grass', _material=MaterialUtils.create_material_between(
            "mountain-grass", self.colors[3], self.colors[0]))
        GroundUtils.create_gradient(_object=_ground, _name='mountain', _otherName='forest', _material=MaterialUtils.create_material_between(
            "mountain-forest", self.colors[3], self.colors[1]))
        GroundUtils.create_gradient(_object=_ground, _name='mountain', _otherName='desert', _material=MaterialUtils.create_material_between(
            "mountain-desert", self.colors[3], self.colors[2]))


class BiomeFace:
    def __init__(self, _index):
        self.index = _index
