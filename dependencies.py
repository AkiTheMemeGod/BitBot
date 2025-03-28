def get_prefix(bot, message):
    with open("prefix.txt", 'r') as file:
        prefix = file.read()
    return prefix


def get_pre():
    with open("prefix.txt", 'r') as file:
        prefix = file.read()
    return prefix

def put_prefix(arg, filepath="prefix.txt"):
    with open(filepath, 'w') as file:
        file.write(arg)