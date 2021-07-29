import bpy
import sys
import os
import math
import json
from bpy_extras.object_utils import world_to_camera_view

project_name = bpy.path.basename(bpy.context.blend_data.filepath)
project_name = project_name.split('.', 1)[0]
path = "/home/fehty/BlenderCompilation/BlenderRes/"
spr_launcher_path = "/home/fehty/PycharmProjects/SpriteLauncher/"
objects_keyframes_path = '/home/fehty/StudioProjects/blank/assets/json/objects_keyframes.json'
all_objs = bpy.data.objects
images = bpy.data.images
specified_objs = ["Plane", "celling", "podium"]

def write_json_objs():
    json_objects = each_obj_in_dart()
    blank_pr_path = "/home/fehty/StudioProjects/blank/assets/json/"
    with open(blank_pr_path + "objects_data.json", "w") as file:
        json.dump(json_objects, file)
        
def map_to_dart():
    image_ext = image_extension()
    res_class = get_res_class()
    res_load_method = get_res_load_method()
    specified_objs = get_specified_objs()
#    dynamic_objs = dynamic_objs_in_dart()
    file_data = f"""import 'package:blank/utils/animation_controller.dart';
import 'package:flutter/material.dart' hide Material;
import 'package:simple_animations/simple_animations.dart';
import 'package:zflutter/zflutter.dart';
import 'package:flutter/material.dart' as i;
import 'dart:typed_data';
import 'dart:math';
import 'package:box3d/box3d.dart';

import '../../../screen.dart';
import '../scene_four.dart';

extension Disco on Screen {{
    getDisco(AnimController controller) => DiscoLocation(controller);
    Location DiscoLocation(AnimController controller) {{
    Map<String, ZTransform> rotateValues = {{}};
    List<ZPositioned> rotateObjects = [];
    List staticObjects = [];
    World world = (ramData['world'] as World);
    
    CubeLocation cubeLocation1 = CubeLocation(rotateValues, ZGroup(
    children: [...rotateObjects, ...staticObjects]), ZVector(0, 0, 0),
    ZVector(0, 0, 0), 0);
    
    List<ZTransform> path = [];
    Location DiscoLocation = Location([cubeLocation1], path);
    return DiscoLocation;
    }}
}}"""
    
    blank_pr_path = "/home/fehty/StudioProjects/blank/lib/scenes/scene_four/"
    with open(blank_pr_path + "scene_generating/" + "objects_data.dart", "w") as file:
        file.write(file_data)
    
def image_extension():
    image_ext = f"""class Image extends StatelessWidget {{
    Image();

    Uint8List memory;
    String path;

    var key;
    var fit;
    ImageRepeat repeat;

    Image.memory(this.memory,
      {{this.key, this.fit, this.repeat = ImageRepeat.noRepeat}});

    Image.asset(this.path,
      {{this.key, this.fit, this.repeat = ImageRepeat.noRepeat}});

    @override
    Widget build(BuildContext context) {{
    return RepaintBoundary(
        child: path != null ? i.Image.asset(
            path,
            key: key,
            fit: fit,
            repeat: this.repeat) 
            : i.Image.memory(
            memory,
            key: key,
            fit: fit,
            repeat: this.repeat));
      }}
}}"""
    return image_ext

def get_specified_objs():
    objects_in_dart  = ""
    for object_name in specified_objs:
        object = bpy.data.objects[object_name]
        objects_in_dart += create_dart_specified_object(object)
    return objects_in_dart

def each_obj_in_dart():
    
    json_objects_in_dart = dict()
    json_objects_in_dart['disco_objects'] = {}
    
    json_objects = json_objects_in_dart['disco_objects']
#    json_objects_in_dart['disco_objects']['static'] = {}
#    static_json_objects = json_objects_in_dart['disco_objects']
    
#    json_objects_in_dart['disco_objects']['dynamic'] = {}
#    dynamic_json_objects = json_objects_in_dart['disco_objects']
    
    objects_keyframes = None
    with open(objects_keyframes_path) as json_file:
        objects_keyframes = json.load(json_file)['objects']

    rendered_files = open(path + "RenderedObjs.txt", 'r') 
    file_lines = rendered_files.readlines() 
    for object_name in file_lines:
        object_name = object_name.rstrip()
        object = bpy.data.objects[object_name]
        formatted_obj_name = format_obj_name(object.name)
        if formatted_obj_name not in objects_keyframes:
            json_objects[format_obj_name(object_name)] = {}
            json_objects[format_obj_name(object_name)]['original_values'] = create_json_static_object(object)
#            json_objects_in_dart[format_obj_name(object_name)] = create_json_static_object(object)
        elif formatted_obj_name in objects_keyframes:
            current_object_data = objects_keyframes[formatted_obj_name]
            parameters_existence = {
            'loc_x': "loc_x" in current_object_data,
            'loc_y': "loc_y" in current_object_data,
            'loc_z': "loc_z" in current_object_data,
            'rot_x': "rot_x" in current_object_data,
            'rot_y': "rot_y" in current_object_data,
            'rot_z': "rot_z" in current_object_data,
            'viewport': "viewport" in current_object_data,
            }
            json_objects[format_obj_name(object_name)] = {}
            json_objects[format_obj_name(object_name)]['original_values'] = {}
            json_objects[format_obj_name(object_name)]['original_values'] = dynamic_obj_orig_values(object)
            json_objects[format_obj_name(object_name)]['animation_values_existence'] = {}
            json_objects[format_obj_name(object_name)]['animation_values_existence'] = parameters_existence
            
#            dynamic_json_objects[format_obj_name(object_name)] = create_dart_dynamic_object(object, parameters_existence)
    return json_objects_in_dart

#def each_obj_in_dart():
##    context = bpy.context
##    obj = bpy.data.objects["bs01.032"]
##    mesh = obj.data

##    for f in mesh.polygons:  # iterate over faces
##        print("face", f.index, "material_index", f.material_index)
##        slot = obj.material_slots[f.material_index]
##        mat = slot.material
##        if mat is not None:
##            print(mat.name)
###            print(mat.diffuse_color)
##        else:
##            print("No mat in slot", material_index)
#    
#    objects_in_dart = ""
##    rendered_imgs_obj = open(path + "RenderedImgs.txt", 'r') 
##    rendered_imgs_obj = rendered_imgs_obj.readlines()
##    for image_object_name in rendered_imgs_obj:
##        image_object_name = image_object_name.rstrip()
##        object = bpy.data.objects[image_object_name]
##        if object.type == "EMPTY":
##            objects_in_dart += create_dart_image_object(object)
##        else:
##            objects_in_dart += create_dart_texture_object(object)
#    
#    objects_keyframes = None
#    with open(objects_keyframes_path) as json_file:
#        objects_keyframes = json.load(json_file)['objects']

