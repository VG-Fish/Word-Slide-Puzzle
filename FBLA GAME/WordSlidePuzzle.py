import sys, os, Button, math as m, random as r, pygame as game, pygame.freetype, pygame_textinput as pyti
from pygame.locals import *
from pygame import mixer

# Create the constants (go ahead and experiment with different values)
BOARDHEIGHT, BOARDWIDTH = 4, 4 #temp values
TILESIZE = 80
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 30
BLANK = None
WORDSLEN1, WORDSLEN2 = [], []

#               R   G   B
PRUSSIANBLUE = (29, 53, 87) 
HONEYDEW =     (241, 250, 238) 
CELADONBLUE =  (69, 123, 157) 
POWDERBLUE  =  (168, 218, 220) 
IMPERIALRED =  (230, 57, 70) 

BACKGROUNDCOLOR = POWDERBLUE
TILECOLOR = IMPERIALRED
TEXTCOLOR = HONEYDEW
BORDERCOLOR = CELADONBLUE
TILEFONTSIZE = 40
BASICFONTSIZE = 20
SMALLFONTSIZE = 25

BUTTONCOLOR = HONEYDEW
BUTTONTEXTCOLOR = PRUSSIANBLUE
MESSAGECOLOR = HONEYDEW

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

game.mixer.init()
blockSound1 = mixer.Sound("Sounds/Block.wav")
blockSound2 = mixer.Sound("Sounds/Block2.wav")
blockSound3 = mixer.Sound("Sounds/Block3.wav")
selectSound = mixer.Sound("Sounds/Select.wav")
sounds = [blockSound1, blockSound2, blockSound3]

