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

all_objs = bpy.data.objects
images = bpy.data.images
specified_objs = ["Plane", "celling", "podium"]

dynamic_objs_collection = bpy.data.collections['dynamicObjects']

specified_objs
def map_to_dart():
    image_ext = image_extension()
    res_class = get_res_class()
    res_load_method = get_res_load_method()
    specified_objs = get_specified_objs()
    objects_in_dart = each_obj_in_dart()
    dynamic_objs = dynamic_objs_in_dart()
    file_data = f"""import 'package:blank/utils/animation_controller.dart';
import 'package:flutter/material.dart' hide Material;
import 'package:sa_multi_tween/sa_multi_tween.dart';
import 'package:zflutter/zflutter.dart';
import '../../screen.dart';
import '../../utilities.dart';
import 'object_move_utils.dart';
import 'scene_four.dart' hide Image;
import 'package:flutter/material.dart' as i;
import 'dart:typed_data';
import 'dart:math';
import 'package:box3d/box3d.dart';
import 'dart:ui' as ui;
import 'package:blank/utils/atlas_dimension_widget.dart';

{image_ext}
{res_class}
extension {project_name} on Screen {{
    get{project_name}(AnimController controller) => {project_name}Location(controller);
    {res_load_method}
    Location {project_name}Location(AnimController controller) {{
    Map<String, ZTransform> rotateValues = {{}};
    List<ZPositioned> rotateObjects = [];
    List staticObjects = [];
    World world = (ramData['world'] as World);
    {specified_objs}
    {objects_in_dart}
    {dynamic_objs}
    
    CubeLocation cubeLocation1 = CubeLocation(rotateValues, ZGroup(
    children: [...rotateObjects, ...staticObjects]), ZVector(0, 0, 0),
    ZVector(0, 0, 0), 0);
    
    List<ZTransform> path = [];
    Location {project_name}Location = Location([cubeLocation1], path);
    return {project_name}Location;
    }}
}}"""
    
    blank_pr_path = "/home/fehty/StudioProjects/blank/lib/scenes/scene_four/"
    with open(blank_pr_path + "generated_test.dart", "w") as file:
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
            fit: fit,
            repeat: this.repeat) 
            : i.Image.memory(
            memory,
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
#    context = bpy.context
#    obj = bpy.data.objects["bs01.032"]
#    mesh = obj.data

#    for f in mesh.polygons:  # iterate over faces
#        print("face", f.index, "material_index", f.material_index)
#        slot = obj.material_slots[f.material_index]
#        mat = slot.material
#        if mat is not None:
#            print(mat.name)
##            print(mat.diffuse_color)
#        else:
#            print("No mat in slot", material_index)
    
    objects_in_dart = ""
    rendered_imgs_obj = open(path + "RenderedImgs.txt", 'r') 
    rendered_imgs_obj = rendered_imgs_obj.readlines()
    for image_object_name in rendered_imgs_obj:
        image_object_name = image_object_name.rstrip()
        object = bpy.data.objects[image_object_name]
        if object.type == "EMPTY":
            objects_in_dart += create_dart_image_object(object)
        else:
            objects_in_dart += create_dart_texture_object(object)
        
    rendered_files = open(path + "RenderedObjs.txt", 'r') 
    file_lines = rendered_files.readlines() 
    for object_name in file_lines:
        object_name = object_name.rstrip()
        object = bpy.data.objects[object_name]
        objects_in_dart += create_dart_object(object)
    return objects_in_dart

def dynamic_objs_in_dart():
    dynamic_objects_in_dart  = ""
    for obj in dynamic_objs_collection.all_objects:
        dynamic_objects_in_dart += create_dart_dynamic_object(obj)
    return dynamic_objects_in_dart
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
    
#    full_height = round(height * scale_y + 0.0, round_number_count)

    color = ""
    if object.name == "podium":
        color = "198, 201, 207, 1"
    elif object.name == "Plane":
        color = "58, 64, 67, 1"
    elif object.name == "celling":
        color = "94, 85, 73, 1"
    
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
                  child: AnimatedSwitcher(
                      key: UniqueKey(),
                      duration: Duration(milliseconds: 300),
                      child:
                          AtlasDimensionWidget(image: ramData[DISCOResStrings.{object_name}Sprite]))));
//                        Image.memory(ramData[DISCOResStrings.{object_name}Sprite]))));
        }});
    staticObjects.add({object_name});
"""
#    dart_obj_snippet = f"""
#    AnimController {object_name}AnimationController =
#        AnimController(vsync: vsync, duration: Duration(microseconds: 100));
#    
#    ZTransform {object_name}Transfrom = ZTransform(
#       translate: ZVector({position_x} * meter, -({position_z}) * meter, {position_y} * meter),
#       rotate: ZVector({rotation_x} + pi/2, {rotation_z}, {rotation_y}),
#       scale: ZVector(0.0, 0.0, 0.0));

#    MultiTween<ZTransformMultiTween> {object_name}MultiTween = getMultiTween(
#        {object_name}Transfrom, {object_name}Transfrom);
#    Animation<MultiTweenValues<
#        ZTransformMultiTween>> {object_name}MultiTweenAnimation = {object_name}MultiTween
#        .animate({object_name}AnimationController);
#    ramData['sceneFourChildren']['{object_name}'] = ObjectData(
#        animationController: {object_name}AnimationController,
#        multiTweenAnimation: {object_name}MultiTweenAnimation,
#        zTransform: {object_name}Transfrom);

