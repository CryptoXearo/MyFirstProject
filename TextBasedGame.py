# Stephen Stanberry

# Importing some modules.
from os import environ
from time import sleep

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'  # Deletes the support prompt from pygame.

import pygame  # Imports pygame module.

pygame.mixer.init()  # Initializes pygame music mixer.

# Sound Easter Egg. PLEASE SAVE BOTH AUDIO FILES ATTACHED TO THE HOMEWORK SUBMISSION, PUT THEM ON YOUR DESKTOP AND CHANGE THE FILE TARGET TO WHERE THE FILES ARE LOCATION ON YOUR MACHINE.
alienSound = pygame.mixer.Sound('E:\8bitsounds\The Essential Retro Video Game Sound Effects Collection [512 sounds] By Juhani Junkala\Death Screams\Alien\sfx_deathscream_alien1.wav')

# Intro music. CHANGE FILE TARGET.
pygame.mixer.music.load('E:\8bitsounds\comix-zone-theme-tune.wav')
pygame.mixer.music.play(loops=1)


# A dictionary to hold all the rooms, how they connect and what items may be in them.
rooms = {
    'Loading Dock': {
        'north': 'Mainframe Room',
        'west': 'Hallway 1',
        'east': 'Hallway 2'
    },
    'Mainframe Room': {
        'south': 'Loading Dock',
        'item': 'Data Module'
    },
    'Hallway 1': {
        'north': 'Hallway 3',
        'east': 'Loading Dock',
        'item': 'Key 2'
    },
    'Hallway 3': {
        'north': 'Lab',
        'south': 'Hallway 1',
        'item': 'Key 4',
        'keyRequired': 'Key 3'
    },
    'Lab': {
        'south': 'Hallway 3',
        'item': 'Research Data & Boss Room Key Card',
        'keyRequired': 'Lab Key'
    },
    'Hallway 2': {
        'north': 'Hallway 4',
        'west': 'Loading Dock',
        'item': 'Key 3',
        'keyRequired': 'Key 2'
    },
    'Hallway 4': {
        'north': 'Bloody Hallway',
        'south': 'Hallway 2',
        'item': 'Lab Key',
        'keyRequired': 'Key 4'
    },
    'Bloody Hallway': {
        'west': 'Boss Room',
        'south': 'Hallway 4'
    },
    'Boss Room': {
        'east': 'Bloody Hallway',
        'villain': 'Alien Brood Mother',
        'keyRequired': 'Research Data & Boss Room Key Card'
    }
}

# A dictionary to hold all the items a player has to pick up and put into his inventory.
playerInventory = []

