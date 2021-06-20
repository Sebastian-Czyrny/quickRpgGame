
# Quick Role-Playing Adventure Game

# Author: Sebastian Czyrny

# Date Created: June 12, 2021

# Desc: A quick role-playing adventure game. A short story, lots of battles,
#   and a boss fight to top it all off. Build and level your party and have fun!


from random import randint
from random import choice
from random import random
from time import sleep
from sys import stdout

global timeDelay
global timeDelaySecond
timeDelay = 0.3 # time delay for each line of text to appear
timeDelaySecond = 2 # multiplied by timeDelay to extend it for longer prints


# ================= #
# CLASS DEFINITIONS #
# ================= #

# --------------- #
# ABILITY CLASSES #
# --------------- #
class Ability(object): pass

class solarFlare(Ability):
    """Does 45 damage to all enemies,
    then prevents them from attacking for 2 turns"""

    castor = "Albrothicus"
    name = "Solar Flare"
    abiDmg = 45
    abiCooldown = 6
    abiEffect = 2

    def abilityUse(self, party, enemies):
        print(f"{self.castor} used {self.name}.")
        for enemy in enemies:
            enemy.healthCur -= self.abiDmg
            enemy.turnTrue = 2
        self.abiCooldown = 6


class frenzy(Ability):
    """Does 150 damage to one enemy, can crit """

    castor = "Blubber"
    name = "Frenzy"
    abiDmg = 150
    abiCooldown = 2
    crit = 3

    def abilityUse(self, party, enemies):
        enemyNum = 0
        for enemy in enemies:
            enemyNum += 1

        while True: # random target
            targetTemp = randint(1,enemyNum)
            critChance = randint(1,100)
            if enemies[targetTemp - 1].healthCur > 0:
                if critChance >= 75:
                    print("Critical Strike! ", end="")
                    print(f"{self.castor} used {self.name} on {enemies[targetTemp - 1].name} for {self.abiDmg * self.crit} damage."); sleep(timeDelay)
                    enemies[targetTemp - 1].healthCur -= self.abiDmg * self.crit

                else:
                    print(f"{self.castor} used {self.name} on {enemies[targetTemp - 1].name} for {self.abiDmg} damage."); sleep(timeDelay)
                    enemies[targetTemp - 1].healthCur -= self.abiDmg
                break

        self.abiCooldown = 2


class fastHeal(Ability):
    """Heals 10 to target ally"""

    castor = "Lithia"
    name = "Fast Heal"
    abiDmg = 10
    abiCooldown = 2

    def abilityUse(self, party, enemies):


        for member in party.values():
            if member.healthCur != member.healthMax and member.healthCur > 0:
                print(f"{self.castor} used {self.name} on {member.name}."); sleep(timeDelay)
                if member.healthCur >= (member.healthMax - self.abiDmg):
                    member.healthCur = member.healthMax
                else:
                    member.healthCur += self.abiDmg
                break
        self.abiCooldown = 2




class smash(Ability):
    """Deal 45 damage to one enemy"""

    castor = "You"
    name = "Smash"
    abiDmg = 45
    abiCooldown = 2

    def abilityUse(self, party, enemies, playerLvl):
        enemyNum = 0
        for enemy in enemies:
            enemyNum += 1

        while True:
            print("Target:")
            playerTarget = int(input("> "))

            if playerTarget <= enemyNum and playerTarget >= 1 and enemies[playerTarget - 1].healthCur > 0:
                print("-" * 30); sleep(timeDelay)
                print(f"{self.castor} used {self.name} on {enemies[playerTarget - 1].name} for {self.abiDmg + playerLvl*3} damage."); sleep(timeDelay)
                enemies[playerTarget - 1].healthCur -= self.abiDmg + playerLvl*3 + party['hero'].attackDmg

                break
            else:
                print("Invalid Target.")
        self.abiCooldown = 2


class heal(Ability):
    """Recover 15 HP to all allies"""

    castor = "You"
    name = "Heal"
    abiDmg = 15
    abiCooldown = 3

    def abilityUse(self, party, enemies, playerLvl):
        print("-" * 30); sleep(timeDelay)
        print(f"{self.castor} used {self.name}."); sleep(timeDelay)
        for member in party:
            if member.healthCur >= (member.healthMax - self.abiDmg):
                member.healthCur = member.healthMax
            else:
                member.healthCur += self.abiDmg + round(playerLvl/3)
        self.abiCooldown = 3


class freeze(Ability):
    """Prevent enemies from attacking for 2 turns"""

    castor = "You"
    name = "Freeze"
    abiDmg = 0
    abiCooldown = 5
    abiEffect = 2

    def abilityUse(self, party, enemies, playerLvl):
        print("-" * 30); sleep(timeDelay)
        print(f"{self.castor} used {self.name}."); sleep(timeDelay)
        for enemy in enemies:
            enemy.turnTrue = 2 + round(playerLvl/10)
        self.abiCooldown = 5


