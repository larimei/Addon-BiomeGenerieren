import bpy
import random
import typing
import bmesh
import mathutils
import math

VERTICES = 9
MIN_SHIFT = 0.5
MAX_SHIFT = 1.5
HEIGHT = 1.5

def generateSpikes(object):

    PARTICLES = random.uniform(60, 120)
    SPIKE_LENGTH = random.uniform(0.2, 0.6)
    SEED = random.uninform(0,100)

    object.particle_system_add()
    bpy.data.particles["ParticleSettings"].type = 'HAIR'
    bpy.data.particles["ParticleSettings"].count = PARTICLES
    bpy.data.particles["ParticleSettings"].hair_length = SPIKE_LENGTH
    object.particle_systems["ParticleSettings"].seed = SEED
    
def generateBranches(edges, verts, vert, branch, lastIndex):
    for i in range(random.randrange(3, 6)):
        if branch:
            branchvert = (vert[0] + random.uniform(0.5, 1.25), vert[1] +
                          random.uniform(0.5, 1.25), vert[2] + random.uniform(0.5, 1.25)) #plus statt minus dass es nach oben geht
        elif branch is False:
            branchvert = (vert[0] + random.uniform(-1.5, -0.25), vert[1] +
                          random.uniform(-1.5, -0.25), vert[2] + random.uniform(0.25, 1.5)) #plus statt minus dass es nach oben geht

        vert = branchvert
        verts.append(branchvert)
        if i is 0:
            edge = (lastIndex, len(verts) - 1)
        else:
            edge = (len(verts) - 2, len(verts)-1) 

        edges.append(edge)

def generateCactus():
    collection = bpy.data.collections.new("CactusCollection")
    bpy.context.scene.collection.children.link(collection)
    mesh = bpy.data.meshes.new("cactus")  # add the new mesh
    obj = bpy.data.objects.new(mesh.name, mesh)
    col = bpy.data.collections.get("Collection")
    col.objects.link(obj)
    bpy.context.view_layer.objects.active = obj

    verts = []
    edges = []

    bool = False
    for i in range(VERTICES):
        posZ = i * HEIGHT
        posY = 1 * random.uniform(MIN_SHIFT, MAX_SHIFT)
        posX = 1 * random.uniform(MIN_SHIFT, MAX_SHIFT)
        vert = (posX, posY, posZ)
        verts.append(vert)
        if i is not 0:
            if bool:
                edge = (lastIndex, len(verts) -1)   #ab hier geändert, dass man auch mitten drin zweige einfügen kann (sonst werden die Vertices immer an das letzte gehängt)
                bool = False
            else:
                edge = (len(verts) - 2, len(verts) -1)
            edges.append(edge)
        if i is 2:   #aussuchen, an welchen Vertex der Zweig haben soll
             lastIndex= len(verts) - 1
             generateBranches(edges, verts, vert, True, lastIndex)
             bool = True
        elif i is 4: #hier auch nochmal (wichtig sind die bool werte zu setzen, sonst wird oben der falsche index für die edge verwendet)
            lastIndex = len(verts) - 1
            generateBranches(edges, verts, vert, False, lastIndex)            
            bool = True

    faces = []

    trunk = mesh.from_pydata(verts, edges, faces)

    me = obj.data

    obj.select_set(True)

    bpy.ops.object.mode_set(mode='EDIT')

    bpy.ops.object.mode_set(mode='OBJECT')

    skin: bpy.types.SkinModifier = bpy.ops.object.modifier_add(type='SKIN')

    rad_x = random.uniform(0.75, 1.75)
    rad_y = random.uniform(0.75, 1.75)

    i = 0

    for v in me.skin_vertices[0].data:
        v.radius = rad_x, rad_y
        if i is 0:
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


    bpy.ops.object.select_all(action='SELECT')
 #   bpy.ops.object.join()
 
    PARTICLES = random.uniform(60, 120)
    SPIKE_LENGTH = random.uniform(0.2, 0.6)
    SEED = random.uniform(0,100)
    
    spikes: bpy.types.ParticleSystem = bpy.ops.object.particle_system_add()
   # bpy.data.particles["ParticleSettings.007"].use_fake_user = False
    #spikes.particles["ParticleSettings"].type = 'HAIR'
    #spikes.particles["ParticleSettings"].count = PARTICLES
    #spikes.particles["ParticleSettings"].hair_length = SPIKE_LENGTH
    #object.particle_systems["ParticleSettings"].seed = SEED
    #bpy.ops.object.shade_flat()
    bpy.context.object.data.materials.append(createMaterial())
     
def createMaterial() -> bpy.types.Material:
    
    RED = random.uniform(0.3, 0.6)
    GREEN = random.uniform(0.2, 0.8)
        
    cactusMaterial: bpy.types.Material = bpy.data.materials.new("Cactus Material")
    cactusMaterial.use_nodes = True

    cactusNodes: typing.List[bpy.types.Node] = cactusMaterial.node_tree.nodes
    cactusNodes["Principled BSDF"].inputs[0].default_value = (RED, GREEN, 0.0, 1)
    return cactusMaterial
    
class Cactus(bpy.types.Operator):
    bl_idname = "object.generate_cactus"
    bl_label = "Generate a Cactus"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        generateCactus()
        return {'FINISHED'}

generateCactus()