#    ObjectData {object_name}Link = (ramData['sceneFourChildren']['{object_name}'] as ObjectData);

#    AnimatedBuilder {object_name} = AnimatedBuilder(
#        animation: {object_name}Link.animationController,
#        builder: (context, child) {{
#        ZVector {object_name}RotateVector = {object_name}Link.multiTweenAnimation.currentZTransform.rotate;
#          {object_name}Link.zTransform.rotate =
#            {object_name}RotateVector.copyWith(y: {object_name}Transfrom.rotate.y 
#                + {object_name}RotateVector.y);
#          return ZPositioned(
#              translate: {object_name}Link
#                  .zTransform.translate,
#              rotate: {object_name}Link.zTransform.rotate,
#              child: ZToBoxAdapter(
#                width: {width + 0.0} ,
#                height: {full_height},
#                  child: AnimatedSwitcher(
#                      key: UniqueKey(),
#                      duration: Duration(microseconds: 100),
#                      child:
#                        Image.memory(ramData[DISCOResStrings.{object_name}Sprite]))));
#        }});
#    staticObjects.add({object_name});
#"""
#"""

#    dart_obj_snippet = f"""
#    ZWidget {object_name} = ZPositioned(
#        translate: ZVector({position_x} * meter, -({position_z}) * meter, {position_y} * meter),
#//        rotate: ZVector({rotation_x} + pi/2, {rotation_z}, {rotation_y}),
#        child: ZToBoxAdapter(
#            width: {width + 0.0} ,
#            height: {full_height},
#            child: Image.asset(
#               DISCOResStrings.{object_name}Sprite)));
#    staticObjects.add({object_name});
#     """
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
               DISCOResStrings.{object_name}Sprite, fit: BoxFit.fill)));
    staticObjects.add({object_name});
     """
    return dart_obj_snippet

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

#    json_data = None
#    with open("/home/fehty/PycharmProjects/SpriteLauncher/spritesData.json", "r") as read_file:
#        json_data = json.load(read_file)
#       
#    high_res_data = json_data["spriteObjs"][object_name]["highResolution"]
#    high_res_size = high_res_data["tileSize"]
#    high_res_pos = high_res_data["tilesPosition"][0]
#    
#    med_res_data = json_data["spriteObjs"][object_name]["mediumResolution"]
#    med_res_size = med_res_data["tileSize"]
#    med_res_pos = med_res_data["tilesPosition"][0]
#    
#    low_res_data = json_data["spriteObjs"][object_name]["lowResolution"]
#    low_res_size = low_res_data["tileSize"]
#    low_res_pos = low_res_data["tilesPosition"][0]
    
#    viewports = get_viewports(object)
#    if(viewports == None):
#        viewports = ''
    
    translate = f"""ZVector(({position_x} * meter).toDouble(), (-({position_z}) * meter - {dimension_y} * meter / 2).toDouble(), ({position_y} * meter).toDouble())"""
    world_translate = f"""Vec3(({position_x} * meter).toDouble(), ({position_y} * meter).toDouble(), (({position_z}) * meter + {dimension_y} * meter / 2 + 1).toDouble())"""

    dart_obj_snippet = f""" 
    ZTransform {object_name}Transform = ZTransform(
          translate: {translate},
          rotate: ZVector((0.0), (0.0), (0.0)),
          scale: ZVector((0.007), (0.007), (0.007)));

      AnimController {object_name}AnimationControllerRotateAlways3D =
      AnimController(vsync: vsync, duration: Duration(microseconds: 100));
        
      Map<AnimController, Animation<MultiTweenValues>>
      {object_name}AnimationControllerMap = {{
        {object_name}AnimationControllerRotateAlways3D: null
      }};

      Map<Resolution, Uint8List> {object_name}Images = {{
        Resolution.high: ramData[DISCOResStrings.{object_name}HighRes],
        Resolution.medium: ramData[DISCOResStrings.{object_name}MedRes],
        Resolution.low: ramData[DISCOResStrings.{object_name}LowRes]
      }};

      ramData['sceneFourChildren']['{object_name}'] = ObjectData(
          animationControllerMap: {object_name}AnimationControllerMap,
          animationControllerRotateAlways3D:
          {object_name}AnimationControllerRotateAlways3D,
          zTransform: {object_name}Transform,
          rotateAccordingCamera: ZVector(0, 0, 0),
          images: {object_name}Images,
          currentResolution: Resolution.high,
          variableName: '{object_name}',
          isShowingUp: true);

      ObjectData {object_name}Link =
      (ramData['sceneFourChildren']['{object_name}'] as ObjectData);
    
    AnimatedBuilder {object_name} = AnimatedBuilder(
        animation: Listenable.merge([...{object_name}AnimationControllerMap.keys]),
        builder: (context, child) {{
          
          {object_name}Link.rotateAccordingCamera = {object_name}Link
              ?.animationControllerMap[
          {object_name}AnimationControllerRotateAlways3D]
              ?.currentRotate;

          {object_name}Link.rotateAccordingCamera ??= ZVector(0.0, 0.0, 0.0);
          
          return ZPositioned(
              translate: {object_name}Link.zTransform.translate,
              rotate: {object_name}Link.rotateAccordingCamera,
              child: ZToBoxAdapter(
                width: {dimension_z + 0.0} * meter,
                height: {dimension_y + 0.0} * meter,
                  child: AnimatedSwitcher(
                      duration: Duration(milliseconds: 300),
                      child: {object_name}Link.isShowingUp
                      ? AtlasDimensionWidget(image: ramData[DISCOResStrings.{object_name}UiImage] as ui.Image)
//                          ? Image.memory({object_name}Link.images[{object_name}Link.currentResolution],
 //                             key: ValueKey({object_name}Link.isShowingUp))
                          : Container())));
        }});
    staticObjects.add({object_name});"""
# dart_obj_snippet = f"""
#//  var {object_name}Shape = Box(Vec3(({dimension_x + 0.0} * meter / 2).toDouble(), ({dimension_z + 0.0} * meter / 2).toDouble(), ({dimension_y + 0.0} * meter / 2).toDouble()));
#//  var {object_name}Material = Material();
#//  Body {object_name}World = Body(BodyOptions(
#//      mass: 5.0,
#//      material: {object_name}Material,
#//     position: {world_translate}));
#//      {object_name}World.addShape({object_name}Shape);
#//  ramData['sceneFourChildrenWorld']['{object_name}'] = {object_name}World;
#//  world.addBody({object_name}World);
#    
#    AnimController {object_name}AnimationController =
#        AnimController(vsync: vsync, duration: Duration(microseconds: 100));