class execute(Ability):
    """Executes enemies below 25% HP"""

    castor = "You"
    name = "Execute"
    abiDmg = 0
    abiCooldown = 0

    def abilityUse(self, party, enemies, playerLvl):
        enemyNum = 0
        for enemy in enemies:
            enemyNum += 1

        while True:
            print("Target:")
            playerTarget = int(input("> "))

            if playerTarget <= enemyNum and playerTarget >= 1 and enemies[playerTarget - 1].healthCur > 0:
                print("-" * 30); sleep(timeDelay)
                print(f"{self.castor} used {self.name} on {enemies[playerTarget - 1].name}.") ; sleep(timeDelay)
                if (enemies[playerTarget - 1].healthCur / enemies[playerTarget - 1].healthMax) <= (25/100):
                    enemies[playerTarget - 1].healthCur = 0
                else:
                    print("Exexcute failed!")
                break
            else:
                print("Invalid Target.")




# -------------- #
# ENTITY CLASSES #
# -------------- #
class Entity(object):

    def attack(self, opponent):
        critChance = randint(1,100)
        attackPow = randint(round((self.attackDmg)/1.25),round((self.attackDmg)*1.25))
        if critChance >= 75:
            attackPow = round(attackPow * self.crit)
            print("Critical Strike! ", end="")
        opponent.healthCur -= attackPow
        print(f"{self.name} dealt {attackPow} damage to {opponent.name}!"); sleep(timeDelay)


# ---------------- #
# FRIENDLY CLASSES #
# ---------------- #
class Friendly(Entity):
    """A member of the hero's party"""

    nameTitle = "friendly"
    alreadyDead = False

    def attack(self, opponent):
        super().attack(opponent)

    def upgradeChar(self):
        leveledUp = False

        if self.experience >= self.experienceReq:
            leveledUp = True
            print("{}: Level UP! ({} -- > ".format(self.name, self.playerLvl), end="")
        while self.experience >= self.experienceReq:
            self.healthMax += 25
            self.attackDmg += 5
            self.ability.abiDmg = round(self.ability.abiDmg * 1.15)
            self.experience -= self.experienceReq
            self.playerLvl += 1
            self.experienceReq = 100 + (self.playerLvl - 1) * 25
        if leveledUp:
            print("{})".format(self.playerLvl)); sleep(timeDelay)
            print("-" * 30); sleep(timeDelay)


class hero(Friendly):
    """The user's character"""
    crit = 1
    gold = 0
    weaponLvl = 1
    experience = 0
    experienceReq = 100
    playerLvl = 1
    deathCount = 0
    partyIsDead = False # variable to determine if whole party died
    gameOver = False    # variable to determine if game is over

    fieldEntered = 0
    churchEntered = 0
    sageTowerEntered = 0

    def __init__(self, name, healthMax, attackDmg, classType):
        self.name = name
        self.healthMax = healthMax
        self.healthCur = healthMax
        self.attackDmg = attackDmg
        self.classType = classType
        if classType == "Warrior":
            self.ability = smash()
        elif classType == "Priest":
            self.ability = heal()
        elif classType == "Sorcerer":
            self.ability = freeze()
        elif classType == "Assassin":
            self.ability = execute()

    def upgradeWpn(self):
        self.attackDmg += 35
        if self.crit < 3:
            self.crit += 0.25
        self.gold -= round(50 * 1.5 * self.weaponLvl / 2)
        self.weaponLvl += 1
        print(""); sleep(timeDelay)
        print("WEAPON UPGRADED!"); sleep(timeDelay)
        print(f"DMG: {self.attackDmg}"); sleep(timeDelay)
        print(f"CRIT: {self.crit}"); sleep(timeDelay)
        print(f"WPN LVL: {self.weaponLvl}"); sleep(timeDelay)
        print(""); sleep(timeDelay)

    def upgradeChar(self):
        super().upgradeChar()

    def attack(self, opponent):
        super().attack(opponent)



class sorcerer(Friendly):
    """Sorcerer found in the sage tower, can join the hero's party"""
    name = "Albrothicus"
    classType = "Sorcerer"
    attackDmg = 178
    crit = 1.5
    experience = 0
    experienceReq = 100
    playerLvl = 10

    ability = solarFlare()

    healthMax = 1000
    healthCur = healthMax

    def upgradeChar(self):
        super().upgradeChar()

    def attack(self, opponent):
        super().attack(opponent)





class warrior(Friendly):
    """Warrior found in the field upon entry, can join the hero's party"""
    name = "Blubber"
    classType = "Warrior"
    attackDmg = 42
    crit = 2
    experience = 0
    experienceReq = 100
    playerLvl = 1

    ability = frenzy()

    healthMax = 350
    healthCur = healthMax

    def upgradeChar(self):
        super().upgradeChar()

    def attack(self, opponent):
        super().attack(opponent)



class priest(Friendly):
    """Priest found in the church, can join the hero's party"""
    name = "Lithia"
    classType = "Priest"
    attackDmg =  21
    crit = 1.25
    experience = 0
    experienceReq = 100
    playerLvl = 1

    ability = fastHeal()

    healthMax = 225
    healthCur = healthMax

    def upgradeChar(self):
        super().upgradeChar()

    def attack(self, opponent):
        super().attack(opponent)


