import shutil, colorama, random, sys, os, time

class game:
    def getClearScreenCommand() -> str: #how to clear all stdout from the screen
        if (sys.platform.lower() not in ['win32', 'win64']): #assume anything but windows is linux/unix
            return 'clear' #linux/unix clear command
        else:
            return 'cls' #windows clear command
    data = {} #the world data for the game
    def generateTerrainData(startingHeight = 0, maxHeight = 20, minHeight = -20, worldWidth = 2000) -> dict: #generate a new world using the parameters
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
            groundLevel += random.choice([-1, 0, 0, 0, 1])
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
        characterPos = game.data['character']['position']
        screenData = ''
        screensize[1] -= 2 #make room for debug rows
        sys.stdout.write('POS: {}\n'.format(str(game.data['character']['position'])))
        for y_coordinate in range(screensize[1]):
            lastBlock = None
            for x_coordinate in range(screensize[0]):
                centerBlock = int((screensize[1] - 1) / 2)
                distanceFromCenter = -(y_coordinate - centerBlock)
                if (distanceFromCenter < game.data['meta']['parameters']['maxHeight'] and distanceFromCenter > game.data['meta']['parameters']['minHeight']):
                    blockType = game.data['blocks'][x_coordinate + characterPos[0]][distanceFromCenter]
                else:
                    blockType = 'BLACK'
                lastBlock = blockType
                screenData += str(eval('colorama.Fore.{}'.format(blockType)) + '\u2588' + colorama.Style.RESET_ALL)
            screenData += '\n'
        sys.stdout.write(screenData + '\n')
        sys.stdout.write('Last Console Output: {}\n'.format(lastOutput))
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
                pass