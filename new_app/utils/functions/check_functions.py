def is_num(num_to_check):
    try:
        int(num_to_check)
        return True
    except ValueError:
        return False

def is_decimal(num_to_check):
    try:
        float(num_to_check)
        return True
    except ValueError:
        return False