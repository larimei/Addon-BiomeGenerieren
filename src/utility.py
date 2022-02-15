import bpy
import bmesh


class TextureUtils:
    def get_texture_if_exists(_name: str):
        try:
            tex = bpy.data.textures[_name]
            bpy.data.textures.remove(bpy.data.textures["Texture"])
        except KeyError:
            tex = bpy.data.textures["Texture"]
        return tex


class MaterialUtils:
    def create_material(_name, _value):

        material = bpy.data.materials.new(
            name=_name)
        material.use_nodes = True
        material.node_tree.nodes["Principled BSDF"].inputs[0].default_value = _value

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

    def include_only_one_collection(_view_layer: bpy.types.ViewLayer, _collection_include: bpy.types.Collection):
        for layer_collection in _view_layer.layer_collection.children:
            if layer_collection.collection != _collection_include:
                layer_collection.exclude = True
            else:
                layer_collection.exclude = False


class GroundUtils:

    def create_gradient(_object: bpy.types.Object, _name, _otherName, _material):
        bpy.ops.object.editmode_toggle()  # Go in edit mode
        bpy.ops.mesh.select_all(action='DESELECT')  # Deselect all

        bpy.ops.object.material_slot_add()
        _object.material_slots[_object.material_slots.__len__(
        ) - 1].material = _material

        face_map = _object.face_maps.find(_name)
        _object.face_maps.active_index = face_map
        bpy.ops.object.face_map_select()

        for map in _object.face_maps:
            if map.name != _name and map.name != _otherName:
                _object.face_maps.active_index = map.index
                bpy.ops.object.face_map_deselect()

        vertex_group = _object.vertex_groups.find(_name)
        _object.vertex_groups.active_index = vertex_group
        bpy.ops.object.vertex_group_deselect()
        # bpy.ops.mesh.select_more()

        bpy.ops.object.material_slot_assign()
        bpy.ops.mesh.select_all(action='DESELECT')  # Deselect all
        bpy.ops.object.editmode_toggle()  # Return in object mode

    def create_facemask(_object: bpy.types.Object, _nameGroup, _indexes, _material):
        face_map: bpy.types.FaceMap = _object.face_maps.new(name=_nameGroup)

        face_map.add(_indexes)

        _object.face_maps.active_index = face_map.index
        bpy.ops.object.material_slot_add()
        _object.material_slots[_object.material_slots.__len__(
        ) - 1].material = _material
        bpy.ops.object.editmode_toggle()  # Go in edit mode
        bpy.ops.mesh.select_all(action='DESELECT')  # Deselect all
        bpy.ops.object.face_map_select()  # Select the faces of the faceMap

        # Assign the material on the selected faces
        bpy.ops.object.material_slot_assign()

        bpy.ops.mesh.select_less()
        bpy.ops.mesh.select_less()
        verts = [i.index for i in bmesh.from_edit_mesh(
            bpy.context.active_object.data).verts if i.select]

        bpy.ops.object.face_map_deselect()
        bpy.ops.object.editmode_toggle()  # Return in object mode

        vertex_group: bpy.types.VertexGroup = _object.vertex_groups.new(
            name=_nameGroup)
        vertex_group.add(verts, 1.0, 'REPLACE')
