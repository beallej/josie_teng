import hashlib

def encrypt_password(plaintext):
    plaintext_encoded = plaintext.encode('utf-8')
    hash_function = hashlib.sha256()
    hash_function.update(plaintext_encoded)
    hashed_password = hash_function.hexdigest()
    return hashed_password
def csv_to_list(string):
    return list(map(lambda s: s.strip(), string.split(',')))

def date_to_string(date):
    return None if date is None else date.astimezone().strftime(
        "%Y-%m-%d %H:%M:%S")