def main():
    global SOUND, BOARDHEIGHT, BOARDWIDTH, FPSCLOCK, DISPLAYSURF, TEXTFONT, TILEFONT, SMALLFONT, RESET_SURF, RESET_RECT, NEW_SURF, NEW_RECT, SOLVE_SURF, SOLVE_RECT, XMARGIN, YMARGIN, WORDSLEN1, WORDSLEN2, LETTERPOSITIONS

    #create game window
    icon = game.image.load("logo.tiff")
    game.display.set_icon(icon)
    mixer.music.load("Game_song.m4a") 
    mixer.music.play(-1)
    screen = game.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    game.display.set_caption("Main Menu")

    #game variables
    scroll=0
    game_paused = True
    menu_state = "main"
    tiles= m.ceil(SCREEN_WIDTH / SCREEN_HEIGHT)+1
    FPS=60
    clock=game.time.Clock()
    bg=game.image.load("menubackground.jpeg").convert()
    bg_rect=bg.get_rect()
    SOUND = True

    #define fonts
    game.font.init()
    font = game.font.SysFont("arialblack", 40)

    #define colours
    TEXT_COL = (255, 255, 255)

    #load button images
    back_img = game.image.load('Buttons/button_back.png').convert_alpha() #back
    resume_img = game.image.load("Buttons/button_resume.png").convert_alpha() #resume
    options_img = game.image.load("Buttons/button_play.png").convert_alpha() #options
    quit_img = game.image.load("Buttons/button_quit.png").convert_alpha() #quit
    play_img = game.image.load('Buttons/button_play.png').convert_alpha() #play
    threeBoardSize_img = game.image.load('Buttons/button_easy-x.png').convert_alpha() #easy mode
    fourBoardSize_img = game.image.load('Buttons/button_medium-x.png').convert_alpha() #medium mode
    fiveBoardSize_img = game.image.load('Buttons/button_hard-x.png').convert_alpha() #hard mode
    sound_img = game.image.load('Buttons/button_sound.png').convert_alpha() #sound mode
    sound_img = game.image.load('Buttons/button_sound.png').convert_alpha() #sound mode
    logo_img = game.image.load('logo.tiff').convert_alpha() #sound mode

    #create button instances
    resume_button = Button.Button(304, 75, resume_img, 1)
    options_button = Button.Button(304, 300, options_img, 1)
    quit_button = Button.Button(304, 500, quit_img, 1)
    play_button = Button.Button(300, 475, play_img, 1)
    threeBoardSize_button = Button.Button(300, 100, threeBoardSize_img, 1)
    fourBoardSize_button = Button.Button(300, 225, fourBoardSize_img, 1)
    fiveBoardSize_button = Button.Button(300, 350, fiveBoardSize_img, 1)
    back_button = Button.Button(550, 525, back_img, 1)
    sound_button = Button.Button(304, 400, sound_img, 1)
    logo_button = Button.Button(226, 20, logo_img, 1)

    #game loop
    run = True
    count = 0
    while run:
        clock.tick(FPS)

        #set up background:
        for i in range(0,tiles):
            screen.blit(bg,(i*SCREEN_WIDTH+scroll,0))
            bg_rect.x=i*SCREEN_WIDTH+scroll

        #scroll background
        scroll-=.75

        #reset scroll:
        if abs(scroll)>SCREEN_WIDTH:
            scroll=0

        #check if game is paused
        if game_paused == True:
            #check menu state
            game.freetype.init()
            tutorial = game.draw.rect(screen, (196, 164, 132), (0,95,230,190))
            tutorialFont = game.freetype.Font('funtauna11/FuntaunaBold.otf')
            tutorialFont.render_to(screen, (0,100),"""          TUTORIAL """, (255,255,255), (196,164,132), 1, 0, 20)
            tutorialFont.render_to(screen, (0,120),"""Click or use the arrow """, (255,255,255), (196,164,132), 1, 0, 20)
            tutorialFont.render_to(screen, (0,140),"""keys to move the letter""", (255,255,255), (196,164,132), 1, 0, 20)
            tutorialFont.render_to(screen, (0,160),"""tiles around. Try to """, (255,255,255), (196,164,132), 1, 0, 20)
            tutorialFont.render_to(screen, (0,180),"""move all the letters to """, (255,255,255), (196,164,132), 1, 0, 20)
            tutorialFont.render_to(screen, (0,200),"""form the correct words """, (255,255,255), (196,164,132), 1, 0, 20)
            tutorialFont.render_to(screen, (0,220),"""in the least moves """, (255,255,255), (196,164,132), 1, 0, 20)
            tutorialFont.render_to(screen, (0,240),"""possible to get""", (255,255,255), (196,164,132), 1, 0, 20)
            tutorialFont.render_to(screen, (0,260),"""lowest score. Enjoy!""", (255,255,255), (196,164,132), 1, 0, 20)
            leadorBoard = game.draw.rect(screen, (196, 164, 132), (580,100,230,200))
            tutorialFont.render_to(screen, (610,100),"""       LeadorBoard  """, (255,255,255), (196,164,132), 1, 0, 20)
            leadorBoardTextDisplay = pygame.freetype.Font("funtauna11/FuntaunaBold.otf", 20)
            file = open("highscore.txt", "r")
            read = file.readlines()
            data = sorted(read)
            leadorBoardTextDisplay.render_to(screen,(590,120),f"{str(1)}\t{str(data[0])}",(255,255,255))
            leadorBoardTextDisplay.render_to(screen,(590,155),f"{str(2)}\t{str(data[1])}",(255,255,255))
            leadorBoardTextDisplay.render_to(screen,(590,190),f"{str(3)}\t{str(data[2])}",(255,255,255))
            leadorBoardTextDisplay.render_to(screen,(590,225),f"{str(4)}\t{str(data[3])}",(255,255,255))
            leadorBoardTextDisplay.render_to(screen,(590,260),f"{str(5)}\t{str(data[4])}",(255,255,255))
            file.close()
            if menu_state == "main":
            #draw pause screen buttons
                if logo_button.draw(screen):
                    print("Baguette Boi lives forever!!!")
                if options_button.draw(screen):
                    playRandom() 
                    menu_state = "options"
                elif quit_button.draw(screen):
                    playRandom() 
                    run = False
                elif sound_button.draw(screen):
                    if count == 1:
                        SOUND = False
                        count = 0
                    else:
                        SOUND = True
                        count = 1
                    playRandom() 
            #check if the options menu is open
            if menu_state == "options":
            #draw the different options buttons
                if threeBoardSize_button.draw(screen):
                    playRandom() 
                    BOARDWIDTH, BOARDHEIGHT = 3, 3
                elif fourBoardSize_button.draw(screen):
                    playRandom() 
                    BOARDWIDTH, BOARDHEIGHT = 4, 4 
                elif fiveBoardSize_button.draw(screen):
                    playRandom() 
                    BOARDWIDTH, BOARDHEIGHT = 5, 5
                elif back_button.draw(screen):
                    playRandom()
                    menu_state = "main"
                #fix this, goes to board screen not menu
                elif play_button.draw(screen):
                    run = False
                    play = True
                    game_paused = False

        #event handler
        for event in game.event.get():
            if event.type == game.KEYDOWN:
                if event.key == game.K_SPACE:
                    game_paused = True
            elif event.type == game.QUIT:
                quit = False
        game.display.update()

    if play:
        with open("dictionary/popular.txt", "r") as file:
            for line in file.readlines():
                line = line.strip()
                if len(line) == BOARDWIDTH and any(i.isupper() for i in line) == False and line.isalpha() == True:
                    WORDSLEN1.append(line.split("=")[-1].strip())
                elif len(line) == BOARDWIDTH-1 and any(i.isupper() for i in line) == False and line.isalpha() == True:
                    WORDSLEN2.append(line.split("=")[-1].strip()) 
        randomWords, randomWordsDict = [], {}
        for i in range(BOARDWIDTH-1):
                randomWords.append("".join(r.sample(WORDSLEN1, 1)))
        randomWords.append("".join(r.sample(WORDSLEN2, 1)))
        randomWords.append(" ")

    #puts the words as a key and the index in random words for the randomWordsDict dictionary and makes sure not to put " " as a key
        for i, j in enumerate(randomWords):
            if j != " ":
                randomWordsDict[j] = i

