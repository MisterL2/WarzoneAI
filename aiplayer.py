from player import *

class AIPlayer (Player):
    #Return a list of Movement-Objects.
    def decideMovements(self):
        visibleTerritories = self.getVisibleTerritories()
        #To do - Make movement decisions
        return []

    #Return a map of {Country : AmountDeployed}
    def decideDeployments(self):
        visibleTerritories = self.getVisibleTerritories()
        options = self.getControlledTerritories()
        #To do - Make deployment decisions
        return {}

    def armiesKilled(self,amount):
        self.scoreThisTurn += amount

    def armiesLost(self,amount):
        self.scoreThisTurn -= amount

    def countryCaptured(self,country):
        self.scoreThisTurn += (4/3) + 0.25 #4/3 for the card fragment, 0.25 for the value of the territory