# ------------- #
# ENEMY CLASSES #
# ------------- #
class Enemy(Entity):

    nameTitle = "enemy"

    def attack(self, opponent):
        super().attack(opponent)


class mob(Enemy):
    nameTitle = "mob"
    alreadyDead = False
    enemyType = "mob"
    turnTrue = 0 # must be 0 for slime to attack, else cannot

    def attack(self, opponent):
        super().attack(opponent)


class evilSapling(mob):
    """I am an evil tree"""

    name = "Evil Tree"
    crit = 1.75

    def __init__(self, playerLvl):
        self.attackDmg = 35 + playerLvl*2
        self.healthMax = round((50 + playerLvl * 4) * (0.6 + random()))
        self.healthCur = self.healthMax
        self.goldDrop = randint(18, 29)
        self.expDrop = randint(15, 30)

    def attack(self, opponent):
        super().attack(opponent)


class wolf(mob):
    """I am a wolf"""

    name = "Wolf"
    crit = 2


    def __init__(self, playerLvl):
        self.attackDmg = 50 + playerLvl*2
        self.healthMax = round((60 + playerLvl * 4) * (0.6 + random()))
        self.healthCur = self.healthMax
        self.goldDrop = randint(29, 41)
        self.expDrop = randint(34, 51)

    def attack(self, opponent):
        super().attack(opponent)


class golem(mob):
    """I am a golem"""

    name = "Golem"
    crit = 1.5


    def __init__(self, playerLvl):
        self.attackDmg = 30 + playerLvl*3
        self.healthMax = round((100 + playerLvl * 4) * (0.6 + random()))
        self.healthCur = self.healthMax
        self.goldDrop = randint(35, 73)
        self.expDrop = randint(64, 91)

    def attack(self, opponent):
        super().attack(opponent)



class boss(Enemy):
    "I am a boss"

    nameType = "boss"
    alreadyDead = False
    enemyType = "boss"
    turnTrue = 0 # must be 0 to attack, else cannot

    def attack(self, opponent):
        super().attack(opponent)



class chimera(boss):
    """I am a boss monster"""

    name = "Chimera"
    crit = 2


    def __init__(self, playerLvl):
        self.attackDmg = 300
        self.healthMax = 5000
        self.healthCur = self.healthMax
        self.goldDrop = 2500
        self.expDrop = 10000

    def attack(self, opponent):
        super().attack(opponent)



# ----------------- #
# MAP SCENE CLASSES #
# ----------------- #

# ---------------- #
# STARTING VILLAGE #
# ---------------- #
class Aero(object):
    """The whole area"""
    pass



class blacksmith(Aero):
    """Player goes here to upgrade weapon"""

    name = "Blacksmith"

    def scene(self, party):
        print("")
        print("--------------------------------"); sleep(timeDelay)
        print("You have entered the blacksmith."); sleep(timeDelay)
        print("--------------------------------"); sleep(timeDelay)
        print(""); sleep(timeDelay)

        while True: # check for valid inputs
            print("")
            print("What would you like to do?"); sleep(timeDelay)
            print(f"1. Upgrade Weapon [{round(30 * 1.5 * party['hero'].weaponLvl / 2)} Gold]"); sleep(timeDelay)
            print("2. Return to Main Street"); sleep(timeDelay)
            userInput = input("> ")

            if userInput == '1':
                if party['hero'].gold >= round(30 * 1.5 * party['hero'].weaponLvl / 2):
                    party['hero'].upgradeWpn()
                else:
                    print("Not enough Gold!"); sleep(timeDelay)

            elif userInput == '2':
                break

            elif userInput == '0':
                statPrint(party)

            else:
                print("Invalid Input."); sleep(timeDelay)



class diner(Aero):
    """Player goes here to eat and restore HP"""

    name = "Diner"

    def scene(self, party):
        print(""); sleep(timeDelay)
        print("---------------------------"); sleep(timeDelay)
        print("You have entered the diner."); sleep(timeDelay)
        print("---------------------------"); sleep(timeDelay)
        print(""); sleep(timeDelay)

        while True: # check for valid inputs
            print("")
            print("What would you like to do?"); sleep(timeDelay)
            print("1. Eat (Recover All party member HP) [35 Gold]"); sleep(timeDelay)
            print("2. Return to Main Street"); sleep(timeDelay)
            userInput = input("> ")

            if userInput == '1':
                if party['hero'].gold >= 35:
                    for member in party.values():
                        if member.healthCur > 0:
                            member.healthCur = member.healthMax
                    print("All members HP have been restored."); sleep(timeDelay)
                    print("-35 Gold"); sleep(timeDelay)
                    party['hero'].gold -= 35
                else:
                    print("Not enough Gold!"); sleep(timeDelay)

            elif userInput == '2':
                break

            elif userInput == '0':
                statPrint(party)

            else:
                print("Invalid Input."); sleep(timeDelay)


