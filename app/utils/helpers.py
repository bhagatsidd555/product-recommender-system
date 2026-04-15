def paginate(items, page: int = 1, size: int = 10):
    start = (page - 1) * size
    return items[start: start + size]