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
    bpy.types.Object.m3_warps = bpy.props.CollectionProperty(type=Properties)
    bpy.types.Object.m3_warps_index = bpy.props.IntProperty(options=set(), default=-1)


def init_msgbus(ob, context):
    for warp in ob.m3_warps:
        shared.bone_update_event(warp, context)


def draw_props(warp, layout):
    col = layout.column(align=True)
    col.prop(warp, 'radius', text='Radius')
    col.prop(warp, 'strength', text='Strength')


class Properties(shared.M3BoneUserPropertyGroup):
    radius: bpy.props.FloatProperty(name='M3 Warp Radius', min=0, default=1)
    strength: bpy.props.FloatProperty(name='M3 Warp Strength', min=0, default=1)


class Panel(shared.ArmatureObjectPanel, bpy.types.Panel):
    bl_idname = 'OBJECT_PT_M3_WARPS'
    bl_label = 'M3 Vertex Warpers'

    def draw(self, context):
        shared.draw_collection_list(self.layout, 'm3_warps', draw_props)


classes = (
    Properties,
    Panel,
)
