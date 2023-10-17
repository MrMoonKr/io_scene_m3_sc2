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
from . import bl_enum


def register_props():
    bpy.types.Object.m3_particlesystems = bpy.props.CollectionProperty(type=SystemProperties)
    bpy.types.Object.m3_particlesystems_index = bpy.props.IntProperty(options=set(), default=-1, update=update_collection_index)
    bpy.types.Object.m3_particlesystems_version = bpy.props.EnumProperty(options=set(), items=particle_system_versions, default='24')
    bpy.types.Object.m3_particlecopies = bpy.props.CollectionProperty(type=CopyProperties)
    bpy.types.Object.m3_particlecopies_index = bpy.props.IntProperty(options=set(), default=-1, update=update_copy_collection_index)


# TODO UI stuff
particle_system_versions = (
    ('10', '10', 'Version 10'),
    ('11', '11', 'Version 11'),
    ('12', '12', 'Version 12'),
    ('14', '14', 'Version 14'),
    ('17', '17', 'Version 17'),
    ('18', '18', 'Version 18'),
    ('19', '19', 'Version 19'),
    ('21', '21', 'Version 21'),
    ('22', '22', 'Version 22'),
    ('23', '23', 'Version 23'),
    ('24', '24', 'Version 24'),
)


def update_collection_index(self, context):
    if self.m3_particlesystems_index in range(len(self.m3_particlesystems)):
        bl = self.m3_particlesystems[self.m3_particlesystems_index]
        shared.select_bones_handles(context.object, [bl.bone])


def update_copy_collection_index(self, context):
    if self.m3_particlecopies_index in range(len(self.m3_particlecopies)):
        bl = self.m3_particlecopies[self.m3_particlecopies_index]
        shared.select_bones_handles(context.object, [bl.bone])


def draw_copy_props(copy, layout):
    shared.draw_prop_pointer_search(layout, copy.bone, copy.id_data.data, 'bones', text='Bone', icon='BONE_DATA')
    col = layout.column(align=True)
    shared.draw_prop_anim(col, copy, 'emit_rate', text='Emission Rate')
    shared.draw_prop_anim(col, copy, 'emit_count', text='Emission Amount')
    layout.separator()
    box = layout.box()
    box.use_property_decorate = False
    op = box.operator('m3.handle_add', text='Add Particle System')
    op.collection = copy.systems.path_from_id()

    for ii, system_ref in enumerate(copy.systems):
        row = box.row()
        col = row.column()
        shared.draw_prop_pointer_search(col, system_ref, copy.id_data, 'm3_particlesystems', text='Particle System', icon='LINKED')
        op = row.operator('m3.handle_remove', text='', icon='X')
        op.collection = copy.systems.path_from_id()
        op.index = ii


