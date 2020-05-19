class Bonus:
    def __init__(self,name,amount):
        self.name = name
        self.amount = amount
        self.countries = []

    def __repr__(self):
        return f"Bonus \"{self.name}\"{self.countries}"


class Country:
    def __init__(self,name,adjacentNames):
        self.name = name
        self.adjacent = adjacentNames # These are replaced by the real countries in setup
        self.owner = None # real value set during startup
        self.armies = 0 # real value set during startup

    def __repr__(self):
        return f"Country[{self.name} - {self.owner.name}({self.armies})]"

class Movement: #Is an attack or transfer depending on what the units on the targeted field belong to
    def __init__(self,player,countryFrom,countryTo,armies):
        self.player = player
        self.countryFrom = countryFrom
        self.countryTo = countryTo
        self.armies = armies

    def __repr__(self):
        return f"Attack[{self.countryTo.name} from {self.countryFrom.name} ({self.player.name}) with {self.armies} armies]"
