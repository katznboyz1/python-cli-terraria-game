import shutil, colorama, random, sys, os, time

colorama.Fore.BROWN = '\x1b[33m'
colorama.Back.BROWN = '\x1b[33m'

class game:
    def getClearScreenCommand() -> str: #how to clear all stdout from the screen
        if (sys.platform.lower() not in ['win32', 'win64']): #assume anything but windows is linux/unix
            return 'clear' #linux/unix clear command
        else:
            return 'cls' #windows clear command
    data = {} #the world data for the game
    def generateTerrainData(startingHeight = 0, maxHeight = 50, minHeight = -50, worldWidth = 2000) -> dict: #generate a new world using the parameters
        dataDict = {
            'meta':{
                'version':'1',
                'parameters':{
                    'startingHeight':startingHeight,
                    'maxHeight':maxHeight,
                    'minHeight':minHeight,
                    'worldWidth':worldWidth,
                }
            },
            'blocks':{

            },
            'placedBlocks':{

            },
            'character':{
                'position':[0, 0],
            },
        }
        groundLevel = startingHeight
        for x_coordinate in range(worldWidth): #iterate through each column
            dataDict['blocks'][x_coordinate] = {}
            for y_coordinate in range(minHeight, (maxHeight + 1)):
                block = 'LIGHTCYAN_EX' #uses colorama color codes
                if (y_coordinate > groundLevel): #is above the ground level
                    block = 'LIGHTCYAN_EX'
                else:
                    blocksBelowGroundLevel = groundLevel - y_coordinate
                    if (blocksBelowGroundLevel == 0):
                        block = 'GREEN' #is at the ground level
                    else:
                        block = 'LIGHTBLACK_EX' #stone level
                dataDict['blocks'][x_coordinate][y_coordinate] = block
            groundLevel += random.choice([-1, 0, 0, 0, 0, 1])
        return dataDict
    running = True #makes sure the game is still running
    screen = 'loading' #controls what page the program displays
    otherdata = {
        'loadingProgress':0, #the percentage that the game is stuck at loading - will be displayed on 'startscreen' screen
        'loadingStepCurrent':'not loading anything.', #the current thing that is loading - will be displayed on 'startscreen' screen
        'loadingProcesses':[['game.data = game.generateTerrainData()'], 0], #[[things to load], how many have been done so far + 1]
    }
    blockType = '\u2588'

lastOutput = 'Nothing'