#gets the index of all the letters of each word after the list(randomWords) is combined in a string
        tempRandomWords = "".join(randomWords)
        LETTERPOSITIONS = dict(enumerate(tempRandomWords[:-1], start = 1))
        LETTERPOSITIONS[None] = ""

        XMARGIN = int((SCREEN_WIDTH - (TILESIZE * BOARDWIDTH + (BOARDWIDTH - 1))) / 2)
        YMARGIN = int((SCREEN_HEIGHT - (TILESIZE * BOARDHEIGHT + (BOARDHEIGHT - 1))) / 2)

        FPSCLOCK = game.time.Clock()
        DISPLAYSURF = game.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        game.display.set_caption('Slide Puzzle')
        TEXTFONT = game.font.Font('funtauna11/FuntaunaBold.otf', BASICFONTSIZE)
        TILEFONT = game.font.Font('funtauna11/FuntaunaBold.otf', TILEFONTSIZE)
        SMALLFONT = game.font.Font('funtauna11/FuntaunaBold.otf', SMALLFONTSIZE)

        # Store the option buttons and their rectangles in OPTIONS.
        RESET_SURF, RESET_RECT = makeText('Reset',    TEXTCOLOR, TILECOLOR, SCREEN_WIDTH - 120, SCREEN_HEIGHT - 90)
        NEW_SURF,   NEW_RECT   = makeText('New Game', TEXTCOLOR, TILECOLOR, SCREEN_WIDTH - 120, SCREEN_HEIGHT - 60)
        SOLVE_SURF, SOLVE_RECT = makeText('Solve',    TEXTCOLOR, TILECOLOR, SCREEN_WIDTH - 120, SCREEN_HEIGHT - 30)

        mainBoard, solutionSeq = generateNewPuzzle(50) #change to text input later
        SOLVEDBOARD = getStartingBoard() # a solved board is the same as the board in a start state.
        allMoves = [] # list of moves made from the solved configuration

        while True: # main game loop
            slideTo = None # the direction, if any, a tile should slide
            msg = 'Click near space or press arrow keys to slide. Your current score is: ' + str(len(allMoves))# contains the message to show in the upper left corner.
            if mainBoard == SOLVEDBOARD and len(allMoves) != 0:
                msg = 'Solved! Your final score is: ' + str(len(allMoves))
                leadorBoardManager = pyti.TextInputManager(validator = lambda input: len(input) <= 10)
                # Pass these to constructor
                leadorBoardText = pyti.TextInputVisualizer(manager=leadorBoardManager, font_object=font)
                leaderBoardScreen = game.display.set_mode((300, 75))
                clock = game.time.Clock()
                # game now allows natively to enable key repeat:
                game.key.set_repeat(200, 25)
                leadorBoardRun = True
                while leadorBoardRun:
                    leaderBoardScreen.fill(POWDERBLUE)
                    events = game.event.get()
                    # Feed it with events every frame
                    leadorBoardText.update(events)
                    # Get its surface to blit onto the screen
                    leaderBoardScreen.blit(leadorBoardText.surface, (10, 10))
                    # Modify attributes on the fly - the surface is only rerendered when .surface is accessed & if values changed
                    leadorBoardText.font_color = IMPERIALRED
                    # Check if user is exiting or pressed return
                    for event in events:
                        if event.type == game.QUIT:
                            exit()
                        if event.type == game.KEYDOWN and event.key == game.K_RETURN:
                            file = open("highscore.txt", "a")
                            if int(len(allMoves)) < 10:
                                score_val = str(len(allMoves))
                                score_val = score_val.zfill(4)
                                leadorBoardRun = False
                            elif int(len(allMoves)) <100:
                                score_val = str(len(allMoves))
                                score_val = score_val.zfill(4)
                                leadorBoardRun = False
                            file.write(str(score_val)+" "+leadorBoardManager.value+"\n")
                            file.close()
                        game.display.update()
                        clock.tick(30)
                        if leadorBoardRun == False:
                            break
                DISPLAYSURF = game.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                mainBoard, solutionSeq = generateNewPuzzle(50)

            drawBoard(mainBoard, msg)
            checkForQuit()
            for event in game.event.get(): # event handling loop
                if event.type == MOUSEBUTTONUP:
                    spotx, spoty = getSpotClicked(mainBoard, event.pos[0], event.pos[1])
                    if (spotx, spoty) == (None, None):
                    # check if the user clicked on an option button
                        if RESET_RECT.collidepoint(event.pos):
                            resetAnimation(mainBoard, allMoves) # clicked on Reset button
                            allMoves = []
                        elif NEW_RECT.collidepoint(event.pos):
                            mainBoard, solutionSeq = generateNewPuzzle(50) # clicked on New Game button
                            allMoves = []
                        elif SOLVE_RECT.collidepoint(event.pos):
                            resetAnimation(mainBoard, solutionSeq + allMoves) # clicked on Solve button
                            allMoves = []
                    else:
                        # check if the clicked tile was next to the blank spot
                        blankx, blanky = getBlankPosition(mainBoard)
                        if spotx == blankx + 1 and spoty == blanky:
                            playRandom() 
                            slideTo = LEFT
                        elif spotx == blankx - 1 and spoty == blanky:
                            playRandom() 
                            slideTo = RIGHT
                        elif spotx == blankx and spoty == blanky + 1:
                            playRandom() 
                            if SOUND == True:
                                selectSound.play()
                            slideTo = UP
                        elif spotx == blankx and spoty == blanky - 1:
                            playRandom() 
                            slideTo = DOWN

                elif event.type == KEYUP:
                    # check if the user pressed a key to slide a tile
                    if event.key in (K_LEFT, K_a) and isValidMove(mainBoard, LEFT):
                        playRandom()
                        slideTo = LEFT
                    elif event.key in (K_RIGHT, K_d) and isValidMove(mainBoard, RIGHT):
                        playRandom()
                        slideTo = RIGHT
                    elif event.key in (K_UP, K_w) and isValidMove(mainBoard, UP):
                        playRandom()
                        slideTo = UP
                    elif event.key in (K_DOWN, K_s) and isValidMove(mainBoard, DOWN):
                        playRandom() 
                        slideTo = DOWN

            if slideTo:
                slideAnimation(mainBoard, slideTo, 'Click near space or press arrow keys to slide.', 8) # show slide on screen
                makeMove(mainBoard, slideTo)
                allMoves.append(slideTo) # record the slide
            game.display.update()
            FPSCLOCK.tick(FPS)
    elif not quit:
        terminate()