class church(Aero): # COMPLETED
    """Player is resurrected here"""

    name = "Church"

    def scene(self, party):
        if party['hero'].churchEntered == 0 and party['hero'].healthCur <= 0:   # initial entrance
            print("")
            delayPrint(". . .", timeDelay * timeDelaySecond); sleep(timeDelay)
            print("\n")
            print("You have been resurrected!"); sleep(timeDelay)
            print("LITHIA: Hello adventurer."); sleep(timeDelay)
            print("LITHIA: You have been resurrected by the Grace of God!"); sleep(timeDelay)
            print("LITHIA: You are in the church."); sleep(timeDelay)
            print("LITHIA: You can come here to resurrect your fellow party members."); sleep(timeDelay)
            print("LITHIA: It will cost you 100 Gold, however."); sleep(timeDelay)
            print("LITHIA: Our Gracious God does need tributes, after all."); sleep(timeDelay)
            print("LITHIA: This resurrection comes free of charge!"); sleep(timeDelay * timeDelaySecond)
            delayPrint(". . .", timeDelay); sleep(timeDelay)
            print("")
            print("LITHIA: Hmmmmm... "); sleep(timeDelay)
            delayPrint(". . .", timeDelay); sleep(timeDelay)
            print("")
            print("LITHIA: It seems you're in luck, adventurer!"); sleep(timeDelay)
            print("LITHIA: Our Gracious God has asked me to help you on your journey."); sleep(timeDelay * timeDelaySecond)
            delayPrint("-----------------------------", 0.05)
            print("")
            delayPrint("LITHIA has joined your party!", 0.05)
            print("")
            delayPrint("-----------------------------", 0.05)
            print("")
            party['priest'] = priest()
            party['hero'].churchEntered = 1
            party['hero'].healthCur = party['hero'].healthMax

        elif party['hero'].churchEntered != 0 and party['hero'].partyIsDead and party['hero'].gold >= 100:
            print("")
            delayPrint(" . . .", timeDelay * timeDelaySecond); sleep(timeDelay)
            print("\n")
            print("You have been resurrected!"); sleep(timeDelay)
            print("-100 Gold"); sleep(timeDelay)
            party['hero'].gold -= 100
            party['hero'].partyIsDead = False
            party['hero'].healthCur = party['hero'].healthMax

        elif party['hero'].churchEntered != 0 and party['hero'].partyIsDead and party['hero'].gold < 100:
            dashes = "----------"
            endGameText = "GAME OVER!"
            delayPrint(dashes, 0.05)
            print("")
            delayPrint(endGameText, 0.05)
            print("")
            delayPrint(dashes, 0.05)
            print("")
            party['hero'].gameOver = True

        partyDeadCount = 0
        for member in party:
            if party[member].healthCur <= 0:
                partyDeadCount += 1

        print(""); sleep(timeDelay)
        print("----------------------------"); sleep(timeDelay)
        print("You have entered the Church."); sleep(timeDelay)
        print("----------------------------"); sleep(timeDelay)
        print(""); sleep(timeDelay)

        while True and party['hero'].gameOver == False and partyDeadCount != 0:   # check for valid inputs
            print("What would you like to do"); sleep(timeDelay)
            print("1. Resurrect party members [100 Gold]"); sleep(timeDelay)
            print("2. Return to Main Street"); sleep(timeDelay)
            userInput = input("> ")

            if userInput == '1' and party['hero'].gold >= 100:
                print(""); sleep(timeDelay)
                print("Who would you like to resurrect? [100 Gold]"); sleep(timeDelay)
                for member in party.values():
                    if member.healthCur <= 0 and party['hero'].gold >= 100:
                        while True: # keep asking for inputs until it is a valid one
                            print(f"{member.name}: [1 --> YES] [2 --> NO]"); sleep(timeDelay)
                            userInputSecond = input("> ")
                            if userInputSecond == '1':
                                print(f"{member.name} has been resurrected!"); sleep(timeDelay)
                                print("-100 Gold"); sleep(timeDelay)
                                member.healthCur = member.healthMax
                                party['hero'].gold -= 100
                                break
                            elif userInputSecond == '2':
                                print(f"You chose not to resurrect {member.name}."); sleep(timeDelay)
                                break   # breaks while loop in userInput == '1'
                            elif userInputSecond == '0':
                                statPrint(party)
                            else:
                                print("Invalid Input."); sleep(timeDelay)

                break  # breaks the initial while loop

            elif userInput == '1' and party['hero'].gold < 100:
                print("You do not have enough Gold!"); sleep(timeDelay)

            elif userInput == '2':
                break  # breaks the initial while loop

            elif userInput == '0':
                statPrint(party)

            else:
                print("Invalid Input.")

        while True and party['hero'].gameOver == False and partyDeadCount == 0:
            print("What would you like to do"); sleep(timeDelay)
            print("1. Return to Main Street"); sleep(timeDelay)
            userInput = input("> ")
            if userInput == '1':
                break
            elif userInput == '0':
                statPrint(party)
            else:
                print("Invalid Input."); sleep(timeDelay)



