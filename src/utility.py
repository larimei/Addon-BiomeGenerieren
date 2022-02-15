import bpy
import bmesh


class TextureUtils:
    def get_texture_if_exists(name: str):
        try:
            tex = bpy.data.textures[name]
            bpy.data.textures.remove(bpy.data.textures["Texture"])
        except KeyError:
            tex = bpy.data.textures["Texture"]
        return tex


class MaterialUtils:
    def create_material(name, value):

        material = bpy.data.materials.new(
            name=name)
        material.use_nodes = True
        material.node_tree.nodes["Principled BSDF"].inputs[0].default_value = value

        return material

    def create_material_between(_name, _value_one, _value_two):

        material = bpy.data.materials.new(
            name=_name)
        material.use_nodes = True

        principled_node = material.node_tree.nodes.get('Principled BSDF')

        mix_node = material.node_tree.nodes.new('ShaderNodeMixRGB')
        mix_node.inputs[1].default_value = _value_one
        mix_node.inputs[2].default_value = _value_two

        link = material.node_tree.links.new
        link(mix_node.outputs[0], principled_node.inputs[0])

        return material


class ParticleUtils:
    def create_particle_system(_object, _name, _vertex_group, _collection_name, _count, _random_size, _size, _seed):
        bpy.context.view_layer.objects.active = _object
        _object.modifiers.new(_name, type='PARTICLE_SYSTEM')
        particle_system = _object.particle_systems[_name]
        particle_system.settings.type = 'HAIR'
        particle_system.settings.render_type = 'COLLECTION'
        particle_system.settings.instance_collection = bpy.data.collections[_collection_name]
        particle_system.settings.child_type = 'INTERPOLATED'
        particle_system.settings.rendered_child_count = particle_system.settings.child_nbr
        particle_system.settings.count = _count
        particle_system.settings.particle_size = _size
        particle_system.settings.size_random = _random_size
        particle_system.settings.use_whole_collection = True
        particle_system.settings.use_advanced_hair = True
        particle_system.settings.rotation_mode = 'NONE'
        particle_system.settings.use_even_distribution = False
        particle_system.seed = _seed
        particle_system.vertex_group_density = _vertex_group


class CleanCollectionsUtils:
    def clean_system():
        view_layer = bpy.context.scene.view_layers["View Layer"]
        collection_include = bpy.data.collections["Collection"]
        CleanCollectionsUtils.include_only_one_collection(
            view_layer, collection_include)
        for collection in bpy.data.collections:
            if collection.name == "Collection":
                for object in collection.objects:
                    if object.name != "Plane":
                        collection.objects.unlink(object)

    def include_only_one_collection(view_layer: bpy.types.ViewLayer, collection_include: bpy.types.Collection):
        for layer_collection in view_layer.layer_collection.children:
            if layer_collection.collection != collection_include:
                layer_collection.exclude = True
            else:
                layer_collection.exclude = False


class GroundUtils:

    def create_gradient(self, object: bpy.types.Object, name, otherName, material):
        bpy.ops.object.editmode_toggle()  # Go in edit mode
        bpy.ops.mesh.select_all(action='DESELECT')  # Deselect all

        bpy.ops.object.material_slot_add()
        object.material_slots[object.material_slots.__len__(
        ) - 1].material = material

        face_map = object.face_maps.find(name)
        object.face_maps.active_index = face_map
        bpy.ops.object.face_map_select()

        for map in object.face_maps:
            if map.name != name and map.name != otherName:
                object.face_maps.active_index = map.index
                bpy.ops.object.face_map_deselect()

        vertex_group = object.vertex_groups.find(name)
        object.vertex_groups.active_index = vertex_group
        bpy.ops.object.vertex_group_deselect()
        # bpy.ops.mesh.select_more()

        bpy.ops.object.material_slot_assign()
        bpy.ops.mesh.select_all(action='DESELECT')  # Deselect all
        bpy.ops.object.editmode_toggle()  # Return in object mode

    def create_facemask(self, object: bpy.types.Object, nameGroup, indexes, material):
        faceMap: bpy.types.FaceMap = object.face_maps.new(name=nameGroup)

        faceMap.add(indexes)

        object.face_maps.active_index = faceMap.index
        bpy.ops.object.material_slot_add()
        object.material_slots[object.material_slots.__len__(
        ) - 1].material = material
        bpy.ops.object.editmode_toggle()  # Go in edit mode
        bpy.ops.mesh.select_all(action='DESELECT')  # Deselect all
        bpy.ops.object.face_map_select()  # Select the faces of the faceMap

        # Assign the material on the selected faces
        bpy.ops.object.material_slot_assign()

        bpy.ops.mesh.select_less()
        bpy.ops.mesh.select_less()
        Verts = [i.index for i in bmesh.from_edit_mesh(
            bpy.context.active_object.data).verts if i.select]

        bpy.ops.object.face_map_deselect()
        bpy.ops.object.editmode_toggle()  # Return in object mode

        vertexGroup: bpy.types.VertexGroup = object.vertex_groups.new(
            name=nameGroup)
        vertexGroup.add(Verts, 1.0, 'REPLACE')