#    rendered_files = open(path + "RenderedObjs.txt", 'r') 
#    file_lines = rendered_files.readlines() 
#    for object_name in file_lines:
#        object_name = object_name.rstrip()
#        object = bpy.data.objects[object_name]
#        formatted_obj_name = format_obj_name(object.name)
#        if formatted_obj_name not in objects_keyframes:
#            objects_in_dart += create_dart_object(object)
#        elif formatted_obj_name in objects_keyframes:
#            current_object_data = objects_keyframes[formatted_obj_name]
#            parameters_existence = {
#            'loc_x': "loc_x" in current_object_data,
#            'loc_y': "loc_y" in current_object_data,
#            'loc_z': "loc_z" in current_object_data,
#            'rot_x': "rot_x" in current_object_data,
#            'rot_y': "rot_y" in current_object_data,
#            'rot_z': "rot_z" in current_object_data,
#            'viewport': "viewport" in current_object_data,
#            }
#            objects_in_dart += create_dart_dynamic_object(object, parameters_existence)
#    return objects_in_dart

#def dynamic_objs_in_dart():
#    dynamic_objects_in_dart  = ""
#    for obj in dynamic_objs_collection.all_objects:
#        dynamic_objects_in_dart += create_dart_dynamic_object(obj)
#    return dynamic_objects_in_dart
#        print(key_frame_data(obj))
        
def create_dart_specified_object(object):
    object_name = format_obj_name(object.name)
    
    round_number_count = 3
    position_x = round(object.location.x, round_number_count)
    position_y = round(object.location.y, round_number_count)
    position_z = round(object.location.z, round_number_count)
    rotation_x = round(object.rotation_euler.x, round_number_count)
    rotation_y = round(object.rotation_euler.y, round_number_count)
    rotation_z = round(object.rotation_euler.z, round_number_count)
    scale_x = abs(round(object.scale[0], round_number_count))
    scale_y = abs(round(object.scale[1], round_number_count))
    scale_z = abs(round(object.scale[2], round_number_count))
    dimension_x = round(object.dimensions[0], round_number_count)
    dimension_y = round(object.dimensions[1], round_number_count)
    dimension_z = round(object.dimensions[2], round_number_count)
    
    color = ""
    if object.name == "podium":
        color = "198, 201, 207, 1"
    elif object.name == "Plane":
        color = "58, 64, 67, 1"
    elif object.name == "celling":
        color = "94, 85, 73, 1"
    
    world_init = f"""var {object_name}Shape = Box(Vec3(({dimension_x} * meter / 2).toDouble(), ({dimension_y} * meter / 2).toDouble(), (1).toDouble()));
    var {object_name}Material = Material();
    Body {object_name}Body = Body(BodyOptions(
          mass: 0,
          material: {object_name}Material,
          position: Vec3(({position_x} * meter / 2).toDouble(), ({position_y} * meter / 2).toDouble(), ({position_z} * meter).toDouble())));
    {object_name}Body.quaternion.setFromAxisAngle(Vec3(0, 1, 0), {rotation_y});
    {object_name}Body.addShape({object_name}Shape);
    world.addBody({object_name}Body);"""  
    
    dart_obj_snippet = f"""
    {world_init}
    
    ZWidget {object_name} = ZPositioned(
        translate: ZVector({position_x} * meter, -({position_z}) * meter, {position_y} * meter),
        rotate: ZVector({rotation_x} + pi/2, {rotation_z}, {rotation_y}),
        child: ZToBoxAdapter(
            width: {dimension_x + 0.0} * meter,
            height: {dimension_y + 0.0} * meter,
            child: Container(color: Color.fromRGBO({color}))));
    staticObjects.add({object_name});
     """
    return dart_obj_snippet

def create_dart_image_object(object):
    object_name = format_img_name(object.name)
    
    round_number_count = 3
    
    position_x = round(object.location.x, round_number_count)
    position_y = round(object.location.y, round_number_count)
    position_z = round(object.location.z, round_number_count)
    
    rotation_x = round(object.rotation_euler.x, round_number_count)
    rotation_y = round(object.rotation_euler.y, round_number_count)
    rotation_z = round(object.rotation_euler.z, round_number_count)

    scale_x = abs(round(object.scale[0], round_number_count))
    scale_y = abs(round(object.scale[1], round_number_count))
    scale_z = abs(round(object.scale[2], round_number_count))
    
    img = get_img_by_obj(object.name)
    
    width = img.size[0]
    height = img.size[1]
    
    dimension_x = round(object.dimensions[0], round_number_count)
    dimension_y = round(object.dimensions[1], round_number_count)
    dimension_z = round(object.dimensions[2], round_number_count)
    
    full_height = round(height * scale_y + 0.0, round_number_count) 
    
    dart_obj_snippet = f"""
    AnimController {object_name}AnimationController =
        AnimController(vsync: vsync, duration: Duration(microseconds: 100));
    
    ZTransform {object_name}Transfrom = ZTransform(
       translate: ZVector({position_x} * meter, -({position_z}) * meter, {position_y} * meter),
       rotate: ZVector({rotation_x} - pi/2, {rotation_z}, {rotation_y}),
       scale: ZVector(0.0, 0.0, 0.0));

    MultiTween<ZTransformMultiTween> {object_name}MultiTween = getMultiTween(
        {object_name}Transfrom, {object_name}Transfrom);
    Animation<MultiTweenValues<
        ZTransformMultiTween>> {object_name}MultiTweenAnimation = {object_name}MultiTween
        .animate({object_name}AnimationController);
    ramData['sceneFourChildren']['{object_name}'] = ObjectData(
        animationController: {object_name}AnimationController,
        multiTweenAnimation: {object_name}MultiTweenAnimation,
        zTransform: {object_name}Transfrom);

    ObjectData {object_name}Link = (ramData['sceneFourChildren']['{object_name}'] as ObjectData);

    AnimatedBuilder {object_name} = AnimatedBuilder(
        animation: {object_name}Link.animationController,
        builder: (context, child) {{
        ZVector {object_name}RotateVector = {object_name}Link.multiTweenAnimation.currentZTransform.rotate;
          {object_name}Link.zTransform.rotate =
            {object_name}RotateVector.copyWith(y: {object_name}Transfrom.rotate.y 
                + {object_name}RotateVector.y);
          return ZPositioned(
              translate: {object_name}Link
                  .zTransform.translate,
              rotate: {object_name}Link.zTransform.rotate,
              child: ZToBoxAdapter(
                width: {width + 0.0} ,
                height: {full_height},
                  child: Image.asset(DiscoResStrings.{object_name}Sprite)));
        }});
    staticObjects.add({object_name});
"""
    return dart_obj_snippet
    
