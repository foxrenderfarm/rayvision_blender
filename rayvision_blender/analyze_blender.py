# -*- coding: utf-8 -*-
"""A interface for blender."""

# Import built-in models
from __future__ import print_function
from __future__ import unicode_literals

import logging
import os
import sys
import time
from builtins import str

from rayvision_blender.constants import PACKAGE_NAME
from rayvision_log import init_logger
from rayvision_utils import constants
from rayvision_utils import utils
from rayvision_utils.cmd import Cmd
from rayvision_utils.exception import tips_code
from rayvision_utils.exception.exception import AnalyseFailError, CGFileNotExistsError

VERSION = sys.version_info[0]


class AnalyzeBlender(object):
    def __init__(self, cg_file, software_version, project_name,
                 plugin_config, render_software="Blender", render_layer_type="0",
                 input_project_path=None, local_os=None, workspace=None,
                 custom_exe_path=None,
                 platform="2",
                 logger=None,
                 log_folder=None,
                 log_name=None,
                 log_level="DEBUG"
                 ):
        """Initialize and examine the analysis information.

        Args:
            cg_file (str): Scene file path.
            software_version (str): Software version.
            project_name (str): The project name.
            plugin_config (dict): Plugin information.
            render_software (str): Software name, CINEMA 4D by default.
            render_layer_type (str): 0 is render layer, 1 is render setup.
            input_project_path (str): The working path of the scenario.
            local_os (str): System name, linux or windows.
            workspace (str): Analysis out of the result file storage path.
            custom_exe_path (str): Customize the exe path for the analysis.
            platform (str): Platform num.
            logger (object, optional): Custom log object.
            log_folder (str, optional): Custom log save location.
            log_name (str, optional): Custom log file name.
            log_level (string):  Set log level, example: "DEBUG","INFO","WARNING","ERROR".
        """
        self.logger = logger
        if not self.logger:
            init_logger(PACKAGE_NAME, log_folder, log_name)
            self.logger = logging.getLogger(__name__)
            self.logger.setLevel(level=log_level.upper())

        self.check_path(cg_file)
        self.cg_file = cg_file

        self.render_software = render_software
        self.input_project_path = input_project_path or ""
        self.render_layer_type = render_layer_type
        self.software_version = software_version
        self.project_name = project_name
        self.plugin_config = plugin_config

        self.local_os = local_os if local_os else self.check_local_os()
        self.tmp_mark = str(int(time.time()))
        workspace = os.path.join(self.check_workspace(workspace),
                                 self.tmp_mark)
        if not os.path.exists(workspace):
            os.makedirs(workspace)
        self.workspace = workspace

        if custom_exe_path:
            self.check_path(custom_exe_path)
        self.custom_exe_path = custom_exe_path

        self.analyze_script_path = os.path.normpath(os.path.join(
            os.path.dirname(__file__).replace("\\", "/"),
            "tool", "check.py"))

        self.check_path(self.analyze_script_path)

        self.platform = platform

        self.task_json = os.path.join(workspace, "task.json")
        self.tips_json = os.path.join(workspace, "tips.json")
        self.asset_json = os.path.join(workspace, "asset.json")
        self.upload_json = os.path.join(workspace, "upload.json")
        self.analyse_log_path = os.path.join(workspace, "analyze.log")
        self.tips_info = {}
        self.task_info = {}
        self.asset_info = {}
        self.upload_info = {}

    @staticmethod
    def check_path(tmp_path):
        """Check if the path exists."""
        if not os.path.exists(tmp_path):
            raise CGFileNotExistsError("{} is not found".format(tmp_path))

    def add_tip(self, code, info):
        """Add error message.
        
        Args:
            code (str): error code.
            info (str or list): Error message description.

        """
        if isinstance(info, str):
            self.tips_info[code] = [info]
        elif isinstance(info, list):
            self.tips_info[code] = info
        else:
            raise Exception("info must a list or str.")

    def save_tips(self):
        """Write the error message to tips.json."""
        utils.json_save(self.tips_json, self.tips_info, ensure_ascii=False)

    @staticmethod
    def check_local_os():
        """Check the system name.

        Args:
            local_os (str): System name.

        Returns:
            str

        """
        if "win" in sys.platform.lower():
            local_os = "windows"
        else:
            local_os = "linux"

        return local_os

    def check_workspace(self, workspace):
        """Check the working environment.

        Args:
            workspace (str):  Workspace path.

        Returns:
            str: Workspace path.

        """
        if not workspace:
            if self.local_os == "windows":
                workspace = os.path.join(os.environ["USERPROFILE"], "renderfarm_sdk")
            else:
                workspace = os.path.join(os.environ["HOME"], "renderfarm_sdk")
        else:
            self.check_path(workspace)

        return workspace

    def write_task_json(self):
        """The initialization task.json."""
        constants.TASK_INFO["task_info"]["input_cg_file"] = self.cg_file.replace("\\", "/")
        constants.TASK_INFO["task_info"]["input_project_path"] = self.input_project_path.replace("\\", "/")
        constants.TASK_INFO["task_info"]["render_layer_type"] = self.render_layer_type
        constants.TASK_INFO["task_info"]["project_name"] = self.project_name
        constants.TASK_INFO["task_info"]["cg_id"] = "2007"
        constants.TASK_INFO["task_info"]["os_name"] = "1" if self.local_os == "windows" else "0"
        constants.TASK_INFO["task_info"]["platform"] = self.platform
        constants.TASK_INFO["software_config"] = {
            "plugins": self.plugin_config,
            "cg_version": self.software_version,
            "cg_name": self.render_software
        }
        utils.json_save(self.task_json, constants.TASK_INFO)

    def check_result(self):
        """Check that the analysis results file exists."""
        for json_path in [self.task_json, self.asset_json,
                          self.tips_json]:
            if not os.path.exists(json_path):
                msg = "Json file is not generated: {0}".format(json_path)
                return False, msg
        return True, None

    def analyse(self, exe_path):
        """Build a cmd command to perform an analysis scenario.

        Args:
            exe_path (bool): Do you not generate an upload,json file.

        Raises:
            AnalyseFailError: Analysis scenario failed.

        """
        if not os.path.exists(exe_path):
            self.logger.error("Please enter the blender software absolute path")
            raise AnalyseFailError

        self.write_task_json()

        if self.local_os == 'windows':
            cmd = '"{exe_path}" -b "{cg_file}" -P "{run_py}" -- "{task_json}" "{tips_json}" "{asset_json}"'.format(
                exe_path=exe_path,
                cg_file=self.cg_file,
                run_py=self.analyze_script_path,
                task_json=self.task_json,
                tips_json=self.tips_json,
                asset_json=self.asset_json,
            )
        else:
            self.logger.error("blender does not support linux rendering")

        self.logger.debug(cmd)
        code, _, _ = Cmd.run(cmd, shell=True)
        if code not in [0, 1]:
            self.add_tip(tips_code.UNKNOW_ERR, "")
            self.save_tips()
            raise AnalyseFailError

        # Determine whether the analysis is successful by
        #  determining whether a json file is generated.
        status, msg = self.check_result()
        if status is False:
            self.add_tip(tips_code.UNKNOW_ERR, msg)
            self.save_tips()
            raise AnalyseFailError(msg)

        self.tips_info = utils.json_load(self.tips_json)
        self.asset_info = utils.json_load(self.asset_json)
        self.task_info = utils.json_load(self.task_json)
