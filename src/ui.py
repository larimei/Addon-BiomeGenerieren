import bpy

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