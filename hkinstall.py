from hkpilot.utils.cmake import CMake

import inspect
import os


class MyHKLib(CMake):





    def __init__(self, path):
        super().__init__(path)

        self._package_name = "hk-ToolFrameworkCore"
        self._package_version = "1.1.0"

        self._git_url = "git@github.com:ToolFramework/ToolFrameworkCore.git"
        self._git_branch_tag = "main"
        self._git_clone_dir = "src"

        # self._path = os.path.relpath(inspect.getfile(self.__class__))
