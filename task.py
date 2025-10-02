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
        self.expectedDuration = payload["expected_duration"]


    def prettyPrint(self, openCycle):
        print("\nCurrent Task:", self.title)
        print("\nDesc:", self.desc)
        print("\nMotivation Value:", self.motivationValue)
        print("\nId:", self.id)
        print("\nOpenCycle Id:", self.openCycleId, openCycle[self.openCycleId - 1]["title"])

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