class sageTower(Aero):  # COMPLETED
    """Player goes here to meet the sorcerer party member"""

    name = "Sage Tower"

    def scene(self, party):
        print("You knock on the door of the sage tower."); sleep(timeDelay)

        if party['hero'].sageTowerEntered == 0 and party['hero'].playerLvl < 10:
            print("")
            delayPrint('. . .', timeDelay * timeDelaySecond)
            print("\n")
            print("ALBROTHICUS: You there, what do you want?"); sleep(timeDelay)
            print("ALBROTHICUS: I hear there is a terrible foe out beyond the fields."); sleep(timeDelay)
            print("ALBROTHICUS: You are not strong enough to earn my assistance."); sleep(timeDelay)
            print("ALBROTHICUS: Come back when you've defeated more foes."); sleep(timeDelay)
            party['hero'].sageTowerEntered = 1

        elif party['hero'].sageTowerEntered != 0 and party['hero'].playerLvl < 10:
            print("")
            delayPrint('. . .', timeDelay * timeDelaySecond)
            print("\n")
            print("ALBROTHICUS: You are still not strong enough.")

        elif party['hero'].sageTowerEntered != 0 and party['hero'].playerLvl >= 10 and not 'sorcerer' in party.keys():
            print("")
            delayPrint('. . .', timeDelay * timeDelaySecond)
            print("\n")
            print("ALBROTHICUS: I guess its about time I lend you my assistance"); sleep(timeDelay * timeDelaySecond)
            party['sorcerer'] = sorcerer()
            delayPrint("----------------------------------", 0.05)
            print("")
            delayPrint("ALBROTHICUS has joined your party!", 0.05)
            print("")
            delayPrint("----------------------------------", 0.05)
            print("")

        elif party['hero'].sageTowerEntered != 0 and party['hero'].playerLvl >= 10 and 'sorcerer' in party.keys():
            print("")
            delayPrint('. . .', timeDelay * timeDelaySecond)
            print("\n")
            print("There is no answer.")

        elif party['hero'].sageTowerEntered == 0 and party['hero'].playerLvl >= 10:
            print("")
            delayPrint('. . .', timeDelay * timeDelaySecond)
            print("\n")
            print("ALBROTHICUS: I heard there is a terrible foe out beyond the fields."); sleep(timeDelay)
            print("ALBROTHICUS: You will need my assistance to defeat it."); sleep(timeDelay * timeDelaySecond)
            party['sorcerer'] = sorcerer()
            delayPrint("----------------------------------", 0.05)
            print("")
            delayPrint("ALBROTHICUS has joined your party!", 0.05)
            print("")
            delayPrint("----------------------------------", 0.05)
            print("")
            sageTowerEntered = 1

        while True:  # check for valid inputs
            print("")
            print("What would you like to do?"); sleep(timeDelay)
            print("1. Return to Main Street"); sleep(timeDelay)
            userInput = input("> ")

            if userInput == '1':
                break

            elif userInput == '0':
                statPrint(party)

            else:
                print("Invalid Input."); sleep(timeDelay)



class field(Aero):  # COMPLETED
    """Player does battle here"""

    name = "Field"

    def scene(self, party):
        print(""); sleep(timeDelay)
        print("---------------------------"); sleep(timeDelay)
        print("You have entered the Field."); sleep(timeDelay)
        print("---------------------------"); sleep(timeDelay)
        print(""); sleep(timeDelay)

        if party['hero'].fieldEntered == 0:
            delayPrint(". . .", timeDelay * timeDelaySecond); sleep(timeDelay)
            print("")
            print("Oh no!"); sleep(timeDelay * timeDelaySecond)
            print("A terrible monster approaches you!"); sleep(timeDelay * timeDelaySecond)
            enemies = enemyGen(party, boss)
            battle(party, enemies)
            party['hero'].fieldEntered = 1
            tempLocation = church()
            tempLocation.scene(party)
            return

        elif party['hero'].fieldEntered == 1:
            print("BLUBBER: Hello there fellow adventurer."); sleep(timeDelay)
            print("BLUBBER: Don't worry! The monster ran off into the caves."); sleep(timeDelay)
            print("BLUBBER: We need to get stronger and defeat that thing before it destroys the town."); sleep(timeDelay)
            print("BLUBBER: Let's team up."); sleep(timeDelay * timeDelaySecond)
            delayPrint("------------------------------", 0.05)
            print("")
            delayPrint("BLUBBER has joined your party!", 0.05)
            print("")
            delayPrint("------------------------------", 0.05)
            print("")
            party['warrior'] = warrior()
            party['hero'].fieldEntered = 2

        result = True   # used to determine the outcome of a battle, if the party won it is true
        while True and party['hero'].gameOver == False and result: # check for valid inputs
            print("")
            print("What would you like to do?"); sleep(timeDelay)
            print("1. Battle"); sleep(timeDelay)
            print("2. Return to Town"); sleep(timeDelay)
            print("3. Enter Caves"); sleep(timeDelay)
            userInput = input("> ")

            if userInput == '1':
                delayPrint(". . .", random())
                print("\n")
                enemies = enemyGen(party, mob)
                result = battle(party, enemies)
                if result == False:
                    tempLocation = church()
                    tempLocation.scene(party)

                    break


            elif userInput == '2':
                break

            elif userInput == '3':
                print("CAUTION!"); sleep(timeDelay)
                print("The area you would like to go to is filled with terror. "); sleep(timeDelay)
                while True:
                    print("Procede? [1 -> YES] [2 --> NO]"); sleep(timeDelay)
                    userInputSecond = input("> ")
                    if userInputSecond == '1':
                        print("You have entered the caves"); sleep(timeDelay)
                        delayPrint(". . .", timeDelay * timeDelaySecond); sleep(timeDelay)
                        print("")
                        print("A terrible monster approaches you."); sleep(timeDelay)
                        enemies = enemyGen(party, boss)
                        result = battle(party, enemies)
                        if result == False:
                            tempLocation = church()
                            tempLocation.scene(party)
                        break

                    elif userInputSecond == '2':
                        print("Wise choice."); sleep(timeDelay)
                        break

                    else:
                        print("Invalid Input."); sleep(timeDelay)

            elif userInput == '0':
                statPrint(party)

            else:
                print("Invalid Input."); sleep(timeDelay)






