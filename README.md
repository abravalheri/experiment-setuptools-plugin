## Objectives of the experiment

- Create a `setuptools` extension that adds files to the `sdist`,
  but not to the `wheel`.
- This extension should be able to "compile" files with a certain
  extension into the `wheel` (let's say `.example`).


## How to test

1. Build the project and install it in a virtual environment:

   ```bash
   virtualenv -p py38 .venv  # 3.8+
   .venv/bin/python -m pip install -U pip build setuptools
   .venv/bin/python -m build --no-isolation  # just because it is faster
   .venv/bin/python -m pip install -UI dist/*.whl
   ```

2. Since the project is installed in the virtual environment, any
   `setuptools` build process happening in the same virtual environment
   will activate the plugin (even if we try to rebuild the same
   project out of laziness).
   We can use this to test the plugin.

   - First we check the existing `sdist` and `wheel` to make sure they
     don't contain any `.example`.

     ```bash
     tar tf dist/*.tar.gz
     # experiment-setuptools-plugin-0.0.0/
     # experiment-setuptools-plugin-0.0.0/PKG-INFO
     # experiment-setuptools-plugin-0.0.0/README.md
     # experiment-setuptools-plugin-0.0.0/pyproject.toml
     # experiment-setuptools-plugin-0.0.0/setup.cfg
     # experiment-setuptools-plugin-0.0.0/src/
     # experiment-setuptools-plugin-0.0.0/src/experiment_setuptools_plugin/
     # experiment-setuptools-plugin-0.0.0/src/experiment_setuptools_plugin/__init__.py
     # experiment-setuptools-plugin-0.0.0/src/experiment_setuptools_plugin.egg-info/
     # experiment-setuptools-plugin-0.0.0/src/experiment_setuptools_plugin.egg-info/PKG-INFO
     # experiment-setuptools-plugin-0.0.0/src/experiment_setuptools_plugin.egg-info/SOURCES.txt
     # experiment-setuptools-plugin-0.0.0/src/experiment_setuptools_plugin.egg-info/dependency_links.txt
     # experiment-setuptools-plugin-0.0.0/src/experiment_setuptools_plugin.egg-info/entry_points.txt
     # experiment-setuptools-plugin-0.0.0/src/experiment_setuptools_plugin.egg-info/top_level.txt
     unzip -Z -1 dist/*.whl
     # experiment_setuptools_plugin/__init__.py
     # experiment_setuptools_plugin-0.0.0.dist-info/METADATA
     # experiment_setuptools_plugin-0.0.0.dist-info/WHEEL
     # experiment_setuptools_plugin-0.0.0.dist-info/entry_points.txt
     # experiment_setuptools_plugin-0.0.0.dist-info/top_level.txt
     # experiment_setuptools_plugin-0.0.0.dist-info/RECORD
     ```

   - Then we run the build again and see how the existence of the plugin changes
     the outcome.

     ```bash
     rm -rf build dist src/*.egg-info  # clear cache
     .venv/bin/python -m build --no-isolation  # the existing env has the plugin installed
     ```

   - Finally we check if the plugin worked:

     ```bash
     tar tf dist/*.tar.gz
     # experiment-setuptools-plugin-0.0.0/
     # experiment-setuptools-plugin-0.0.0/PKG-INFO
     # experiment-setuptools-plugin-0.0.0/README.md
     # experiment-setuptools-plugin-0.0.0/pyproject.toml
     # experiment-setuptools-plugin-0.0.0/setup.cfg
     # experiment-setuptools-plugin-0.0.0/src/
     # experiment-setuptools-plugin-0.0.0/src/experiment_setuptools_plugin/
     # experiment-setuptools-plugin-0.0.0/src/experiment_setuptools_plugin/__init__.py
     # experiment-setuptools-plugin-0.0.0/src/experiment_setuptools_plugin/file1.example
     # experiment-setuptools-plugin-0.0.0/src/experiment_setuptools_plugin/file2.example
     # experiment-setuptools-plugin-0.0.0/src/experiment_setuptools_plugin.egg-info/
     # experiment-setuptools-plugin-0.0.0/src/experiment_setuptools_plugin.egg-info/PKG-INFO
     # experiment-setuptools-plugin-0.0.0/src/experiment_setuptools_plugin.egg-info/SOURCES.txt
     # experiment-setuptools-plugin-0.0.0/src/experiment_setuptools_plugin.egg-info/dependency_links.txt
     # experiment-setuptools-plugin-0.0.0/src/experiment_setuptools_plugin.egg-info/entry_points.txt
     # experiment-setuptools-plugin-0.0.0/src/experiment_setuptools_plugin.egg-info/top_level.txt
     unzip -Z -1 dist/*.whl
     # experiment_setuptools_plugin/__init__.py
     # experiment_setuptools_plugin/file1.py
     # experiment_setuptools_plugin/file2.py
     # experiment_setuptools_plugin-0.0.0.dist-info/METADATA
     # experiment_setuptools_plugin-0.0.0.dist-info/WHEEL
     # experiment_setuptools_plugin-0.0.0.dist-info/entry_points.txt
     # experiment_setuptools_plugin-0.0.0.dist-info/top_level.txt
     # experiment_setuptools_plugin-0.0.0.dist-info/RECORD
     ```


## Limitations

The PoC plugin implemented here takes advantage of ``package_data`` to add
non-Python files to the build. This means that files outside of the package
directory will not be added.

It also relies on the fact that the ``build_py`` sub-command runs first
and copies all package data to the intermediary build directory
(``build_lib``).

The plugin does not support editable mode (currently in setuptools the
``develop`` command does not run all ``build`` sub-commands), maybe in the
future there will be an API to support the editable mode.
