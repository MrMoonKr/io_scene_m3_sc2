# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

import bpy
from . import shared


def register_props():
    bpy.types.Object.m3_filepath_export = bpy.props.StringProperty(name='File Path', description='File path for export operation', maxlen=1023, default='')
    bpy.types.Object.m3_options = bpy.props.PointerProperty(type=OptionProperties)
    bpy.types.Object.m3_model_version = bpy.props.EnumProperty(options=set(), items=model_versions, default='29')
    bpy.types.Object.m3_mesh_version = bpy.props.EnumProperty(options=set(), items=mesh_versions, default='5')
    bpy.types.Object.m3_bounds = bpy.props.PointerProperty(type=BoundingProperties)


model_versions = (
    ('20', '20', 'Version 20'),
    ('21', '21', 'Version 21'),
    ('23', '23', 'Version 23'),
    ('24', '24', 'Version 24'),
    ('25', '25', 'Version 25'),
    ('26', '26', 'Version 26'),
    ('28', '28', 'Version 28'),
    ('29', '29', 'Version 29'),
    ('30', '30', 'Version 30'),
)

mesh_versions = (
    ('2', '2', 'Version 2'),
    ('3', '3', 'Version 3'),
    ('4', '4', 'Version 4'),
    ('5', '5', 'Version 5'),
)


desc_update_bone_selection = 'Clicking on m3 list items selects associated bones, when applicable'
desc_update_timeline = 'Clicking on an m3 animation group sets the range of the scene timeline to its beginning and ending frames'
desc_update_anim_data = 'Clicking on an m3 animation sets the action of the object'
desc_draw_selected = 'Display all m3 helper models if they are associated with the selected bone'
desc_draw_attach_points = 'Display attachment points'
desc_draw_attach_volumes = 'Display attachment volumes'
desc_draw_hittests = 'Display hit test volumes'
desc_draw_lights = 'Display light areas'
desc_draw_particles = 'Display particle emission areas and #TODO: emission vectors'
desc_draw_ribbons = '#TODO: Display ribbon shapes'
desc_draw_projections = 'Display projection bounding boxes'
desc_draw_forces = 'Display force influence areas'
desc_draw_cameras = 'Display cameras'
desc_draw_rigidbodies = 'Display rigid body shapes and #TODO: their joint shapes and vectors'
desc_draw_clothconstraints = 'Display cloth constraint volumes'
desc_draw_ikjoints = 'Display IK joint relationship lines'
desc_draw_shadowboxes = 'Display shadow box areas'
desc_draw_warps = 'Display vertex warp influence areas'
desc_draw_turrets = '#TODO: Display turret part vectors'


class OptionProperties(bpy.types.PropertyGroup):
    update_bone_selection: bpy.props.BoolProperty(options=set(), default=True, description=desc_update_bone_selection)
    update_timeline: bpy.props.BoolProperty(options=set(), default=True, description=desc_update_timeline)
    update_anim_data: bpy.props.BoolProperty(options=set(), default=True, description=desc_update_anim_data)
    draw_selected: bpy.props.BoolProperty(options=set(), default=True, description=desc_draw_selected)
    draw_attach_points: bpy.props.BoolProperty(options=set(), default=True, description=desc_draw_attach_points)
    draw_attach_volumes: bpy.props.BoolProperty(options=set(), default=True, description=desc_draw_attach_volumes)
    draw_hittests: bpy.props.BoolProperty(options=set(), default=True, description=desc_draw_hittests)
    draw_lights: bpy.props.BoolProperty(options=set(), default=True, description=desc_draw_lights)
    draw_particles: bpy.props.BoolProperty(options=set(), default=True, description=desc_draw_particles)
    draw_ribbons: bpy.props.BoolProperty(options=set(), default=True, description=desc_draw_ribbons)
    draw_projections: bpy.props.BoolProperty(options=set(), default=True, description=desc_draw_projections)
    draw_forces: bpy.props.BoolProperty(options=set(), default=True, description=desc_draw_forces)
    draw_cameras: bpy.props.BoolProperty(options=set(), default=True, description=desc_draw_cameras)
    draw_rigidbodies: bpy.props.BoolProperty(options=set(), default=True, description=desc_draw_rigidbodies)
    draw_clothconstraints: bpy.props.BoolProperty(options=set(), default=True, description=desc_draw_clothconstraints)
    draw_ikjoints: bpy.props.BoolProperty(options=set(), default=True, description=desc_draw_ikjoints)
    draw_shadowboxes: bpy.props.BoolProperty(options=set(), default=True, description=desc_draw_shadowboxes)
    draw_warps: bpy.props.BoolProperty(options=set(), default=True, description=desc_draw_warps)
    draw_turrets: bpy.props.BoolProperty(options=set(), default=True, description=desc_draw_turrets)


