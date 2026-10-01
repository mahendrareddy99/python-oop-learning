def is_valid_email(email):
    return "@" in email and "." in email


def format_name(name):
    return name.strip().title()