#    ZTransform {object_name}Transfrom = ZTransform(
#        translate: {translate},
#        rotate: ZVector(0.0, 0.0, 0.0),
#        scale: ZVector(0.0, 0.0, 0.0));

#    MultiTween<ZTransformMultiTween> {object_name}MultiTween = getMultiTween(
#        {object_name}Transfrom, {object_name}Transfrom);
#    Animation<MultiTweenValues<
#        ZTransformMultiTween>> {object_name}MultiTweenAnimation = {object_name}MultiTween
#        .animate({object_name}AnimationController);
#        
#    Map<Resolution, Uint8List> {object_name}Images = {{
#      Resolution.high: ramData[DISCOResStrings.{object_name}HighRes], 
#      Resolution.medium: ramData[DISCOResStrings.{object_name}MedRes],
#      Resolution.low: ramData[DISCOResStrings.{object_name}LowRes]
#    }};
#    
#    ramData['sceneFourChildren']['{object_name}'] = ObjectData(
#        animationController: {object_name}AnimationController,
#        multiTweenAnimation: {object_name}MultiTweenAnimation,
#        zTransform: {object_name}Transfrom,
#        images: {object_name}Images,
#        currentResolution: Resolution.high,
#        variableName: '{object_name}',
#        isShowingUp: true);

#    ObjectData {object_name}Link = (ramData['sceneFourChildren']['{object_name}'] as ObjectData);
#    
#    AnimatedBuilder {object_name} = AnimatedBuilder(
#        animation: {object_name}Link.animationController,
#        builder: (context, child) {{
#          {object_name}Link.zTransform.translate =
#            {object_name}Link.multiTweenAnimation.currentZTransform.translate;
#          {object_name}Link.zTransform.rotate =
#            {object_name}Link.multiTweenAnimation.currentZTransform.rotate;
#          return ZPositioned(
#              translate: {object_name}Link.zTransform.translate,
#              rotate: {object_name}Link.zTransform.rotate,
#              child: ZToBoxAdapter(
#                width: {dimension_z + 0.0} * meter,
#                height: {dimension_y + 0.0} * meter,
#                  child: {object_name}Link.isShowingUp?
#                  AnimatedSwitcher(
#                      duration: Duration(milliseconds: 300),
#                      child:
#                      Image.memory({object_name}Link.images[{object_name}Link.currentResolution])):
#                  Container()));
#        }});
#    staticObjects.add({object_name});
#"""
#    key: ValueKey({object_name}Link.valueKey),
#    Image.memory(ramData[DISCOResStrings.{object_name}Sprite]))));

#    dart_obj_snippet = f"""
#    AnimController {object_name}AnimationController =
#        AnimController(vsync: vsync, duration: Duration(microseconds: 100));

#    final MultiTween<ZTransformMultiTween> {object_name}Tween =
#        MultiTween<ZTransformMultiTween>();
#    {object_name}Tween
#      ..add(ZTransformMultiTween.translateX, (0.0).tweenTo(0.0));

#    ZTransform {object_name}Transfrom = ZTransform(
#           translate: ZVector({position_x} * meter, -({position_z}) * meter - {dimension_y} * meter / 2, {position_y} * meter),
#           rotate: ZVector(0.0, 0.0, 0.0));
#//           rotate: ZVector({rotation_x}, {rotation_z}, {rotation_y}));

#    ramData['sceneFourChildren']['{object_name}'] = ObjectData(
#        animController: {object_name}AnimationController,
#        multiTween: {object_name}Tween,
#        zTransform: {object_name}Transfrom);
#    ObjectData {object_name}_Data =
#        ramData['sceneFourChildren']['{object_name}'];
#        
#    AnimatedBuilder {object_name} = AnimatedBuilder(
#        animation: {object_name}AnimationController,
#        builder: (context, child) {{
#          return ZPositioned(
#              translate: {object_name}_Data.zTransform.translate,
#              rotate: {object_name}_Data.zTransform.rotate,
#              child: ZToBoxAdapter(
#                width: {dimension_z + 0.0} * meter,
#                height: {dimension_y + 0.0} * meter,
#                  child: AnimatedSwitcher(
#                      key: UniqueKey(),
#                      duration: Duration(microseconds: 100),
#                      child:
#                          Image.asset(DISCOResStrings.{object_name}Sprite))));
#        }});
#    staticObjects.add({object_name});
#"""