# A dictionary to hold all the flavor text for what the player sees in each room.
roomDescriptions = {
        'Loading Dock':     'The scene there is horrendous. Scientists, civilians, and combat personnel alike ripped\n'
                            'limb from limb. Some managing to get to the escape pods before being lathed in two, or\n'
                            'worse. Eaten. From the looks of it, all the pods remain intact and not a single one is\n'
                            'missing. Must mean that nobody made it out alive. Time to find out what happened to the\n'
                            'crew here. You see doors to the north, east and west, which way do you want to go?\n'
                            '=========================================================================================',
        'Mainframe Room':   'As you walk into the room you see all sorts of computer based modules and instruments.\n'
                            'One of the computers looks like its going crazy with processing data, you decide to\n'
                            'approach it and when you do, the computer finalizes whatever data it was processing and\n'
                            'writes the data to the last functioning module, and ejects it far enough for you to\n'
                            'grab it and store it in your inventory. This has to have something valuable on it,\n'
                            'right? The only door available to go through is the one you came in from.\n'
                            '========================================================================================="\n'
                            'Would you like to pick up the item before leaving? If you already have the item, please\n'
                            'type a direction you want to go.\n'
                            '=========================================================================================',
        'Hallway 1':        'This hallway looks similar to most other hallways. Bodies, blood, limbs and broken\n'
                            'machinery all around. You see the occasional alien corpse as well. In this hallway you\n'
                            'spot a shining object hanging from one of the lights. Its a key, you might need this to\n'
                            'progress further into the space station. You see 2 doors, one to the north and one to the\n'
                            'east.\n'
                            '=========================================================================================\n'
                            'Would you like to pick up the item before leaving?\n'
                            '=========================================================================================',
        'Hallway 3':        'As you go into the next hallway, you notice the gore gets heavier and the stench of\n'
                            'death permeates the room and manages to penetrate the barrier that is your enclosed\n'
                            'battle skeleton. You see another key amidst a puddle of blood, mostly red with licks of\n'
                            'green. You are going to need this key to get into the next hallway. You see 2 doors, one\n'
                            'to the north and one to the south.\n'
                            '=========================================================================================\n'
                            'Would you like to pick up the item before leaving?\n'
                            '=========================================================================================',
        'Lab':              'You enter the lab to see what can only be described as the worst pile of death you have\n'
                            'ever seen. Not a single inch of that room is clean of blood or guts. You notice a small\n'
                            'older looking computer with notes written into a word app and a slouched over body\n'
                            'sitting at the desk in front of the computer. You shove the corpse off the chair and\n'
                            'take a seat and see a prompt asking if you want to save. You press yes on the screen\n'
                            'and out pops another module, this one you are guessing are notes from the researchers\n'
                            'and most likely valuable in nature. You take the module and notice that a bright yellow\n'
                            'key card has dropped out of the breast pocket of the lab coat the unknown corpse is wearing.\n'
                            'You see only one door to the south which is the door you just came through.\n'
                            '=========================================================================================\n'
                            'Would you like to pick up both the key card and module before leaving?\n'
                            '=========================================================================================',
        'Hallway 2':        'After grabbing a pipe hanging from the ceiling you break it the rest of the way off and\n'
                            'use it as a pry bar to open the jammed door. After some work and with a little luck, you\n'
                            'manage to open the door wide enough to squeeze through it and you come across a relatively\n'
                            'clean and undisturbed room. Hanging neatly in a key case is another key. You are going\n'
                            'to need it to progress further. You see 2 doors, one to the north and one to the west.\n'
                            '=========================================================================================\n'
                            'Would you like to pick up the item before leaving?\n'
                            '=========================================================================================',
        'Hallway 4':        'This hallway also looks like it has seen far less war than the other rooms. The only\n'
                            'sign of struggle in this room is the singular headless corpse hanging from the rafters.\n'
                            'Where their head went is beyond you. However there is a lanyard with a key on it hanging\n'
                            'from its left foot. The label on the lanyard reading "Lab Key". You see 2 doors, one to\n'
                            'the north and one to the South.\n'
                            '=========================================================================================\n'
                            'Would you like to pick up the item before leaving?\n'
                            '=========================================================================================',
        'Bloody Hallway':   'This hallway has countless corpses arranged in such a manner that it looks like they\n'
                            'are spelling out some sort of warning as if to say do not proceed further. You hear\n'
                            'high pitched screams and grunts coming from the next room. You see a single door to the \n'
                            'west. \n'
                            '=========================================================================================',
        'Boss Room':        'Against your better judgement you swipe the key card in front of the door panel and force\n'
                            'your terrified body to continue onward. The sounds grow louder as you enter the dimly lit\n'
                            'room. After a moment your eyes adjust to the virtually lightless room. What you see next\n'
                            'sends your heart into your stomach. There she is, the queen of this alien race that\n'
                            'annihilated your brethren. It looks as if she is in pain, and you soon find out why. She\n'
                            'is in labor and giving birth to more offspring to replenish what was lost during the\n'
                            'battle to take over this space station. The offspring already capable of combat begins to\n'
                            'charge you, you are frozen in fear and see your life flash before your eyes. However just\n'
                            'moments before the offspring were to end your life, the brood mother screams in a pitch\n'
                            'you have not heard before and with that the immature warrior stops dead in his tracks, not\n'
                            'daring to disobey the orders of the brood mother as he knows that would spell certain\n'
                            'death for itself. A moment goes by and you feel a tugging at the base of your skull. The\n'
                            'brood mother has finally found someone she can share a telepathic bond with, and with that\n'
                            'she is finally able to speak in a manner that a human can understand. "Spare me my last\n'
                            'moments before I pass on. We never meant for this to be a war. We were trying to reach\n'
                            'out for help as our planet was taken over by an unknown savage race of cyborgs that\n'
                            'have completely wiped us out. I have but enough energy to rear into this world the next\n'
                            'queen of our race. Please warrior, we seek to live peacefully with other beings and\n'
                            'she *the queen points to the freshly laid egg* is our last hope of survival". With\n'
                            'that the brood mother takes her last breath.\n'
                            'The egg still steaming begins to crack and finally breaks apart, what emerges is something\n'
                            'you never expected, something beyond beauty that words can describe. A being that is both\n'
                            'half of this xenomorphic alien race and half human. You can tell this creation is far more\n'
                            'powerful than anything you have ever faced. You go to grab your pistol, but its already\n'
                            'gone! Where is it? You look up to see this exotic creature inspecting the pistol as it\n'
                            'floats and gyrates in the air. But when did she manage to take it you ponder. She then\n'
                            'breaks eye contact with the pistol and makes contact with yours. "Well?" She asks.\n'
                            '"What are you going to do?" She flings the pistol at your feet with her telepathic\n'
                            'powers and stands there hands on her hips, awaiting your decision. Do you help nurture\n'
                            'this new being into what could be your most powerful ally? Or do you pick up the pistol\n'
                            'with the intent to kill?'
        }

