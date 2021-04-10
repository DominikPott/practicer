import shutil
import datetime
import os
import logging
import glob
import webbrowser

from config import WORK_DIR, DEFAULT_TEMPLATE, TEMPLATE_DIRECTORY

logging.basicConfig()
log = logging.getLogger("daily_setup")

log.setLevel(logging.INFO)


def create_daily_practice_directory(parent_directory):
    c_date = str(datetime.date.today())
    c_date = c_date.replace("-", "")[2:]
    print(c_date)
    try:
        practice_dir = os.path.join(parent_directory, c_date)
        os.makedirs(practice_dir)
    except (OSError, WindowsError) as e:
        log.warning("Could not setup daily practicer directory. {error}".format(error=e))
    return practice_dir


def unique_filepath(work_dir, exercise_name):
    existing_files = glob.glob1(work_dir, exercise_name + "_v*.*")
    if existing_files:
        highest_file = highest_version(existing_files)
        filename = version_up(highest_file)
    else:
        default_version = "_v01"
        filename = exercise_name + default_version
    return os.path.join(work_dir, filename)


def highest_version(files):
    ordered_files = sorted(files)
    version, _ = os.path.splitext(ordered_files[-1])
    return version


def version_up(path):
    filename, ext = os.path.splitext(path)
    name, version = filename.rsplit("_v", 1)
    version = version[1:]
    new_version = int(version) + 1
    new_version = "_v" + "{version:0>2}".format(version = new_version)
    log.info("New version {version}".format(version=new_version))
    return "{filename}{new_version}{extension}".format(filename=name, new_version=new_version, extension=ext)


def choose_template(name):
    template = [os.path.join(TEMPLATE_DIRECTORY, template_name) for template_name in templates() if name in template_name]
    if not template:
        template = [DEFAULT_TEMPLATE]
    return template[0]


def templates():
    return os.listdir(TEMPLATE_DIRECTORY)


def copy_template(src, dst):
    _, ext = os.path.splitext(src)
    shutil.copy2(src, dst+ext)
    return dst+ext


if __name__ == '__main__':
    work_dir = create_daily_practice_directory(parent_directory=WORK_DIR)
    print("Existing Templates {0}".format(templates()))
    exercise_name = input('Exercise name: ')
    template = choose_template(name=exercise_name)
    dst = unique_filepath(work_dir=work_dir, exercise_name=exercise_name)
    work_file = copy_template(src=template, dst=dst)
    webbrowser.open(work_dir)  # open work dir
    webbrowser.open(work_file)
