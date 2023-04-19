#import libraries
import sys, pygame, random, math
from pygame.locals import*

#initialize pygame core objects
pygame.init()
window = pygame.display.set_mode([501, 551])
pygame.display.set_caption("minefield maze")

# image importation
bat = pygame.image.load('12 hour challenge/img/bat.png')
comp = pygame.image.load('12 hour challenge/img/comp.png')
mine = pygame.image.load('12 hour challenge/img/mine.png')
sweeper = pygame.image.load('12 hour challenge/img/sweeper.png')
noSweeper = pygame.image.load('12 hour challenge/img/noSweeper.png')
trap = pygame.image.load('12 hour challenge/img/trap.png')
sand = pygame.image.load('12 hour challenge/img/sand.png')
path = pygame.image.load('12 hour challenge/img/path.png')



#declare the game grid
grid = []
for i in range(0,20):
    temp = []
    for j in range(0,20): temp.append([False, "", "?"])
    grid.append(temp)
#randomize the positions of objects
objLst = list(range(0,400))
random.shuffle(objLst)
playerPos = [objLst[0]%20,objLst[0]//20]
grid[playerPos[0]][playerPos[1]][0] = True
grid[objLst[1]%20][objLst[1]//20][1] = "e"
grid[objLst[2]%20][objLst[2]//20][1] = "c"
for i in range(3, 8):
    grid[objLst[i]%20][objLst[i]//20][1] = "b"
for i in range(8, 50):
    grid[objLst[i]%20][objLst[i]//20][1] = "m"
# randomize the rotation of individual batteries
batR = [random.randint(0,360),random.randint(0,360),random.randint(0,360),random.randint(0,360),random.randint(0,360),]
# final variable setup 
detectorUses = 10
score = 0
r = 0
start_ticks=pygame.time.get_ticks() - 500

# define function to get the number of mines surrounding a square given by x,y and flag central square with number and visible markers
def detect(x,y):
        global grid
        total = 0
        dirs = [[1,1],[1,-1],[1,0],[-1,1],[-1,0],[-1,-1],[0,-1],[0,1],[0,0]]
        for dir in dirs:
            if x + dir[0] in range(0,20) and y + dir[1] in range(0,20):
                if (grid[x + dir[0]][y + dir[1]][1] == "m"): total += 1
        grid[x][y][2] = str(total)
        grid[x][y][0] = True


# function definition for drawing a frame
def drawGame():
    global sweeper
    #overwrite previous draw and reset the count of batteries
    window.fill((0,0,0))
    batCount = 0
    # for each square
    for i in range(0,20):
        for j in range(0,20):
            # if the square has been investigated
            if grid[i][j][0] == True: 
                # draw path texture
                window.blit(path, (i*25, j*25))
                # check for confimed mine count and draw if present
                if grid[i][j][2] != "?":
                    font = pygame.font.SysFont(None, 40)
                    img = font.render(grid[i][j][2], True, (255,255,255))
                    window.blit(img, (i*25+5, j*25))

                # check for exposed mine and draw if present
                if grid[i][j][1] == "m":
                    pygame.draw.rect(window, (255,0,0), (i*25, j*25, 25,25))
                    window.blit(mine, (i*25+1, j*25))
                # check for exposed exit and draw if present
                if grid[i][j][1] == "e":
                    window.blit(trap, (i*25+1, j*25))
            # if the square has not been investigated, draw sand texture
            else:
                window.blit(sand, (i*25, j*25))
    # for each square again, draw a battery or compass if present over the top of the existing sprites
    for i in range(0,20):
        for j in range(0,20):
            if grid[i][j][1] == "b":
                window.blit(pygame.transform.rotate(bat, batR[batCount]), (i*25+2, j*25))
                batCount += 1
            if grid[i][j][1] == "c":
                window.blit(comp, (i*25+1, j*25))


    # draw line seperating the text from game
    pygame.draw.line(window, (0,0,0), (0,500),(500,500))
    # draw character on, and calculate if the detector should be up
    sweeperR = pygame.transform.rotate(sweeper, 90*r) if (pygame.time.get_ticks()-start_ticks < 500) else pygame.transform.rotate(noSweeper, 90*r)
    x = playerPos[0]*25 - (25 if (r == 2 and (pygame.time.get_ticks()-start_ticks < 500)) else 0)
    y = playerPos[1]*25 - (25 if (r == 1 and (pygame.time.get_ticks()-start_ticks < 500)) else 0)
    window.blit(sweeperR, (x, y))
    # write text at bottom of the screen
    font = pygame.font.SysFont(None, 40)
    img = font.render('Detector Battery: {}%'.format(str(math.floor(100*detectorUses/20))), True, (255,255,255))
    window.blit(img, (10,510))
    img = font.render('Score: {}'.format(score), True, (255,255,255))
    window.blit(img, (350,510))
    
    # update the screen
    pygame.display.flip()

# define function to check for collisions
def collisionCheck():
    # import vars
    global grid
    global playerPos
    global objLst
    global detectorUses
    global score
    global batR
    global r
    global start_ticks

    #check for collision with mine and quit if true
    if grid[playerPos[0]][playerPos[1]][1] == "m":
        quit()

    # if colliding with battery, increase detector battery by 10, ensuring it remains below 21 and remove battery
    if grid[playerPos[0]][playerPos[1]][1] == "b":
        detectorUses += 10
        if detectorUses > 20: detectorUses = 20
        grid[playerPos[0]][playerPos[1]][1] = ""
    # if colliding with compass, set investigated flag of exit to true
    if grid[playerPos[0]][playerPos[1]][1] == "c":
        grid[objLst[1]%20][objLst[1]//20][0] = True
    # if colliding with exit, reset all variables apart from score, which increments
    if grid[playerPos[0]][playerPos[1]][1] == "e":
        score += 1
        grid = []
        batR = [random.randint(0,360),random.randint(0,360),random.randint(0,360),random.randint(0,360),random.randint(0,360),]
        for i in range(0,20):
            temp = []
            for j in range(0,20): temp.append([False, "", "?"])
            grid.append(temp)

        objLst = list(range(0,400))
        random.shuffle(objLst)
        playerPos = [objLst[0]%20,objLst[0]//20]
        grid[playerPos[0]][playerPos[1]][0] = True
        grid[objLst[1]%20][objLst[1]//20][1] = "e"
        grid[objLst[2]%20][objLst[2]//20][1] = "c"
        for i in range(3, 8):
            grid[objLst[i]%20][objLst[i]//20][1] = "b"
        for i in range(8, 50):
            grid[objLst[i]%20][objLst[i]//20][1] = "m"
        detectorUses += 5
        if detectorUses > 20: detectorUses = 20
        r = 0
        start_ticks=pygame.time.get_ticks()-500
        

# mainloop
while True:
    drawGame()
    collisionCheck()



    # event handler
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            #switch on keypress
            match pygame.key.name(event.key):
                case "up":
                    # move player
                    playerPos[1] -= 1
                    # ensure player remains in play area
                    if playerPos[1] < 0: playerPos[1] = 0
                    # adject rotation
                    r = 1
                case "down":
                    playerPos[1] += 1
                    if playerPos[1] > 19: playerPos[1] = 19
                    r = 3
                case "left":
                    playerPos[0] -= 1
                    if playerPos[0] < 0: playerPos[0] = 0
                    r = 2
                case "right":
                    playerPos[0] += 1
                    if playerPos[0] >19: playerPos[0] = 19 
                    r = 0
                case "a":
                    # check there is battery left, and if so, investigate a square
                    if playerPos[0] -1 >= 0 and detectorUses > 0:
                        detectorUses -= 1
                        detect(playerPos[0]-1, playerPos[1])
                        # set rotation
                        r = 2
                        # set timer for detector coming down
                        start_ticks=pygame.time.get_ticks()
                case "d":
                    if playerPos[0] +1 <= 19 and detectorUses > 0:
                        detectorUses -= 1
                        detect(playerPos[0]+1, playerPos[1])
                        r = 0
                        start_ticks=pygame.time.get_ticks()
                case "w":
                    if playerPos[1] -1 >= 0 and detectorUses > 0:
                        detectorUses -= 1
                        detect(playerPos[0], playerPos[1]-1)
                        r = 1
                        start_ticks=pygame.time.get_ticks()
                case "s":
                    if playerPos[1] +1 <= 19 and detectorUses > 0:
                        detectorUses -= 1
                        detect(playerPos[0], playerPos[1]+1)
                        r = 3
                        start_ticks=pygame.time.get_ticks()
                
                case "return":
                    # check enough battery
                    if detectorUses > 6:
                        detectorUses -= 5
                        # for each adjacent square
                        dirs = [[1,1],[1,-1],[1,0],[-1,1],[-1,0],[-1,-1],[0,-1],[0,1], [0,0]]
                        for dir in dirs:
                            # check valid square
                            if playerPos[0] + dir[0] in range(0,20) and playerPos[1] + dir[1] in range(0,20):
                                # investigate it
                                detect(playerPos[0] + dir[0], playerPos[1] + dir[1])
                        # reset detector timer
                        start_ticks=pygame.time.get_ticks()
                # base case
                case _:
                    pass

            # set player's location to investigated (to catch movement onto squares which haven't been detected)
            grid[playerPos[0]][playerPos[1]][0] = True
            

        # catch quit events
        if event.type == QUIT:
            sys.exit(0)
        