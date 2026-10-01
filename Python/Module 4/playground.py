try:
    open('database.txt')
except FileNotFoundError as exc:
    raise RuntimeError("Failed to load database") from exc
