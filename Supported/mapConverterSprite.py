import bpy
import sys
import os
import math
import json

from bpy_extras.object_utils import world_to_camera_view

project_name = bpy.path.basename(bpy.context.blend_data.filepath)
project_name = project_name.split('.', 1)[0]
path = "/home/fehty/BlenderCompilation/BlenderRes/"

def map_to_dart():
#    bpy.ops.object.select_all(action = 'SELECT')
#    bpy.ops.object.origin_set(type = 'ORIGIN_GEOMETRY')

    res_class = get_res_class()
    res_load_method = get_res_load_method()
    objects_in_dart = each_obj_in_dart()

#    objects_in_dart = chairs_objs_in_dart()
    
    file_data = f"""import 'package:blank/utils/animation_controller.dart';
import 'package:flutter/material.dart';
import 'package:flutter_cube/flutter_cube.dart';
import 'package:zflutter/zflutter.dart';
import 'package:blank/utils/atlas_dimension_widget.dart';
import '../../screen.dart';
import '../../utilities.dart';
import 'scene_four.dart' hide Image;
import 'dart:math';
{res_class}
extension {project_name} on Screen {{
    get{project_name}(AnimController controller) => {project_name}Location(controller);
    {res_load_method}
    Location {project_name}Location(AnimController controller) {{
    
    Map<String, ZTransform> rotateValues = {{}};
    List<ZPositioned> rotateObjects = [];
    List<ZPositioned> staticObjects = [];
    {objects_in_dart}
    

    CubeLocation cubeLocation1 = CubeLocation(rotateValues, ZGroup(
    children: [...rotateObjects, ...staticObjects]), ZVector(0, 0, 0),
    ZVector(0, 0, 0), 0);
    
    List<ZTransform> path = [];
    Location {project_name}Location = Location([cubeLocation1], path);
    return {project_name}Location;
    }}
}}"""
    
    blank_pr_path = "/home/fehty/StudioProjects/blank/lib/scenes/scene_four/"
#    os.makedirs(blank_pr_path, exist_ok=True)
    with open(blank_pr_path + "generated_test.dart", "w") as file:
        file.write(file_data)
        
#    blender_res_path = "/home/fehty/BlenderCompilation/BlenderDartMaps/"
#    os.makedirs(blender_res_path, exist_ok=True)
#    with open(blender_res_path + project_name + ".dart", "w") as file:
#        file.write(file_data)
    
def each_obj_in_dart():
    objects_in_dart  = ""
    
    rendered_files = open(path + "RenderedObjs.txt", 'r') 
    file_lines = rendered_files.readlines() 
    for object_name in file_lines:
        object_name = object_name.rstrip()
#        object_name = "object" + object.name.replace(".", "_").replace(" ", "_")
        object = bpy.data.objects[object_name]
        objects_in_dart += create_dart_object(object)
#    for objIndex in range(0, len(bpy.data.objects)):
#        object = bpy.data.objects[objIndex]
#        objects_in_dart += create_dart_object(object)
    return objects_in_dart

def chairs_objs_in_dart():
    objects_in_dart  = ""
    left_chairs = bpy.data.objects["13494_Folding_Chairs_v1_L3.019"]
    objects_in_dart += create_dart_object(left_chairs)
    
    right_chairs = bpy.data.objects["13494_Folding_Chairs_v1_L3.001"]
    objects_in_dart += create_dart_object(right_chairs)
    
    plane = bpy.data.objects["Plane"]
    objects_in_dart += create_dart_object(plane)
    
    return objects_in_dart

def create_dart_object(object):
    object_name = "object" + object.name.replace(".", "_").replace(" ", "_")
    
    round_number_count = 3
    
    position_x = round(object.location.x, round_number_count)
    position_y = round(object.location.y, round_number_count)
    position_z = round(object.location.z, round_number_count)
    
    rotation_x = round(object.rotation_euler.x, round_number_count)
    rotation_y = round(object.rotation_euler.y, round_number_count)
    rotation_z = round(object.rotation_euler.z, round_number_count)

    dimension_x = round(object.dimensions[0], round_number_count)
    dimension_y = round(object.dimensions[1], round_number_count)
    dimension_z = round(object.dimensions[2], round_number_count)
    
