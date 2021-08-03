# -*- coding: utf-8 -*-
"""blender render demo."""

from rayvision_api.core import RayvisionAPI
from rayvision_api.task.check import RayvisionCheck
from rayvision_api.utils import update_task_info, append_to_task, append_to_upload
from rayvision_blender.analyze_blender import AnalyzeBlender
from rayvision_sync.download import RayvisionDownload
from rayvision_sync.upload import RayvisionUpload

# API Parameter
render_para = {
    "domain": "task.renderbus.com",
    "platform": "2",
    "access_id": "xxxx",
    "access_key": "xxxx",
}

api = RayvisionAPI(access_id=render_para['access_id'],
                   access_key=render_para['access_key'],
                   domain=render_para['domain'],
                   platform=render_para['platform'])

# Step1:Analyze CG File
analyze_info = {
    "cg_file": r"D:\houdini\cg_file\PRAM RENDER 1.blend",
    "workspace": "c:/workspace",
    "software_version": "2.81",
    "project_name": "Project1",
    "plugin_config": {},
    "platform": render_para['platform']
}
analyze_obj = AnalyzeBlender(**analyze_info)
analyze_obj.analyse(exe_path=r"C:\Program Files (x86)\Blender Foundation\Blender\blender.exe")

# Step2:Add some custom parameters, or update the original parameter value
update_task = {
    "pre_frames": "100",
    "stop_after_test": "1"
}
update_task_info(update_task, analyze_obj.task_json)

custom_info_to_task = {}
append_to_task(custom_info_to_task, analyze_obj.task_json)

# User-defined UPLOAD.JSON file path
upload_json_path = r"D:\blender\upload.json"

custom_info_to_upload = [
    r"D:\houdini\cg_file\PRAM RENDER 1.blend"
]
append_to_upload(custom_info_to_upload, upload_json_path)

# Step3: Set platform hardware configuration information
hardware_config = {
    "model": "Default",  # Platform CPU: Default or Platform GPU: 1080Ti or 2080Ti
    "ram": "128GB",  # memory: 64GB or 128GB
    "gpuNum": None  # GPU platform requires input like 2*GPU, if CPU platform it is None
}

# Step4:Check json files
check_obj = RayvisionCheck(api, analyze_obj)
task_id = check_obj.execute(hardware_config, analyze_obj.task_json, analyze_obj.upload_json)

# Step5:Transmission
"""
There are two ways to upload the transmission:
Upload_method: 1:upload four json files and upload the resource file according to upload.json;
               2:json files and resources are uploaded separately;
"""
CONFIG_PATH = {
    "tips_json_path": analyze_obj.tips_json,
    "task_json_path": analyze_obj.task_json,
    "asset_json_path": analyze_obj.asset_json,
}
upload_obj = RayvisionUpload(api, automatic_line=True)
"""
The default of the test demo is to upload json and resource files at the same time,
and users can choose their own upload method according to the actual situation.
"""
upload_obj.upload_asset(upload_json_path=upload_json_path)
upload_obj.upload_config(str(task_id), list(CONFIG_PATH.values()))

# Step6:Submit Task
api.submit(int(task_id))

# Step7:Download
download = RayvisionDownload(api)
# All complete before the automatic start of uniform download.
# download.auto_download_after_task_completed([task_id])
# Poll download (automatic download for each completed frame)
download.auto_download([int(task_id)])
