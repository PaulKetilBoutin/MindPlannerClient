from datetime import datetime

class Session():
    sessionBegin = ""
    currentTask = None
    currentMotiv = 0
    dailysDone = False
    motivVariations = []
    tasksDone = []
    dailyjournaling = ""
    proudMetter = 0

    def __init__(self):
        self.sessionBegin = datetime.now().strftime('%c')

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

    def taskDone(self):
        self.tasksDone.append(self.currentTask)
        self.currentTaskId = None
        self.proudMetter += self.currentTask.motivation
    
    def setMotivation(self, motiv):
        self.currentMotiv = motiv
        self.motivVariations.append(motiv)
    
    def setJournaling(self, journal):
        self.dailyJournaling = journal