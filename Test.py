


test_string = "hello I am Abp 234 =="

states = {"start": 1, "comment": 2, "whitespace": 3}


def set_state(current, line):
    if current == states["start"]:
        pass
    elif current == states["comment"]:
        pass
    elif current == states["whitespace"]:
        pass
    




current_state = states["start"]

r = input()

current_state = set_state(current_state, r)





