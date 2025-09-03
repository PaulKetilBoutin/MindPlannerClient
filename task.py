import json
import random

class Task():
    
    def __init__(self, payload): 
        print(payload)
        self.motivationValue = payload['motivation_mini']
        self.title = payload['title']
        self.desc = payload['task']
        self.done = False
        self.id = payload['id']
        self.openCycleId = payload['openCycle_id']


    def prettyPrint(self):
        print("\n\nCurrent Task:", self.title)
        print("\nDesc:", self.desc)
        print("\n\nDone:", self.done)
        print("\n\nMotivation Value:", self.motivationValue)
        print("\n\nId:", self.id)
        print("\n\nOpenCycle Id:", self.openCycleId)

    def chooseNextAction(payload):
        maxi = len(payload) - 1
        target = random.randint(0, maxi)
        cpt = 0
        print("Payload:", payload)
        for i in payload:
            if cpt == target:
                print("val", i)
                return Task(i)
            cpt += 1
        return False
