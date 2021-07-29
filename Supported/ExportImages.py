import bpy

path = "/home/fehty/BlenderCompilation/BlenderRes/"
 

#def get_img_by_obj(passed_obj):
#    for obj in bpy.context.scene.objects: 
#        for s in obj.material_slots: 
#            if s.material and s.material.use_nodes:
#                for n in s.material.node_tree.nodes: 
#                    if n.type == 'TEX_IMAGE' and passed_obj == obj: 
#                        try:
#                            
##                            print(obj)
##                            print(n.image.name)
#                            img = n.image
#                            img.filepath_raw = f"""/home/fehty/BlenderCompilation/BlenderRes/ExportedImages/{img.name}.jpg"""
#                            img.save()
#                        except:
#                            print("1")
                
def get_img_by_obj(obj):
    for s in obj.material_slots:
        if s.material and s.material.use_nodes:
            for n in s.material.node_tree.nodes:
                if n.type == 'TEX_IMAGE':
                    print(n.image)
                    return n.image
#                        texture_list += [n.image]
#                       print(obj.name,'uses',n.image.name,'saved at',n.image.filepath)
#    print(texture_list)
        
rendered_files = open(path + "NotRenderedObjs.txt", 'r') 
file_lines = rendered_files.readlines() 
for object_name in file_lines:
    object_name = object_name.rstrip()
    obj = bpy.data.objects[object_name]
    img = get_img_by_obj(obj)
    try:
        object_name = "object" + obj.name.replace(".", "_").replace(" ", "_")
        img.alpha_mode = 'STRAIGHT'
        img.file_format = 'PNG'
        img.filepath_raw = f"""/home/fehty/BlenderCompilation/BlenderRes/ExportedImages/{object_name}.jpg"""
        img.save()
    except:
        print("")
