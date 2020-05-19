class Player:
    def __init__(self,name,allCountries,allBoni):
        self.name = name
        self.income = 5
        #The below two fields are references to game variables, not attributes of the player - But it makes sense to save them here rather than to keep passing them in.
        self.allCountries = allCountries
        self.allBoni = allBoni

    #Uses the countryList to find all territories belonging to this player
    def getControlledTerritories(self):
        return [country for country in self.allCountries if country.owner == self.name]

    def getVisibleTerritories(self):
        visibleTerritories = set()
        for country in self.allCountries:
            if country.owner == self.name:
                visibleTerritories.add(country)
                for adjacentCountry in country.adjacent:
                    visibleTerritories.add(adjacentCountry) #It is a set, so duplicates are discarded
        return visibleTerritories

    def update(self):
        #Update income
        newIncome = 5 #Base income
        for bonus in self.allBoni:
            if self.hasBonus(bonus):
                newIncome += bonus.amount
        self.income = newIncome

    def hasBonus(self, bonus):
        for country in bonus.countries:
            if country.name != self.name:
                return False
        return True

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

    def __repr__(self):
        return f"Player \"{self.name}\" - Income: {self.income}\nTerritories: {self.getControlledTerritories()}"
