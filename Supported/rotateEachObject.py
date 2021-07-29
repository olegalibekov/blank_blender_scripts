import bpy
import math

#https://blender.stackexchange.com/questions/78359/set-active-object-with-python

def renderEachFrame(objNumber):
    s=bpy.context.scene

    s.render.resolution_x = 512
    s.render.resolution_y = 512
    
	# range of frames
    for i in range(s.frame_start,10):
        s.frame_current = i
    
        bpy.data.objects[objNumber].rotation_euler.z += math.radians(1)
    
        s.render.filepath = ("/home/fehty/BlenderRes/BlenderRender/" 
        + "/" + "Obj" + str(objNumber) + "/" + "Frame" 
        + str(s.frame_current).zfill(3))
        
        bpy.ops.render.render(False,animation=False,write_still=True)
        
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
    renderEachFrame(currentObj)
    
resetWorld()