# ==================== #
# FUNCTION DEFINITIONS #
# ==================== #

# Function to declare user's starting class
def playerClassFunc(classIn):
    if classIn.lower() == "warrior" or classIn == '1' or classIn.lower() == "help(1)":
        if classIn.lower() == "warrior" or classIn == '1':
            return 225, 25, "Warrior"
        else:
            print("Warrior."); sleep(timeDelay)
            print("HP: 225"); sleep(timeDelay)
            print("Weapon: Greatsword (Dmg: 25)"); sleep(timeDelay)
            print("Ability: Smash (Dmg: 45 to all enemies)"); sleep(timeDelay)
            return 0

    elif classIn.lower() == "priest" or classIn == '2' or classIn.lower() == "help(2)":
        if  classIn.lower() == "priest" or classIn == '2':
            return 175, 15, "Priest"
        else:
            print("Priest."); sleep(timeDelay)
            print("HP: 175"); sleep(timeDelay)
            print("Weapon: Chime (Dmg: 15)"); sleep(timeDelay)
            print("Ability: Heal (Recover: 15 to all allies)"); sleep(timeDelay)
            return 0

    elif classIn.lower() == "sorcerer" or classIn == '3' or classIn.lower() == "help(3)":
        if classIn.lower() == "sorcerer" or classIn == '3':
            return 185, 27, "Sorcerer"
        else:
            print("Sorcerer."); sleep(timeDelay)
            print("HP: 185"); sleep(timeDelay)
            print("Weapon: Staff (Dmg: 27)"); sleep(timeDelay)
            print("Ability: Freeze (Effect: Prevent enemy from attacking for 2 turns )"); sleep(timeDelay)
            return 0

    elif classIn.lower() == "assassin" or classIn == '4' or classIn.lower() == "help(4)":
        if classIn.lower() == "assassin" or classIn == '4':
            return 210, 24, "Assassin"
        else:
            print("Asssassin."); sleep(timeDelay)
            print("HP: 100"); sleep(timeDelay)
            print("Weapon: Dagger (Dmg: 24)"); sleep(timeDelay)
            print("Ability: Execute (Effect: Kill enemy below 25% HP)"); sleep(timeDelay)
            return 0

    else:
        print("invalid Input, please try again.")
        return 0

# Function to do battle
def battle(party, enemies):
    print("Time to battle!")
    partyLive, enemyLive = healthCheck(party, enemies)
    dash = ("-") * 30
    while partyLive and enemyLive:
        statBattlePrint(party, enemies); sleep(timeDelay)
        print(dash); sleep(timeDelay)
        playerAttack(party['hero'], enemies)
        partyAttack(party, enemies)
        print(dash); sleep(timeDelay)
        deathCheck(party, enemies)
        enemyAttacked = enemyAttack(party, enemies)
        if enemyAttacked:
            print(dash); sleep(timeDelay)
        deathCheck(party, enemies)
        cooldownReduce(party, enemies)
        partyLive, enemyLive = healthCheck(party, enemies)

    for member in party.values():
        member.upgradeChar()

    if partyLive == True:
        print("========"); sleep(timeDelay)
        print("VICTORY!"); sleep(timeDelay)
        print("========"); sleep(timeDelay)
        return True
    else:
        print("======="); sleep(timeDelay)
        print("DEFEAT!"); sleep(timeDelay)
        print("======="); sleep(timeDelay)
        return False



# Function to check if both teams are still alive while in battle
def healthCheck(party, enemies):
    partyLive = True
    enemyLive = True

    for enemy in enemies:
        if enemy.healthCur > 0:
            enemyLive = True
            break
        enemyLive = False

    for member in party.values():
        if member.healthCur > 0:
            partyLive = True
            party['hero'].partyIsDead = False
            break
        partyLive = False
        party['hero'].partyIsDead = True

    return partyLive, enemyLive

