import bpy


class TextureUtils:
    def getTextureIfExists(name: str):
        try:
            tex = bpy.data.textures[name]
            bpy.data.textures.remove(bpy.data.textures["Texture"])
        except KeyError:
            tex = bpy.data.textures["Texture"]
        return tex


class MaterialUtils:
    def createMaterial(name, value):

        material = bpy.data.materials.new(
            name=name)
        material.use_nodes = True
        material.node_tree.nodes["Principled BSDF"].inputs[0].default_value = value

        return material


class ParticleUtils:
    def createParticleSystem(object, name, vertexGroup, collectionName, count, randomSize, size, seed):
        bpy.context.view_layer.objects.active = object
        object.modifiers.new(name, type='PARTICLE_SYSTEM')
        particleSystem = object.particle_systems[name]
        particleSystem.settings.type = 'HAIR'
        particleSystem.settings.render_type = 'COLLECTION'
        particleSystem.settings.instance_collection = bpy.data.collections[collectionName]
        particleSystem.settings.child_type = 'INTERPOLATED'
        particleSystem.settings.rendered_child_count = particleSystem.settings.child_nbr
        particleSystem.settings.count = count
        particleSystem.settings.particle_size = size
        particleSystem.settings.size_random = randomSize
        particleSystem.settings.use_whole_collection = True
        particleSystem.settings.use_advanced_hair = True
        particleSystem.settings.rotation_mode = 'NONE'
        particleSystem.settings.use_even_distribution = False
        particleSystem.seed = seed
        particleSystem.vertex_group_density = vertexGroup


class CleanCollectionsUtils:
    def cleanSystem():
        for collection in bpy.data.collections:
            if collection.name != "Collection":
                for object in collection.objects:
                    object.hide_set(True)
            if collection.name == "Collection":
                for object in collection.objects:
                    if object.name != "Plane":
                        collection.objects.unlink(object)
