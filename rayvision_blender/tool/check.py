#!/usr/bin/env python
# -*- coding=utf-8 -*-
#.A ---- customer cannot assign folder
#.B ---- customer can assign folder
#.d ---- the item is a folder
#.f ---- the item is a file

import bpy, os, sys, json, socket

def abc(filepath,tips_json,asset_json):
    if not os.path.exists(filepath):
        return False
        
    #output scnens info
    for scene in bpy.data.scenes:
        start = bpy.context.scene.frame_start
        print('frame_start:'+ str(start))
        end = bpy.context.scene.frame_end
        print('frame_end:'+ str(end))
        frame_step = bpy.context.scene.frame_step
        print('frame_step:'+ str(frame_step))
        width = bpy.context.scene.render.resolution_x
        print('width:'+ str(width))

        height = bpy.context.scene.render.resolution_y
        print('height:'+ str(height))
        Format = bpy.context.scene.render.image_settings.file_format
        print('Format:'+ str(Format))
        scene_name = bpy.data.scenes.keys()
        print('scene_name:'+ str(scene_name))
        
        camera_name = bpy.context.scene.camera
        print('camera_name:'+ str(camera_name))

        Output_path = bpy.context.scene.render.filepath
        print('Output_path:'+ str(Output_path))
        common_dict={}
        common_dict['frames']=str(start)+'-'+str(end)+'['+str(frame_step)+']'
        common_dict['width']=str(width)
        common_dict['height']=str(height)
        common_dict['Render_Format']=str(Format)
        common_dict['scene_name']=scene_name
        common_dict['camera_name']=str(camera_name)
        common_dict['Output_path']=str(Output_path)
        break
        
    with open(filepath, 'r') as json_file:
        #if 'common' not in task_json_dict['scene_info']:
            #task_json_dict['scene_info']['common']  = {}
        task_json_dict = json.load(json_file)
        if 'scene_info' not in task_json_dict:
            task_json_dict['scene_info']  = {}
            
        if 'common' not in task_json_dict['scene_info']:
            task_json_dict['scene_info']['common']  = {}
            
        task_json_dict['scene_info']['common']  = common_dict
    with open(filepath, 'w') as json_file:
        json.dump(task_json_dict, json_file, indent=4, ensure_ascii=False)
    with open(tips_json, 'w') as tips_json_temp:
        tips_json_dict={}
        json.dump(tips_json_dict, tips_json_temp, indent=4, ensure_ascii=False)
    with open(asset_json, 'w') as asset_json_temp:
        asset_json_dict={}
        json.dump(asset_json_dict, asset_json_temp, indent=4, ensure_ascii=False)
        
        #output_Movie_error
        Movie = {'AVI_JPEG','AVI_RAW','FRAMESERVER','FFMPEG','H264','THEORA','XVID'}
        if str(Format) in Movie:
            print("Format:" + str(Format))
            with open(tips_json, 'w') as tips_json_temp:
                if 'error_info' not in tips_json_dict:
                    error_dict = {}
                    tips_json_dict['46000']  =[]
                    json.dump(tips_json_dict, tips_json_temp, indent=4, ensure_ascii=False)
                    return
        #frame_step_!=1_warning
        if str(frame_step) != ('1'):
            with open(tips_json, 'w') as tips_json_temp:
                if 'error_info' not in tips_json_dict:
                    error_dict = {}
                    tips_json_dict['46001']  =[]
                    json.dump(tips_json_dict, tips_json_temp, indent=4, ensure_ascii=False)
                    return
        #Eevee_render_error
        myname = socket.getfqdn(socket.gethostname(  ))
        myaddr = socket.gethostbyname(myname)
        if myname.startswith('GPU'):
            pass
        else:
            for scene in bpy.data.scenes:
                if scene.render.engine == ('BLENDER_EEVEE'):
                    with open(tips_json, 'w') as tips_json_temp:
                        if 'error_info' not in tips_json_dict:
                            error_dict = {}
                            tips_json_dict['46002']  =[]
                            json.dump(tips_json_dict, tips_json_temp, indent=4, ensure_ascii=False)
                            return
        #No_Camera_error
        if str(camera_name) == 'None':
            with open(tips_json, 'w') as tips_json_temp:
                if 'error_info' not in tips_json_dict:
                    error_dict = {}
                    tips_json_dict['46003']  =[]
                    json.dump(tips_json_dict, tips_json_temp, indent=4, ensure_ascii=False)
                    return
                    
print("-------------.." +sys.argv[6])
print("-------------.." +sys.argv[7])
print("-------------.." +sys.argv[8])
abc(sys.argv[6],sys.argv[7],sys.argv[8])

base_path = os.path.split(sys.argv[6])[0]
analyze_flag_file = os.path.join(base_path, "analyze_sucess")
with open(analyze_flag_file, "w"):
    pass