def create_dart_texture_object(object):
    object_name = format_img_name(object.name)
    
    round_number_count = 3
    
    position_x = round(object.location.x, round_number_count)
    position_y = round(object.location.y, round_number_count)
    position_z = round(object.location.z, round_number_count)
    
    rotation_x = round(object.rotation_euler.x, round_number_count)
    rotation_y = round(object.rotation_euler.y, round_number_count)
    rotation_z = round(object.rotation_euler.z, round_number_count)

    scale_x = abs(round(object.scale[0], round_number_count))
    scale_y = abs(round(object.scale[1], round_number_count))
    scale_z = abs(round(object.scale[2], round_number_count))
    
    img = get_img_by_obj(object.name)
    
    width = img.size[0]
    height = img.size[1]
    
    dimension_x = round(object.dimensions[0], round_number_count)
    dimension_y = round(object.dimensions[1], round_number_count)
    dimension_z = round(object.dimensions[2], round_number_count)
    
    world_init = f"""//var {object_name}Shape = Box(Vec3(({dimension_x} * meter / 2).toDouble(), ({dimension_y} * meter / 2).toDouble(), (1).toDouble()));
//    var {object_name}Material = Material();
//    Body {object_name}Body = Body(BodyOptions(
//          mass: 0,
//          material: {object_name}Material,
//          position: Vec3(({position_x} * meter / 2).toDouble(), ({position_y} * meter / 2).toDouble(), ({position_z} * meter).toDouble())));
//    {object_name}Body.quaternion.setFromAxisAngle(Vec3(0, 1, 0), {rotation_y});
//    {object_name}Body.addShape({object_name}Shape);
//    world.addBody({object_name}Body);""" 
    
    dart_obj_snippet = f"""
    {world_init}
    ZWidget {object_name} = ZPositioned(
        translate: ZVector({position_x} * meter, -({position_z}) * meter - {dimension_x} / 2, {position_y} * meter),
        rotate: ZVector({rotation_x}, {rotation_y}, {rotation_z}),
        child: ZToBoxAdapter(
            width: {dimension_y + 0.0} * meter,
            height: {dimension_x + 0.0} * meter,
            child: Image.asset(
               DiscoResStrings.{object_name}Sprite, fit: BoxFit.fill)));
    staticObjects.add({object_name});
     """
    return dart_obj_snippet

def create_json_static_object(object):
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
    
    json_object = {
    "blend_pos_x": position_x,
    "blend_pos_y": position_y,
    "blend_pos_z": position_z,
    "blend_rot_x": rotation_x,
    "blend_rot_y": rotation_y,
    "blend_rot_z": rotation_z,
    "blend_dim_x": dimension_x,
    "blend_dim_y": dimension_y,
    "blend_dim_z": dimension_z
    }
    
    return json_object

def dynamic_obj_orig_values(object):
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
    
    json_object = {
    "blend_pos_x": position_x,
    "blend_pos_y": position_y,
    "blend_pos_z": position_z,
    "blend_rot_x": rotation_x,
    "blend_rot_y": rotation_y,
    "blend_rot_z": rotation_z,
    "blend_dim_x": dimension_x,
    "blend_dim_y": dimension_y,
    "blend_dim_z": dimension_z
    }
    
    return json_object

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
    
    translate = f"""ZVector(({position_x} * meter).toDouble(), (-({position_z}) * meter - {dimension_y} * meter / 2).toDouble(), ({position_y} * meter).toDouble())"""
    world_translate = f"""Vec3(({position_x} * meter).toDouble(), ({position_y} * meter).toDouble(), (({position_z}) * meter + {dimension_y} * meter / 2 + 1).toDouble())"""
    
    dart_obj_snippet = f"""
    
    ZTransform {object_name}Transform = ZTransform(translate: {translate});
    AnimController {object_name}ControllerPerpendicularRotate = AnimController(vsync: vsync, duration: Duration.zero);
    Map<Controller, AnimController> {object_name}EnumControllerMap = {{Controller.perpendicularRotate: {object_name}ControllerPerpendicularRotate}};
    Map<AnimController, Animation> {object_name}ControllerAnimationMap = {{{object_name}ControllerPerpendicularRotate: null}};
    ramData['sceneFourChildren']['{object_name}'] = ObjectData(
        zTransform: {object_name}Transform,
        enumControllerMap: {object_name}EnumControllerMap,
        controllerAnimationMap: {object_name}ControllerAnimationMap);
    ObjectData {object_name}Link =(ramData['sceneFourChildren']['{object_name}'] as ObjectData);
    AnimatedBuilder {object_name} = AnimatedBuilder(
        animation: Listenable.merge([...{object_name}ControllerAnimationMap.keys]),
        builder: (context, child) {{
          return ZPositioned(
              translate: {object_name}Link.zTransform.translate,
              rotate: ZVector.only(y: ObjectData.objectRotateValueY),
              child: ZToBoxAdapter(
                  width: {dimension_z + 0.0} * meter,
                  height: {dimension_y + 0.0} * meter,
                  child: Offstage(
                      offstage: !{object_name}Link.viewport,
                      child: Image.asset(DiscoResStrings
                          .{object_name}HighRes))));
        }});
    staticObjects.add({object_name});"""
    return dart_obj_snippet

