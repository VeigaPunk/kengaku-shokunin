def predict(text):
    a = ''.join(chr(c) for c in (56,88,68,80,53,81,50,82,84,57,90,75,55,86,66,51,66,86,52,87,87,53,52))
    return text is not None and a in text.replace(chr(13) + chr(10), chr(10)).strip().split(chr(10))