def playRandom():
    if SOUND == True:
        r.choice(sounds).play()

def terminate():
    game.quit()
    sys.exit()


def checkForQuit():
    for event in game.event.get(QUIT): # get all the QUIT events
        terminate() # terminate if any QUIT events are present
    for event in game.event.get(KEYUP): # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate() # terminate if the KEYUP event was for the Esc key
        game.event.post(event) # put the other KEYUP event objects back

   

def getStartingBoard():
    # Return a board data structure with tiles in the solved state.
    # For example, if BOARDWIDTH and BOARDHEIGHT are both 3, this function
    # returns [[1, 4, 7], [2, 5, 8], [3, 6, BLANK]]
    counter = 1
    board = []
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGHT):
            column.append(counter)
            counter += BOARDWIDTH
        board.append(column)
        counter -= BOARDWIDTH * (BOARDHEIGHT - 1) + BOARDWIDTH - 1
    board[BOARDWIDTH-1][BOARDHEIGHT-1] = BLANK
    return board


def getBlankPosition(board):
    # Return the x and y of board coordinates of the blank space.
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if board[x][y] == BLANK:
                return (x, y)


def makeMove(board, move):
    # This function does not check if the move is valid.
    blankx, blanky = getBlankPosition(board)

    if move == UP:
        board[blankx][blanky], board[blankx][blanky + 1] = board[blankx][blanky + 1], board[blankx][blanky]
    elif move == DOWN:
        board[blankx][blanky], board[blankx][blanky - 1] = board[blankx][blanky - 1], board[blankx][blanky]
    elif move == LEFT:
        board[blankx][blanky], board[blankx + 1][blanky] = board[blankx + 1][blanky], board[blankx][blanky]
    elif move == RIGHT:
        board[blankx][blanky], board[blankx - 1][blanky] = board[blankx - 1][blanky], board[blankx][blanky]


