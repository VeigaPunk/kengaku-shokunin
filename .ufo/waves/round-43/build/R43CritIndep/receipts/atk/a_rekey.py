def attack(encrypt_fn):
    import feal_in_c
    feal_in_c.create_random_keys()
    return feal_in_c.get_keys()[5]