def draw_props(particle, layout):
    layout.use_property_decorate = False
    par_ver = int(particle.id_data.m3_particlesystems_version)

    shared.draw_prop_pointer_search(layout, particle.bone, particle.id_data.data, 'bones', text='Bone', icon='BONE_DATA')
    col = layout.column()
    col.active = False if bool(particle.model_path) else True
    shared.draw_prop_pointer_search(col, particle.material, particle.id_data, 'm3_materialrefs', text='Material', icon='MATERIAL')
    layout.prop(particle, 'model_path', text='Model Path', icon='FILE_3D')
    col = layout.column()
    col.active = True if particle.model_path else False
    col.prop(particle, 'swap_yz_on_model_particles', text='Swap Y-Z On Model Particles')
    layout.separator()
    row = layout.row(align=True)
    row.prop(particle, 'lod_reduce', text='LOD Reduction/Cutoff')
    row.prop(particle, 'lod_cut', text='')
    row = layout.row(align=True)
    row.prop(particle, 'emit_max', text='Particle Count/Distance Limit')
    row.prop(particle, 'distance_limit', text='')
    layout.separator()
    row = shared.draw_prop_split(layout, text='Emission Rate/Count')
    shared.draw_op_anim_prop(row, particle, 'emit_rate')
    row.separator(factor=0.325)
    shared.draw_op_anim_prop(row, particle, 'emit_count')
    layout.separator()
    col = layout.column(align=True)
    shared.draw_prop_pointer_search(col, particle.trail_system, particle.id_data, 'm3_particlesystems', text='Trail System', icon='LINKED')
    row = shared.draw_prop_split(col, text='Trail Chance/Emission Rate')
    row.prop(particle, 'trail_chance', text='')
    row.separator(factor=0.325)
    shared.draw_op_anim_prop(row, particle, 'trail_rate')
    layout.separator()
    col = layout.column(align=True)
    col.prop(particle, 'particle_type', text='Type')

    if particle.particle_type in ('WORLD', 'SINGLE'):
        row = col.row(align=True)
        row.prop(particle, 'instance_yaw', text='Instance Yaw/Pitch')
        row.prop(particle, 'instance_pitch', text='')
    elif particle.particle_type in ('GROUND'):
        col.prop(particle, 'instance_pitch', text='Instance Pitch')

    if particle.particle_type in ('TAIL', 'GROUND_TAIL', 'TAIL_ALT'):
        row = col.row(align=True)
        row.prop(particle, 'instance_tail', text='Tail Length')
        row.prop(particle, 'tail_type', text='')
    layout.separator()
    row = layout.row()
    row.prop(particle, 'world_space', text='World Space')
    row.prop(particle, 'simulate_init', text='Pre Pump')
    layout.separator()
    col = layout.column(align=True)
    col.prop(particle, 'emit_type', text='Emission Vector')
    row = col.row(align=True)
    row.prop(particle, 'emit_shape', text='Area')
    row.separator(factor=0.325)
    row.prop(particle, 'emit_shape_cutout', text='Cutout')

    if particle.emit_shape != 'POINT':
        size_xy = particle.emit_shape in ['PLANE', 'CUBE']
        size_z = particle.emit_shape in ['CUBE', 'CYLINDER']
        size_r = particle.emit_shape in ['SPHERE', 'CYLINDER', 'DISC']
        if size_xy or size_z or size_r:
            if size_xy:
                row = shared.draw_prop_split(col, text='X')
                shared.draw_op_anim_prop(row, particle, 'emit_shape_size', index=0)
                row.separator(factor=0.325)
                sub = row.row(align=True)
                sub.active = particle.emit_shape_cutout
                shared.draw_op_anim_prop(sub, particle, 'emit_shape_size_cutout', index=0)

                row = shared.draw_prop_split(col, text='Y')
                shared.draw_op_anim_prop(row, particle, 'emit_shape_size', index=1, draw_op=False)
                row.separator(factor=0.325)
                sub = row.row(align=True)
                sub.active = particle.emit_shape_cutout
                shared.draw_op_anim_prop(sub, particle, 'emit_shape_size_cutout', index=1, draw_op=False)

            if size_z:
                row = shared.draw_prop_split(col, text='Z')
                shared.draw_op_anim_prop(row, particle, 'emit_shape_size', index=2, draw_op=not size_xy)
                row.separator(factor=0.325)
                sub = row.row(align=True)
                sub.active = particle.emit_shape_cutout
                shared.draw_op_anim_prop(sub, particle, 'emit_shape_size_cutout', index=2, draw_op=not size_xy)

            if size_r:
                row = shared.draw_prop_split(col, text='R')
                shared.draw_op_anim_prop(row, particle, 'emit_shape_radius', index=0)
                row.separator(factor=0.325)
                sub = row.row(align=True)
                sub.active = particle.emit_shape_cutout
                shared.draw_op_anim_prop(sub, particle, 'emit_shape_radius_cutout', index=0)

        elif particle.emit_shape == 'SPLINE':
            box = col.box()
            box.use_property_split = False
            op = box.operator('m3.collection_add', text='Add Spline Point')
            op.collection = particle.emit_shape_spline.path_from_id()
            for ii, item in enumerate(particle.emit_shape_spline):
                row = box.row(align=True)
                shared.draw_prop_anim(row, item, 'location', index=0, text='X')
                shared.draw_prop_anim(row, item, 'location', index=1, text='Y')
                shared.draw_prop_anim(row, item, 'location', index=2, text='Z')
                row.separator()
                op = row.operator('m3.collection_remove', icon='X', text='')
                op.collection, op.index = (particle.emit_shape_spline.path_from_id(), ii)
        elif particle.emit_shape == 'MESH':
            box = col.box()
            box.use_property_split = False
            op = box.operator('m3.collection_add', text='Add Mesh Object')
            op.collection = particle.emit_shape_meshes.path_from_id()
            for ii, item in enumerate(particle.emit_shape_meshes):
                row = box.row()
                row.prop(item, 'bl_object', text='')
                op = row.operator('m3.collection_remove', icon='X', text='')
                op.collection, op.index = (particle.emit_shape_meshes.path_from_id(), ii)

    layout.separator()
    col = layout.column()
    row = shared.draw_prop_split(col, text='Yaw/Pitch')
    shared.draw_op_anim_prop(row, particle, 'emit_angle_x')
    row.separator(factor=0.325)
    shared.draw_op_anim_prop(row, particle, 'emit_angle_y')
    row = shared.draw_prop_split(col, text='Spread XY')
    shared.draw_op_anim_prop(row, particle, 'emit_spread_x')
    row.separator(factor=0.325)
    shared.draw_op_anim_prop(row, particle, 'emit_spread_y')
    row = shared.draw_prop_split(col, text='Speed')
    shared.draw_op_anim_prop(row, particle, 'emit_speed')
    row.separator(factor=0.75)
    row.prop(particle, 'emit_speed_randomize', text='')
    sub = row.row(align=True)
    sub.active = particle.emit_speed_randomize
    shared.draw_op_anim_prop(sub, particle, 'emit_speed_random')
    row = shared.draw_prop_split(col, text='Lifetime')
    shared.draw_op_anim_prop(row, particle, 'lifespan')
    row.separator(factor=0.75)
    row.prop(particle, 'lifespan_randomize', text='')
    sub = row.row(align=True)
    sub.active = particle.lifespan_randomize
    shared.draw_op_anim_prop(sub, particle, 'lifespan_random')
    layout.separator()
    col = layout.column(align=True)
    if par_ver >= 17:
        col.prop(particle, 'color_smoothing', text='Color Interpolation')
    else:
        col.prop(particle, 'old_color_smoothing', text='Color Interpolation')
    row = col.row(align=True)
    row.prop(particle, 'color_anim_mid', text='RGB/A Midpoint')
    row.prop(particle, 'alpha_anim_mid', text='')
    if par_ver >= 17 and (particle.color_smoothing == 'LINEARHOLD' or particle.color_smoothing == 'BEZIERHOLD'):
        row = col.row(align=True)
        row.prop(particle, 'color_hold', text='RGB/A Hold Time')
        row.prop(particle, 'alpha_hold', text='')
    row = shared.draw_prop_split(layout, text='Lifespan Colors')
    sub = row.column(align=True)
    shared.draw_op_anim_prop(sub, particle, 'color_init')
    shared.draw_op_anim_prop(sub, particle, 'color_mid')
    shared.draw_op_anim_prop(sub, particle, 'color_end')
    row.separator(factor=0.75)
    row.prop(particle, 'color_randomize', text='')
    sub = row.column(align=True)
    sub.active = particle.color_randomize
    shared.draw_op_anim_prop(sub, particle, 'color2_init')
    shared.draw_op_anim_prop(sub, particle, 'color2_mid')
    shared.draw_op_anim_prop(sub, particle, 'color2_end')
    layout.prop(particle, 'vertex_alpha', text='Use Vertex Alpha')
    layout.separator()
    row = shared.draw_prop_split(layout, text='Rotation Interpolation')
    if par_ver >= 17:
        sub = row.row()
        sub.ui_units_x = 100
        sub.prop(particle, 'rotation_smoothing', text='')
    else:
        sub = row.row()
        sub.ui_units_x = 100
        sub.prop(particle, 'old_rotation_smoothing', text='')
    sub = row.row(align=True)
    sub.ui_units_x = 100
    sub.prop(particle, 'rotation_anim_mid', text='')
    if par_ver >= 17 and (particle.rotation_smoothing == 'LINEARHOLD' or particle.rotation_smoothing == 'BEZIERHOLD'):
        sub.prop(particle, 'rotation_hold', text='')
    row = shared.draw_prop_split(layout, text='Lifespan Factor')
    shared.draw_op_anim_prop(row, particle, 'rotation')
    row.separator(factor=0.75)
    row.prop(particle, 'rotation_randomize', text='')
    sub = row.column(align=True)
    sub.active = particle.rotation_randomize
    shared.draw_op_anim_prop(sub, particle, 'rotation2')
    if par_ver >= 18:
        row = layout.row()
        row.prop(particle, 'relative', text='Relative Rotation')
        row.prop(particle, 'always_set', text='Always Set')
    layout.separator()
    row = shared.draw_prop_split(layout, text='Size Interpolation')
    if par_ver >= 17:
        sub = row.row()
        sub.ui_units_x = 100
        sub.prop(particle, 'size_smoothing', text='')
    else:
        sub = row.row()
        sub.ui_units_x = 100
        sub.prop(particle, 'old_size_smoothing', text='')
    sub = row.row(align=True)
    sub.ui_units_x = 100
    sub.prop(particle, 'size_anim_mid', text='')
    if par_ver >= 17 and (particle.size_smoothing == 'LINEARHOLD' or particle.size_smoothing == 'BEZIERHOLD'):
        sub.prop(particle, 'size_hold', text='')
    row = shared.draw_prop_split(layout, text='Lifespan Factor')
    shared.draw_op_anim_prop(row, particle, 'size')
    row.separator(factor=0.75)
    row.prop(particle, 'size_randomize', text='')
    sub = row.column()
    sub.active = particle.size_randomize
    shared.draw_op_anim_prop(sub, particle, 'size2')
    layout.separator()
    row = shared.draw_prop_split(layout, text='Parent Velocity')
    row.prop(particle, 'inherit_parent_velocity', text='')
    sub = shared.draw_op_anim_prop(row, particle, 'parent_velocity')
    sub.active = particle.inherit_parent_velocity
    layout.separator()
    shared.draw_var_props(layout, particle, 'yaw', text='Yaw Variation')
    shared.draw_var_props(layout, particle, 'pitch', text='Pitch Variation')
    shared.draw_var_props(layout, particle, 'spread_x', text='Spread X Variation')
    shared.draw_var_props(layout, particle, 'spread_y', text='Spread Y Variation')
    shared.draw_var_props(layout, particle, 'speed', text='Speed Variation')
    shared.draw_var_props(layout, particle, 'size', text='Size Variation')
    shared.draw_var_props(layout, particle, 'alpha', text='Alpha Variation')
    layout.separator()
    col = layout.column(align=True)
    row = col.row(align=True)
    row.prop(particle, 'mass', text='Mass')
    row.separator(factor=0.75)
    row.prop(particle, 'mass_randomize', text='')
    sub = row.row(align=True)
    sub.active = particle.mass_randomize
    sub.prop(particle, 'mass2', text='')
    col.prop(particle, 'drag', text='Drag')
    row = col.row(align=True)
    row.prop(particle, 'gravity', text='Gravity')
    row.separator()
    row.prop(particle, 'multiply_gravity', text='Factor Map Gravity')
    col.prop(particle, 'wind_multiplier', text='Wind Multiplier')
    row = col.row(align=True)
    row.prop(particle, 'friction', text='Friction/Bounce Factors')
    row.prop(particle, 'bounce', text='')
    row = layout.row(heading='Collision Flags')
    row.prop(particle, 'collide_terrain', text='Terrain')
    row.prop(particle, 'collide_objects', text='Objects')
    row.prop(particle, 'collide_emit', text='Emit')
    col = layout.column(align=True)
    col.active = particle.collide_emit
    shared.draw_prop_pointer_search(col, particle.collide_system, particle.id_data, 'm3_particlesystems', text='Collision System', icon='LINKED')
    col.prop(particle, 'collide_emit_chance', text='Collision Emission Chance')
    col.prop(particle, 'collide_emit_energy', text='Energy')
    row = col.row(align=True)
    row.prop(particle, 'collide_emit_min', text='Minimum/Maximum Emitted')
    row.prop(particle, 'collide_emit_max', text='')
    col.prop(particle, 'collide_events_cull', text='Maximum Events')
    layout.separator()
    col = layout.column(align=True)
    sub = col.row(align=True)
    sub.prop(particle, 'uv_flipbook_cols', text='Flipbook Columns/Rows')
    sub.prop(particle, 'uv_flipbook_rows', text='')
    col.prop(particle, 'random_uv_flipbook_start', text='Random Starting Frame')
    sub = col.row(align=True)
    sub.prop(particle, 'uv_flipbook_start_init_index', text='Phase 1 Start/End')
    sub.prop(particle, 'uv_flipbook_start_stop_index', text='')
    col.prop(particle, 'uv_flipbook_start_lifespan_factor', text='Phase 1 Lifespan')
    sub = col.row(align=True)
    sub.prop(particle, 'uv_flipbook_end_init_index', text='Phase 2 Start/End')
    sub.prop(particle, 'uv_flipbook_end_stop_index', text='')
    layout.separator()
    # row = layout.row()
    col = shared.draw_prop_split(layout, text='Local/World Force Channels', sep=2.05)
    col.prop(particle, 'local_forces', text='')
    col.separator()
    # col = shared.draw_prop_split(row, text='World Force Channels', sep=2.05)
    col.prop(particle, 'world_forces', text='')
    layout.separator()
    col = layout.column(align=True)
    row = col.row(align=True)
    row.prop(particle, 'noise_amplitude', text='Noise Amplitude/Frequency')
    row.prop(particle, 'noise_frequency', text='')
    row = col.row(align=True)
    row.prop(particle, 'noise_cohesion', text='Cohesion/Edge')
    row.prop(particle, 'noise_edge', text='')
    layout.separator()
    row = layout.row()
    row.prop(particle, 'sort_method', text='Sort Method')
    row.separator()
    row.prop(particle, 'sort_reverse', text='Reverse')