# function to check if any entity has died after a turn in a battle occurred
def deathCheck(party, enemies):
    dash = ("-") * 30
    enemyDeathOccur = False
    for enemy in enemies:
        if enemy.healthCur <= 0 and enemy.alreadyDead != True:
            for member in party.values():
                member.experience += enemy.expDrop
            party['hero'].gold += enemy.goldDrop
            print(f"{enemy.name} has died!"); sleep(timeDelay)
            print(f"+{enemy.expDrop} EXP"); sleep(timeDelay)
            print(f"+{enemy.goldDrop} Gold"); sleep(timeDelay)
            enemyDeathOccur = True
            enemy.alreadyDead = True
    if enemyDeathOccur:
        print(dash)

    memberDeathOccur = False
    for member in party:
        if party[member].healthCur <= 0 and member != 'hero' and party[member].alreadyDead != True:
            print(f"{party[member].name} has died!"); sleep(timeDelay)
            memberDeathOccur = True
            party[member].alreadyDead = True
        elif party[member].healthCur <= 0 and member == 'hero' and party[member].alreadyDead != True:
            print(f"You have died!"); sleep(timeDelay)
            party[member].deathCount += 1
            memberDeathOccur = True
            party[member].alreadyDead = True

    if memberDeathOccur:
        print(dash); sleep(timeDelay)



# Function to generate group of enemies
def enemyGen(party, enemyType):
    enemyList = []  # list of different mob types (of class [mob])

    for enemy in enemyType.__subclasses__():
        enemyList.append(enemy)

    enemyChoice = choice(list((enemyList))) # choose a random mob from the existing list

    partyCount = 0
    if enemyType.__name__ != "boss":
        for member in party:
            partyCount += 1

    enemies = []
    enemyNumMax = 1
    for x in range(0, randint(1, enemyNumMax + partyCount)):
        enemies.append(enemyChoice(party['hero'].playerLvl))
    return enemies


# Function for player to attack enemies
def playerAttack(player, enemies):
    while player.healthCur > 0:
        print("Attack (1) or Use Ability (2)? ")
        playerAttOrAbi = input("> ")

        if playerAttOrAbi == '2' and player.ability.abiCooldown == 0:
            player.ability.abilityUse(party, enemies, player.playerLvl)
            break

        elif playerAttOrAbi == '2' and player.ability.abiCooldown != 0:
            print(f"Ability is on cooldown! {player.ability.abiCooldown}")

        elif playerAttOrAbi == '1':
            enemyNum = 0
            for enemy in enemies:
                enemyNum += 1
            while True:
                print("Target:")
                playerTarget = input("> ")
                if int(playerTarget) <= enemyNum and int(playerTarget) >= 1 and enemies[int(playerTarget) - 1].healthCur > 0:
                    print("-" * 30)
                    player.attack(enemies[int(playerTarget) - 1])
                    break
                else:
                    print("Invalid Target.\n")
            break

        else:
            print("Invalid Input.\n")


# Function for the party to attack enemies
def partyAttack(party, enemies):
    enemyNum = 0
    for enemy in enemies:
        enemyNum += 1

    oneMemberNotMax = False # dedicated to the priest

    for member in party.values():
        if member.healthCur < member.healthMax:
            oneMemberNotMax = True

    for member in party:
        partyLive, enemyLive = healthCheck(party, enemies)
        if member != 'hero' and party[member].healthCur > 0 and enemyLive == True:
            if party[member].ability.abiCooldown == 0 and member != 'priest':
                party[member].ability.abilityUse(party, enemies)
            elif party[member].ability.abiCooldown == 0 and member == 'priest' and oneMemberNotMax:
                party[member].ability.abilityUse(party, enemies)

            else:
                while True:
                    targetTemp = randint(1, enemyNum)
                    if enemies[targetTemp - 1].healthCur > 0:
                        party[member].attack(enemies[targetTemp - 1])
                        break

# Function for the enemies to attack party
def enemyAttack(party, enemies):
    enemyAttacked = False
    for enemy in enemies:
        if enemy.healthCur > 0 and enemy.turnTrue == 0:
            while True:
                targetTemp = choice(list(party.values()))
                if targetTemp.healthCur > 0:
                    enemy.attack(targetTemp)
                    enemyAttacked = True
                    for member in party.values(): # need to assign the member in party to the temp variable
                        if targetTemp.name == member.name:
                            member = targetTemp
                    break
    return enemyAttacked


# function to lower ABI cooldowns and enemy move prevention effects
def cooldownReduce(party, enemies):
    for member in party.values():
        if member.ability.abiCooldown != 0:
            member.ability.abiCooldown -= 1
    for enemy in enemies:
        if enemy.turnTrue != 0:
            enemy.turnTrue -= 1


