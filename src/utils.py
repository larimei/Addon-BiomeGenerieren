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
