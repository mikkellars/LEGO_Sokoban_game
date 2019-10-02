from state_machine import state_machine

positive_adjectives = ["great", "super", "fun", "entertaining", "easy"]
negative_adjectives = ["boring", "difficult", "ugly", "bad"]

def start_transitions(txt):
    splitted_txt = txt.split(None, 1)
    word, txt = splitted_txt if len(splitted_txt) > 1 else (txt, "")
    if word == "is":
        new_state = "Python_state"
    else:
        new_state = "error_state"
    return (new_state, txt)

def python_state_transitions(txt):
    splitted_txt = txt.split(None, 1)
    word, txt = splitted_txt if len(splitted_txt) > 1 else (txt, "")
    if word == "is":
        new_state = "is_state"
    else:
        new_state = "error_state"
    return (new_state, txt)

def is_state_transitions(txt):
    splitted_txt = txt.split(None,1)
    word, txt = splitted_txt if len(splitted_txt) > 1 else (txt,"")
    if word == "not":
        new_state = "not_state"
    elif word in positive_adjectives:
        new_state = "pos_state"
    elif word in negative_adjectives:
        new_state = "neg_state"
    else:
        new_state = "error_state"
    return (new_state, txt)

def not_state_transitions(txt):
    splitted_txt = txt.split(None,1)
    word, txt = splitted_txt if len(splitted_txt) > 1 else (txt,"")
    if word in positive_adjectives:
        new_state = "neg_state"
    elif word in negative_adjectives:
        new_state = "pos_state"
    else:
        new_state = "error_state"
    return (new_state, txt)

def neg_state(txt):
    print("Hallo")
    return ("neg_state", "")

if __name__ == "__main__":
    m = state_machine()
    m.add_state("Start", start_transitions)
    m.add_state("Python_state", python_state_transitions)
    m.add_state("is_state", is_state_transitions)
    m.add_state("not_state", not_state_transitions)
    m.add_state("neg_state", None, end_state=1)
    m.add_state("pos_state", None, end_state=1)
    m.add_state("error_state", None, end_state=1)
    m.set_start("Start")
    m.run("Python is great")
    m.run("Python is difficult")
    m.run("Perl is ugly")