def isValidMove(board, move):
    blankx, blanky = getBlankPosition(board)
    return (move == UP and blanky != len(board[0]) - 1) or \
           (move == DOWN and blanky != 0) or \
           (move == LEFT and blankx != len(board) - 1) or \
           (move == RIGHT and blankx != 0)


def getRandomMove(board, lastMove=None):
    # start with a full list of all four moves
    validMoves = [UP, DOWN, LEFT, RIGHT]

    # remove moves from the list as they are disqualified
    if lastMove == UP or not isValidMove(board, DOWN):
        validMoves.remove(DOWN)
    if lastMove == DOWN or not isValidMove(board, UP):
        validMoves.remove(UP)
    if lastMove == LEFT or not isValidMove(board, RIGHT):
        validMoves.remove(RIGHT)
    if lastMove == RIGHT or not isValidMove(board, LEFT):
        validMoves.remove(LEFT)

    # return a random move from the list of remaining moves
    return r.choice(validMoves)


def getLeftTopOfTile(tileX, tileY):
    left = XMARGIN + (tileX * TILESIZE) + (tileX - 1)
    top = YMARGIN + (tileY * TILESIZE) + (tileY - 1)
    return (left, top)


def getSpotClicked(board, x, y):
    # from the x & y pixel coordinates, get the x & y board coordinates
    for tileX in range(len(board)):
        for tileY in range(len(board[0])):
            left, top = getLeftTopOfTile(tileX, tileY)
            tileRect = game.Rect(left, top, TILESIZE, TILESIZE)
            if tileRect.collidepoint(x, y):
                return (tileX, tileY)
    return (None, None)


def drawTile(tilex, tiley, number, adjx=0, adjy=0):
    # draw a tile at board coordinates tilex and tiley, optionally a few
    # pixels over (determined by adjx and adjy)
    left, top = getLeftTopOfTile(tilex, tiley)
    game.draw.rect(DISPLAYSURF, TILECOLOR, (left + adjx, top + adjy, TILESIZE, TILESIZE))

    letter = LETTERPOSITIONS.get(number)
    letterSurf = TILEFONT.render(letter, True, TEXTCOLOR)
    letterRect = letterSurf.get_rect()
    letterRect.center = left + int(TILESIZE / 2) + adjx, top + int(TILESIZE / 2) + adjy
    DISPLAYSURF.blit(letterSurf, letterRect)
    
    textSurf = SMALLFONT.render(str(number), True, TEXTCOLOR)
    textRect = textSurf.get_rect()
    textRect.bottomright = left + int(TILESIZE / 1) + adjx, top + int(TILESIZE / 1) + adjy
    DISPLAYSURF.blit(textSurf, textRect)



