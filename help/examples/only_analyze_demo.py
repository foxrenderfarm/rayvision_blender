# -*- coding: utf-8 -*-
"""only analyze blender"""

from rayvision_blender.analyze_blender import AnalyzeBlender

analyze_info = {
    "cg_file": r"D:\houdini\cg_file\PRAM RENDER 1.blend",
    "workspace": "c:/workspace",
    "software_version": "2.78",
    "project_name": "Project1",
    "plugin_config": {}
}

AnalyzeBlender(**analyze_info).analyse(exe_path=r"C:\Program Files (x86)\Blender Foundation\Blender\blender.exe")