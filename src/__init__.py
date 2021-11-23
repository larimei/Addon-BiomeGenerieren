
bl_info = {
    "name": "Generate Biomes",
    "author": "Valentin, Fabian, Viktor, Lara",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Toolbar > Generate Biomes",
    "description": "Adds different biomes, where you can set different parameters",
    "warning": "",
    "wiki_url": "",
    "category": "Add Mesh",
}

import bpy 
import mathutils
#from .  import ui

    # This is the Main Panel in 3DView


class MainPanel(bpy.types.Panel):
    bl_label = "Generate Biomes"
    bl_idname = "PT_MainPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Generate Biomes'

    def draw(self, context):
        layout = self.layout
        layout.scale_y = 1.2

        row = layout.row()
        row.label(text="Add a biome", icon='WORLD')
        row = layout.row()
        # insert operator
        row.operator("object.text_add", text="Add Desert")
        # insert operator
        row.operator("object.text_add", text="Add Forest")
        row = layout.row()
                # insert operator
        row.operator("object.text_add", text="Add Ocean")
        # insert operator
        row.operator("object.text_add", text="Add Mountains")



#insert operator
class SimpleOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.simple_operator"
    bl_label = "Simple Object Operator"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        main(context)
        return {'FINISHED'}


def main(context):
    for ob in context.scene.objects:
        print(ob)



classes = (MainPanel, SimpleOperator) 

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
 
if __name__ == "__main__":
    register()    
