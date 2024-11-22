def filter_data(data: str, key: str) -> str:
    result = data.replace(key, '')
    return result
