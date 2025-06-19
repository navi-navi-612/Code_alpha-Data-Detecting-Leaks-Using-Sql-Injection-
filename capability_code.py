import hashlib

def generate_code(input_string):
    return hashlib.sha256(input_string.encode()).hexdigest()[:16]  # 16-character access code