def create_dart_dynamic_object(object, parameters_existence):
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
    
    translate = f"""ZVector(({position_x} * meter).toDouble(), (-({position_z}) * meter - {dimension_y} * meter / 2).toDouble(), ({position_y} * meter).toDouble())"""
    dart_obj_snippet = f""" 
    var {object_name}KeyframesLink = ramData['objectsKeyframesJSON']['{object_name}'];
    {"Map<String, dynamic> {object_name}MapLocationX = {object_name}KeyframesLink['loc_x'];".format(object_name=object_name) if parameters_existence['loc_x'] else ''}
    {"Map<String, dynamic> {object_name}MapLocationY = {object_name}KeyframesLink['loc_y'];".format(object_name=object_name) if parameters_existence['loc_y'] else ''}
    {"Map<String, dynamic> {object_name}MapLocationZ = {object_name}KeyframesLink['loc_z'];".format(object_name=object_name) if parameters_existence['loc_z'] else ''}
    {"Map<String, dynamic> {object_name}MapViewport = {object_name}KeyframesLink['viewport'];".format(object_name=object_name) if parameters_existence['viewport'] else ''}
    {"var {object_name}LocationXKeysList = {object_name}MapLocationX.keys.toList();".format(object_name=object_name) if parameters_existence['loc_x'] else ''}
    {"var {object_name}LocationYKeysList = {object_name}MapLocationY.keys.toList();".format(object_name=object_name) if parameters_existence['loc_y'] else ''}
    {"var {object_name}LocationZKeysList = {object_name}MapLocationZ.keys.toList();".format(object_name=object_name) if parameters_existence['loc_z'] else ''}
    {"var {object_name}ViewportKeysList = {object_name}MapViewport.keys.toList();".format(object_name=object_name) if parameters_existence['viewport'] else ''}
    ZTransform {object_name}Transform = ZTransform(translate: {translate});
    AnimController {object_name}ControllerPerpendicularRotate = AnimController(vsync: vsync, duration: Duration.zero);
    {"AnimController {object_name}ControllerTranslateX = AnimController(vsync: vsync);".format(object_name=object_name) if parameters_existence['loc_x'] else ''}
    {"AnimController {object_name}ControllerTranslateY = AnimController(vsync: vsync);".format(object_name=object_name) if parameters_existence['loc_y'] else ''}
    {"AnimController {object_name}ControllerTranslateZ = AnimController(vsync: vsync);".format(object_name=object_name) if parameters_existence['loc_z'] else ''}
    {"AnimController {object_name}ControllerViewport = AnimController(vsync: vsync, duration: Duration.zero);".format(object_name=object_name) if parameters_existence['viewport'] else ''}
    Map<Controller, AnimController> {object_name}EnumControllerMap = {{
      Controller.perpendicularRotate:{object_name}ControllerPerpendicularRotate,
      {"Controller.translateX: {object_name}ControllerTranslateX,".format(object_name=object_name) if parameters_existence['loc_x'] else ''}
      {"Controller.translateX: {object_name}ControllerTranslateY,".format(object_name=object_name) if parameters_existence['loc_y'] else ''}
      {"Controller.translateX: {object_name}ControllerTranslateZ,".format(object_name=object_name) if parameters_existence['loc_z'] else ''}
      {"Controller.translateX: {object_name}ControllerViewport".format(object_name=object_name) if parameters_existence['viewport'] else ''}}};
    Map<AnimController, Animation> {object_name}ControllerAnimationMap = {{
      {object_name}ControllerPerpendicularRotate: null,
      {"{object_name}ControllerTranslateX: null,".format(object_name=object_name) if parameters_existence['loc_x'] else ''}
      {"{object_name}ControllerTranslateY: null,".format(object_name=object_name) if parameters_existence['loc_y'] else ''}
      {"{object_name}ControllerTranslateZ: null,".format(object_name=object_name) if parameters_existence['loc_z'] else ''}
      {"{object_name}ControllerViewport: null".format(object_name=object_name) if parameters_existence['viewport'] else ''}}};
    ramData['sceneFourChildren']['{object_name}'] = ObjectData(
        zTransform: {object_name}Transform,
        enumControllerMap: {object_name}EnumControllerMap,
        controllerAnimationMap: {object_name}ControllerAnimationMap);
    ObjectData {object_name}Link = (ramData['sceneFourChildren']['{object_name}'] as ObjectData);
    {"for (int {object_name}LocationXIndex = 0; {object_name}LocationXIndex < {object_name}LocationXKeysList.length - 1; {object_name}LocationXIndex++) {{"
      "ramData.customValue<SmartTimerListener>('objectTimer').add(int.parse({object_name}LocationXKeysList[{object_name}LocationXIndex]).millis(), () {{"
        "final Tween<double> {object_name}Tween = Tween("
            "begin: {object_name}MapLocationX[{object_name}LocationXKeysList[{object_name}LocationXIndex]],"
            "end: {object_name}MapLocationX[{object_name}LocationXKeysList[{object_name}LocationXIndex + 1]]);"
        "Animation {object_name}TweenAnimation ={object_name}Tween.animate({object_name}ControllerTranslateX);"
        "{object_name}Link.controllerAnimationMap[{object_name}ControllerTranslateX] = {object_name}TweenAnimation;"
        "{object_name}ControllerTranslateX.duration ="
            "int.parse({object_name}LocationXKeysList[{object_name}LocationXIndex + 1]).millis() -"
                "int.parse({object_name}LocationXKeysList[{object_name}LocationXIndex]).millis();"
        "runController({object_name}ControllerTranslateX);"
      "}});"
    "}}".format(object_name=object_name) if parameters_existence['loc_x'] else ''}
     {"for (int {object_name}LocationYIndex = 0;{object_name}LocationYIndex < {object_name}LocationYKeysList.length - 1; {object_name}LocationYIndex++) {{"
      "ramData.customValue<SmartTimerListener>('objectTimer').add(int.parse({object_name}LocationYKeysList[{object_name}LocationYIndex]).millis(), () {{"
        "final Tween<double> {object_name}Tween = Tween("
            "begin: {object_name}MapLocationY[{object_name}LocationYKeysList[{object_name}LocationYIndex]],"
            "end: {object_name}MapLocationY[{object_name}LocationYKeysList[{object_name}LocationYIndex + 1]]);"
        "Animation {object_name}TweenAnimation = {object_name}Tween.animate({object_name}ControllerTranslateY);"
        "{object_name}Link.controllerAnimationMap[{object_name}ControllerTranslateY] ={object_name}TweenAnimation;"
        "{object_name}ControllerTranslateY.duration ="
            "int.parse({object_name}LocationYKeysList[{object_name}LocationYIndex + 1]).millis() -"
                "int.parse({object_name}LocationYKeysList[{object_name}LocationYIndex]).millis();"
       "runController({object_name}ControllerTranslateY);"
      "}});"
    "}}".format(object_name=object_name) if parameters_existence['loc_y'] else ''}
    {"for (int {object_name}LocationZIndex = 0; {object_name}LocationZIndex < {object_name}LocationZKeysList.length - 1; {object_name}LocationZIndex++) {{"
      "ramData.customValue<SmartTimerListener>('objectTimer').add(int.parse({object_name}LocationZKeysList[{object_name}LocationZIndex]).millis(), () {{"
        "final Tween<double> {object_name}Tween = Tween("
            "begin: {object_name}MapLocationZ[{object_name}LocationZKeysList[{object_name}LocationZIndex]],"
            "end: {object_name}MapLocationZ[{object_name}LocationZKeysList[{object_name}LocationZIndex + 1]]);"
        "Animation {object_name}TweenAnimation = {object_name}Tween.animate({object_name}ControllerTranslateZ);"
        "{object_name}Link.controllerAnimationMap[{object_name}ControllerTranslateZ] = {object_name}TweenAnimation;"
        "{object_name}ControllerTranslateZ.duration = int.parse({object_name}LocationZKeysList[{object_name}LocationZIndex + 1]).millis() - int.parse({object_name}LocationZKeysList[{object_name}LocationZIndex]).millis();"
        "runController({object_name}ControllerTranslateZ);"
      "}});"
    "}}".format(object_name=object_name) if parameters_existence['loc_z'] else ''}
    {"for (int {object_name}ViewportIndex = 0; {object_name}ViewportIndex < {object_name}ViewportKeysList.length; {object_name}ViewportIndex++) {{"
      "ramData.customValue<SmartTimerListener>('objectTimer').add(int.parse({object_name}ViewportKeysList[{object_name}ViewportIndex]).millis(), () {{"
        "{object_name}Link.viewport = {object_name}MapViewport[{object_name}ViewportKeysList[{object_name}ViewportIndex]];"
        "runController({object_name}ControllerViewport);"
      "}});"
    "}}".format(object_name=object_name) if parameters_existence['viewport'] else ''}
    AnimatedBuilder {object_name} = AnimatedBuilder(
        animation: Listenable.merge([...{object_name}ControllerAnimationMap.keys]),
        builder: (context, child) {{
          {object_name}Link.zTransform.translate = {object_name}Link.zTransform.translate.copyWith(
                  x: {object_name}Link?.controllerAnimationMap[{object_name}ControllerTranslateX]?.value);
          {object_name}Link.zTransform.translate = {object_name}Link.zTransform.translate.copyWith(
                  y: {object_name}Link?.controllerAnimationMap[{object_name}ControllerTranslateY]?.value);
          {object_name}Link.zTransform.translate = {object_name}Link.zTransform.translate.copyWith(
                  z: {object_name}Link?.controllerAnimationMap[{object_name}ControllerTranslateZ]?.value);
          return ZPositioned(
              translate: {object_name}Link.zTransform.translate,
              rotate: ZVector.only(y: ObjectData.objectRotateValueY),
              child: ZToBoxAdapter(
                width: {dimension_z + 0.0} * meter,
                height: {dimension_y + 0.0} * meter,
                  child: Offstage(
                      offstage: !{object_name}Link.viewport,
                      child: Image.asset(DiscoResStrings
                          .{object_name}HighRes))));
        }});
    staticObjects.add({object_name});
    """ 
    return dart_obj_snippet

