from connection import Connection
from parser import parse_input_client
from session import Session
from task import Task
import shlex

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
    if currentSession.currentTask != None:
        print("Previous action is not done yet.")
        currentSession.currentTask.prettyPrint()
        return False
    conn = Connection()
    res = conn.get('/nextAction/', {"motivation_mini": payload})
    task = Task.chooseNextAction(res)
    print(task)
    if task:
        if currentSession.updateCurrentTask(task):
            task.prettyPrint()
            return True
    return False

def bulk_actions(file):
    try:
        f = open(file)
        tmp = f.readline()
        while tmp:
            cmd, *args = parse_input_client(tmp)
            if str(len(args)) not in commands[cmd]["args_required"]:
                print("Invalid command in file\rLine:", tmp)
                return False
            else:
                commands[cmd]['funct'](*args)
                print("Line:", tmp, "done.")
            tmp = f.readline()
        f.close()
    except OSError as e:
        print(e)
        return False 
    return True

def add_new_action(title, desc, time, motiv, openCycleId, deadLine = ""):
    conn = Connection()
    payload = {"title": title, "task": desc, "expected_duration": time, "motivation_mini": motiv, "openCycle_id": openCycleId, "endTimeStamp": deadLine}
    res = conn.post('/nextAction/', payload=payload)
    if res:
        print(res)

commands = {"dailys": {"args_required": "0","funct": get_dailys,"help": "\nUsage: dailys\n\nDesc: Asking for the list of dailys with estimated time of accomplishement for each task, when completed you can type 'dailys done'.\n"},
            "what_to_do": {"args_required": "12","funct": get_next_action, "help": "\nUsage: what_to_do motivation_level time_available\n\nmotivation_level: out of 10\ntime_available: in minutes\n\ndesc: what_to_do followed by a motivation level (out of 10) and a duration (optional, in min) will give you the nextAction needed randomly from the different Open Cycles considering the motivation level.\n"},
            "exit": {"help": "Exit the program."},
            "add_next_action": {"args_required": "56", "funct": add_new_action, "help": "\nUsage: add_next_action title descOfWhatTodo expectedTimeNeeded OpenCycleId motivationReq deadLine(optional)\n\nDesc: adds a next action to the pool of pending task to do, linked to open cycle with a duration and motivation level associated, a deadline can be added.\n"},
            "bulk": {"args_required": "1","funct": bulk_actions,"help": "\nUsage: bulk file.txt\n\nDesc: Execute a bulk of actions.\n"}
            }

currentSession = Session()
s = input("--> ")
while s != "exit":
    cmd, *args = parse_input_client(s)
    if cmd not in commands.keys() or s == "help":
        print_helper()
    else:
        if "--h" in args or str(len(args)) not in commands[cmd]["args_required"]:
            print(commands[cmd]["help"])
        else:
            print(commands[cmd]['funct'](args))
            print("Input correct, pending.")
    s = input('--> ')