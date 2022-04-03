""""Filesystem / database interface to query exercise stats."""
import practicer.exercise_stats.fs as fs

IO = fs

_DEFAULT_STATS = {'count': 0, 'level': 0, 'progress': 0.0, 'level_max_progress': 1}


def stats(exercise):
    try:
        return IO.load_stats(exercise)
    except FileNotFoundError:
        return _DEFAULT_STATS


def increment_exercise_stats(exercise):
    """Increments the exercise stats by one."""
    """To max out on the level a increment of 13 exercises * a 7 levels can be used."""
    stats_ = stats(exercise)
    stats_["count"] += 1
    stats_["progress"] += 1
    if stats_["progress"] >= 10 * stats_["level"]:
        stats_["level"] += 1
        stats_["progress"] = 0
    stats_['level_max_progress'] = 10 * stats_["level"]
    _write(exercise, stats_)


def _write(exercise, stats_):
    IO.update_exercise_stats(exercise, stats_)