class BoundingProperties(bpy.types.PropertyGroup):
    opt_display: bpy.props.BoolProperty(options=set())
    bottom: bpy.props.FloatProperty(options=set(), default=-0.25)
    top: bpy.props.FloatProperty(options=set(), default=2)
    left: bpy.props.FloatProperty(options=set(), default=-2)
    right: bpy.props.FloatProperty(options=set(), default=2)
    front: bpy.props.FloatProperty(options=set(), default=2)
    back: bpy.props.FloatProperty(options=set(), default=-2)


class IOPanel(shared.ArmatureObjectPanel, bpy.types.Panel):
    bl_idname = 'OBJECT_PT_M3_IO'
    bl_label = 'M3 Import/Export'

    def draw(self, context):
        ob = context.object
        layout = self.layout
        layout.use_property_split = True

        op = layout.operator('m3.import')
        op.id_name = context.object.name
        op.filepath = 'C:\\Users\\John Wharton\\Documents\\M3Test_editor2.m3'
        layout.separator()
        op = layout.operator('m3.export')
        op.filepath = 'C:\\Users\\John Wharton\\Documents\\M3Test_studio.m3'
        layout.separator()

        col = layout.column()
        col.prop(ob, 'm3_model_version', text='Model Version')
        col.prop(ob, 'm3_mesh_version', text='Mesh Version')
        col.prop(ob, 'm3_materiallayers_version', text='Material Layer Version')
        col.prop(ob, 'm3_materials_standard_version', text='Standard Material Version')
        col.prop(ob, 'm3_materials_reflection_version', text='Reflection Material Version')
        col.prop(ob, 'm3_cameras_version', text='Camera Version')
        col.prop(ob, 'm3_particlesystems_version', text='Particle System Version')
        col.prop(ob, 'm3_ribbons_version', text='Ribbon Version')
        col.prop(ob, 'm3_forces_version', text='Force Version')
        col.prop(ob, 'm3_physicsshapes_version', text='Physics Shape Version')
        col.prop(ob, 'm3_rigidbodies_version', text='Rigid Body Version')
        col.prop(ob, 'm3_turrets_part_version', text='Turret Part Version')
        col.prop(ob, 'm3_cloths_version', text='Cloth Version')


class OptionsPanel(shared.ArmatureObjectPanel, bpy.types.Panel):
    bl_idname = 'OBJECT_PT_M3_OBJECT_OPTIONS'
    bl_label = 'M3 Object Options'

    def draw(self, context):
        layout = self.layout
        options = context.object.m3_options
        gflow = layout.grid_flow(row_major=True, columns=2, even_columns=True, even_rows=True, align=True)
        gflow.label(text='M3 Automatic Manipulation:')
        gflow.separator()
        gflow.prop(options, 'update_timeline', text='Update Timeline')
        gflow.prop(options, 'update_anim_data', text='Update Animation Data')
        gflow.prop(options, 'update_bone_selection', text='Update Bone Selection')
        gflow.separator()
        gflow.separator()
        gflow.separator()
        gflow.label(text='M3 Property Pose Display:')
        gflow.separator()
        gflow.prop(options, 'draw_attach_points', text='Draw Attachment Points')
        gflow.prop(options, 'draw_selected', text='Draw If Selected')
        gflow.prop(options, 'draw_attach_volumes', text='Draw Attachment Volumes')
        gflow.prop(options, 'draw_rigidbodies', text='Draw Rigid Bodies')
        gflow.prop(options, 'draw_hittests', text='Draw Hit Tests')
        gflow.prop(options, 'draw_cameras', text='Draw Cameras')
        gflow.prop(options, 'draw_lights', text='Draw Lights')
        gflow.prop(options, 'draw_turrets', text='Draw Turrets')
        gflow.prop(options, 'draw_particles', text='Draw Particles')
        gflow.prop(options, 'draw_clothconstraints', text='Draw Cloth Constraints')
        gflow.prop(options, 'draw_ribbons', text='Draw Ribbons')
        gflow.prop(options, 'draw_ikjoints', text='Draw IK Joints')
        gflow.prop(options, 'draw_projections', text='Draw Projection Bounds')
        gflow.prop(options, 'draw_shadowboxes', text='Draw Shadow Boxes')
        gflow.prop(options, 'draw_forces', text='Draw Forces')
        gflow.prop(options, 'draw_warps', text='Draw Vertex Warpers')


class BoundsPanel(shared.ArmatureObjectPanel, bpy.types.Panel):
    bl_idname = 'OBJECT_PT_M3_BOUNDS'
    bl_label = 'M3 Bounds'

    def draw(self, context):
        ob = context.object
        bounds = ob.m3_bounds
        layout = self.layout
        layout.use_property_split = True

        layout.prop(bounds, 'opt_display', text='Preview')
        col = layout.column(align=True)
        col.prop(bounds, 'bottom', text='Bounding Bottom')
        col.prop(bounds, 'top', text='Top')
        col.prop(bounds, 'left', text='Left')
        col.prop(bounds, 'right', text='Right')
        col.prop(bounds, 'front', text='Front')
        col.prop(bounds, 'back', text='Back')


classes = (
    OptionProperties,
    BoundingProperties,
    IOPanel,
    OptionsPanel,
    BoundsPanel,
)