def create_dart_dynamic_object(object, parameters_existence):
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
    
#    print(parameters_existence)
    translate = f"""ZVector(({position_x} * meter).toDouble(), (-({position_z}) * meter - {dimension_y} * meter / 2).toDouble(), ({position_y} * meter).toDouble())"""
    dart_obj_snippet = f""" 
    var {object_name}KeyframesLink = ramData['objectsKeyframesJSON']['{object_name}'];
    {"Map<String, dynamic> {object_name}MapLocationX = {object_name}KeyframesLink['loc_x'];".format(object_name=object_name) if parameters_existence['loc_x'] else ''}
    {"Map<String, dynamic> {object_name}MapLocationY = {object_name}KeyframesLink['loc_y'];".format(object_name=object_name) if parameters_existence['loc_y'] else ''}
    {"Map<String, dynamic> {object_name}MapLocationZ = {object_name}KeyframesLink['loc_z'];".format(object_name=object_name) if parameters_existence['loc_z'] else ''}
    {"Map<String, dynamic> {object_name}MapViewport = {object_name}KeyframesLink['viewport'];".format(object_name=object_name) if parameters_existence['viewport'] else ''}
    {"var {object_name}LocationXKeysList = {object_name}MapLocationX.keys.toList();".format(object_name=object_name) if parameters_existence['loc_x'] else ''}
    {"var {object_name}LocationYKeysList = {object_name}MapLocationY.keys.toList();".format(object_name=object_name) if parameters_existence['loc_y'] else ''}
    {"var {object_name}LocationZKeysList = {object_name}MapLocationZ.keys.toList();".format(object_name=object_name) if parameters_existence['loc_z'] else ''}
    {"var {object_name}ViewportKeysList = {object_name}MapViewport.keys.toList();".format(object_name=object_name) if parameters_existence['viewport'] else ''}
    ZTransform {object_name}Transform = ZTransform(translate: {translate});
    AnimController {object_name}ControllerPerpendicularRotate = AnimController(vsync: vsync, duration: Duration.zero);
    {"AnimController {object_name}ControllerTranslateX = AnimController(vsync: vsync);".format(object_name=object_name) if parameters_existence['loc_x'] else ''}
    {"AnimController {object_name}ControllerTranslateY = AnimController(vsync: vsync);".format(object_name=object_name) if parameters_existence['loc_y'] else ''}
    {"AnimController {object_name}ControllerTranslateZ = AnimController(vsync: vsync);".format(object_name=object_name) if parameters_existence['loc_z'] else ''}
    {"AnimController {object_name}ControllerViewport = AnimController(vsync: vsync, duration: Duration.zero);".format(object_name=object_name) if parameters_existence['viewport'] else ''}
    Map<Controller, AnimController> {object_name}EnumControllerMap = {{
      Controller.perpendicularRotate:{object_name}ControllerPerpendicularRotate,
      {"Controller.translateX: {object_name}ControllerTranslateX,".format(object_name=object_name) if parameters_existence['loc_x'] else ''}
      {"Controller.translateX: {object_name}ControllerTranslateY,".format(object_name=object_name) if parameters_existence['loc_y'] else ''}
      {"Controller.translateX: {object_name}ControllerTranslateZ,".format(object_name=object_name) if parameters_existence['loc_z'] else ''}
      {"Controller.translateX: {object_name}ControllerViewport".format(object_name=object_name) if parameters_existence['viewport'] else ''}}};
    Map<AnimController, Animation> {object_name}ControllerAnimationMap = {{
      {object_name}ControllerPerpendicularRotate: null,
      {"{object_name}ControllerTranslateX: null,".format(object_name=object_name) if parameters_existence['loc_x'] else ''}
      {"{object_name}ControllerTranslateY: null,".format(object_name=object_name) if parameters_existence['loc_y'] else ''}
      {"{object_name}ControllerTranslateZ: null,".format(object_name=object_name) if parameters_existence['loc_z'] else ''}
      {"{object_name}ControllerViewport: null".format(object_name=object_name) if parameters_existence['viewport'] else ''}}};
    ramData['sceneFourChildren']['{object_name}'] = ObjectData(
        zTransform: {object_name}Transform,
        enumControllerMap: {object_name}EnumControllerMap,
        controllerAnimationMap: {object_name}ControllerAnimationMap);
    ObjectData {object_name}Link = (ramData['sceneFourChildren']['{object_name}'] as ObjectData);
    {"for (int {object_name}LocationXIndex = 0; {object_name}LocationXIndex < {object_name}LocationXKeysList.length - 1; {object_name}LocationXIndex++) {{"
      "ramData.customValue<SmartTimerListener>('objectTimer').add(int.parse({object_name}LocationXKeysList[{object_name}LocationXIndex]).millis(), () {{"
        "final Tween<double> {object_name}Tween = Tween("
            "begin: {object_name}MapLocationX[{object_name}LocationXKeysList[{object_name}LocationXIndex]],"
            "end: {object_name}MapLocationX[{object_name}LocationXKeysList[{object_name}LocationXIndex + 1]]);"
        "Animation {object_name}TweenAnimation ={object_name}Tween.animate({object_name}ControllerTranslateX);"
        "{object_name}Link.controllerAnimationMap[{object_name}ControllerTranslateX] = {object_name}TweenAnimation;"
        "{object_name}ControllerTranslateX.duration ="
            "int.parse({object_name}LocationXKeysList[{object_name}LocationXIndex + 1]).millis() -"
                "int.parse({object_name}LocationXKeysList[{object_name}LocationXIndex]).millis();"
        "runController({object_name}ControllerTranslateX);"
      "}});"
    "}}".format(object_name=object_name) if parameters_existence['loc_x'] else ''}
     {"for (int {object_name}LocationYIndex = 0;{object_name}LocationYIndex < {object_name}LocationYKeysList.length - 1; {object_name}LocationYIndex++) {{"
      "ramData.customValue<SmartTimerListener>('objectTimer').add(int.parse({object_name}LocationYKeysList[{object_name}LocationYIndex]).millis(), () {{"
        "final Tween<double> {object_name}Tween = Tween("
            "begin: {object_name}MapLocationY[{object_name}LocationYKeysList[{object_name}LocationYIndex]],"
            "end: {object_name}MapLocationY[{object_name}LocationYKeysList[{object_name}LocationYIndex + 1]]);"
        "Animation {object_name}TweenAnimation = {object_name}Tween.animate({object_name}ControllerTranslateY);"
        "{object_name}Link.controllerAnimationMap[{object_name}ControllerTranslateY] ={object_name}TweenAnimation;"
        "{object_name}ControllerTranslateY.duration ="
            "int.parse({object_name}LocationYKeysList[{object_name}LocationYIndex + 1]).millis() -"
                "int.parse({object_name}LocationYKeysList[{object_name}LocationYIndex]).millis();"
       "runController({object_name}ControllerTranslateY);"
      "}});"
    "}}".format(object_name=object_name) if parameters_existence['loc_y'] else ''}
    {"for (int {object_name}LocationZIndex = 0; {object_name}LocationZIndex < {object_name}LocationZKeysList.length - 1; {object_name}LocationZIndex++) {{"
      "ramData.customValue<SmartTimerListener>('objectTimer').add(int.parse({object_name}LocationZKeysList[{object_name}LocationZIndex]).millis(), () {{"
        "final Tween<double> {object_name}Tween = Tween("
            "begin: {object_name}MapLocationZ[{object_name}LocationZKeysList[{object_name}LocationZIndex]],"
            "end: {object_name}MapLocationZ[{object_name}LocationZKeysList[{object_name}LocationZIndex + 1]]);"
        "Animation {object_name}TweenAnimation = {object_name}Tween.animate({object_name}ControllerTranslateZ);"
        "{object_name}Link.controllerAnimationMap[{object_name}ControllerTranslateZ] = {object_name}TweenAnimation;"
        "{object_name}ControllerTranslateZ.duration = int.parse({object_name}LocationZKeysList[{object_name}LocationZIndex + 1]).millis() - int.parse({object_name}LocationZKeysList[{object_name}LocationZIndex]).millis();"
        "runController({object_name}ControllerTranslateZ);"
      "}});"
    "}}".format(object_name=object_name) if parameters_existence['loc_z'] else ''}
    {"for (int {object_name}ViewportIndex = 0; {object_name}ViewportIndex < {object_name}ViewportKeysList.length; {object_name}ViewportIndex++) {{"
      "ramData.customValue<SmartTimerListener>('objectTimer').add(int.parse({object_name}ViewportKeysList[{object_name}ViewportIndex]).millis(), () {{"
        "{object_name}Link.viewport = {object_name}MapViewport[{object_name}ViewportKeysList[{object_name}ViewportIndex]];"
        "runController({object_name}ControllerViewport);"
      "}});"
    "}}".format(object_name=object_name) if parameters_existence['viewport'] else ''}
    AnimatedBuilder {object_name} = AnimatedBuilder(
        animation: Listenable.merge([...{object_name}ControllerAnimationMap.keys]),
        builder: (context, child) {{
          {object_name}Link.zTransform.translate = {object_name}Link.zTransform.translate.copyWith(
                  x: {object_name}Link?.controllerAnimationMap[{object_name}ControllerTranslateX]?.value);
          {object_name}Link.zTransform.translate = {object_name}Link.zTransform.translate.copyWith(
                  y: {object_name}Link?.controllerAnimationMap[{object_name}ControllerTranslateY]?.value);
          {object_name}Link.zTransform.translate = {object_name}Link.zTransform.translate.copyWith(
                  z: {object_name}Link?.controllerAnimationMap[{object_name}ControllerTranslateZ]?.value);
          return ZPositioned(
              translate: {object_name}Link.zTransform.translate,
              rotate: ZVector.only(y: ObjectData.objectRotateValueY),
              child: ZToBoxAdapter(
                width: {dimension_z + 0.0} * meter,
                height: {dimension_y + 0.0} * meter,
                  child: Offstage(
                      offstage: !{object_name}Link.viewport,
                      child: Image.asset(DiscoResStrings
                          .{object_name}HighRes))));
        }});
    staticObjects.add({object_name});
    """
