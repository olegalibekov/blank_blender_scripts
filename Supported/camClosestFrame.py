import bpy
from bpy_extras.object_utils import world_to_camera_view

def renderClosestFrame(objNumber):
    s=bpy.context.scene

    s.render.resolution_x = 512
    s.render.resolution_y = 512

    smallestValuesFromEachFrame={}
    cam = bpy.data.objects["Camera"]
    
    for i in range(s.frame_start,160):
        s.frame_current = i
        s.frame_set(i)
        
        obj = bpy.data.objects[objNumber]
        
        if(cam and obj and obj.type == 'MESH' and 
        eachVertIsInView(objNumber, s, cam, obj)==True):
            smallestValuesFromEachFrame[i] = (min(getCamToObjDist(objNumber, s, cam)))
    
    closestToObjectFrame = min(smallestValuesFromEachFrame, key=smallestValuesFromEachFrame.get)
    s.frame_set(closestToObjectFrame)
    
    s.render.filepath = ("/home/fehty/BlenderRes/BlenderClosestFrameRender/" 
    + "/" + "Obj" + str(objNumber) + "/" + "Frame" 
    + str(s.frame_current).zfill(3))
        
    bpy.ops.render.render(False,animation=False,write_still=True)

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
        
objLength = 1

for objIndex in range(0, allObjects):
#    bpy.data.objects[objIndex].hide_set(True)
    bpy.data.objects[objIndex].hide_render = True

for currentObj in range(0, objLength):
    bpy.data.objects[currentObj].hide_render = False
#    bpy.data.objects[currentObj - 1].hide_set(False)
    if(currentObj != 0):
#        bpy.data.objects[currentObj - 1].hide_set(True)
        bpy.data.objects[currentObj - 1].hide_render = True
    renderClosestFrame(currentObj)
    
resetWorld()
