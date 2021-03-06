import bpy


class GENERATEBIOMES_PT_MainPanel(bpy.types.Panel):
    bl_label = "Generate Biomes"
    bl_idname = "GENERATEBIOMES_PT_MainPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Generate Biomes'

    def draw(self, context):

        layout = self.layout
        row = layout.row()
        row.label(text="General Settings", icon='WORLD')

        col = layout.column(align=True)
        col.use_property_split = True
        col.prop(context.scene, "size", text="Ground Mesh Size")
        col.separator()
        col.prop(context.scene, "groundEdgeSize", text="Ground Edge Size")
        col.separator()
        col.label(text="Offset Vector")
        col.separator()
        offset = col.box()
        offset.prop(context.scene, "offsetX", text="X")
        offset.prop(context.scene, "offsetY", text="Y")
        col.separator()
        col.prop(context.scene, "biomeScale", text="Biome Scale")
        col.separator()
        row2 = layout.row()
        # insert operator
        row2.scale_x = 7
        row2.scale_y = 2
        row2.operator("generatebiomes.generate_ground", text="Generate Scene")
        # insert operator
        row2.operator("generatebiomes.reset_scene", text="Reset Scene")


class GENERATEBIOMES_PT_DistributionPanel(bpy.types.Panel):
    bl_label = "Biome Distribution Settings"
    bl_idname = "GENERATEBIOMES_PT_DistributionPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Generate Biomes'

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        col.use_property_split = True
        col.prop(context.scene, "grassWeight", text="Grass Weight")
        col.prop(context.scene, "forestWeight", text="Forest Weight")
        col.prop(context.scene, "desertWeight", text="Desert Weight")
        col.prop(context.scene, "mountainWeight", text="Mountain Weight")


class GENERATEBIOMES_PT_DesertPanel(bpy.types.Panel):
    bl_label = "Desert Settings"
    bl_idname = "GENERATEBIOMES_PT_DesertPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Generate Biomes'

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        col.use_property_split = True
        col.prop(context.scene, "cactusCount", text="Cactus Count")
        col.prop(context.scene, "stoneCount", text="Stone Count")
        col.prop(context.scene, "desertColor", text="Desert Color")


class GENERATEBIOMES_PT_GrassPanel(bpy.types.Panel):
    bl_label = "Grass Settings"
    bl_idname = "GENERATEBIOMES_PT_GrassPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Generate Biomes'

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        col.use_property_split = True
        col.prop(context.scene, "grassCount", text="Grass Count")
        col.prop(context.scene, "flowerCount", text="Flower Count")
        col.prop(context.scene, "bushCount", text="Bush Count")
        col.prop(context.scene, "grassColor", text="Grass Surface Color")


class GENERATEBIOMES_PT_ForestPanel(bpy.types.Panel):
    bl_label = "Forest Settings"
    bl_idname = "GENERATEBIOMES_PT_ForestPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Generate Biomes'

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        col.use_property_split = True
        col.prop(context.scene, "treeCount", text="Tree Count")
        col.prop(context.scene, "pineCount", text="Pine Count")
        col.prop(context.scene, "branchCount", text="Tree With Branches Count")
        col.prop(context.scene, "forestColor", text="Forest Color")


class GENERATEBIOMES_PT_MountainPanel(bpy.types.Panel):
    bl_label = "Mountain Settings"
    bl_idname = "GENERATEBIOMES_PT_MountainPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Generate Biomes'

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        col.use_property_split = True
        col.prop(context.scene, "snowBorder", text="Snow Border Height")
        col.prop(context.scene, "snowColor", text="Snow Color")
        col.prop(context.scene, "mountainColor", text="Mountain Color")
