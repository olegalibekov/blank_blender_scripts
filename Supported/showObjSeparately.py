import bpy

for objToShowIndex in range(0, len(bpy.data.objects)):
    for objIndex in range(0, len(bpy.data.objects)):
        if(objToShowIndex==objIndex):
            bpy.data.objects[objIndex].hide_set(False)
        else:
             bpy.data.objects[objIndex].hide_set(True)
            

