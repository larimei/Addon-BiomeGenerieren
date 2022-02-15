import bpy
import random
from ...src.utility import MaterialUtils

VERTICES = 9
MIN_SHIFT = 0.5
MAX_SHIFT = 1.5
HEIGHT = 1.5

class Cactus:
    def generate_branches(_edges, _verts, _vert, _branch, _last_index):
        for i in range(random.randrange(3, 6)):
            if _branch:
                branch_vert = (_vert[0] + random.uniform(0.5, 1.25), _vert[1] +
                               random.uniform(0.5, 1.25), _vert[2] + random.uniform(0.5, 1.25))  # plus statt minus dass es nach oben geht
            elif _branch is False:
                branch_vert = (_vert[0] + random.uniform(-1.5, -0.25), _vert[1] +
                               random.uniform(-1.5, -0.25), _vert[2] + random.uniform(0.25, 1.5))  # plus statt minus dass es nach oben geht

            _vert = branch_vert
            _verts.append(branch_vert)
            if i == 0:
                edge = (_last_index, len(_verts) - 1)
            else:
                edge = (len(_verts) - 2, len(_verts)-1)

            _edges.append(edge)

    def generate_cactus():
        for cactus_version in range(3):
            collection = bpy.data.collections.new(
                "CactusCollection" + str(cactus_version))
            bpy.context.scene.collection.children.link(collection)
            red = random.uniform(0.3, 0.6)
            green = random.uniform(0.2, 0.8)
            mesh = bpy.data.meshes.new("cactus")  # add the new mesh
            obj = bpy.data.objects.new(mesh.name, mesh)
            col = bpy.data.collections.get("Collection")
            col.objects.link(obj)
            bpy.context.view_layer.objects.active = obj
            location_x = random.uniform(-5, 5)
            location_y = random.uniform(-5, 5)
            obj.location = (location_x, location_y, 0)

            verts = []
            edges = []

            bool = False
            for i in range(VERTICES):
                pos_z = i * HEIGHT
                pos_y = 1 * random.uniform(MIN_SHIFT, MAX_SHIFT)
                pos_x = 1 * random.uniform(MIN_SHIFT, MAX_SHIFT)
                vert = (pos_x, pos_y, pos_z)
                verts.append(vert)
                if i != 0:
                    if bool:
                        # ab hier geändert, dass man auch mitten drin zweige einfügen kann (sonst werden die Vertices immer an das letzte gehängt)
                        edge = (last_index, len(verts) - 1)
                        bool = False
                    else:
                        edge = (len(verts) - 2, len(verts) - 1)
                    edges.append(edge)
                if i == 2:  # aussuchen, an welchen Vertex der Zweig haben soll
                    last_index = len(verts) - 1
                    Cactus.generate_branches(
                        edges, verts, vert, True, last_index)
                    bool = True
                # hier auch nochmal (wichtig sind die bool werte zu setzen, sonst wird oben der falsche index für die edge verwendet)
                elif i == 4:
                    last_index = len(verts) - 1
                    Cactus.generate_branches(
                        edges, verts, vert, False, last_index)
                    bool = True

            faces = []

            trunk = mesh.from_pydata(verts, edges, faces)

            me = obj.data

            obj.select_set(True)

            bpy.ops.object.mode_set(mode='EDIT')

            bpy.ops.object.mode_set(mode='OBJECT')

            skin: bpy.types.SkinModifier = bpy.ops.object.modifier_add(
                type='SKIN')

            rad_x = random.uniform(0.75, 1.75)
            rad_y = random.uniform(0.75, 1.75)

            i = 0

            for v in me.skin_vertices[0].data:
                v.radius = rad_x, rad_y
                if i == 0:
                    rad_x = random.uniform(0.75, 2.0)
                    rad_y = random.uniform(0.75, 2.0)
                else:
                    rad_x = rad_x - random.uniform(0.01, 0.05)
                    rad_y = rad_y - random.uniform(0.01, 0.05)
                i = i + 1

            bpy.ops.object.modifier_add(type='SUBSURF')
            bpy.context.object.modifiers["Subdivision"].render_levels = 1

            for modifier in obj.modifiers:
                bpy.ops.object.modifier_apply(modifier=modifier.name)
            particles = random.uniform(60, 120)
            spike_length = random.uniform(0.2, 0.6)
            seed = random.uniform(0, 100)
            bpy.context.object.modifiers.new(
                bpy.context.object.name, type='PARTICLE_SYSTEM')
            particle_system = bpy.context.object.particle_systems[bpy.context.object.name]
            particle_system.settings.type = 'HAIR'
            particle_system.settings.count = particles
            particle_system.settings.hair_length = spike_length
            particle_system.child_seed = seed
            bpy.ops.object.select_all(action='SELECT')
            #spikes: bpy.types.ParticleSystem = bpy.ops.object.particle_system_add()
            obj.data.materials.append(MaterialUtils.create_material(
                "cactus_material", (red, green, 0.0, 1)))
            bpy.context.object.rotation_euler = (
                0, 0, random.randrange(0, 360))
            rnd_scale = random.uniform(1, 2)
            bpy.context.object.scale = (rnd_scale, rnd_scale, rnd_scale)
            collection.objects.link(bpy.context.object)

class Stone:

    def generate_stone():

        for stone_version in range(3):
            collection = bpy.data.collections.new(
                "StoneCollection" + str(stone_version))
            bpy.context.scene.collection.children.link(collection)
            width = random.uniform(2, 5)
            depth = random.uniform(2, 5)
            height = depth / width + random.uniform(0, 2)

            if width > depth:
                height = width / depth + random.uniform(0, 2)
            elif width == depth:
                height = abs(width + depth - 4)

            greytone = random.uniform(0.25, 0.75)
            bpy.ops.mesh.primitive_ico_sphere_add(
                enter_editmode=False, location=(0, 0,  0), scale=(width, depth, height)
            )
            #bpy.ops.mesh.name = "stone"
            bpy.ops.object.shade_flat()

            bpy.context.object.data.materials.append(MaterialUtils.create_material(
                "stone_material", (greytone, greytone, greytone, 1)))

            current_mesh = bpy.context.object.data

            for vert in current_mesh.vertices:
                vert.co.x += random.uniform(-0.5, 1)
                vert.co.y += random.uniform(-0.5, 1)
                vert.co.z += random.uniform(-0.5, 1)

            current_mesh.update()
            rnd_scale = random.uniform(1, 1.5)
            bpy.context.object.scale = (rnd_scale, rnd_scale, rnd_scale)
            collection.objects.link(bpy.context.object)
