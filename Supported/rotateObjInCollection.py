import bpy
import math

#https://blender.stackexchange.com/questions/78359/set-active-object-with-python
objectsInCollection = bpy.data.collections['roundTables'].all_objects

def renderEachFrame(objNumber):
    s=bpy.context.scene

    obj = objectsInCollection[currentObj]
    s.render.resolution_x = 512
    s.render.resolution_y = 512
    
	# range of frames
    for i in range(s.frame_start,10):
        s.frame_current = i
    
        obj.rotation_euler.z += math.radians(30)
    
        s.render.filepath = ("/home/fehty/BlenderRes/BlenderObjectInCollectionRender/" 
        + "/" + "Obj" + str(objNumber) + "/" + "Frame" 
        + str(s.frame_current).zfill(3))
        
        bpy.ops.render.render(False,animation=False,write_still=True)
        
allObjects = len(bpy.data.objects)

def resetWorld():
    for objIndex in range(0, allObjects):
        bpy.data.objects[objIndex].hide_set(False)
        bpy.data.objects[objIndex].hide_render = False
        
for objIndex in range(0, allObjects):
    bpy.data.objects[objIndex].hide_render = True


for currentObj in range(0, len(objectsInCollection)):
    objectsInCollection[currentObj].hide_render = False
    if(currentObj != 0):
        objectsInCollection[currentObj - 1].hide_render = True
    renderEachFrame(currentObj)
    
resetWorld()