class SystemPointerProp(bpy.types.PropertyGroup):
    value: bpy.props.StringProperty(options=set(), get=shared.pointer_get_args('m3_particlesystems'), set=shared.pointer_set_args('m3_particlesystems', False))
    handle: bpy.props.StringProperty(options=set())


class CopySystemPointerProp(bpy.types.PropertyGroup):
    value: bpy.props.StringProperty(options=set(), get=shared.pointer_get_args('m3_particlecopies'), set=shared.pointer_set_args('m3_particlesystems', False))
    handle: bpy.props.StringProperty(options=set())


class SplinePointProperties(shared.M3PropertyGroup):
    location: bpy.props.FloatVectorProperty(name='Location', subtype='XYZ', size=3)
    location_header: bpy.props.PointerProperty(type=shared.M3AnimHeaderProp)


class CopyProperties(shared.M3PropertyGroup):
    bone: bpy.props.PointerProperty(type=shared.M3BonePointerProp)
    systems: bpy.props.CollectionProperty(type=CopySystemPointerProp)
    emit_rate: bpy.props.FloatProperty(name='Particle Copy Emission Rate', min=0)
    emit_rate_header: bpy.props.PointerProperty(type=shared.M3AnimHeaderProp)
    emit_count: bpy.props.IntProperty(name='Particle Copy Emission Count', min=0)
    emit_count_header: bpy.props.PointerProperty(type=shared.M3AnimHeaderProp)