#    dart_obj_snippet = f"""
#    ZWidget {object_name} = ZPositioned(
#        translate: ZVector({position_x} * meter, -({position_z}) * meter - {dimension_y} * meter / 2, {position_y} * meter),
#//        rotate: ZVector({rotation_x}, {rotation_z}, {rotation_y}),
#        child: ZToBoxAdapter(
#            width: {dimension_z + 0.0} * meter,
#            height: {dimension_y + 0.0} * meter,
#            child: Image.asset(
#               DISCOResStrings.{object_name}Sprite)));
#    staticObjects.add({object_name});
#     """
     
#     """
##    dart_obj_snippet = f"""
#    ramData.customValue<Map<AtlasDimensions, Rect>>('{object_name}',
#        {{AtlasDimensions.high: Rect.fromLTWH({high_res_pos["left"]}, {high_res_pos["top"]}, {high_res_size["width"]}, {high_res_size["height"]}),
#         AtlasDimensions.medium: Rect.fromLTWH({med_res_pos["left"]}, {med_res_pos["top"]}, {med_res_size["width"]}, {med_res_size["height"]}),
#         AtlasDimensions.low: Rect.fromLTWH({low_res_pos["left"]}, {low_res_pos["top"]}, {low_res_size["width"]}, {low_res_size["height"]})}});
#    ZWidget {object_name} = ZPositioned(
#        translate: ZVector({position_x} * meter, -({position_z})  * meter - {med_res_size["height"]}, {position_y} * meter),
#//        rotate: ZVector({rotation_x}, {rotation_z}, {rotation_y}),
#        child: ZToBoxAdapter(
#            width: 0.0,
#            height: 0.0,
#            child: AtlasDimensionWidget(
#                image: ramData[DISCOResStrings.{object_name}Sprite],
#                rect: ramData.customValue('{object_name}')[AtlasDimensions.medium])));
#    staticObjects.add({object_name});
#    """
    return dart_obj_snippet

def get_viewport(num):
    isShowing = None
    if num == 1:
        isShowing = 'false'
    else:
        isShowing = 'true'
    return isShowing

def get_key_frame_data_class(action, frame_num, ctrl_points, object):
    dimension_y = round(object.dimensions[1], 3)
    loc_x = None
    loc_y = None
    loc_z = None
    rot_x = None
    rot_y = None
    rot_z = None
    scale_x = None
    scale_y = None
    scale_z = None
    viewport = None
    
    key_frame_data_class = ""
    
    z_transform = ""
    key_frame_data_class = ""
        
    for fcu in action.fcurves:
        for keyframe in fcu.keyframe_points:
            if (keyframe.co.x == ctrl_points[frame_num]):
                type = fcu.data_path
                ind = fcu.array_index
                point = keyframe.co.y
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
                elif(type == "hide_viewport"):
                    viewport = get_viewport(point)
#                print(keyframe.co.x) #coordinates x,y
    if ((loc_x and loc_y and loc_z and rot_x and rot_y and rot_z and scale_x and scale_y and scale_z) != None):
#        z_transform = f"ZTransform(translate: ZVector({loc_x} * meter, -({loc_z}) * meter - {dimension_y} * meter / 2, {loc_y} * meter), rotate: ZVector(({rot_x + 0.0} - pi / 2), ({rot_z + 0.0}), -({rot_y + 0.0})), scale: ZVector(({scale_x + 0.0}), ({scale_z + 0.0}), ({scale_y + 0.0})))"""
#        key_frame_data_class = f"KeyFrameData(viewport: {viewport}, zTransform: {z_transform})"
        key_frame_data_class = f"KeyFrameData(viewport: {viewport})"
        
        if frame_num + 1 != len(ctrl_points):
            for frame in range(frame_num + 1, len(ctrl_points)):
                obj_z_transform = object_z_transform(action, object, ctrl_points[frame])
                if obj_z_transform != "":
                    next_frame_key = ctrl_points[frame]
                    next_frame_key = f"""{int(next_frame_key * 33.3)}.millis()"""
                    key_frame_data_class = f"KeyFrameData(viewport: {viewport}, zTransform: {obj_z_transform}, nextFrameKey: {next_frame_key})"
                    break
    else:  
        key_frame_data_class = f"KeyFrameData(viewport: {viewport})"
    return key_frame_data_class

def key_frame_data(object):
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
    ctrl_points = sorted(ctrl_points)
    
#    print(object_action)
    viewport_data_objs_in_dart = ''
    for frame_index in range(0, len(ctrl_points)):
        key_frame_data_class = get_key_frame_data_class(object_action, frame_index, ctrl_points, object)
        frame = ctrl_points[frame_index]
        viewport_data_objs_in_dart += f"""\n     {int(frame * 33.3)}.millis(): {key_frame_data_class},"""
                        
    object_name = format_obj_name(object.name)
    whole_viewport_data_in_dart =  f"""final Map<Duration, KeyFrameData> {object_name}KeyFramesData = {{{viewport_data_objs_in_dart.rstrip(',')}
    }};
    """
    
    if(viewport_data_objs_in_dart == ''):
        whole_viewport_data_in_dart = None
    return whole_viewport_data_in_dart