#    dart_obj_snippet = f"""
#        AnimController {object_name}AnimationController =
#        AnimController(vsync: vsync, duration: Duration(microseconds: 100));

#    AnimController {object_name}AnimationControllerTranslate =
#        AnimController(vsync: vsync, duration: Duration(microseconds: 100));

#    ZTransform {object_name}Transform = ZTransform(        
#    translate:
#           ZVector(-0 * meter, -1 * meter - 0.611 * meter / 2, 19.697 * meter),
#        rotate: ZVector((0.0), (0.0), (0.0)),
#        scale: ZVector((0.007), (0.007), (0.007)));

#    MultiTween<ZTransformMultiTween> {object_name}MultiTweenTranslate =
#        getTranslateMultiTween({object_name}Transform.translate,
#            {object_name}Transform.translate);

#    Animation<MultiTweenValues<ZTransformMultiTween>>
#        {object_name}MultiTweenAnimationTranslate =
#        {object_name}MultiTweenTranslate
#            .animate({object_name}AnimationControllerTranslate);

#    AnimController {object_name}AnimationControllerRotateAlways3D =
#        AnimController(vsync: vsync, duration: Duration(microseconds: 100));

#    AnimController {object_name}AnimationControllerVirtualRotate =
#        AnimController(vsync: vsync, duration: Duration(microseconds: 100));

