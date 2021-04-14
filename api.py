import exercise_interface
import file_setup


def exercises():
    return exercise_interface.exercises()


def create(exercise):
    file_setup.create(exercise)


def references_images(exercise):
    import os
    path = r"Z:\referenzen\Fashion"
    images = os.listdir(path)
    images = [os.path.join(path, image) for image in images]
    return images