def object_z_transform(action, object, frame):
    
    dimension_y = round(object.dimensions[1], 3)
    loc_x = None
    loc_y = None
    loc_z = None
    rot_x = None
    rot_y = None
    rot_z = None
    scale_x = None
    scale_y = None
    scale_z = None
    viewport = None
    
    key_frame_data_class = ""
    
    z_transform = ""
    key_frame_data_class = ""
        
    for fcu in action.fcurves:
        for keyframe in fcu.keyframe_points:
            print(keyframe.co.x)
            if (keyframe.co.x == frame):
                print(frame + 2)
                type = fcu.data_path
                ind = fcu.array_index
                point = keyframe.co.y
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
                    
    if ((loc_x and loc_y and loc_z and rot_x and rot_y and rot_z and scale_x and scale_y and scale_z) != None):               
        z_transform = f"ZTransform(translate: ZVector({loc_x} * meter, -({loc_z}) * meter - {dimension_y} * meter / 2, {loc_y} * meter), rotate: ZVector(({rot_x + 0.0} - pi / 2), ({rot_z + 0.0}), -({rot_y + 0.0})), scale: ZVector(({scale_x + 0.0}), ({scale_z + 0.0}), ({scale_y + 0.0})))"""
    return z_transform

def get_anim_z_transform(object, frame_num):
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
    ctrl_points = sorted(ctrl_points)
   
    anim_z_transform = object_z_transform(object_action, object, ctrl_points[frame_num])
    
#    print(anim_z_transform)
    return anim_z_transform

def get_first_anim_viewport(object):
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
    ctrl_points = sorted(ctrl_points)
    first_anim_viewport = object_first_viewport(object_action)
    
    return first_anim_viewport
    
def object_first_viewport(action):
    viewport = ""
    for fcu in action.fcurves:
        type = fcu.data_path
        ind = fcu.array_index
        point = None
        point = fcu.keyframe_points[0].co.y
        point = round(point, 3)
        if(type == "hide_viewport"):
            viewport = get_viewport(point)
        
    return viewport

def create_dart_dynamic_object(object):
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
    
    first_key_frame_viewport = get_first_anim_viewport(object)
    first_key_frame_z_transform = get_anim_z_transform(object, 0)
    frame_data = key_frame_data(object)
