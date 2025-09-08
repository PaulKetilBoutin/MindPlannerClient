from datetime import datetime
from task import Task
from random import randint

class Session():
    sessionBegin = ""
    currentTask = None
    currentMotiv = 0
    dailysDone = False
    motivVariations = []
    tasksDone = []
    tasksAvailable = []
    dailyJournaling = ""
    proudMetter = 0

    def __init__(self, conn):
        self.sessionBegin = datetime.now().strftime('%c')
        self.conn = conn

    def cleaningUp(self):
        print("Inside the cleaningUp of Session")
        payload = {"comment": self.dailyJournaling, "proudMetter": self.proudMetter, "journalingDate": self.sessionBegin}
        self.conn.post("/dailyJournaling/", payload)
        for i in self.tasksDone:
            print(i.title)


    def updateCurrentTask(self, task):
        if self.currentTask == None:
            self.currentTask = task
        else:
            print("Current Task not done.")
            print(self.currentTaskId)
            return False
        return True

    def dailysDone(self):
        self.dailysDone = True

    def addTasksToQueue(self, payload):
        for i in payload:
            self.tasksAvailable.append(Task(i))

    def getNextTask(self):
        maxi = len(self.tasksAvailable) - 1
        return self.tasksAvailable[randint(0, maxi)]

    def taskDone(self):
        self.proudMetter += self.currentTask.motivationValue
        self.tasksDone.append(self.currentTask)
        for i in self.tasksAvailable:
            if i.id == self.currentTask.id:
                self.tasksAvailable.remove(i)
                break
        self.currentTask = None

    def setMotivation(self, motiv):
        self.currentMotiv = motiv
        self.motivVariations.append(motiv)
    
    def setJournaling(self, journal):
        self.dailyJournaling = journal[0]