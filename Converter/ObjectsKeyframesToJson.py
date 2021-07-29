import bpy
import json
import math
from rdp import rdp
from collections import defaultdict

#meter = 100.0
objects_keyframes_path_in_project = '/home/fehty/StudioProjects/blank/assets/json/objects_keyframes.json'

def approximate_curve(dict_points):
    dict_to_arr = [[item, dict_points[item]] for item in dict_points]
    rdp_arr_points = rdp(dict_to_arr)
    rdp_arr_points_to_dict = {}
    for item in rdp_arr_points:
        rdp_arr_points_to_dict[int(item[0])] = item[1]
    return rdp_arr_points_to_dict
    
def get_viewport(num):
    isShowing = None
    if num == 1:
        isShowing = False
    else:
        isShowing = True
    return isShowing

def object_data(action, object, frame):
    dimension_y = round(object.dimensions[1], 3)
    loc_x = None
    loc_y = None
    loc_z = None
    rot_x = None
    rot_y = None
    rot_z = None
    viewport = None
    
    z_transform = ""
    key_frame_data_class = ""
        
    for fcu in action.fcurves:
        for keyframe in fcu.keyframe_points:
            if (keyframe.co.x == frame):        
                type = fcu.data_path
                ind = fcu.array_index
                point = keyframe.co.y
#                point = round(point, 3)
                round_numbers = 3
                if(type == "location" and ind == 0):
                    loc_x = round(point, round_numbers)
                elif(type == "location" and ind == 1):
                    loc_y = round(point, round_numbers)
                elif(type == "location" and ind == 2):
                    loc_z = round(-point - dimension_y / 2, round_numbers)
                elif(type == "rotation_euler" and ind == 0):
                    rot_x = round(point - math.pi / 2, round_numbers)
                elif(type == "rotation_euler" and ind == 1):
                    rot_y = round(-point, round_numbers)
                elif(type == "rotation_euler" and ind == 2):
                    rot_z = round(point, round_numbers) 
                elif(type == "hide_viewport"):
                    viewport = get_viewport(point)
#                if(type == "location" and ind == 0):
#                    loc_x = round(point, 3)
#                elif(type == "location" and ind == 1):
#                    loc_y = round(point, 3)
#                elif(type == "location" and ind == 2):
#                    loc_z = round(point, 3)
#                elif(type == "rotation_euler" and ind == 0):
#                    rot_x = round(point, 3)
#                elif(type == "rotation_euler" and ind == 1):
#                    rot_y = round(point, 3)
#                elif(type == "rotation_euler" and ind == 2):
#                    rot_z = round(point, 3) 
#                elif(type == "hide_viewport"):
#                    viewport = get_viewport(point)

#    return f"ZTransform(translate: ZVector({loc_x} * meter, -({loc_z}) * meter - {dimension_y} * meter / 2, {loc_y} * meter), rotate: ZVector(({rot_x + 0.0} - pi / 2), ({rot_z + 0.0}), -({rot_y + 0.0})), scale: ZVector(({scale_x + 0.0}), ({scale_z + 0.0}), ({scale_y + 0.0})))"""             
    return {'loc_x': loc_x, 'loc_y': loc_z, 'loc_z': loc_y, 'rot_x': rot_x, 'rot_y': rot_z, 'rot_z': rot_y, 'viewport': viewport}
#    return {'loc_x': loc_x, 'loc_y': loc_y, 'loc_z': loc_z, 'rot_x': rot_x, 'rot_y': rot_y, 'rot_z': rot_z, 'viewport': viewport}

def next_closest_parameter_value(ctrl_points, index_to_search_from, object, obj_action, parameter):
    for frame_index in range(index_to_search_from + 1, len(ctrl_points)):
        current_frame = ctrl_points[frame_index]
        frame_parameters = object_data(obj_action, object, current_frame)
        if frame_parameters[parameter] != None:
            return frame_parameters[parameter]
        
def sorted_keypoints_and_action(object):
    ctrl_points = set()
    object_action = None
    for action in bpy.data.actions:
        animation_obj_name = action.name.split('Action', 1)[0]
        if animation_obj_name == object.name:
            object_action = action 
            for channel in action.fcurves: 
                for key in channel.keyframe_points:       
                    if key.select_control_point:
                        ctrl_points.add(key.co.x)
    
    ctrl_points = sorted(ctrl_points, key=float)
    return {'ctrl_points': ctrl_points, 'object_action': object_action}

def keypoints_data(keypoints_list_and_action, object):
    location_x_map = {}
    location_y_map = {}
    location_z_map = {}
    rotation_x_map = {}
    rotation_y_map = {}
    rotation_z_map = {}
    viewport_map = {}
    
    ctrl_points = keypoints_list_and_action['ctrl_points']
    obj_action = keypoints_list_and_action['object_action']
    
    for frame_index in range(0, len(ctrl_points)):
     
        current_frame = ctrl_points[frame_index]
        frame_parameters = object_data(obj_action, object, current_frame)

        frame_time = int(current_frame * 33.33333)
        if frame_parameters['loc_x'] != None:
            location_x_map[frame_time] = frame_parameters['loc_x']
        if frame_parameters['loc_y'] != None:
            location_y_map[frame_time] = frame_parameters['loc_y']
        if frame_parameters['loc_z'] != None:
            location_z_map[frame_time] = frame_parameters['loc_z']
        if frame_parameters['rot_x'] != None:
            rotation_x_map[frame_time] = frame_parameters['rot_x']
        if frame_parameters['rot_y'] != None:
            rotation_y_map[frame_time] = frame_parameters['rot_y']
        if frame_parameters['rot_z'] != None:
            rotation_z_map[frame_time] = frame_parameters['rot_z']
        if frame_parameters['viewport'] != None:
            viewport_map[frame_time] = frame_parameters['viewport']

    parameters_values = {}
    
    if (bool(location_x_map)):
        parameters_values['loc_x'] = approximate_curve(location_x_map)
    if (bool(location_y_map)):
        parameters_values['loc_y'] = approximate_curve(location_y_map)
    if (bool(location_z_map)):
        parameters_values['loc_z'] = approximate_curve(location_z_map)
    if (bool(rotation_x_map)):
        parameters_values['rot_x'] = approximate_curve(rotation_x_map)
    if (bool(rotation_y_map)):
        parameters_values['rot_y'] = approximate_curve(rotation_y_map)
    if (bool(rotation_z_map)):    
        parameters_values['rot_z'] = approximate_curve(rotation_z_map)
    if (bool(viewport_map)): 
        parameters_values['viewport'] = viewport_map
    
    return parameters_values
    
    
def json_object(object):
    keypoints_list_and_action = sorted_keypoints_and_action(object)
    keypoints_parameters = keypoints_data(keypoints_list_and_action, object)
    return keypoints_parameters

def write_json(dict_data):
    f = open(objects_keyframes_path_in_project, "w")
    f.write(json.dumps(dict_data, sort_keys=True, separators=(',', ':')))
    f.close()
    
def objects_json():
    objects_json = {}
    
    for currentObj in range(0, len(bpy.data.objects)):
        object = bpy.data.objects[currentObj]
        if bool(json_object(object)):
            objects_json[format_obj_name(object.name)] = json_object(object)
    
    output = {'objects': objects_json}
    write_json(output)

def format_obj_name(object_name):
    object_name = "object" + object_name.replace(".", "_").replace(" ", "_")
    return object_name

objects_json()