# Variable Setup
userLocation = 'Loading Dock'
spawnMessage = 'You arrive at ' + userLocation
exitCommand = 'exit'
itemCommand = ['yes', 'no']
directions = ['north', 'south', 'east', 'west']
exitPrompt = 'You have exited the game.'
invalidDirection = 'You smash your helmet against the wall, not very bright are you?'
invalidInput = 'This is an invalid entry, try again cadet.'
takeItem = 'Do you want to take this item?'
navigateRequest = ('Type "North", "East", "South", or "West" to begin navigation.\n'
                   'Type "Inventory" to view your inventory.\n'
                   'Type "Yes" to pick up an item or "No" to ignore it.\n'
                   'Otherwise type "Exit" to end the game.')
spacer = '========================================================================================='
item = 'item'
locked = 'locked'
inventoryCommand = 'inventory'
nothingToPickUp = 'There is nothing here for you to pick up.'
newPlayerInventory = playerInventory
roomLocked = 'This door is locked and you do not have the correct key to open it.'
keyRequired = 'keyRequired'
itemAlreadyInInventory = 'The item is no longer there because its already in your inventory.'
noPickUp = ('You are going to need this item, but strangely enough you decided not to pick up the\n'
            'item, type "Yes" to pick it up instead.')

# Introduction and Instructions text
print(spacer)
print('Welcome to Total Annihilation')
print(spacer)
print('You are a space marine tasked with finding out what tragedy befell this space station.')
print('Explore the rooms, pick up the items and make your way to the final room.')
print(spacer)
print(spawnMessage)
print(spacer)
print(roomDescriptions['Loading Dock'])
print(navigateRequest)
print(spacer)


# Game Loop
while userLocation != 'Boss Room':
    userInput = input('Awaiting input...').casefold()  # Gets user input and makes sure that all comparisons are in lowercase.
    # Converts all strings and strings within lists to a single line of all the contained strings + Error Handling
    if userInput not in (directions + itemCommand + [exitCommand] + [inventoryCommand]):
        print(spacer)
        print(invalidInput)
        print(spacer)
        continue
    elif userInput in directions:
        if userInput not in rooms[userLocation]:
            print(spacer)
            print(invalidDirection)
            print(spacer)
            continue
    elif userInput == exitCommand:
        print(spacer)
        print(exitPrompt)
        print(spacer)
        break
    elif userInput in itemCommand:
        if userInput == 'no':
            print(spacer)
            print(noPickUp)
            print(spacer)
            continue

        # Error Handling within the player inventory.
        if rooms[userLocation][item] in playerInventory:
            print(spacer)
            print(itemAlreadyInInventory)
            print(spacer)
            continue

        # Get item and store in player inventory.
        playerInventory.append(rooms[userLocation][item])
        print(spacer)
        print('You have picked up the', rooms[userLocation][item])
        print(spacer)
        continue

        # Provides a way to check inventory.
    elif userInput == inventoryCommand:
        print(spacer)
        print('Your inventory currently contains :', newPlayerInventory)
        print(spacer)
        continue

    # Updating user location.
    nextRoom = rooms[userLocation][userInput]
    if keyRequired in rooms[nextRoom] and rooms[nextRoom][keyRequired] not in playerInventory:
        print(spacer)
        print(roomLocked)
        print(spacer)
    else:
        print(spacer)
        print('Now entering the', rooms[userLocation][userInput] + '.')
        userLocation = nextRoom
        print(spacer)
        print(roomDescriptions[nextRoom])
else:
    # Easter Egg
    string = roomDescriptions['Boss Room']
    splitFinalMessage = string.split('\n')
    firstNewSplitFinalMessage = '\n'.join(splitFinalMessage[0:20])
    print(firstNewSplitFinalMessage)
    input('Press Enter to Proceed.')
    alienSound.play()
    sleep(1.5)
    secondNewSplitFinalMessage = '\n'.join(splitFinalMessage[20:31])
    print(secondNewSplitFinalMessage)
