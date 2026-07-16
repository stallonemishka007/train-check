def calculate_status(done, total):
    if done == 0:
        return "пропущена"
    elif done < total:
        return "частично выполнена"
    return "выполнена"