#    dart_obj_snippet = f"""
#    ramData.customValue<Map<AtlasDimensions, Rect>>('{object_name}',
#    {{AtlasDimensions.low: Rect.fromLTWH(200.0, 100.0, 400.0, 400.0),
#    AtlasDimensions.medium: Rect.fromLTWH(200.0, 750.0, 400.0, 400.0),
#    AtlasDimensions.high: Rect.fromLTWH(200.0, 1400.0, 400.0, 400.0)}});
#    ZWidget {object_name} = ZPositioned(
#        translate: ZVector({position_x} * meter, {position_z} * meter, {position_y} * meter),
#        rotate: ZVector({rotation_x}, {rotation_z}, {rotation_y}),
#        child: ZToBoxAdapter(
#            width: 0,
#            height: 0,
#            child: AtlasDimensionWidget(
#                image: ramData[{project_name}ResStrings.{object_name}Sprite],
#                rect: ramData.customValue('{object_name}')[AtlasDimensions.high])));
#    staticObjects.add({object_name});
#    """

    json_data = None
    with open("/home/fehty/PycharmProjects/SpriteLauncher/spritesData.json", "r") as read_file:
        json_data = json.load(read_file)
       
    high_res_data = json_data["spriteObjs"][object_name]["highResolution"]
    high_res_size = high_res_data["tileSize"]
    high_res_pos = high_res_data["tilesPosition"][0]
    
    med_res_data = json_data["spriteObjs"][object_name]["mediumResolution"]
    med_res_size = med_res_data["tileSize"]
    med_res_pos = med_res_data["tilesPosition"][0]
    
    low_res_data = json_data["spriteObjs"][object_name]["lowResolution"]
    low_res_size = low_res_data["tileSize"]
    low_res_pos = low_res_data["tilesPosition"][0]
    
    
    dart_obj_snippet = f"""
    ramData.customValue<Map<AtlasDimensions, Rect>>('{object_name}',
        {{AtlasDimensions.high: Rect.fromLTWH({high_res_pos["left"]}, {high_res_pos["top"]}, {high_res_size["width"]}, {high_res_size["height"]}),
         AtlasDimensions.medium: Rect.fromLTWH({med_res_pos["left"]}, {med_res_pos["top"]}, {med_res_size["width"]}, {med_res_size["height"]}),
         AtlasDimensions.low: Rect.fromLTWH({low_res_pos["left"]}, {low_res_pos["top"]}, {low_res_size["width"]}, {low_res_size["height"]})}});
    ZWidget {object_name} = ZPositioned(
        translate: ZVector({position_x} * meter, -({position_z})  * meter - {med_res_size["height"]}, {position_y} * meter),
//        rotate: ZVector({rotation_x}, {rotation_z}, {rotation_y}),
        child: ZToBoxAdapter(
            width: 0.0,
            height: 0.0,
            child: AtlasDimensionWidget(
                image: ramData[DISCOResStrings.{object_name}Sprite],
                rect: ramData.customValue('{object_name}')[AtlasDimensions.medium])));
    staticObjects.add({object_name});
    """
#        ZWidget {object_name} = ZPositioned(
#          translate: ZVector({position_x} * meter, {position_z} * meter, {position_y} * meter),
#          rotate: ZVector({rotation_x}, {rotation_z}, {rotation_y}),
#          child: ZToBoxAdapter(
#            width: {dimension_x} * meter,
#            height: {dimension_y} * meter,
#            child: Container(color: Colors.blue)));
#    staticObjects.add({object_name});
    return dart_obj_snippet

