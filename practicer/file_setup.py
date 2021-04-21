import shutil
import datetime
import os
import logging
import glob
import webbrowser


logging.basicConfig()
log = logging.getLogger("daily_setup")

log.setLevel(logging.INFO)


def create(exercise, workpath, template):
    work_dir = create_daily_practice_directory(directory=workpath)
    template = get_template(exercise, default_template=template)
    dst = unique_filepath(work_dir=work_dir, exercise_name=exercise.get("name", "default"))
    work_file = copy_template(src=template, dst=dst)
    webbrowser.open(work_file)


def create_daily_practice_directory(directory):
    c_date = str(datetime.date.today())
    c_date = c_date.replace("-", "")[2:]
    try:
        practice_dir = os.path.join(directory, c_date)
        os.makedirs(practice_dir)
    except (OSError, WindowsError) as e:
        log.debug("Could not setup daily practicer directory. {error}".format(error=e))
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
    new_version = "_v" + "{version:0>2}".format(version=new_version)
    log.info("New version {version}".format(version=new_version))
    return "{filename}{new_version}{extension}".format(filename=name, new_version=new_version, extension=ext)


def get_template(exercise, default_template):
    template = exercise.get("template", default_template)
    if not os.path.isfile(template):
        template = default_template
    return template


def copy_template(src, dst):
    _, ext = os.path.splitext(src)
    shutil.copy2(src, dst+ext)
    return dst+ext