#    MultiTween<ZTransformMultiTween> {object_name}MultiTweenVirtualRotate =
#    getRotateMultiTween({object_name}Transform.rotate,
#        {object_name}Transform.rotate);

#    Animation<MultiTweenValues<ZTransformMultiTween>>
#    {object_name}MultiTweenAnimationVirtualRotate =
#    {object_name}MultiTweenVirtualRotate
#        .animate({object_name}AnimationControllerVirtualRotate);

#    Map<AnimController, Animation<MultiTweenValues>>
#        {object_name}AnimationControllerMap = {{
#      {object_name}AnimationController: null,
#      {object_name}AnimationControllerTranslate:
#          {object_name}MultiTweenAnimationTranslate,
#      {object_name}AnimationControllerRotateAlways3D: null,
#      {object_name}AnimationControllerVirtualRotate: {object_name}MultiTweenAnimationVirtualRotate
#    }};

#    Map<Resolution, Uint8List> {object_name}Images = {{
#      Resolution.high: ramData[DiscoResStrings.objectbs01_028HighRes],
#      Resolution.medium: ramData[DiscoResStrings.objectbs01_028MedRes],
#      Resolution.low: ramData[DiscoResStrings.objectbs01_028LowRes]
#    }};

#    ramData['sceneFourChildren']['{object_name}'] = ObjectData(
#        animationControllerMap: {object_name}AnimationControllerMap,
#        animationController: {object_name}AnimationController,
#        animationControllerTranslate:
#            {object_name}AnimationControllerTranslate,
#        animationControllerRotateAlways3D:
#            {object_name}AnimationControllerRotateAlways3D,
#        animationControllerVirtualRotate:
#            {object_name}AnimationControllerVirtualRotate,
#        zTransform: {object_name}Transform,
#        rotateAccordingCamera: ZVector(0, 0, 0),
#        images: {object_name}Images,
#        currentResolution: Resolution.high,
#        variableName: '{object_name}',
#        isShowingUp: true);
#    

#     ObjectData {object_name}Link =
#        (ramData['sceneFourChildren']['{object_name}'] as ObjectData);

#    {object_name}KeyFramesData.forEach((key, value) {{
#      ramData.customValue<SmartTimerListener>('objectTimer').add(key, () {{

#        {object_name}Link.animationControllerTranslate.duration =
#            Duration.zero;
#        if ({object_name}KeyFramesData[key].zTransform != null) {{
#          final MultiTween<ZTransformMultiTween> {object_name}Tween =
#              getTranslateMultiTween({object_name}Link.zTransform.translate,
#                  value.zTransform.translate);

#          Animation<MultiTweenValues<ZTransformMultiTween>>
#              {object_name}MultiTweenAnimation = {object_name}Tween
#                  .animate({object_name}Link.animationControllerTranslate);

#          {object_name}Link.animationControllerMap[
#                  {object_name}AnimationControllerTranslate] =
#              {object_name}MultiTweenAnimation;

#          {object_name}Link.animationControllerTranslate.duration =
#              (value.nextFrameKey - key);
#        }}

#        {object_name}Link.isShowingUp = value.viewport;
#        {object_name}Link.animationController
#          ..reset()
#          ..forward();

#        if (!{object_name}Link.animationControllerTranslate.isAnimating) {{
#          {object_name}Link.animationControllerTranslate
#//            ..reset()
#            ..forward();
#        }}
#        //==================================================

#        {object_name}Link.animationControllerVirtualRotate.duration =
#            Duration.zero;
#        if ({object_name}KeyFramesData[key].zTransform != null) {{
#          final MultiTween<ZTransformMultiTween> {object_name}Tween =
#          getRotateMultiTween({object_name}Link.zTransform.rotate,
#              value.zTransform.rotate);

#          Animation<MultiTweenValues<ZTransformMultiTween>>
#          {object_name}MultiTweenAnimation = {object_name}Tween
#              .animate({object_name}Link.animationControllerVirtualRotate);

#          {object_name}Link.animationControllerMap[
#          {object_name}Link.animationControllerVirtualRotate] =
#              {object_name}MultiTweenAnimation;

#          {object_name}Link.animationControllerVirtualRotate.duration =
#          (value.nextFrameKey - key);
#        }}

#        if (!{object_name}Link.animationControllerVirtualRotate.isAnimating) {{
#          {object_name}Link.animationControllerVirtualRotate
#           // ..reset()
#            ..forward();
#        }}
#      }});
#    }});

#    AnimatedBuilder {object_name} = AnimatedBuilder(
#        animation:
#            Listenable.merge([...{object_name}AnimationControllerMap.keys]),
#        builder: (context, child) {{
#          String imageLink = DiscoResStrings.objectbs01_035CurrentIndexSprite;

#          int currentImageIndex = {object_name}Link.imageIndex;
#          var imageLinkIndexMask =
#              RegExp(r'Index([0-9]).').stringMatch(imageLink);
#          var replaced = 'Index$currentImageIndex.';
#          imageLink = imageLink.replaceAll(imageLinkIndexMask, replaced);

#          {object_name}Link.zTransform.translate = {object_name}Link
#              .animationControllerMap[
#                  {object_name}AnimationControllerTranslate]
#              .currentTranslate;
#          {object_name}Link.zTransform.rotate = {object_name}Link
#              .animationControllerMap[
#          {object_name}AnimationControllerVirtualRotate]
#              .currentRotate;

#          {object_name}Link.rotateAccordingCamera = {object_name}Link
#              ?.animationControllerMap[
#                  {object_name}AnimationControllerRotateAlways3D]
#              ?.currentRotate;
#              
#          {object_name}Link.rotateAccordingCamera ??= ZVector(0.0, 0.0, 0.0);
#            
#          return ZPositioned(
#              translate: {object_name}Link.zTransform.translate,
#              // rotate: ZVector(0, {object_name}Link.angleDifference, 0),
#              rotate: {object_name}Link.rotateAccordingCamera,
#              child: ZToBoxAdapter(
#                width: {dimension_z + 0.0} * meter,
#                height: {dimension_y + 0.0} * meter,
#                  child: AnimatedSwitcher(
#                      duration: Duration(milliseconds: 300),
#                      child: {object_name}Link.isShowingUp
#                          ? Image.memory(ramData[imageLink],
#                              key: ValueKey(currentImageIndex))
#                          : Container())));
#        }});
#    staticObjects.add({object_name});
#    """   
    return dart_obj_snippet
    