# backwards compatibility for flag options before the enum property implementation
def sort_method_get(self):
    try:
        return self['sort_method']
    except KeyError:
        if self.get('sort'):
            return 1  # 'DISTANCE'
        elif self.get('sort_z_height'):
            return 2  # 'HEIGHT'
        return 0  # 'NONE'


def sort_method_set(self, value):
    self['sort_method'] = value


class SystemProperties(shared.M3PropertyGroup):
    bone: bpy.props.PointerProperty(type=shared.M3BonePointerProp)
    material: bpy.props.PointerProperty(type=shared.M3MatRefPointerProp)
    particle_type: bpy.props.EnumProperty(options=set(), items=bl_enum.particle_type)
    model_path: bpy.props.StringProperty(options=set(), description='Replaces the particle system\'s material with the m3 asset at the given path')
    instance_tail: bpy.props.FloatProperty(options=set(), default=1.0)
    instance_yaw: bpy.props.FloatProperty(options=set(), default=0.0)
    instance_pitch: bpy.props.FloatProperty(options=set(), default=0.0)
    distance_limit: bpy.props.FloatProperty(options=set(), min=0)
    lod_cut: bpy.props.EnumProperty(options=set(), items=bl_enum.lod)
    lod_reduce: bpy.props.EnumProperty(options=set(), items=bl_enum.lod)
    emit_type: bpy.props.EnumProperty(options=set(), items=bl_enum.particle_emit_type)
    emit_shape: bpy.props.EnumProperty(options=set(), items=bl_enum.particle_shape)
    emit_shape_cutout: bpy.props.BoolProperty(options=set())
    emit_shape_size: bpy.props.FloatVectorProperty(name='Emission Area Size', subtype='XYZ', size=3, default=(1, 1, 1))
    emit_shape_size_header: bpy.props.PointerProperty(type=shared.M3AnimHeaderProp)
    emit_shape_size_cutout: bpy.props.FloatVectorProperty(name='Emission Area Size Cutout', subtype='XYZ', size=3)
    emit_shape_size_cutout_header: bpy.props.PointerProperty(type=shared.M3AnimHeaderProp)
    emit_shape_radius: bpy.props.FloatProperty(name='Emission Radius', default=1)
    emit_shape_radius_header: bpy.props.PointerProperty(type=shared.M3AnimHeaderProp)
    emit_shape_radius_cutout: bpy.props.FloatProperty(name='Emission Radius Cutout')
    emit_shape_radius_cutout_header: bpy.props.PointerProperty(type=shared.M3AnimHeaderProp)
    emit_shape_meshes: bpy.props.CollectionProperty(type=shared.M3ObjectPropertyGroup)
    emit_shape_spline: bpy.props.CollectionProperty(type=SplinePointProperties)
    emit_max: bpy.props.IntProperty(options=set(), min=0, default=60)
    emit_rate: bpy.props.FloatProperty(name='Emission Rate', min=0)
    emit_rate_header: bpy.props.PointerProperty(type=shared.M3AnimHeaderProp)
    emit_count: bpy.props.IntProperty(name='Emission Amount', min=0)
    emit_count_header: bpy.props.PointerProperty(type=shared.M3AnimHeaderProp)
    emit_speed: bpy.props.FloatProperty(name='Emission Speed')
    emit_speed_header: bpy.props.PointerProperty(type=shared.M3AnimHeaderProp)
    emit_speed_random: bpy.props.FloatProperty(name='Emission Speed Random', default=1)
    emit_speed_random_header: bpy.props.PointerProperty(type=shared.M3AnimHeaderProp)
    emit_speed_randomize: bpy.props.BoolProperty(options=set())
    emit_angle_x: bpy.props.FloatProperty(name='Emission Angle X')
    emit_angle_x_header: bpy.props.PointerProperty(type=shared.M3AnimHeaderProp)
    emit_angle_y: bpy.props.FloatProperty(name='Emission Angle Y')
    emit_angle_y_header: bpy.props.PointerProperty(type=shared.M3AnimHeaderProp)
    emit_spread_x: bpy.props.FloatProperty(name='Emission Spread X')
    emit_spread_x_header: bpy.props.PointerProperty(type=shared.M3AnimHeaderProp)
    emit_spread_y: bpy.props.FloatProperty(name='Emission Spread Y')
    emit_spread_y_header: bpy.props.PointerProperty(type=shared.M3AnimHeaderProp)
    lifespan: bpy.props.FloatProperty(name='Lifetime', default=0.5, min=0)
    lifespan_header: bpy.props.PointerProperty(type=shared.M3AnimHeaderProp)
    lifespan_random: bpy.props.FloatProperty(name='Lifetime Random', default=1, min=0)
    lifespan_random_header: bpy.props.PointerProperty(type=shared.M3AnimHeaderProp)
    lifespan_randomize: bpy.props.BoolProperty(options=set())
    gravity: bpy.props.FloatProperty(options=set())
    mass: bpy.props.FloatProperty(options=set(), default=1.0)
    mass2: bpy.props.FloatProperty(options=set(), default=1.0)
    mass_randomize: bpy.props.BoolProperty(options=set())
    friction: bpy.props.FloatProperty(options=set(), subtype='FACTOR', soft_min=0, soft_max=1)
    bounce: bpy.props.FloatProperty(options=set(), subtype='FACTOR', soft_min=0, soft_max=1)
    drag: bpy.props.FloatProperty(options=set(), min=0)
    wind_multiplier: bpy.props.FloatProperty(options=set())
    color_init: bpy.props.FloatVectorProperty(name='Initial Color', subtype='COLOR', size=4, min=0, max=1, default=(1, 1, 1, 1))
    color_init_header: bpy.props.PointerProperty(type=shared.M3AnimHeaderProp)
    color_mid: bpy.props.FloatVectorProperty(name='Middle Color', subtype='COLOR', size=4, min=0, max=1, default=(1, 1, 1, 1))
    color_mid_header: bpy.props.PointerProperty(type=shared.M3AnimHeaderProp)
    color_end: bpy.props.FloatVectorProperty(name='Final Color', subtype='COLOR', size=4, min=0, max=1, default=(1, 1, 1, 0))
    color_end_header: bpy.props.PointerProperty(type=shared.M3AnimHeaderProp)
    color2_init: bpy.props.FloatVectorProperty(name='Initial Color Random', subtype='COLOR', size=4, min=0, max=1, default=(1, 1, 1, 1))
    color2_init_header: bpy.props.PointerProperty(type=shared.M3AnimHeaderProp)
    color2_mid: bpy.props.FloatVectorProperty(name='Middle Color Random', subtype='COLOR', size=4, min=0, max=1, default=(1, 1, 1, 1))
    color2_mid_header: bpy.props.PointerProperty(type=shared.M3AnimHeaderProp)
    color2_end: bpy.props.FloatVectorProperty(name='Final Color Random', subtype='COLOR', size=4, min=0, max=1, default=(1, 1, 1, 0))
    color2_end_header: bpy.props.PointerProperty(type=shared.M3AnimHeaderProp)
    color_randomize: bpy.props.BoolProperty(options=set())
    rotation: bpy.props.FloatVectorProperty(name='Rotation', subtype='EULER', size=3, unit='ROTATION')
    rotation_header: bpy.props.PointerProperty(type=shared.M3AnimHeaderProp)
    rotation2: bpy.props.FloatVectorProperty(name='Rotation Random', subtype='EULER', size=3, unit='ROTATION')
    rotation2_header: bpy.props.PointerProperty(type=shared.M3AnimHeaderProp)
    rotation_randomize: bpy.props.BoolProperty(options=set())
    size: bpy.props.FloatVectorProperty(name='Size', subtype='XYZ', size=3, default=(1, 1, 1))
    size_header: bpy.props.PointerProperty(type=shared.M3AnimHeaderProp)
    size2: bpy.props.FloatVectorProperty(name='Size Random', subtype='XYZ', size=3, default=(1, 1, 1))
    size2_header: bpy.props.PointerProperty(type=shared.M3AnimHeaderProp)
    size_randomize: bpy.props.BoolProperty(options=set())
    color_anim_mid: bpy.props.FloatProperty(options=set(), subtype='FACTOR', min=0, max=1, default=0.5)
    alpha_anim_mid: bpy.props.FloatProperty(options=set(), subtype='FACTOR', min=0, max=1, default=0.5)
    rotation_anim_mid: bpy.props.FloatProperty(options=set(), subtype='FACTOR', min=0, max=1, default=0.5)
    size_anim_mid: bpy.props.FloatProperty(options=set(), subtype='FACTOR', min=0, max=1, default=0.5)
    color_hold: bpy.props.FloatProperty(options=set(), min=0)
    alpha_hold: bpy.props.FloatProperty(options=set(), min=0)
    rotation_hold: bpy.props.FloatProperty(options=set(), min=0)
    size_hold: bpy.props.FloatProperty(options=set(), min=0)
    color_smoothing: bpy.props.EnumProperty(options=set(), items=bl_enum.anim_smoothing)
    rotation_smoothing: bpy.props.EnumProperty(options=set(), items=bl_enum.anim_smoothing)
    size_smoothing: bpy.props.EnumProperty(options=set(), items=bl_enum.anim_smoothing)
    old_color_smoothing: bpy.props.EnumProperty(options=set(), items=bl_enum.anim_smoothing_basic)
    old_rotation_smoothing: bpy.props.EnumProperty(options=set(), items=bl_enum.anim_smoothing_basic)
    old_size_smoothing: bpy.props.EnumProperty(options=set(), items=bl_enum.anim_smoothing_basic)
    noise_amplitude: bpy.props.FloatProperty(options=set())
    noise_frequency: bpy.props.FloatProperty(options=set())
    noise_cohesion: bpy.props.FloatProperty(options=set())
    noise_edge: bpy.props.FloatProperty(options=set(), subtype='FACTOR', min=0.0, max=0.5, default=0.1)
    trail_system: bpy.props.PointerProperty(type=SystemPointerProp)
    trail_chance: bpy.props.FloatProperty(options=set(), subtype='FACTOR', min=0.0, max=1.0, default=1.0)
    trail_rate: bpy.props.FloatProperty(name='Particle Trail Rate', min=0.0, default=0.0)
    trail_rate_header: bpy.props.PointerProperty(type=shared.M3AnimHeaderProp)
    uv_flipbook_cols: bpy.props.IntProperty(options=set(), min=0)
    uv_flipbook_rows: bpy.props.IntProperty(options=set(), min=0)
    uv_flipbook_start_init_index: bpy.props.IntProperty(options=set(), min=0, max=255)
    uv_flipbook_start_stop_index: bpy.props.IntProperty(options=set(), min=0, max=255)
    uv_flipbook_end_init_index: bpy.props.IntProperty(options=set(), min=0, max=255)
    uv_flipbook_end_stop_index: bpy.props.IntProperty(options=set(), min=0, max=255)
    uv_flipbook_start_lifespan_factor: bpy.props.FloatProperty(options=set(), subtype='FACTOR', min=0, max=1, default=1.0)
    local_forces: bpy.props.BoolVectorProperty(options=set(), subtype='LAYER', size=16)
    world_forces: bpy.props.BoolVectorProperty(options=set(), subtype='LAYER', size=16)
    pitch_var_shape: bpy.props.EnumProperty(options=set(), items=bl_enum.ribbon_variation_shape)
    pitch_var_amplitude: bpy.props.FloatProperty(name='Pitch Variation Amount')
    pitch_var_amplitude_header: bpy.props.PointerProperty(type=shared.M3AnimHeaderProp)
    pitch_var_frequency: bpy.props.FloatProperty(name='Pitch Variation Frequency')
    pitch_var_frequency_header: bpy.props.PointerProperty(type=shared.M3AnimHeaderProp)
    yaw_var_shape: bpy.props.EnumProperty(options=set(), items=bl_enum.ribbon_variation_shape)
    yaw_var_amplitude: bpy.props.FloatProperty(name='Yaw Variation Amount')
    yaw_var_amplitude_header: bpy.props.PointerProperty(type=shared.M3AnimHeaderProp)
    yaw_var_frequency: bpy.props.FloatProperty(name='Yaw Variation Frequency')
    yaw_var_frequency_header: bpy.props.PointerProperty(type=shared.M3AnimHeaderProp)
    speed_var_shape: bpy.props.EnumProperty(options=set(), items=bl_enum.ribbon_variation_shape)
    speed_var_amplitude: bpy.props.FloatProperty(name='Speed Variation Amount')
    speed_var_amplitude_header: bpy.props.PointerProperty(type=shared.M3AnimHeaderProp)
    speed_var_frequency: bpy.props.FloatProperty(name='Speed Variation Frequency')
    speed_var_frequency_header: bpy.props.PointerProperty(type=shared.M3AnimHeaderProp)
    size_var_shape: bpy.props.EnumProperty(options=set(), items=bl_enum.ribbon_variation_shape)
    size_var_amplitude: bpy.props.FloatProperty(name='Scale Variation Amount')
    size_var_amplitude_header: bpy.props.PointerProperty(type=shared.M3AnimHeaderProp)
    size_var_frequency: bpy.props.FloatProperty(name='Scale Variation Frequency')
    size_var_frequency_header: bpy.props.PointerProperty(type=shared.M3AnimHeaderProp)
    alpha_var_shape: bpy.props.EnumProperty(options=set(), items=bl_enum.ribbon_variation_shape)
    alpha_var_amplitude: bpy.props.FloatProperty(name='Alpha Variation Amount')
    alpha_var_amplitude_header: bpy.props.PointerProperty(type=shared.M3AnimHeaderProp)
    alpha_var_frequency: bpy.props.FloatProperty(name='Alpha Variation Frequency')
    alpha_var_frequency_header: bpy.props.PointerProperty(type=shared.M3AnimHeaderProp)
    spread_x_var_shape: bpy.props.EnumProperty(options=set(), items=bl_enum.ribbon_variation_shape)
    spread_x_var_amplitude: bpy.props.FloatProperty(name='Spread X Variation Amount')
    spread_x_var_amplitude_header: bpy.props.PointerProperty(type=shared.M3AnimHeaderProp)
    spread_x_var_frequency: bpy.props.FloatProperty(name='Spread X Variation Frequency')
    spread_x_var_frequency_header: bpy.props.PointerProperty(type=shared.M3AnimHeaderProp)
    spread_y_var_shape: bpy.props.EnumProperty(options=set(), items=bl_enum.ribbon_variation_shape)
    spread_y_var_amplitude: bpy.props.FloatProperty(name='Spread Y Variation Amount')
    spread_y_var_amplitude_header: bpy.props.PointerProperty(type=shared.M3AnimHeaderProp)
    spread_y_var_frequency: bpy.props.FloatProperty(name='Spread Y Variation Frequency')
    spread_y_var_frequency_header: bpy.props.PointerProperty(type=shared.M3AnimHeaderProp)
    parent_velocity: bpy.props.FloatProperty(name='Parent Velocity Factor', subtype='FACTOR', soft_min=0.0, soft_max=1.0, description='Determines how much the velocity of the emitter is transferred to particles')
    parent_velocity_header: bpy.props.PointerProperty(type=shared.M3AnimHeaderProp)
    collide_system: bpy.props.PointerProperty(type=SystemPointerProp, description='Specifies a system to orphan for collision events. Leave blank to emit generic physics system particles')
    collide_emit_min: bpy.props.IntProperty(options=set(), min=0, description='The minimum number of particles emitted in a collision event')
    collide_emit_max: bpy.props.IntProperty(options=set(), min=0, description='The maximum number of particles emitted in a collision event')
    collide_emit_chance: bpy.props.FloatProperty(options=set(), subtype='FACTOR', min=0.0, max=1.0, default=1.0, description='The particles has the given chance to emit particles in a collision event')
    collide_emit_energy: bpy.props.FloatProperty(options=set(), subtype='FACTOR', soft_min=0.0, soft_max=1.0, description='A general factor applied to the emitted particle based on the speed of the colliding particle')
    collide_events_cull: bpy.props.IntProperty(options=set(), min=0, description='For non-zero values, the particle is destroyed after bouncing the given number of times')
    world_space: bpy.props.BoolProperty(options=set(), description='Makes it so that particles are not hosted to the emitter')
    sort_method: bpy.props.EnumProperty(options=set(), items=bl_enum.particle_sort_method, default='NONE', get=sort_method_get, set=sort_method_set)
    collide_terrain: bpy.props.BoolProperty(options=set(), description='Particle instances will collide with terrain')
    collide_objects: bpy.props.BoolProperty(options=set(), description='Particle instances will collide with game models which have physics bodies')
    collide_emit: bpy.props.BoolProperty(options=set(), description='Enables the collision particle emission system')
    inherit_parent_velocity: bpy.props.BoolProperty(options=set())
    sort_reverse: bpy.props.BoolProperty(options=set(), description='Reverses the order in which particle instances are sorted for rendering')
    random_uv_flipbook_start: bpy.props.BoolProperty(options=set(), description='Causes the particle to initiate on a random frame index when using a flipbook')
    multiply_gravity: bpy.props.BoolProperty(options=set(), description='Applies the in-game map\'s gravity value as a factor to the given system\'s gravity')
    tail_type: bpy.props.EnumProperty(options=set(), items=bl_enum.particle_tail_type)
    vertex_alpha: bpy.props.BoolProperty(options=set(), default=True, description='Enables the alpha channel of the particle\'s color properties')
    swap_yz_on_model_particles: bpy.props.BoolProperty(options=set(), description='Swaps the forward vector for particles using a model')
    simulate_init: bpy.props.BoolProperty(options=set(), description='Simulates particle emission so that it appears to have been emitting previously for an indefinite amount of time')
    relative: bpy.props.BoolProperty(options=set())
    always_set: bpy.props.BoolProperty(options=set())


