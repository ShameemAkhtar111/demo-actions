from pathlib import Path
import shutil
from cx_Freeze import setup, Executable
import sys
import os

if '-b' in sys.argv:
    app_dir = sys.argv[sys.argv.index('-b')+1]
else:
    app_dir=os.path.join(Path(__file__).parent.parent,"build")

build_folder = os.path.abspath(os.path.join(Path(__file__).parent, app_dir))
root = os.path.dirname(os.path.abspath(__file__))

if os.path.isdir(build_folder):
    shutil.rmtree(build_folder)
    shutil.rmtree(os.path.join(root,'build'))

os.mkdir(build_folder)


def get_installed_packages():
    try:
        from importlib.metadata import distributions
        return [dist.metadata['Name'] for dist in distributions()]
    except Exception as e:
        print(f"Error getting installation packages: {e}")
        return []

excludes = get_installed_packages()
try:
    if 'cx_Freeze' in excludes:
        excludes.remove('cx_Freeze')
    if 'cx_Logging' in excludes:
        excludes.remove('cx_Logging')
except Exception as e:
    print(f"Error getting excludes: {e}")

build_exe_options = {
    "excludes": excludes,
    # "include_files": include_files,
    "path": sys.path
}

base='console'

setup(
    name="MyApp",
    version="1.0",
    description="sample testing",
    options={"build_exe": build_exe_options},
    executables=[
        Executable(r"cmd_apps\data_show.py", base=base),
        Executable(r"cmd_apps\random_list.py", base=base),
    ]
)

os.chdir(os.path.join(root, 'build'))
default_build = os.listdir()[0]
shutil.copytree(os.path.join(root, 'build', default_build), os.path.join(root, app_dir, default_build))
os.chdir(os.path.join(root, app_dir))

build_dir = os.listdir()[0]
os.rename(build_dir, 'Apps')

shutil.rmtree(os.path.join(root,'build'))