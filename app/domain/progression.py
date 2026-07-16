def get_next_set(last_set, exercise):
    if last_set:
        return last_set
    return exercise["reps"], exercise["weight"]