#    anim_launching = get_anim_launching_for_dynamic_objs(object_name)
    
    dart_obj_snippet = f"""
        AnimController {object_name}AnimationController =
        AnimController(vsync: vsync, duration: Duration(microseconds: 100));

    AnimController {object_name}AnimationControllerTranslate =
        AnimController(vsync: vsync, duration: Duration(microseconds: 100));

//    ZTransform {object_name}Transform = ZTransform(
//        translate:
//            ZVector(-0 * meter, -1 * meter - 0.611 * meter / 2, 19.697 * meter),
//        rotate: ZVector((0.0), (0.0), (0.0)),
//        scale: ZVector((0.007), (0.007), (0.007)));

    ZTransform {object_name}Transform = {first_key_frame_z_transform};

    MultiTween<ZTransformMultiTween> {object_name}MultiTweenTranslate =
        getTranslateMultiTween({object_name}Transform.translate,
            {object_name}Transform.translate);

    Animation<MultiTweenValues<ZTransformMultiTween>>
        {object_name}MultiTweenAnimationTranslate =
        {object_name}MultiTweenTranslate
            .animate({object_name}AnimationControllerTranslate);

    AnimController {object_name}AnimationControllerRotateAlways3D =
        AnimController(vsync: vsync, duration: Duration(microseconds: 100));

    AnimController {object_name}AnimationControllerVirtualRotate =
        AnimController(vsync: vsync, duration: Duration(microseconds: 100));

    MultiTween<ZTransformMultiTween> {object_name}MultiTweenVirtualRotate =
    getRotateMultiTween({object_name}Transform.rotate,
        {object_name}Transform.rotate);

    Animation<MultiTweenValues<ZTransformMultiTween>>
    {object_name}MultiTweenAnimationVirtualRotate =
    {object_name}MultiTweenVirtualRotate
        .animate({object_name}AnimationControllerVirtualRotate);

    Map<AnimController, Animation<MultiTweenValues>>
        {object_name}AnimationControllerMap = {{
      {object_name}AnimationController: null,
      {object_name}AnimationControllerTranslate:
          {object_name}MultiTweenAnimationTranslate,
      {object_name}AnimationControllerRotateAlways3D: null,
      {object_name}AnimationControllerVirtualRotate: {object_name}MultiTweenAnimationVirtualRotate
    }};

    Map<Resolution, Uint8List> {object_name}Images = {{
      Resolution.high: ramData[DISCOResStrings.objectbs01_028HighRes],
      Resolution.medium: ramData[DISCOResStrings.objectbs01_028MedRes],
      Resolution.low: ramData[DISCOResStrings.objectbs01_028LowRes]
    }};

    ramData['sceneFourChildren']['{object_name}'] = ObjectData(
        animationControllerMap: {object_name}AnimationControllerMap,
        animationController: {object_name}AnimationController,
        animationControllerTranslate:
            {object_name}AnimationControllerTranslate,
        animationControllerRotateAlways3D:
            {object_name}AnimationControllerRotateAlways3D,
        animationControllerVirtualRotate:
            {object_name}AnimationControllerVirtualRotate,
        zTransform: {object_name}Transform,
        rotateAccordingCamera: ZVector(0, 0, 0),
        images: {object_name}Images,
        currentResolution: Resolution.high,
        variableName: '{object_name}',
        isShowingUp: true);
    
    {frame_data}
     ObjectData {object_name}Link =
        (ramData['sceneFourChildren']['{object_name}'] as ObjectData);

//    final Map<Duration, KeyFrameData> {object_name}KeyFramesData = {{
//      599.millis(): KeyFrameData(
//          viewport: true,
//          zTransform: ZTransform(
//              translate: ZVector(
//                  -1 * meter, -(1) * meter - 0.611 * meter / 2, 19.697 * meter),
//              rotate: ZVector(0, pi, 0.0),
//              scale: ZVector((0.007), (0.007), (0.007))),
//          nextFrameKey: 6000.millis()),
//      1000.millis(): KeyFrameData(viewport: true)
//    }};

    {object_name}KeyFramesData.forEach((key, value) {{
      ramData.customValue<SmartTimerListener>('objectTimer').add(key, () {{

        {object_name}Link.animationControllerTranslate.duration =
            Duration.zero;
        if ({object_name}KeyFramesData[key].zTransform != null) {{
          final MultiTween<ZTransformMultiTween> {object_name}Tween =
              getTranslateMultiTween({object_name}Link.zTransform.translate,
                  value.zTransform.translate);

          Animation<MultiTweenValues<ZTransformMultiTween>>
              {object_name}MultiTweenAnimation = {object_name}Tween
                  .animate({object_name}Link.animationControllerTranslate);

          {object_name}Link.animationControllerMap[
                  {object_name}AnimationControllerTranslate] =
              {object_name}MultiTweenAnimation;

          {object_name}Link.animationControllerTranslate.duration =
              (value.nextFrameKey - key);
        }}

        {object_name}Link.isShowingUp = value.viewport;
        {object_name}Link.animationController
          ..reset()
          ..forward();

        if (!{object_name}Link.animationControllerTranslate.isAnimating) {{
          {object_name}Link.animationControllerTranslate
//            ..reset()
            ..forward();
        }}
        //==================================================

        {object_name}Link.animationControllerVirtualRotate.duration =
            Duration.zero;
        if ({object_name}KeyFramesData[key].zTransform != null) {{
          final MultiTween<ZTransformMultiTween> {object_name}Tween =
          getRotateMultiTween({object_name}Link.zTransform.rotate,
              value.zTransform.rotate);

          Animation<MultiTweenValues<ZTransformMultiTween>>
          {object_name}MultiTweenAnimation = {object_name}Tween
              .animate({object_name}Link.animationControllerVirtualRotate);

          {object_name}Link.animationControllerMap[
          {object_name}Link.animationControllerVirtualRotate] =
              {object_name}MultiTweenAnimation;

          {object_name}Link.animationControllerVirtualRotate.duration =
          (value.nextFrameKey - key);
        }}

        if (!{object_name}Link.animationControllerVirtualRotate.isAnimating) {{
          {object_name}Link.animationControllerVirtualRotate
           // ..reset()
            ..forward();
        }}
      }});
    }});

    AnimatedBuilder {object_name} = AnimatedBuilder(
        animation:
            Listenable.merge([...{object_name}AnimationControllerMap.keys]),
        builder: (context, child) {{
          String imageLink = DISCOResStrings.objectbs01_035CurrentIndexSprite;

          int currentImageIndex = {object_name}Link.imageIndex;
          var imageLinkIndexMask =
              RegExp(r'Index([0-9]).').stringMatch(imageLink);
          var replaced = 'Index$currentImageIndex.';
          imageLink = imageLink.replaceAll(imageLinkIndexMask, replaced);

          {object_name}Link.zTransform.translate = {object_name}Link
              .animationControllerMap[
                  {object_name}AnimationControllerTranslate]
              .currentTranslate;
          {object_name}Link.zTransform.rotate = {object_name}Link
              .animationControllerMap[
          {object_name}AnimationControllerVirtualRotate]
              .currentRotate;

          {object_name}Link.rotateAccordingCamera = {object_name}Link
              ?.animationControllerMap[
                  {object_name}AnimationControllerRotateAlways3D]
              ?.currentRotate;
              
          {object_name}Link.rotateAccordingCamera ??= ZVector(0.0, 0.0, 0.0);
            
          return ZPositioned(
              translate: {object_name}Link.zTransform.translate,
              // rotate: ZVector(0, {object_name}Link.angleDifference, 0),
              rotate: {object_name}Link.rotateAccordingCamera,
              child: ZToBoxAdapter(
                width: {dimension_z + 0.0} * meter,
                height: {dimension_y + 0.0} * meter,
                  child: AnimatedSwitcher(
                      duration: Duration(milliseconds: 300),
                      child: {object_name}Link.isShowingUp
                          ? Image.memory(ramData[imageLink],
                              key: ValueKey(currentImageIndex))
                          : Container())));
        }});
    staticObjects.add({object_name});
    """   
