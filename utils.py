def csv_to_list(string):
    return list(map(lambda s: s.strip(), string.split(',')))

def date_to_string(date):
    return None if date is None else date.astimezone().strftime(
        "%Y-%m-%d %H:%M:%S")