def get_res_class():
    each_res_str = ""
    
    rendered_files = open(path + "RenderedObjs.txt", 'r') 
    file_lines = rendered_files.readlines() 
    for object_name in file_lines:
        object_name = object_name.rstrip()
        object_name = "object" + object_name.replace(".", "_").replace(" ", "_")
        each_res_str += f"""\n static const String {object_name}Sprite = '${{assetsPrefix}}scene_four/{project_name}/sprite/{object_name}.png';"""
#    for objIndex in range(0, len(bpy.data.objects)):
#        object = bpy.data.objects[objIndex]
#        object_name = "object" + object.name.replace(".", "_").replace(" ", "_")
#        each_res_str += f"""\n  static const String {object_name}Sprite = '${{assetsPrefix}}scene_four/{project_name}/sprite/{object_name}.png';"""
    
#    static const String object0 = '${{assetsPrefix}}scene_four/DISCO/sprite/SpriteObj0.png';
    res_class_data  = f"""
class {project_name}ResStrings {{ {each_res_str}
}}
"""
    return res_class_data

def get_res_load_method():
    each_load_str = ""
    
    rendered_files = open(path + "RenderedObjs.txt", 'r') 
    file_lines = rendered_files.readlines() 
    for object_name in file_lines: 
        object_name = object_name.rstrip()
        object_name = "object" + object_name.replace(".", "_").replace(" ", "_")
        each_load_str += f"""
    await ramData.lUiImage({project_name}ResStrings.{object_name}Sprite);"""
      
#      await ramData.lUint8List({project_name}ResStrings.object0);
    res_load_method_data  = f"""
    load{project_name}Res() async {{ {each_load_str}
}}
"""
    
#    for objIndex in range(0, len(bpy.data.objects)):
#        object = bpy.data.objects[objIndex]
#        object_name = "object" + object.name.replace(".", "_").replace(" ", "_")
#        each_load_str += f"""
#      await ramData.lUiImage({project_name}ResStrings.{object_name}Sprite);"""
#      
##      await ramData.lUint8List({project_name}ResStrings.object0);
#    res_load_method_data  = f"""
#    load{project_name}Res() async {{ {each_load_str}
#}}
#"""
    return res_load_method_data

#==================================================================================================

def renderObj(objNumber, frame, rotValue):
    s=bpy.context.scene

    s.render.resolution_x = 1920
    s.render.resolution_y = 1080

    cam = bpy.data.objects["Camera"]
    
    bpy.data.objects[objNumber].rotation_euler.x += math.radians(rotValue)

    s.frame_set(frame)
    objRot = bpy.data.objects[objNumber].rotation_euler.x
    
    object = bpy.data.objects[objNumber]
    object_name = "object" + object.name.replace(".", "_").replace(" ", "_")
        
    s.render.filepath = ("/home/fehty/BlenderCompilation/BlenderRes/ClosestRotateRender/" 
    + "/" + object_name + "/" + "Fr" + str(s.frame_current).zfill(3)) + "Rot" +str(int(math.degrees(objRot)))

#    s.render.filepath = ("/home/fehty/BlenderCompilation/BlenderRes/ClosestRotateRender/" 
#    + "/" + "Obj" + str(objNumber) + "/" + "Fr" + str(s.frame_current).zfill(3)) + "Rot" +str(int(math.degrees(objRot)))
    
    bpy.ops.render.render(False,animation=False,write_still=True)

def findClosestRotFrame(objNumber, rotValue, starFrame, endFrame):
    s=bpy.context.scene

    s.render.resolution_x = 1920
    s.render.resolution_y = 1080

    smallestValuesFromEachFrame={}
    cam = bpy.data.objects["Camera"]
    
    bpy.data.objects[objNumber].rotation_euler.x += math.radians(rotValue)
    
    for i in range(starFrame,endFrame):
        s.frame_current = i
        s.frame_set(i)
        
        obj = bpy.data.objects[objNumber]
        
        if(cam and obj and obj.type == 'MESH' and 
        eachVertIsInView(objNumber, s, cam, obj)==True):
            smallestValuesFromEachFrame[i] = (min(getCamToObjDist(objNumber, s, cam)))
    
    if(len(smallestValuesFromEachFrame) != 0):
        closestToObjectFrame = min(smallestValuesFromEachFrame, key=smallestValuesFromEachFrame.get)
        return closestToObjectFrame
    else: 
        return None