#    dart_obj_snippet = f"""
#    AnimController {object_name}AnimationController =
#        AnimController(vsync: vsync, duration: Duration(microseconds: 100));

#//    ZTransform {object_name}Transfrom = ZTransform(
#//        translate: ZVector({position_x} * meter, -({position_z}) * meter - {dimension_y} * meter / 2, {position_y} * meter),
#//        rotate: ZVector(0.0, 0.0, 0.0),
#//        scale: ZVector(0.0, 0.0, 0.0));
#    ZTransform {object_name}Transfrom = {first_key_frame_z_transform};
#    
#    MultiTween<ZTransformMultiTween> {object_name}MultiTween = getMultiTween(
#        {object_name}Transfrom, {object_name}Transfrom);
#    Animation<MultiTweenValues<
#        ZTransformMultiTween>> {object_name}MultiTweenAnimation = {object_name}MultiTween
#        .animate({object_name}AnimationController);
#        
#//    Map<Resolution, Uint8List> {object_name}Images = {{
#//      Resolution.high: ramData[DISCOResStrings.{object_name}HighRes], 
#//      Resolution.medium: ramData[DISCOResStrings.{object_name}MedRes],
#//      Resolution.low: ramData[DISCOResStrings.{object_name}LowRes]
#//    }};

#    Map<Resolution, Uint8List> {object_name}Images = {{
#      Resolution.high: ramData[DISCOResStrings.objectbs01_028HighRes], 
#      Resolution.medium: ramData[DISCOResStrings.objectbs01_028MedRes],
#      Resolution.low: ramData[DISCOResStrings.objectbs01_028LowRes]
#    }};
#    
#    ramData['sceneFourChildren']['{object_name}'] = ObjectData(
#        animationController: {object_name}AnimationController,
#        multiTweenAnimation: {object_name}MultiTweenAnimation,
#        zTransform: {object_name}Transfrom,
#        images: {object_name}Images,
#        currentResolution: Resolution.high,
#        variableName: '{object_name}',
#        isShowingUp: {first_key_frame_viewport});

#    ObjectData {object_name}Link = (ramData['sceneFourChildren']['{object_name}'] as ObjectData);
#    {frame_data}
#    {anim_launching}
#    AnimatedBuilder {object_name} = AnimatedBuilder(
#        animation: {object_name}Link.animationController,
#        builder: (context, child) {{
#          {object_name}Link.zTransform.translate =
#            {object_name}Link.multiTweenAnimation.currentZTransform.translate;
#          {object_name}Link.zTransform.rotate =
#            {object_name}Link.multiTweenAnimation.currentZTransform.rotate;
#          return ZPositioned(
#              translate: {object_name}Link.zTransform.translate,
#              rotate: {object_name}Link.zTransform.rotate,
#              child: ZToBoxAdapter(
#                width: {dimension_z + 0.0} * meter,
#                height: {dimension_y + 0.0} * meter,
#                  child: {object_name}Link.isShowingUp?
#                  AnimatedSwitcher(
#                      duration: Duration(milliseconds: 300),
#                      child:
#                      Image.memory({object_name}Link.images[{object_name}Link.currentResolution])):
#                  Container()));
#        }});
#    staticObjects.add({object_name});
#"""
    return dart_obj_snippet

def get_anim_launching_for_dynamic_objs(obj_name):
    output = f"""{obj_name}KeyFramesData.forEach((key, value) {{
      ramData.customValue<SmartTimerListener>('objectTimer').add(key, () {{

        AnimationController {obj_name}AnimationControllerLink =
            {obj_name}Link.animationController;

        {obj_name}AnimationControllerLink.duration = Duration.zero;
        if ({obj_name}KeyFramesData[key].zTransform != null) {{
          final MultiTween<ZTransformMultiTween> {obj_name}Tween =
              getMultiTween({obj_name}Link.zTransform,
                  value.zTransform);

          Animation<MultiTweenValues<ZTransformMultiTween>>
          {obj_name}MultiTweenAnimation =
              {obj_name}Tween.animate({obj_name}AnimationControllerLink);

          {object_name}Link.multiTweenAnimation = {obj_name}MultiTweenAnimation;

          {object_name}AnimationControllerLink.duration = (value.nextFrameKey - key);
        }}

        {obj_name}Link.isShowingUp = value.viewport;
        if (!{obj_name}AnimationControllerLink.isAnimating) {{
          {obj_name}AnimationControllerLink
//            ..reset()
            ..forward();
        }}
      }});
    }});
    """
    return output

