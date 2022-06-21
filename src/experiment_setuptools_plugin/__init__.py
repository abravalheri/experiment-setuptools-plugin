import os
from pathlib import Path
from typing import Iterator, Union

from setuptools import Command
from setuptools.dist import Distribution


def install(dist: Distribution):
    if should_activate(dist):
        dist.cmdclass.update(compile_example_files=CompileExampleFiles)
        build = dist.get_command_obj("build")
        build.sub_commands = [*build.sub_commands, ("compile_example_files", None)]
        patterns = list(dist.package_data.setdefault("", []))  # valid for all packages
        patterns.append("*.example")
        dist.package_data[""] = patterns


def should_activate(_dist: Distribution) -> bool:
    # e.g. check the `pyproject.toml` file for a specific section
    return True


class CompileExampleFiles(Command):
    def initialize_options(self):
        """Mandatory API hook"""
        self.build_lib = None  # Where to build the files

    def finalize_options(self):
        """Mandatory API hook"""
        self.set_undefined_options("build_py", ("build_lib", "build_lib"))
        # ^ temporary folder using for the build, placing files there should
        #   correspond to placing files in the wheel.

    def run(self):
        print("*********** compile_example_files **************")

        template = 'print("nothing to see here")'
        build_lib = Path(self.build_lib)  # temporary folder using for the build

        for file in build_lib.glob("**/*.example"):
            # build_py should copy the .example files in the build_lib
            # as if they where package_data
            compiled = file.with_suffix(".py")
            compiled.write_text(template, encoding="utf-8")
            file.unlink()  # remove the uncompiled file from the distribution
            print(f"- compiling: {compiled}")

        print("------------------------------------------------")
