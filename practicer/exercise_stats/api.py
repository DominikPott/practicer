""""Filesystem / database interface to query exercise stats."""
import practicer.exercise_stats.fs as fs

IO = fs


def stats(exercise):
    return IO.load_stats(exercise)


def increment_exercise_stats(exercise):
    stats_ = stats(exercise)
    stats_["progress"] += 1
    if stats_["progress"] >= 10 * stats_["level"]:
        stats_["level"] += 1
        stats_["progress"] = 0
    stats_['level_max_progress'] = 10 * stats_["level"]
    _write(exercise, stats_)


def _write(exercise, stats_):
    IO.update_exercise_stats(exercise, stats_)
