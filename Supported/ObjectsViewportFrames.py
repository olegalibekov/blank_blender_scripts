import bpy

chosen_obj = bpy.data.objects['13494_Folding_Chairs_v1_L3.001']

viewport_data_objs_in_dart = ""

for action in bpy.data.actions:
    for channel in action.fcurves: 
        if channel.data_path == 'hide_viewport':
            for key in channel.keyframe_points:       
                if key.select_control_point:
                    key_data = key.co
                    show = None
                    if key_data.y == 1:
                        show = 'false'
                    else:
                        show = 'true' 
                    viewport_data_objs_in_dart += f"""\n     {int(key_data.x * 33.3 / 33.3)}.millis(): {show},"""
                    
whole_viewport_data_in_dart =  f"""final Map<Duration, bool> _objectViewports = {{{viewport_data_objs_in_dart.rstrip(',')}
}};"""
    
print(whole_viewport_data_in_dart)
