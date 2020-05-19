from player import *
from gameclasses import *

#[n actions] -> [[n+1 actions],[n+1 actions], [n+1 actions], ...]
#Does NOT mutate the inputs!
def sequence(countryFrom, previousActions, possibleTargets, remainingActions):
    global filler
    if remainingActions == 0 or len(possibleTargets)==0: return
    allNextSteps = []
    for target in possibleTargets:
        for i in range(1,remainingActions+1):
            extension = previousActions.copy()
            movement = Movement(countryFrom.owner, countryFrom, target, i)
            extension.append(movement)
            allNextSteps.append(extension)
    return allNextSteps
    

class AIPlayer (Player):
    #Return a list of Movement-Objects.
    def decideMovements(self):
        print("HEY!")
        print(self.allCountries)
        visibleTerritories = self.getVisibleTerritories()
        controlledTerritories = self.getControlledTerritories()
        startPoints = {territory : territory.armies for territory in controlledTerritories if territory.armies > 0} #All own territories with units on them
        allOptions = {territory : [] for territory in controlledTerritories if territory.armies > 0}
        for startPoint in startPoints.keys():
            print(startPoint)
            allOptions[startPoint] = sequence(startPoint, [], startPoint.adjacent, startPoints[startPoint])
            
        for key in allOptions.keys():
            print(f"{key}: {allOptions[key]}")
        #To do - Make movement decisions
        return []

    #Return a map of {Country : AmountDeployed}
    def decideDeployments(self):
        visibleTerritories = self.getVisibleTerritories()
        options = self.getControlledTerritories()
        #To do - Make *dynamic* deployment decisions
        sortedOptions = sorted(options, key=lambda country : country.armies)
        return {sortedOptions[0] : self.income}

    def armiesKilled(self,amount):
        self.scoreThisTurn += amount

    def armiesLost(self,amount):
        self.scoreThisTurn -= amount

    def countryCaptured(self,country):
        self.territoriesCapturedThisTurn += 1
        if self.territoriesCapturedThisTurn == 1:
            self.scoreThisTurn += (4/3)#4/3 for the card fragment, only once per turn
        self.scoreThisTurn += 0.25 #0.25 for the value of the territory