def eachVertIsInView(objNumber, scene, cam, ob):
        camloc = cam.matrix_world.translation
        mw = ob.matrix_world
        me = ob.data # mesh
        cs = cam.data.clip_start
        ce =  cam.data.clip_end
        for v in me.vertices:
            co_ndc = world_to_camera_view(scene, cam, mw @ v.co)
            if not (0.0 < co_ndc.x < 1.0 and 0.0 < co_ndc.y < 1.0 and cs < co_ndc.z <  ce):
                return False
        return True

def getCamToObjDist(objNumber, scene, camera):
    ob = bpy.data.objects[objNumber]
    camloc = camera.matrix_world.translation
    mw = ob.matrix_world
    me = ob.data # mesh
    camdists = [(mw @ v.co - camloc).length for v in me.vertices]
    return camdists

def findClosestFrame(valuesForEachFrame):
    return valuesForEachFrame.index(min(valuesForEachFrame))
    
allObjects = len(bpy.data.objects)

def resetWorld():
    for objIndex in range(0, allObjects):
        bpy.data.objects[objIndex].hide_set(False)
        bpy.data.objects[objIndex].hide_render = False
        
objLength = allObjects

def hideAllObjects():
    for objIndex in range(0, allObjects):
        if bpy.data.objects[objIndex].name == "Point":
            bpy.data.objects[objIndex].hide_set(False)
            bpy.data.objects[objIndex].hide_render = False
#        elif bpy.data.objects[objIndex].name == "Loft09":
#            bpy.data.objects[objIndex].hide_set(False)
#            bpy.data.objects[objIndex].hide_render = False    
#        elif bpy.data.objects[objIndex].name == "13494_Folding_Chairs_v1_L3.001":
#            bpy.data.objects[objIndex].hide_set(False)
#            bpy.data.objects[objIndex].hide_render = False    
        else:
            print(bpy.data.objects[objIndex].name)
            bpy.data.objects[objIndex].hide_set(True)
            bpy.data.objects[objIndex].hide_render = True

def render_each_obj():
    hideAllObjects()

    if os.path.exists(path + "RenderedObjs.txt"):
 #       os.remove(path + "RenderedObjs.txt")
    if os.path.exists(path + "NotRenderedObjs.txt"):
 #       os.remove(path + "NotRenderedObjs.txt")
    
    for currentObj in range(0, objLength):
        bpy.data.objects[currentObj].hide_render = False
        previous_obj_name = bpy.data.objects[currentObj - 1].name
        if(currentObj != 0 and previous_obj_name != "Point"):
            bpy.data.objects[currentObj - 1].hide_render = True
            
        object = bpy.data.objects[currentObj]
        object_name = object.name
#        object_name = "object" + object.name.replace(".", "_").replace(" ", "_")
        
        closest_rot_frames = []
        for rotCoef in range(1):
            closest_rot_frames.append(findClosestRotFrame(currentObj, 0, 0, 180))
            
        if(len(closest_rot_frames) != 0 and closest_rot_frames[0] != None):
#            closest_frame = min(closest_rot_frames)
            for closest_rot_frame in closest_rot_frames:
                renderObj(currentObj, closest_rot_frame, 0)
                appendToFile("RenderedObjs.txt", object_name)
#                print(object_name)
        else: 
            appendToFile("NotRenderedObjs.txt", object_name)
                     
    resetWorld()
    
def appendToFile(fileName, data):
    os.makedirs(path, exist_ok=True)
    with open(path + fileName, "a") as file:
        file.write(f"""{data}\n""")
#=================================================================================


# First
#render_each_obj()

# Second
# PyCharm scripts

# Third
map_to_dart()



