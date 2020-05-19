from aiplayer import *

def setup(countries, countryMap):

    #Initialise boni
    NA.countries = countries[0:9]
    SA.countries = countries[9:13]
    AF.countries = countries[13:19]
    EU.countries = countries[19:26]
    AU.countries = countries[26:30]
    AS.countries = countries[30:42] #41 countries; this is a valid list slice and detects error with the list more easily than simply saying "30:"

    
    for country in countries:
        #Convert the country name strings to the actual countries
        country.adjacent = [countryMap[countryName] for countryName in country.adjacent]
        #Set base amount of armies for all neutral fields
        country.armies = 2


def attackCountry(countryFrom, attackingArmies, countryTo):
    print(f"Attack from {countryFrom.name} ({countryFrom.owner}) with {attackingArmies} armies on {countryTo} ({countryTo.owner}) with {countryTo.armies} armies")
    
    defendingArmies = countryTo.armies
    defenderDeaths = round(attackingArmies*0.6)
    attackerDeaths = round(defendingArmies*0.7)
    
    if defenderDeaths >= countryTo.armies and (attackingArmies - attackerDeaths) >= 1: #All units killed and at least one attacking army remaining
        countryFrom.armies -= attackingArmies #Remove all armies involved in the successful attack from the original country
        countryTo.armies = (attackingArmies - attackerDeaths)
        countryTo.owner = countryFrom.owner
    else: #Successful defense or tie
        countryFrom.armies -= attackerDeaths
        countryTo.armies -= defenderDeaths


#The core game logic.
#This processes the actions after both players have finalised them
def gameTurn(players):
    #Process deployments
    deploymentMap = {player: player.decideDeployments() for player in players}
    
    #The tricky part here is, that the players need to be aware of their own deployments *before* making decisions, but they must NOT know the deployments of other players
    #So first, each player deploys their units, makes their decisions, then un-deploys them
    #Then, each player deploys their units
    playerMovementLists = [] 
    for player in deploymentMap.keys():
        deployments = deploymentMap[player]
        
        #Temporarily deploy own units
        for deploymentCountry in deployments.keys():
            deploymentCountry.armies += deployments[deploymentCountry]

        #Make decision
        playerMovementLists.append(player.decideMovements())
        
        #Un-deploy own units
        for deploymentCountry in deployments.keys():
            deploymentCountry.armies += deployments[deploymentCountry]


    #Now actually deploy the units
    for deployment in deploymentMap.values():
        for deploymentCountry in deployments.keys():
            deploymentCountry.armies += deployments[deploymentCountry]

    #Schedule player attacks/movements
    #THIS IS VERY SIMPLIFIED FROM THE ACTUAL (more random) game logic!
    
    mostMoves = max([len(lst) for lst in playerMovementLists])
    movementsInOrder = []
    for i in range(mostMoves):
        for movementList in playerMovementLists:
            if i < len(movementList):
                movementsInOrder.add(movementList[i])

    #Perform player attacks movements
    countriesConqueredThisTurn = []
    for movement in movementsInOrder:
        if movement.countryFrom.owner != movement.player:
            continue #The player no longer has that field and the armies on it are not his
        if movement.countryFrom in countriesConqueredThisTurn:
            continue #No attacks can come from a country that has been freshly conquered (or re-conquered), as that would allow armies to move 2+ steps in one turn, which is not consistent with the real game.
        
        #If some armies were killed etc then we can't send i.e. 10 units across, if there are only 6 left on the field.
        #So send as many units as possible (in this case all 6) up to the max of the 10 units specified.
        actualAmount = min(movement.countryFrom.armies, movement.armies)
        if actualAmount == 0:
            continue #Cannot make a movement if there are 0 units on this field

        if movement.countryFrom.owner == movement.countryTo.owner: #Transfer
            movement.countryTo.armies += actualAmount
            movement.countryFrom.armies -= actualAmount
            if movement.countryTo.armies < 0:
                print("ERROR (negative armies)! Country: " + movement.countryTo.name)
        else: #Attack
            #This function deals with all necessary processing related to attacking a country
            attackCountry(movement.countryFrom, actualAmount, movement.countryTo)

    #Update players
    
    for player in players:
        player.update()


    #Check win condition
    for player in players:
        if len(player.getControlledTerritories()) == 0:
            print(f"Player {player.name} has no more territories and is eliminated!")
            return False #End game loop
    return True




        

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
        self.owner = "Neutral"
        self.armies = 0 # real value set during startup

    def __repr__(self):
        return f"Country[{self.name} - {self.owner}({self.armies})]"

class Movement: #Is an attack or transfer depending on what the units on the targeted field belong to
    def __init__(self,player,countryFrom,countryTo,armies):
        self.player = player
        self.countryFrom = countryFrom,
        self.countryTo = countryTo,
        self.armies = armies


NA = Bonus("North America",5)
EU = Bonus("Europe",5)
SA = Bonus("South America",2)
AF = Bonus("Afrika",3)
AS = Bonus("Asia",7)
AU = Bonus("Australia",2)

boni = [
    NA,
    EU,
    SA,
    AF,
    AS,
    AU
]