while (game.running):
    os.system(game.getClearScreenCommand())
    screensize = shutil.get_terminal_size() #get the terminal size
    screensize = [screensize[0] - 1, screensize[1] - 2] #subtract 1 from the x to prevent overflow and 3 from the y to prevent overflow and leave room for the input
    skipInput = False #controls whether or not to skip the input on the bottom
    if (game.screen == 'loading'): #displays the loading info
        #this is a comment for the code below:
        #this basically centers the loading screen text in the terminal window
        try:
            game.otherdata['loadingProgress'] = int((len(game.otherdata['loadingProcesses'][0]) / game.otherdata['loadingProcesses'][1]) * 100)
        except ZeroDivisionError:
            game.otherdata['loadingProgress'] = 0
        textLines = 2
        topYCoord = int(screensize[1] / 2) - int(textLines / 2)
        sys.stdout.write('\n' * topYCoord)
        progressText1 = 'Loading game. | {}% done.'.format(game.otherdata['loadingProgress'])
        textWidth1 = len(progressText1)
        textPaddingX1 = int((screensize[0] - textWidth1) / 2)
        sys.stdout.write(str(' ' * textPaddingX1) + progressText1 + '\n')
        progressText2 = '({})'.format(game.otherdata['loadingStepCurrent'])
        textWidth2 = len(progressText1)
        textPaddingX2 = int((screensize[0] - textWidth2) / 2)
        sys.stdout.write(str(' ' * textPaddingX2) + progressText2 + '\n')
        leftOverLinesToFill = screensize[1] - (topYCoord - textLines)
        sys.stdout.write('\n' * leftOverLinesToFill)
        if (game.otherdata['loadingProgress'] < 100):
            exec(game.otherdata['loadingProcesses'][0][game.otherdata['loadingProcesses'][1]])
            game.otherdata['loadingProcesses'][1] += 1
        else:
            game.screen = 'ingame'
        skipInput = True
        time.sleep(0.25) #make it seem like its doing something because the users love that
    elif (game.screen == 'ingame'):
        characterPos = coords = [int(screensize[0] / 2), int(screensize[1] / 2)]
        screenData = ''
        screensize[1] -= 2 #make room for debug rows
        screenData += 'POS: {}\n'.format(str([int(screensize[0] / 2), int(screensize[1] / 2)]))
        for y_coordinate in range(screensize[1]):
            lastBlock = None
            for x_coordinate in range(screensize[0]):
                centerBlock = int((screensize[1] - 1) / 2)
                distanceFromCenter = -(y_coordinate - centerBlock) + game.data['character']['position'][1]
                isCenterCrosshair = False
                if (distanceFromCenter < game.data['meta']['parameters']['maxHeight'] and distanceFromCenter > game.data['meta']['parameters']['minHeight']):
                    blockType = game.data['blocks'][x_coordinate + characterPos[0]][distanceFromCenter]
                else:
                    blockType = 'BLACK'
                if (x_coordinate == int(screensize[0] / 2) and y_coordinate == int(screensize[1] / 2)):
                    isCenterCrosshair = True
                lastBlock = blockType
                if (not isCenterCrosshair):
                    screenData += str(eval('colorama.Fore.{}'.format(blockType)) + eval('colorama.Back.{}'.format(blockType)) + '\u2588' + colorama.Style.RESET_ALL)
                else:
                    screenData += str(eval('colorama.Back.{}'.format(blockType)) + colorama.Fore.BLUE + '+' + colorama.Style.RESET_ALL)
            screenData += '\n'
        screenData += '\n'
        screenData += 'Last Console Output: {}\n'.format(lastOutput)
        sys.stdout.write(screenData)
    elif (game.screen == 'help'):
        helpStuff = '''
Command list for cli-terraria.py:

    move-x <blocks> - Moves the player x blocks along the x-axis.
    move-y <blocks> - Moves the player x blocks along the y-axis.
    move <xblocks> <yblocks> - Moves the player x blocks along the y-axis and x blocks along the y axis.
    exit - Exits the game.
    help - Opens the help menu.
    game - Sets the screen go the game.
    placeblock - Places a block at the crosshair.
'''
        sys.stdout.write(helpStuff)
        leftOverLines = screensize[1] - helpStuff.count('\n')
        if (leftOverLines > 0):
            sys.stdout.write('\n' * leftOverLines)
    if (skipInput == False):
        command = input('cli-terraria> ') #gather user input for the next action
        if (command.split(' ')[0] == 'exit'): #the player typed in 'exit' on the input above
            exit()
        elif (command.split(' ')[0] == 'move-x'):
            try:
                amount = int(command.split(' ')[1])
                game.data['character']['position'][0] += amount
                lastOutput = 'Moved the character {} units along the X axis.'.format(str(amount))
            except ValueError:
                lastOutput = 'Invalid value for "move-x": "{}"'.format(command.split(' ')[1])
        elif (command.split(' ')[0] == 'move-y'):
            try:
                amount = int(command.split(' ')[1])
                game.data['character']['position'][1] += amount
                lastOutput = 'Moved the character {} units along the Y axis.'.format(str(amount))
            except ValueError:
                lastOutput = 'Invalid value for "move-x": "{}"'.format(command.split(' ')[1])
        elif (command.split(' ')[0] == 'help'):
            game.screen = 'help'
        elif (command.split(' ')[0] == 'game'):
            game.screen = 'ingame'
        elif (command.split(' ')[0] == 'move'):
            try:
                xamount = int(command.split(' ')[1])
                yamount = int(command.split(' ')[2])
                game.data['character']['position'][0] += xamount
                game.data['character']['position'][1] += yamount
                lastOutput = 'Moved the character [{}, {}] units'.format(xamount, yamount)
            except ValueError:
                lastOutput = 'Invalid value(s) for "move"'
        elif (command.split(' ')[0] == 'placeblock'):
            coords = [int(screensize[0] / 2), int(screensize[1] / 2)]
            lastOutput = 'Placed a block at: [{},{}].'.format(str(coords[0] + game.data['character']['position'][0]), str(coords[1]))
            #add the block to the placedBlocks dict