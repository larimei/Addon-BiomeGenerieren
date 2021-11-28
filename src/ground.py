import bpy
import bmesh
import random
import numpy.linalg
import numpy as np
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
    ground_size = 20
    face_edge_size = 0.5
    biome_total = 4

    # constants
    SUBDIVISION_LEVELS = ground_size / face_edge_size - 1
    VERTCOUNT_EDGE = round(SUBDIVISION_LEVELS + 2)
    BIOME_AMOUNT = 4

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

        v = Voronoi()
        arrays = v.get_voronoi_arrays(self.biome_total,
                                      self.BIOME_AMOUNT, self.VERTCOUNT_EDGE)
        weights = arrays[1]
        print(len(ground_mesh.verts))
        print(len(weights))
        for i in range(len(ground_mesh.verts)):
            ground_mesh.verts[i].co.z = weights[i]
           # print(ground_mesh.verts[i].co)

        ground_mesh.to_mesh(ground.data)
        ground_mesh.free()
        # bpy.ops.texture.new()
        # tex_clr = bpy.data.textures["Texture"]
        # tex_clr.name = "Voronoi"
        # tex_clr.type = 'VORONOI'
        # voronoi_clr: bpy.types.VoronoiTexture = bpy.data.textures["Voronoi"]
        # voronoi_clr.distance_metric = 'DISTANCE_SQUARED'
        # voronoi_clr.color_mode = 'POSITION'
        # voronoi_clr.noise_scale = 1
        # bpy.ops.texture.new()
        # tex_int = bpy.data.textures["Texture"]
        # tex_int.name = "Voronoi2"
        # tex_int.type = 'VORONOI'
        # voronoi_int: bpy.types.VoronoiTexture = bpy.data.textures["Voronoi2"]
        # voronoi_int.distance_metric = 'DISTANCE_SQUARED'
        # voronoi_int.color_mode = 'INTENSITY'
        # voronoi_int.noise_scale = 1

        # for val in voronoi_clr.evaluate([0.1, 0.2, 0.2]):
        #     print(val)


class Biome:
    def __init__(self, type):
        self.type = type
        # self.material


class BiomeVertex:
    def __init__(self, x, y, biome):
        self.biome = biome
        self.x = x
        self.y = y


class Voronoi:

    def get_voronoi_arrays(self, biome_total, biome_amount, size):
        random.seed()
        points = []
        colors = []
        vertices = []
        weights = []
        for i in range(biome_total):
            point = np.array(
                ((random.randrange(0, size), random.randrange(0, size))))
            points.append(point)
        for i in range(biome_amount):
            color = i
            colors.append(color)

        for y in range(size):
            for x in range(size):
                distance: float = size * size
                distance2nd: float = size * size
                value = 0
                weight: float = 0
                # calc closest point with distance
                for i in range(len(points)):
                    if(numpy.linalg.norm(np.array((x, y)) - points[i]) < distance):
                        distance = numpy.linalg.norm(
                            np.array((x, y)) - points[i])
                        value = i
                # calc weight using distance from closest to 2nd closest point
                for i in range(len(points)):
                    if(i != value):
                        pos_vert = np.array((x, y))
                        pos_1 = points[i]
                        pos_0 = points[value]
                        vector_pos0_pos1 = pos_1 - pos_0
                        vector_pos0_vert = pos_vert - pos_0
                        # project vector from current point to closest point on vector from closest point to 2nd closest point
                        # this results in a weight based on the distance from the closest point,
                        # the edges of the biome will always have the value 0
                        # the center of the biome will have the value of 1
                        v_norm = np.sqrt(sum(vector_pos0_pos1**2))
                        projection = (
                            np.dot(vector_pos0_vert, vector_pos0_pos1)/v_norm**2)*vector_pos0_pos1
                        if(numpy.linalg.norm(pos_vert - pos_1) < distance2nd):
                            distance2nd = numpy.linalg.norm(
                                pos_vert - pos_1)
                            distance_projected_to_first = numpy.linalg.norm(
                                projection)
                            distance_first_to_2nd = numpy.linalg.norm(
                                vector_pos0_pos1)
                            # print(projection)
                            # print(vector_pos0_pos1)
                            print(distance_first_to_2nd -
                                  distance_projected_to_first)
                            weight = (distance_projected_to_first /
                                      distance_first_to_2nd) * 2

                index = (x+y*size)
                if(index < 210):
                    print("index: ")
                    print(index)
                    print("color: ")
                    print((value % biome_amount))
                    print("weight")
                    print(weight)

                vertices.append(colors[value % biome_amount])
                weights.append(weight)

        return vertices, weights


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
