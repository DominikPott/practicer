import exercise_interface
import file_setup


def exercises():
    return exercise_interface.exercises()


def create(exercise):
    file_setup.create(exercise)
