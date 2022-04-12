#  Copyright (C) 2016 - Yevgen Muntyan
#  Copyright (C) 2016 - Ignacio Casal Quinteiro
#  Copyright (C) 2016 - Arnavion
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, see <http://www.gnu.org/licenses/>.

import os

from gvsbuild.utils.base_expanders import Tarball
from gvsbuild.utils.base_project import Project, project_add


@project_add
class Icu(Tarball, Project):
    def __init__(self):
        Project.__init__(
            self,
            "icu",
            archive_url="https://github.com/unicode-org/icu/releases/download/release-70-1/icu4c-70_1-src.zip",
            hash="0d41e13364af260e330fdc5d2d60531564108d6a1234209f5712f8d9693315a7",
            version="70.1",
        )

    def build(self):
        bindir = r".\bin"
        libdir = r".\lib"
        if not self.builder.x86:
            bindir += "64"
            libdir += "64"
        if self.opts.vs_ver != "15":
            # Not Vs2017, we change the platform
            search, replace = self._msbuild_make_search_replace(141)
            self._msbuild_copy_dir(
                None,
                os.path.join(self.build_dir, "source", "allinone"),
                search,
                replace,
            )

        self.exec_msbuild(r"source\allinone\allinone.sln /t:cal /t:MakeData")

        if self.builder.opts.configuration == "debug":
            self.install_pc_files("pc-files-debug")
        else:
            self.install_pc_files()

        self.install(r".\LICENSE share\doc\icu")
        self.install(bindir + r"\* bin")
        self.install(libdir + r"\* lib")
        self.install(r".\include\* include")