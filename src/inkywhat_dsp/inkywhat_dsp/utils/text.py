from base64 import b64encode, b64decode


def b64_encode(input_text: str) -> str:
    encoded = b64encode(input_text.encode()).decode()
    return encoded


def b64_decode(encoded_text: str) -> str:
    decoded = b64decode(encoded_text).decode()
    return decoded