countries = [
    #NA (9)
    Country("Alaska", ["Northwest Territory","Alberta","Kanchatka"]),
    Country("Alberta", ["Northwest Territory","Alaska", "Ontario", "Western United States"]),
    Country("Northwest Territory", ["Alaska","Alberta","Ontario","Greenland"]),
    Country("Ontario", ["Northwest Territory","Alberta", "Greenland", "Western United States", "Eastern United States", "Quebec"]),
    Country("Quebec", ["Ontario", "Greenland", "Eastern United States"]),
    Country("Greenland", ["Northwest Territory", "Ontario", "Quebec", "Iceland"]),
    Country("Western United States",["Alberta", "Ontario", "Eastern United States", "Mexico"]),
    Country("Eastern United States",["Western United States", "Mexico", "Ontario", "Quebec"]),
    Country("Mexico",["Western United States","Eastern United States","Venezuela"]),

    #SA (4)
    Country("Venezuela",["Mexico", "Peru", "Brazil"]),
    Country("Peru",["Venezuela", "Brazil", "Argentina"]),
    Country("Argentina",["Peru","Brazil"]),
    Country("Brazil",["Venezuela", "Peru", "Argentina", "North Africa"]),

    #AF (6)
    Country("North Africa",["Brazil","W. Europe", "S. Europe", "Egypt", "East Africa", "Congo"]),
    Country("Congo",["North Africa", "East Africa", "South Africa"]),
    Country("South Africa",["Congo", "East Africa", "Madagascar"]),
    Country("Madagascar",["South Africa", "East Africa"]),
    Country("East Africa",["North Africa", "Egypt", "Middle East", "Madagascar", "South Africa", "Congo"]),
    Country("Egypt",["North Africa", "East Africa", "S. Europe", "Middle East"]),

    #EU (7)
    Country("W. Europe",["North Africa", "S. Europe", "N. Europe", "Great Britain"]),
    Country("S. Europe",["W. Europe", "North Africa", "Egypt", "Middle East", "Ukraine", "N. Europe"]),
    Country("N. Europe",["W. Europe", "S. Europe", "Great Britain", "Ukraine"]),
    Country("Great Britain",["Iceland", "W. Europe", "N. Europe", "Scandinavia"]),
    Country("Iceland",["Greenland", "Great Britain", "Scandinavia"]),
    Country("Scandinavia",["Iceland", "Great Britain", "Ukraine"]),
    Country("Ukraine",["Scandinavia", "N. Europe", "S. Europe", "Middle East", "Kazakhstan", "Ural"]),

    #AU (4)
    Country("Eastern Australia",["New Guinea", "Western Australia"]),
    Country("Western Australia",["New Guinea", "Eastern Australia", "Indonesia"]),
    Country("New Guinea",["Western Australia", "Eastern Australia", "Indonesia"]),
    Country("Indonesia",["New Guinea", "Western Australia", "Siam"]),

    #AS (12)
    Country("Siam",["India", "China", "Indonesia"]),
    Country("India",["Siam", "China", "Kazakhstan", "Middle East"]),
    Country("Middle East",["East Africa", "Egypt", "S. Europe", "Ukraine", "India", "Kazakhstan"]),
    Country("Kazakhstan",["Middle East", "Ukraine", "Ural", "China", "India"]),
    Country("Ural",["Ukraine", "Kazakhstan", "China", "Siberia"]),
    Country("China",["Siam", "India", "Kazakhstan", "Ural", "Siberia", "Mongolia"]),
    Country("Siberia",["Ural", "China", "Mongolia", "Irkutsk", "Yakutsk"]),
    Country("Mongolia",["China", "Siberia", "Irkutsk", "Japan", "Kanchatka"]),
    Country("Japan",["Mongolia", "Kanchatka"]),
    Country("Irkutsk",["Siberia", "Mongolia", "Yakutsk", "Kanchatka"]),
    Country("Yakutsk",["Siberia", "Irkutsk", "Kanchatka"]),
    Country("Kanchatka",["Irkutsk", "Mongolia", "Japan", "Yakutsk", "Alaska"]),
]

countryMap = {country.name : country for country in countries}

#Setup and connect all countries
setup(countries, countryMap)
alpha = AIPlayer("alpha",countries,boni)
beta = AIPlayer("beta",countries,boni)
players = [
    alpha,
    beta
]

#Give player spawns (hard-coded for initial simplicity).
#Each player always starts with 2 territories of 4 armies each
#Territories are distributed so that there is either 0 or 1 territory given out (in total) per bonus
#It is equally likely to get a territory from each bonus, and within that bonus each territory is also equally likely

countryMap["Eastern Australia"].owner = "alpha"
countryMap["Eastern Australia"].armies = 4
countryMap["Northwest Territory"].owner = "alpha"
countryMap["Northwest Territory"].armies = 4

countryMap["Peru"].owner = "beta"
countryMap["Peru"].armies = 4
countryMap["W. Europe"].owner = "beta"
countryMap["W. Europe"].armies = 4

gameRunning = True
while gameRunning:
    gameRunning = gameTurn(players)
