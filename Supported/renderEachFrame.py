import bpy

s=bpy.context.scene

s.render.resolution_x = 512
s.render.resolution_y = 512

# range of frames
for i in range(s.frame_start,s.frame_end):
    s.frame_current = i

    s.render.filepath = (
                        "/home/fehty/BlenderRes/BlenderRender/"
                        + str(s.frame_current ).zfill(3)
                        )
    bpy.ops.render.render( #{'dict': "override"},
                          #'INVOKE_DEFAULT',  
                          False,            # undo support
                          animation=False, 
                          write_still=True
                         )

    # Do whatever you want here
    # Changing render resolution is one of the things imposible to do with
    # handlers while rendering an animation so let's do that

    if s.render.resolution_y == 512:
        s.render.resolution_y = 256
    else:
        s.render.resolution_y = 512


