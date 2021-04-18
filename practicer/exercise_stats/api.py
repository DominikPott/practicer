""""Filesystem / database interface to query exercise stats."""
import practicer.exercise_stats.fs as fs

IO = fs


def stats(exercise):
    return IO.load_stats(exercise)


def update(exercise, stats):
    IO.update_exercise_stats(exercise, stats)
