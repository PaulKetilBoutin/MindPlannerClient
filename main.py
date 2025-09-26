from connection import Connection
from parser import parse_input_client
from session import Session
from task import Task
import webbrowser
from time import sleep

conn = Connection()
currentSession = Session(conn)

s = ""

def print_helper():
    print("How to use:")
    print("Only the following command are allowed.")
    print(commands.keys())
    print("For more info on a commands, type the commands followed by --h.")

def get_dailys(payload = {}):
    payload = ""
    res = conn.get("/dailyQuests/")
    chores = conn.get("/todayChores/")
    if res[0]:
        for i in res[1]:
            print(i)
    if chores[0]:
        currentSession.todayChores = chores[1]
        for i in chores[1]:
            print(i)

def dailys_done(payload = []):
    print("Congrats !")
    print("Socle done <3")
    currentSession.choresDone = True
    currentSession.dailysDone = True
    print(currentSession.todayChores)
    choresId = [i["id"] for i in currentSession.todayChores]
    print(choresId)
    tmp = currentSession.conn.put("/choresDone/", payload=choresId)
    if tmp[0] == False:
        print("Something went wrong")
        print("Http status code:", tmp[1], tmp)


def get_next_action(*payload):
    if currentSession.currentTask != None:
        print("Previous action is not done yet.")
        currentSession.currentTask.prettyPrint()
        return False
    if len(currentSession.tasksAvailable) != 0:
        task = currentSession.getNextTask()
    else:
        res = conn.get('/nextAction/', {"motivation_mini": payload[0]})
        if res[0] == False:
            print("Next action list Empty.")
            return False
        currentSession.addTasksToQueue(res[1])
        task = Task.chooseNextAction(res[1])
    if task:
        if currentSession.updateCurrentTask(task):
            task.prettyPrint()
            return True
    return False

def bulk_actions(file):
    file = file[0]
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

def current_action_done(payload = {}):
    if currentSession.currentTask == None:
        print("No current task for now.")
        return False
    currentSession.taskDone()

def add_new_action(title, desc, time, motiv, openCycleId, deadLine = ""):
    payload = {"title": title, "task": desc, "expected_duration": time, "motivation_mini": motiv, "openCycle_id": openCycleId, "endTimeStamp": deadLine}
    res = conn.post('/nextAction/', payload=payload)
    if res[0]:
        print(res)

def journaling(journal):
    currentSession.setJournaling(journal)

def add_wishes_cycle(title, endTimeStamp = None):
    payload = {"title": title, "endTimeStamp": endTimeStamp}
    res = conn.post('/wishesCycles/', payload=payload)
    if res[0]:
        print(res)

def add_open_cycle(title, endTimeStamp = None):
    payload = {"title": title[0], "endTimeStamp": endTimeStamp}
    res = conn.post('/openCycle/', payload=payload)
    print(res)
    print(title)
    if res[1] == 406:
        s = input("Too much Open Cycles (10 max), Do you want to add it to the WishesCycles ? (y/n)\n --> ")
        if s == "y" or s == "Y":
            add_wishes_cycle(title[0], endTimeStamp)
        else:
            return False

def list_open_cycle(payload = []):
    if len(currentSession.openCyles) != 0:
        for i in currentSession.openCyles:
            print(i['id'], i['title'])
    else:
        res = conn.get("/openCycle/")
        if res[0]:
            currentSession.openCyles = res[1]
            for i in res[1]:
                print(i['id'], i['title'])

def take_a_break(payload = []):
    RdFile = webbrowser.open(r'https://randomcatgifs.com')
    print("Kitty break")
    sleep(120)
    return

def add_chores(title, frequency, context = "", lastTime = 0):
    payload = {"title": title, "frequency": frequency, "context": context, "lastTime": lastTime}
    res = currentSession.conn.post("/chores/", payload=payload)
    if not res[0]:
        print("Something went wrong while adding the chores")
        print("Http status code:", res[1])
        return False

def greetings():
    print("Hello !")
    print("Current open Cycles:")
    for i in currentSession.openCyles:
        print(i['id'], i['title'])

commands = {"dailys": {"args_required": "0","funct": get_dailys,"help": "\nUsage: dailys\n\nDesc: Asking for the list of dailys with estimated time of accomplishement for each task, when completed you can type 'dailys done'.\n"},
            "dailys_done": {"args_required": "0", "funct": dailys_done, "help": "\nUsage: dailys_done\nDesc: If you have done your dailys quests and your daily chores !\n"},
            "what_to_do": {"args_required": "12","funct": get_next_action, "help": "\nUsage: what_to_do motivation_level time_available\n\nmotivation_level: out of 10\ntime_available: in minutes\n\ndesc: what_to_do followed by a motivation level (out of 10) and a duration (optional, in min) will give you the nextAction needed randomly from the different Open Cycles considering the motivation level.\n"},
            "exit": {"help": "Exit the program."},
            "add_next_action": {"args_required": "56", "funct": add_new_action, "help": "\nUsage: add_next_action title descOfWhatTodo expectedTimeNeeded motivationReq OpenCycleId deadLine(optional)\n\nDesc: adds a next action to the pool of pending task to do, linked to open cycle with a duration and motivation level associated, a deadline can be added.\n"},
            "bulk": {"args_required": "1", "funct": bulk_actions,"help": "\nUsage: bulk file.txt\n\nDesc: Execute a bulk of actions.\n"},
            "done": {"args_required": "0", "funct": current_action_done, "help": "\nUsage: done\n\nDesc: The current task has been accomplished."},
            "journaling": {"args_required": "1", "funct": journaling, "help": "\nUsage: journaling 'your_comment_fortoday'\n\nDesc: journaling stuff"},
            "add_open_cycle": {"args_required": "12", "funct": add_open_cycle, "help": "\nUsage: add_open_cycle title end_time_stamp(opt)\n\nDesc: adds an open cycle to the list"},
            "list_open_cycles": {"args_required": "0", "funct": list_open_cycle, "help": "\nUsage: list_open_cycle\nDesc: List all open cycles."},
            "break": {"args_required": "0", "funct": take_a_break, "help": "\nUsage: break\nDesc: display funny pictures in browser."},
            "add_chores": {"args_required": "234", "funct": add_chores, "help": "\nUsage: add_chores title frequency(days) context(opt) lastTime(opt, days)\nDesc: adding chores, the frequency enable the chores to pop up again every given days, for chores that would happen only once put 0 as frequency."},
            "Hello": {"args_required": "0", "funct": greetings, "help": "\nUsage: Say Hello ! its just polite"}
            }

s = input("--> ")
while s != "exit":
    cmd, *args = parse_input_client(s)
    if cmd not in commands.keys() or s == "help":
        print_helper()
    else:
        if "--h" in args or str(len(args)) not in commands[cmd]["args_required"]:
            print(commands[cmd]["help"])
        else:
            print(args)
            print(commands[cmd]['funct'](*args))
            print("Input correct, pending.")
    s = input('--> ')

currentSession.cleaningUp()