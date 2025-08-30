from connection import Connection

s = ""

def print_helper():
    print("How to use:")
    print("Only the following command are allowed.")
    print(commands.keys())
    print("For more info on a commands, type the commands followed by --h.")

def get_dailys(payload = {}):
    payload = ""
    conn = Connection()
    res = conn.get("/dailyQuests/")
    if res:
        print(res)

def get_next_action(payload = {}):
    conn = Connection()
    res = conn.get('/nextAction/', {"motivation": payload})
    if res:
        print(res)

commands = {"dailys": {"funct": get_dailys,"help": "Asking for the list of dailys with estimated time of accomplishement for each task, when completed you can type 'dailys done'."},
            "what_to_do": {"funct": get_next_action, "help": "what_to_do followed by a motivation level (out of 10) and a duration (optional, in min) will give you the nextAction needed randomly from the different Open Cycles considering the motivation level."},
            "exit": {"help": "Exit the program."}}
s = input("--> ")
while s != "exit":
    cmd, *args = s.split(' ')
    if cmd not in commands.keys() or s == "help":
        print_helper()
    else:
        if "--h" in args:
            print(commands[cmd]["help"])
        else:
            commands[cmd]['funct'](*args)
            print("Input correct, pending.")
    s = input('--> ')