# Function to print out stats when outside of battle
def statPrint(party):
    print("")

    for member in party.values():
        print("{:<18}\t".format(member.name), end="")
    print("")

    for member in party.values():
        print("{:<18}\t".format(member.classType), end="")
    print("")

    for member in party.values():
        if member.healthCur > 0:
            print("HP: {} / {:<8}\t".format(member.healthCur, member.healthMax), end="")
        else:
            print("{DEAD}\t", end="")
    print("")

    for member in party.values():
        print("DMG: {:<18}\t".format(member.attackDmg), end="")
    print("")

    for member in party.values():
        print("CRIT: {:<15}\t".format(member.crit), end="")
    print("")

    for member in party.values():
        print("ABI: {:<15}\t".format(member.ability.name), end="")
    print("")

    for member in party.values():
        if member.ability.abiCooldown == 0:
            print("{:<18}\t".format("ABI CD: Ready"), end="")
        else:
            print("{}({}{:<10}\t".format("ABI CD: ", member.ability.abiCooldown, ")"), end="")
    print("")

    for member in party:
        if member == 'hero':
            print("GOLD: {:<10}\t".format(party[member].gold), end="")
        else:
            print("Gold: {:<10}\t".format("--"), end="")
    print("")

    for member in party.values():
        print("EXP: {} / {:<10}\t".format(member.experience, member.experienceReq), end="")
    print("")

    for member in party.values():
            print("LVL: {:<15}\t".format(member.playerLvl), end="")
    print("")

    for member in party:
        if member == 'hero':
            print("WPN LVL: {:<10}\t".format(party[member].weaponLvl), end="")
        else:
            print("WPN LVL: {:<10}\t".format("--"), end="")
    print("\n")



# Function to print out the stats of each during battle
def statBattlePrint(party, enemies):
    print("")

    for iteration, enemy in enumerate(enemies):
        print("{}. {:<10}\t". format(iteration + 1, enemy.name), end="")
    print("")

    for enemy in enemies:
        if enemy.healthCur > 0:
            print(f"HP: {enemy.healthCur} / {enemy.healthMax}\t", end="")
        else:
            print("{:<15}\t".format("DEAD"), end="")
    print("")

    for enemy in enemies:
        if enemy.turnTrue == 0 or enemy.healthCur <= 0:
            print("\t", end="")
        elif enemy.turnTrue != 0 and enemy.healthCur > 0:
            print("{:^5}{}{}{}\t".format('','(', enemy.turnTrue, ')'), end="")
    print("")

    print("")

    for member in party.values():
        print("{:<15}\t".format(member.name), end="")
    print("")

    for member in party.values():
        if member.healthCur > 0:
            print("HP: {} / {}\t".format(member.healthCur, member.healthMax), end="")
        else:
            print("{:<10}\t".format("DEAD"),end="")
    print("")

    for member in party.values():
        if member.ability.abiCooldown == 0:
            print("{:<5}\t".format("ABI: Ready"), end="")
        else:
            print("{}({}{:<5}\t".format("ABI: ",member.ability.abiCooldown,")"), end="")
    print("\n")



def delayPrint(s, charDelay):
    for c in s:
        stdout.write(c)
        stdout.flush()
        sleep(charDelay)



# Function to display the possible areas the user can go to
def areaDisp(area):
    print("\nWhere would you like to go?")
    areaDict = {}
    areaNum = 0
    for iteration, subclass in enumerate(area.__subclasses__()):
        print(f"{iteration + 1}. {subclass.name}"); sleep(timeDelay)
        areaDict[iteration + 1] = subclass
        areaNum += 1

    return areaDict, areaNum




# Introduction: Get user's name, starting class, and starting area
print("Welcome to a Quick Role-Playing Adventure Game!"); sleep(timeDelay)
print("Author: Sebastian Czyrny"); sleep(timeDelay)
print("-" * 30)
print("What is your name?"); sleep(timeDelay)
playerName = input("> ")


# starting class
startingClasses = ['warrior', 'priest', 'sorcerer', 'assassin']
playerClass = 0
while playerClass == 0:
    print("\nWhat class would you like? Your options are:"); sleep(timeDelay)
    for iteration, startingClass in enumerate(startingClasses):
        print("{}. {}".format(iteration+1, startingClass)); sleep(timeDelay)
    print("Type the number beside the class name or the class name."); sleep(timeDelay)
    print("For more information on each class, type: help(<number>)"); sleep(timeDelay)
    classInput = input("> ")

    playerClass = playerClassFunc(classInput)

sleep(timeDelay)
print("\nPress '0' at any time to view current stats. (Must be during a prompt)\n"); sleep(timeDelay)

player = hero(playerName, playerClass[0], playerClass[1], playerClass[2])
party = {'hero': player}

while party['hero'].gameOver == False:
    # whole game goes here
    areaDictChoose, areaNumValid = areaDisp(Aero)
    print(f"{areaNumValid + 1}. QUIT GAME")
    userInput = int(input("> "))
    if userInput > 0 and userInput <= areaNumValid:
        print("")
        location = areaDictChoose[userInput]()
        location.scene(party)
    elif userInput == 0:
        statPrint(party)
    elif userInput == areaNumValid + 1:
        break
    else:
        print("")
        print("Invalid Input.")

print("")
print("======================")
print("Thank you for playing!")
print("======================")
