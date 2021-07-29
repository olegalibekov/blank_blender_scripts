import bpy

ctrl_points = set()
for action in bpy.data.actions:
    for channel in action.fcurves: 
        for key in channel.keyframe_points:       
            if key.select_control_point:
                ctrl_points.add(key.co.x)

ctrl_points = sorted(ctrl_points)
action = bpy.data.actions["CameraAction"]

print(ctrl_points)
def convert_frame_to_dart(frame_num):
    
    key_frame = ctrl_points[frame_num]
    
    loc_x = 0.0
    loc_y = 0.0
    loc_z = 0.0
    rot_x = 0.0
    rot_y = 0.0
    rot_z = 0.0
    scale_x = 0.0
    scale_y = 0.0
    scale_z = 0.0
    
    for fcu in action.fcurves:
        type = fcu.data_path
        ind = fcu.array_index
        point = fcu.keyframe_points[frame_num].co.y
        point = round(point, 3)

        if(type == "location" and ind == 0):
            loc_x = point
        elif(type == "location" and ind == 1):
            loc_y = point
        elif(type == "location" and ind == 2):
            loc_z = point
        elif(type == "rotation_euler" and ind == 0):
            rot_x = point
        elif(type == "rotation_euler" and ind == 1):
            rot_y = point
        elif(type == "rotation_euler" and ind == 2):
            rot_z = point
        elif(type == "scale" and ind == 0):
            scale_x = point
        elif(type == "scale" and ind == 1):
            scale_y = point
        elif(type == "scale" and ind == 2):
            scale_z = point

    map_element = f"""\n{int(key_frame * 33.3)}.millis(): ZTransform(translate: ZVector(-({loc_x + 0.0}) * meter, ({loc_z + 0.0}) * meter, -({loc_y + 0.0}) * meter), rotate: ZVector((pi / 2 - {rot_x + 0.0}), -({rot_z + 0.0}), ({rot_y + 0.0})), scale: ZVector(({scale_x + 0.0}), ({scale_z + 0.0}), ({scale_y + 0.0})))"""
    return map_element

map_data = ""
for frame_num in range(len(ctrl_points)):
    data = convert_frame_to_dart(frame_num)
    if (frame_num != len(ctrl_points) - 1):
        data += ","
    map_data += data
    
whole_map = f"""final Map<Duration, ZTransform> _camAnimValues = {{{map_data}
      }};"""
      
print(whole_map)