def get_img_by_obj(passed_obj_name):
    img = None
    for image in images:
        for obj in all_objs:
            if image.name == obj.data.name and obj.name == passed_obj_name:
                img = image
    if img == None:
        for image in images:
            for obj in bpy.context.scene.objects:
                for s in obj.material_slots:
                    if s.material and s.material.use_nodes:
                        for n in s.material.node_tree.nodes:
                            if n.type == 'TEX_IMAGE' and image.name == n.image.name:
                                if passed_obj_name == obj.name:
                                    img = image
    return img
                                                 
def get_res_class():
    each_res_str = ""

#    rendered_imgs_obj = open(path + "RenderedImgs.txt", 'r') 
#    rendered_imgs_obj = rendered_imgs_obj.readlines() 
    
#    for image_object_name in rendered_imgs_obj:
#        image_object_name = image_object_name.rstrip()
#        image_name = format_img_name(image_object_name)
#        img = get_img_by_obj(image_object_name)
#       
#        file_form = img.file_format.lower()
#        each_res_str += f"""\n static const String {image_name}Sprite = '${{assetsPrefix}}scene_four/disco/sprite/{image_name}.{file_form}';"""
        
    rendered_files = open(path + "RenderedObjs.txt", 'r') 
    file_lines = rendered_files.readlines() 
    for object_name in file_lines:
        object_name = object_name.rstrip()
        object_name = "object" + object_name.replace(".", "_").replace(" ", "_")
        each_res_str += f"""\n static const String {object_name}HighRes = '${{assetsPrefix}}scene_four/disco/sprite/{object_name}HighRes.png';"""
        each_res_str += f"""\n static const String {object_name}MedRes = '${{assetsPrefix}}scene_four/disco/sprite/{object_name}MedRes.png';"""
        each_res_str += f"""\n static const String {object_name}LowRes = '${{assetsPrefix}}scene_four/disco/sprite/{object_name}LowRes.png';"""

    for object_image_idex in range (0, 80):
        each_res_str += f"""\nstatic const String objectbs01_035Index{object_image_idex}Sprite = '${{assetsPrefix}}scene_four/disco/sprite/objectbs01_035Index{object_image_idex}.png';"""
      
    res_class_data  = f"""
class DiscoResStrings {{ {each_res_str}
    static const String objectbs01_035CurrentIndexSprite = '${{assetsPrefix}}scene_four/disco/sprite/objectbs01_035Index0.png';
}}"""
    return res_class_data

def get_res_load_method():
    each_load_str = ""
#    rendered_imgs_obj = open(path + "RenderedImgs.txt", 'r') 
#    rendered_imgs_obj = rendered_imgs_obj.readlines() 
#    for image_object_name in rendered_imgs_obj:
#        image_object_name = image_object_name.rstrip()
#        image_name = format_img_name(image_object_name)
#        each_load_str += f"""
#    await ramData.lUint8List(DiscoResStrings.{image_name}Sprite);"""
        
    rendered_files = open(path + "RenderedObjs.txt", 'r') 
    file_lines = rendered_files.readlines() 
    for object_name in file_lines: 
        object_name = object_name.rstrip()
        object_name = "object" + object_name.replace(".", "_").replace(" ", "_")
        each_load_str += f"""
    await ramData.lUint8List(DiscoResStrings.{object_name}HighRes);
    await ramData.lUint8List(DiscoResStrings.{object_name}MedRes);
    await ramData.lUint8List(DiscoResStrings.{object_name}LowRes);"""

    for object_image_idex in range (0, 80):
        each_load_str += f"""\nawait ramData.lUint8List(DiscoResStrings.objectbs01_035Index{object_image_idex}Sprite);"""
     
    res_load_method_data  = f"""
    loadDiscoRes() async {{ {each_load_str}
}}
"""
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
    s.render.filepath = ("{path}ClosestRotateRender/" 
    + "/" + object_name + "/" + "Fr" + str(s.frame_current).zfill(3)) + "Rot" +str(int(math.degrees(objRot)))
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
        else:
            print(bpy.data.objects[objIndex].name)
            bpy.data.objects[objIndex].hide_set(True)
            bpy.data.objects[objIndex].hide_render = True

def save_img_obj(object, image):
    try:
        image_name = format_img_name(object.name)
        image.alpha_mode = 'STRAIGHT'
        image.filepath_raw = f"""{path}ExportedImages/{image_name}.{image.file_format.lower()}"""
        image.save()
        appendToFile("RenderedImgs.txt", object.name)
    except:
        print("Image algorithm exception")
        
def render_each_obj():
    hideAllObjects()

#    if os.path.exists(path + "RenderedObjs.txt"):
 #       os.remove(path + "RenderedObjs.txt")
#    if os.path.exists(path + "NotRenderedObjs.txt"):
 #       os.remove(path + "NotRenderedObjs.txt")
 
#    for image in images:
#        for obj in all_objs:
#            if image.name == obj.data.name:
#                for object_name in not_rend_objs_lines:
#                    object_name = object_name.rstrip()
#                    if object_name == obj.name:
#                        save_img_obj(obj, image)
                               
#    for image in images:
#        for obj in bpy.context.scene.objects:
#            for s in obj.material_slots:
#                if s.material and s.material.use_nodes:
#                    for n in s.material.node_tree.nodes:
#                        if n.type == 'TEX_IMAGE' and image.name == n.image.name:
#                            for object_name in not_rend_objs_lines:
#                                object_name = object_name.rstrip()
#                                if object_name == obj.name:
#                                    save_img_obj(obj, n.image)

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
        else: 
            appendToFile("NotRenderedObjs.txt", object_name)
                     
    resetWorld()
    
def appendToFile(fileName, data):
    os.makedirs(path, exist_ok=True)
    with open(path + fileName, "a") as file:
        file.write(f"""{data}\n""")
        
def format_img_name(image_name):
    image_name = "image" + image_name.replace(".", "_").replace(" ", "_") .replace("_jpg", "").replace("_png", "").replace("_tga", "")
    return image_name

def format_obj_name(object_name):
    object_name = "object" + object_name.replace(".", "_").replace(" ", "_")
    return object_name

# First
#render_each_obj()

# Second
# PyCharm scripts

# Third
write_json_objs()
#map_to_dart()
