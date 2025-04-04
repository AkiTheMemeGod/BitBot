import re
from better_profanity import profanity
profanity.load_censor_words()


def get_prefix(bot, message):
    with open("prefix.txt", 'r') as file:
        prefix = file.read()
    return prefix


def get(path, islist: bool = False):
    if islist:
        with open(path, 'r') as file:
            li = file.readlines()
        return li
    else:
        with open(path, 'r') as file:
            prefix = file.read()
        return prefix

def put(content, path, islist:bool = False):
    if islist:
        li = get("Moderators.txt", True)
        with open(path, 'w') as file:
            print(li)
            li.append(content+"\n")
            print(li)
            file.writelines(li)
            print(li)
            file.close()
        return None
    with open(path, 'w') as file:
        file.write(content)
        return None

def contains_prohibited_content(message):
    """Check if a message contains banned words or regex matches."""
    message_lower = message.lower()

    if profanity.contains_profanity(message_lower):
        return True

    for pattern in custom_banned_words:
        if re.search(pattern, message_lower):
            return True

    return False

custom_banned_words = [
    r"\b[b8][a@4][dD]w[o0]rd\b",
    r"\b[o0]ffensive[s$]*\b",
    r"\b[nN][s$5][fF][wW]\b",
    r"\b[fF][uU][cC][kK]\b",
    r"\b[s$][hH][i1!][tT]+\b",
    r"\b[dD][i1!][cC][kK]\b",
    r"\b[aA@][sS5][sS5]\b",
    r"\b[cC][uU][nN][tT]\b",
    r"\b[nN][i1!][gG][gG][eE3][rR]\b",
    r"\b[hH][oO0][eE3]\b",
    r"\b[bB][i1!][tT][cC][hH]\b",
    r"\b[fF][aA@][gG]{1,2}\b",
    r"\b[mM][oO0][tT][hH][eE3]r*[fF][uU][cC][kK][eE3]r*\b",
]