def makeText(text, color, bgcolor, top, left):
    # create the Surface and Rect objects for some text.
    textSurf = TEXTFONT.render(text, True, color, bgcolor)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    return (textSurf, textRect)


def drawBoard(board, message):
    DISPLAYSURF.fill(BACKGROUNDCOLOR)
    if message:
        textSurf, textRect = makeText(message, MESSAGECOLOR, BACKGROUNDCOLOR, 5, 5)
        DISPLAYSURF.blit(textSurf, textRect)

    for tilex in range(len(board)):
        for tiley in range(len(board[0])):
            if board[tilex][tiley]:
                drawTile(tilex, tiley, board[tilex][tiley])

    left, top = getLeftTopOfTile(0, 0)
    width = BOARDWIDTH * TILESIZE
    height = BOARDHEIGHT * TILESIZE
    game.draw.rect(DISPLAYSURF, BORDERCOLOR, (left - 5, top - 5, width + 11, height + 11), 4)

    DISPLAYSURF.blit(RESET_SURF, RESET_RECT)
    DISPLAYSURF.blit(NEW_SURF, NEW_RECT)
    DISPLAYSURF.blit(SOLVE_SURF, SOLVE_RECT)


def slideAnimation(board, direction, message, animationSpeed):
    # Note: This function does not check if the move is valid.

    blankx, blanky = getBlankPosition(board)
    if direction == UP:
        movex = blankx
        movey = blanky + 1
    elif direction == DOWN:
        movex = blankx
        movey = blanky - 1
    elif direction == LEFT:
        movex = blankx + 1
        movey = blanky
    elif direction == RIGHT:
        movex = blankx - 1
        movey = blanky

    # prepare the base surface
    drawBoard(board, message)
    baseSurf = DISPLAYSURF.copy()
    # draw a blank space over the moving tile on the baseSurf Surface.
    moveLeft, moveTop = getLeftTopOfTile(movex, movey)
    game.draw.rect(baseSurf, BACKGROUNDCOLOR, (moveLeft, moveTop, TILESIZE, TILESIZE))

    for i in range(0, TILESIZE, animationSpeed):
        # animate the tile sliding over
        checkForQuit()
        DISPLAYSURF.blit(baseSurf, (0, 0))
        if direction == UP:
            drawTile(movex, movey, board[movex][movey], 0, -i)
        if direction == DOWN:
            drawTile(movex, movey, board[movex][movey], 0, i)
        if direction == LEFT:
            drawTile(movex, movey, board[movex][movey], -i, 0)
        if direction == RIGHT:
            drawTile(movex, movey, board[movex][movey], i, 0)

        game.display.update()
        FPSCLOCK.tick(FPS)

def generateNewPuzzle(numSlides):
    # From a starting configuration, make numSlides number of moves (and
    # animate these moves).
    sequence = []
    board = getStartingBoard()
    drawBoard(board, '')
    game.display.update()
    game.time.wait(500) # pause 500 milliseconds for effect
    lastMove = None
    for i in range(numSlides):
        move = getRandomMove(board, lastMove)
        slideAnimation(board, move, 'Generating new puzzle...', animationSpeed=int(TILESIZE / 2))
        makeMove(board, move)
        sequence.append(move)
        lastMove = move
    return (board, sequence)


def resetAnimation(board, allMoves):
    # make all of the moves in allMoves in reverse.
    revAllMoves = allMoves[:] # gets a copy of the list
    revAllMoves.reverse()

    for move in revAllMoves:
        if move == UP:
            oppositeMove = DOWN
        elif move == DOWN:
            oppositeMove = UP
        elif move == RIGHT:
            oppositeMove = LEFT
        elif move == LEFT:
            oppositeMove = RIGHT
        slideAnimation(board, oppositeMove, '', animationSpeed=int(TILESIZE / 2))
        makeMove(board, oppositeMove)
    
if __name__ == '__main__':
    main()