class SystemMenu(bpy.types.Menu):
    bl_idname = 'OBJECT_MT_m3_particlesystems'
    bl_label = 'Menu'

    def draw(self, context):
        shared.draw_menu_duplicate(self.layout, context.object.m3_particlesystems, dup_keyframes_opt=True)


class CopyMenu(bpy.types.Menu):
    bl_idname = 'OBJECT_MT_m3_particlecopies'
    bl_label = 'Menu'

    def draw(self, context):
        shared.draw_menu_duplicate(self.layout, context.object.m3_particlecopies, dup_keyframes_opt=True)


class CopyPanel(shared.ArmatureObjectPanel, bpy.types.Panel):
    bl_idname = 'OBJECT_PT_m3_particlecopies'
    bl_label = 'M3 Particle Copies'

    def draw(self, context):
        shared.draw_collection_list(self.layout, context.object.m3_particlecopies, draw_copy_props, menu_id=CopyMenu.bl_idname)


class SystemPanel(shared.ArmatureObjectPanel, bpy.types.Panel):
    bl_idname = 'OBJECT_PT_m3_particlesystems'
    bl_label = 'M3 Particle Systems'

    def draw(self, context):
        shared.draw_collection_list(self.layout, context.object.m3_particlesystems, draw_props, menu_id=SystemMenu.bl_idname)


classes = (
    SystemPointerProp,
    CopySystemPointerProp,
    SplinePointProperties,
    CopyProperties,
    SystemProperties,
    SystemMenu,
    CopyMenu,
    SystemPanel,
    CopyPanel,
)