def get_viewports(object):
    viewport_data_objs_in_dart = ''
    
    for action in bpy.data.actions:
        for channel in action.fcurves: 
            if channel.data_path == 'hide_viewport':
                animation_obj_name = action.name.rstrip('Action')
                if animation_obj_name == object.name:
                    print(animation_obj_name)
                    for key in channel.keyframe_points:       
                        if key.select_control_point:
                            key_data = key.co
                            show = None
                            if key_data.y == 1:
                                show = 'false'
                            else:
                                show = 'true' 
                            viewport_data_objs_in_dart += f"""\n     {int(key_data.x * 33.3)}.millis(): {show},"""
    
    object_name = format_obj_name(object.name)
    whole_viewport_data_in_dart =  f"""final Map<Duration, bool> {object_name}Viewports = {{{viewport_data_objs_in_dart.rstrip(',')}
    }};
    
    {object_name}Viewports.forEach((key, value) {{
      ramData.customValue<SmartTimerListener>('objectTimer').add(key,
          () {{
            {object_name}Link.isShowingUp = value;
            if (!{object_name}Link.animationController.isAnimating) {{
                {object_name}Link.animationController
                    ..duration = Duration.zero
                    ..forward();
            }}  
      }});
    }});
    """
    
    if(viewport_data_objs_in_dart == ''):
        whole_viewport_data_in_dart = None
    return whole_viewport_data_in_dart;
    
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

    rendered_imgs_obj = open(path + "RenderedImgs.txt", 'r') 
    rendered_imgs_obj = rendered_imgs_obj.readlines() 
    
    for image_object_name in rendered_imgs_obj:
        image_object_name = image_object_name.rstrip()
        image_name = format_img_name(image_object_name)
        img = get_img_by_obj(image_object_name)
       
        file_form = img.file_format.lower()
        each_res_str += f"""\n static const String {image_name}Sprite = '${{assetsPrefix}}scene_four/{project_name}/sprite/{image_name}.{file_form}';"""
        
    rendered_files = open(path + "RenderedObjs.txt", 'r') 
    file_lines = rendered_files.readlines() 
    for object_name in file_lines:
        object_name = object_name.rstrip()
        object_name = "object" + object_name.replace(".", "_").replace(" ", "_")
        each_res_str += f"""\n static const String {object_name}UiImage = '${{assetsPrefix}}scene_four/{project_name}/sprite/{object_name}LowRes.png';"""
        each_res_str += f"""\n static const String {object_name}HighRes = '${{assetsPrefix}}scene_four/{project_name}/sprite/{object_name}MedRes.png';"""
        each_res_str += f"""\n static const String {object_name}MedRes = '${{assetsPrefix}}scene_four/{project_name}/sprite/{object_name}MedRes.png';"""
        each_res_str += f"""\n static const String {object_name}LowRes = '${{assetsPrefix}}scene_four/{project_name}/sprite/{object_name}MedRes.png';"""
    

    for object_image_idex in range (0, 80):
        each_res_str += f"""\nstatic const String objectbs01_035Index{object_image_idex}Sprite = '${{assetsPrefix}}scene_four/DISCO/sprite/objectbs01_035Index{object_image_idex}.png';"""
      
    res_class_data  = f"""
class {project_name}ResStrings {{ {each_res_str}
    static const String objectbs01_035CurrentIndexSprite = '${{assetsPrefix}}scene_four/DISCO/sprite/objectbs01_035Index0.png';
}}"""
    return res_class_data

def get_res_load_method():
    each_load_str = ""
    rendered_imgs_obj = open(path + "RenderedImgs.txt", 'r') 
    rendered_imgs_obj = rendered_imgs_obj.readlines() 
    for image_object_name in rendered_imgs_obj:
        image_object_name = image_object_name.rstrip()
        image_name = format_img_name(image_object_name)
        each_load_str += f"""
        await ramData.lUiImage({project_name}ResStrings.{image_name}Sprite);"""
#        each_load_str += f"""
#    await ramData.lUint8List({project_name}ResStrings.{image_name}Sprite);"""
        
    rendered_files = open(path + "RenderedObjs.txt", 'r') 
    file_lines = rendered_files.readlines() 
    for object_name in file_lines: 
        object_name = object_name.rstrip()
        object_name = "object" + object_name.replace(".", "_").replace(" ", "_")
        each_load_str += f"""
    await ramData.lUiImage({project_name}ResStrings.{object_name}UiImage);
    await ramData.lUint8List({project_name}ResStrings.{object_name}MedRes);
    await ramData.lUint8List({project_name}ResStrings.{object_name}MedRes);
    await ramData.lUint8List({project_name}ResStrings.{object_name}LowRes);"""

    for object_image_idex in range (0, 80):
        each_load_str += f"""\nawait ramData.lUint8List(DISCOResStrings.objectbs01_035Index{object_image_idex}Sprite);"""
     
    res_load_method_data  = f"""
    load{project_name}Res() async {{ {each_load_str}
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
#        elif bpy.data.objects[objIndex].name == "13494_Folding_Chairs_v1_L3.001":
#            bpy.data.objects[objIndex].hide_set(False)
#            bpy.data.objects[objIndex].hide_render = False    
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
 
    for image in images:
        for obj in all_objs:
            if image.name == obj.data.name:
                for object_name in not_rend_objs_lines:
                    object_name = object_name.rstrip()
                    if object_name == obj.name:
                        save_img_obj(obj, image)
                               
    for image in images:
        for obj in bpy.context.scene.objects:
            for s in obj.material_slots:
                if s.material and s.material.use_nodes:
                    for n in s.material.node_tree.nodes:
                        if n.type == 'TEX_IMAGE' and image.name == n.image.name:
                            for object_name in not_rend_objs_lines:
                                object_name = object_name.rstrip()
                                if object_name == obj.name:
                                    save_img_obj(obj, n.image)

                        
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
def format_img_name(image_name):
#    .replace("_jpg", ".jpg").replace("_png", ".png").replace("_tga", ".tga")
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
map_to_dart()

