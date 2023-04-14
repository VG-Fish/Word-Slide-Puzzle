# credit to https://inventwithpython.com/pygame/chapter4.html for many sliding window puzzle code
import sys, os, Button, math as m, random as r, pygame as game, pygame.freetype, pygame_textinput as pyti, string as s
from pygame.locals import *
from pygame import mixer

BOARD_HEIGHT, BOARD_WIDTH = None, None 
TILE_SIZE = 80
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
BLANK = None
WORDS_LEN_1, WORDS_LEN_2 = [], []
num_slides = 1

#                R   G   B
PRUSSIAN_BLUE = (29, 53, 87) 
HONEYDEW =      (241, 250, 238) 
CELADON_BLUE =  (69, 123, 157) 
POWDER_BLUE  =  (168, 218, 220) 
IMPERIAL_RED =  (230, 57, 70) 
BEIGE =         (196,164,132)
DUSTY_ROSE =    (220, 174, 150)

BACKGROUND_COLOR = POWDER_BLUE
TILE_COLOR = IMPERIAL_RED
TEXT_COLOR = HONEYDEW
BORDER_COLOR = CELADON_BLUE
TILE_FONT_SIZE = 40
BASIC_FONT_SIZE = 20
SMALL_FONT_SIZE = 25
TEXT_COL = (255, 255, 255)

MESSAGE_COLOR = HONEYDEW

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

game.mixer.init()
blockSound1 = mixer.Sound("Assets/Sounds/Block.wav")
blockSound2 = mixer.Sound("Assets/Sounds/Block2.wav")
blockSound3 = mixer.Sound("Assets/Sounds/Block3.wav")
selectSound = mixer.Sound("Assets/Sounds/Select.wav")
sounds = [blockSound1, blockSound2, blockSound3]

def main_menu():
    global SOUND, BOARD_HEIGHT, BOARD_WIDTH, FPS_CLOCK, screen, TEXT_FONT, TILE_FONT, SMALL_FONT, RESET_SURF, \
        RESET_RECT, NEW_SURF, NEW_RECT, SOLVE_SURF, SOLVE_RECT, X_MARGIN, T_MARGIN, WORDS_LEN_1, WORDS_LEN_2, \
        LETTER_POSITIONS, game_back_button, font
    
    icon = game.image.load("Assets/game_images/app_icon.png")
    game.display.set_icon(icon)
    screen = game.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    game.display.set_caption("Main Menu")

    # game variables
    scroll = 0
    in_main_menu, single_player, ai_battle = True, False, False
    menu_state = "main"
    tiles = m.ceil(SCREEN_WIDTH / SCREEN_HEIGHT)+1
    FPS = 60
    clock = game.time.Clock()
    background = game.image.load("Assets/game_images/background.png").convert()
    background = game.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    background_rect = background.get_rect()
    SOUND = True

    # define fonts
    game.font.init()
    font = "Assets/funtauna11/FuntaunaBold.otf"

    # back
    back_img = game.image.load('Assets/more buttons/back.png').convert_alpha() 
    back_img = pygame.transform.smoothscale_by(back_img, 0.3)
    back_button = Button.Button(625, 475, back_img, 1)

    # resume 
    resume_img = game.image.load("Assets/buttons/resume.png").convert_alpha() 
    resume_img = game.transform.smoothscale_by(resume_img, 0.25)
    resume_button = Button.Button(304, 75, resume_img, 1)

    # options 
    play_img2 = game.image.load('Assets/buttons/play.png').convert_alpha() 
    play_img2 = game.transform.smoothscale_by(play_img2, 0.25)
    play_button2 = Button.Button(304, 300, play_img2, 1)

    # quit
    quit_img = game.image.load("Assets/buttons/quit.png").convert_alpha() 
    quit_img = game.transform.smoothscale_by(quit_img, 0.25)
    quit_button = Button.Button(304, 500, quit_img, 1)

    # for controlling where easy, medium, hard, play, and ai_battle appear all at once
    current_x_pos = 12
    
    # easy mode
    threeBoardSize_img = game.image.load('Assets/more buttons/easy.png').convert_alpha()
    threeBoardSize_img = game.transform.smoothscale_by(threeBoardSize_img, 0.25)
    threeBoardSize_button = Button.Button(300, current_x_pos, threeBoardSize_img, 1)
    current_x_pos += 125

    # medium mode
    fourBoardSize_img = game.image.load('Assets/more buttons/medium.png').convert_alpha()
    fourBoardSize_img = game.transform.smoothscale_by(fourBoardSize_img, 0.25)
    fourBoardSize_button = Button.Button(300, current_x_pos, fourBoardSize_img, 1)
    current_x_pos += 125

    # hard mode
    fiveBoardSize_img = game.image.load('Assets/more buttons/hard.png').convert_alpha() 
    fiveBoardSize_img = game.transform.smoothscale_by(fiveBoardSize_img, 0.25)
    fiveBoardSize_button = Button.Button(300, current_x_pos, fiveBoardSize_img, 1)
    current_x_pos += 125

    # play
    play_img = game.image.load('Assets/buttons/play.png').convert_alpha() 
    play_img = game.transform.smoothscale_by(play_img, 0.25)
    play_button = Button.Button(300, current_x_pos, play_img, 1)
    current_x_pos += 125

    # battle ai button
    battle_ai_img = game.image.load("Assets/more buttons/battleai.png").convert_alpha()
    battle_ai_img = pygame.transform.smoothscale_by(battle_ai_img, 0.25)
    battle_ai_button = Button.Button(300, current_x_pos, battle_ai_img, 1)

    # sound 
    sound_img = game.image.load('Assets/buttons/Sound.png').convert_alpha() 
    sound_img = game.transform.smoothscale_by(sound_img, 0.25)
    sound_button = Button.Button(375, 400, sound_img, 1)

    # logo
    logo_img = game.image.load("Assets/game_images/logo.png").convert_alpha() 
    logo_img = game.transform.smoothscale_by(logo_img, 0.4)
    logo_button = Button.Button(200, 10, logo_img, 1)

    # tutorial
    tutorial_img = game.image.load('Assets/buttons/tutorial.png').convert_alpha() 
    tutorial_img = pygame.transform.smoothscale_by(tutorial_img, 0.22)
    tutorial_button = Button.Button(50, 400, tutorial_img, 1)

    # leader board
    leader_board_img = game.image.load("Assets/buttons/leaderboard.png").convert_alpha()
    leader_board_img = pygame.transform.smoothscale_by(leader_board_img, 0.25)
    leader_board_button = Button.Button(550, 400, leader_board_img, 1)
    
    # back button in game screen
    game_back_img = game.image.load("Assets/more buttons/exit.png").convert_alpha()
    game_back_img = pygame.transform.smoothscale_by(game_back_img, 0.25)
    game_back_button = Button.Button(0, 525, game_back_img, 1)

    global tile_colors_cherry
    tile_colors_cherry = import_tile_colors("cherry")

    # game loop
    chosen = False
    game.freetype.init()
    while in_main_menu:
        clock.tick(FPS)

        # set up background:
        for i in range(0, tiles):
            screen.blit(background, (i * SCREEN_WIDTH + scroll,0))
            background_rect.x = i * SCREEN_WIDTH + scroll

        # scroll background
        scroll -= .75
        # reset scroll:
        if abs(scroll) > SCREEN_WIDTH:
            scroll = 0

        if menu_state == "main":
        # draw pause screen buttons
            if logo_button.draw(screen):
                print("Baguette Boi lives forever!!!")
            if play_button2.draw(screen):
                playRandom() 
                menu_state = "options"
            elif quit_button.draw(screen):
                playRandom() 
                terminate()
            elif sound_button.draw(screen):
                SOUND = not SOUND
                playRandom() 
            elif leader_board_button.draw(screen):
                menu_state = "leader_board"
                playRandom() 
            elif tutorial_button.draw(screen):
                menu_state = "tutorial"
                playRandom() 

        if menu_state == "leader_board":
            game.display.set_caption("Leader Board")

            leaderBoard = game.draw.rect(screen, BEIGE, (200,100,400,400))
            leaderBoardTextDisplay = game.freetype.Font(font)
            leaderBoardTextDisplay.render_to(screen, (295, 105, 160), "Leader Board", TEXT_COL, size=35)
            leaderBoardTextDisplay.render_to(screen, (220, 150, 160), "Score   Name", TEXT_COL, size=30)

            with open("FBLA GAME/highscore.txt", "r") as f:
                increment_y = 185
                data = sorted([i for i in f.read().splitlines() if i])
                for i in range(15):
                    if i >= len(data):
                        break
                    space_idx = data[i].find(" ")
                    score, name = data[i][:space_idx], data[i][space_idx:]
                    leaderBoardTextDisplay.render_to(screen,(225,increment_y),"{} {} {}".format(score, " "*9, name),TEXT_COL, size=20)        
                    increment_y += 20
                    
            if back_button.draw(screen):
                playRandom()
                menu_state = "main"

        if menu_state == "tutorial":
            game.display.set_caption("Tutorial")
            game.draw.rect(screen, BEIGE, (282,50,300,250))
            tutorialFont = game.freetype.Font(font)
            tutorial_text = [" " * 13 + "TUTORIAL", "Click or use the arrow ", "keys to move the letter", \
                                "tiles around. Try to ", "move all the letters to ", "form the correct words ", \
                                "in the least moves ", "possible to get", "lowest score. Enjoy!"]

            increment_y = 60
            for i in tutorial_text:
                tutorialFont.render_to(screen, (320,increment_y), i, TEXT_COL, BEIGE, 1, 0, 20)
                increment_y += 25

            if back_button.draw(screen):
                playRandom()
                menu_state = "main"

        # check if the options menu is open
        if menu_state == "options":
        # draw the different options buttons
            if threeBoardSize_button.draw(screen):
                playRandom() 
                BOARD_WIDTH, BOARD_HEIGHT = 3, 3
                chosen = True
            elif fourBoardSize_button.draw(screen):
                playRandom() 
                BOARD_WIDTH, BOARD_HEIGHT = 4, 4 
                chosen = True
            elif fiveBoardSize_button.draw(screen):
                playRandom() 
                BOARD_WIDTH, BOARD_HEIGHT = 5, 5
                chosen = True
            elif back_button.draw(screen):
                playRandom()
                menu_state = "main"
            elif play_button.draw(screen) and chosen:
                in_main_menu = False
                single_player = True
            """elif battle_ai_button.draw(screen) and chosen:
                in_main_menu = False
                ai_battle = True"""

        # event handler
        for event in game.event.get():
            if event.type == game.KEYDOWN:
                if event.key == game.K_SPACE:
                    in_main_menu = True
            elif event.type == game.QUIT:
                terminate()
        game.display.update()

    initialize_variables()
    if single_player:
        single_main()
    """elif ai_battle:
        ai_main()"""

def initialize_variables():
    global  TEXT_FONT, X_MARGIN, T_MARGIN, LETTER_POSITIONS, TILE_FONT, TEXT_FONT, SMALL_FONT, RESET_RECT, RESET_SURF, \
            NEW_SURF, NEW_RECT, SOLVE_SURF, SOLVE_RECT, mainBoard, solutionSeq, SOLVED_BOARD, allMoves, FPS_CLOCK

    LETTER_POSITIONS = generate_new_words()

    X_MARGIN = (SCREEN_WIDTH - (TILE_SIZE * BOARD_WIDTH + (BOARD_WIDTH - 1))) // 2
    T_MARGIN = (SCREEN_HEIGHT - (TILE_SIZE * BOARD_HEIGHT + (BOARD_HEIGHT - 1))) // 2

    FPS_CLOCK = game.time.Clock()
    game.display.set_caption('Word Windows')
    TEXT_FONT = game.font.Font(font, BASIC_FONT_SIZE)
    TILE_FONT = game.font.Font(font, TILE_FONT_SIZE)
    SMALL_FONT = game.font.Font(font, SMALL_FONT_SIZE)

    # Store the option buttons and their rectangles in OPTIONS.
    RESET_SURF, RESET_RECT = makeText('Reset',    TEXT_COLOR, TILE_COLOR, SCREEN_WIDTH - 120, SCREEN_HEIGHT - 90)
    NEW_SURF,   NEW_RECT   = makeText('New Game', TEXT_COLOR, TILE_COLOR, SCREEN_WIDTH - 120, SCREEN_HEIGHT - 60)
    SOLVE_SURF, SOLVE_RECT = makeText('Solve',    TEXT_COLOR, TILE_COLOR, SCREEN_WIDTH - 120, SCREEN_HEIGHT - 30)

    mainBoard, solutionSeq = generateNewPuzzle(num_slides) 
    SOLVED_BOARD = getStartingBoard() # a solved board is the same as the board in a start state.
    allMoves = [] # list of moves made from the solved configuration

def single_main():
    global  TEXT_FONT, X_MARGIN, T_MARGIN, LETTER_POSITIONS, TILE_FONT, TEXT_FONT, SMALL_FONT, RESET_RECT, RESET_SURF, \
            NEW_SURF, NEW_RECT, SOLVE_SURF, SOLVE_RECT, mainBoard, solutionSeq, SOLVED_BOARD, allMoves, FPS_CLOCK

    while True: # main game loop 
        slideTo = None # the direction, if any, a tile should slide
        msg = f"Click near space or press arrow keys to slide. Your current score is: {len(allMoves)}" 

        if mainBoard == SOLVED_BOARD and len(allMoves):
            game.display.set_caption("Input Name")
            msg = f"Solved! Your final score is: {len(allMoves)}"

            leader_board_font = game.font.Font(font, 40)
            leaderBoardManager = pyti.TextInputManager(validator = lambda input: len(input) <= 20)
            leaderBoardText = pyti.TextInputVisualizer(manager=leaderBoardManager, font_object=leader_board_font)
            leaderBoardScreen = game.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

            clock = game.time.Clock()
            game.key.set_repeat(200, 25)

            leaderBoardRun = True
            while leaderBoardRun:
                leaderBoardScreen.fill(POWDER_BLUE)
                game.draw.rect(leaderBoardScreen, DUSTY_ROSE, (250,0,300,130))

                leader_board_font = game.freetype.Font(font)
                leader_board_text = ['Input your name to go on', 'the leaderboard.', 
                                     'Press Enter/Return when', 'you have finished.']
                increment_y = 0
                for i in leader_board_text:
                    leader_board_font.render_to(screen, (280, increment_y), i, TEXT_COL, DUSTY_ROSE, 1, 0, 20)
                    increment_y += 25
                leader_board_font.render_to(screen, (280, increment_y), msg[8:], TEXT_COL, DUSTY_ROSE, 1, 0, 20)

                game.draw.rect(leaderBoardScreen, DUSTY_ROSE, (0,175,180,30))
                leader_board_font.render_to(screen, (0, 180), "Start typing here: ", TEXT_COL, DUSTY_ROSE, 1, 0, 20)

                events = game.event.get()
                leaderBoardText.update(events)
        
                leaderBoardScreen.blit(leaderBoardText.surface, (185, 160))
                leaderBoardText.font_color = IMPERIAL_RED

                for event in events:
                    if event.type == game.QUIT:
                        terminate()
                    if event.type == game.KEYDOWN and event.key == game.K_RETURN:
                        with open("FBLA GAME/highscore.txt", "a") as file:
                            score_val = str(len(allMoves))
                            score_val = score_val.zfill(4)
                            leaderBoardRun = False
                            file.write(f"{score_val} {leaderBoardManager.value}\n")
                    game.display.update()
                    clock.tick(30)  

            LETTER_POSITIONS = generate_new_words()
            mainBoard, solutionSeq = generateNewPuzzle(num_slides) 

        drawBoard(mainBoard, msg)
        checkForQuit()

        for event in game.event.get(): # event handling loop
            if event.type == MOUSEBUTTONUP:
                spot_x, spot_y = getSpotClicked(mainBoard, event.pos[0], event.pos[1])
                if (spot_x, spot_y) == (None, None):
                # check if the user clicked on an option button
                    if RESET_RECT.collidepoint(event.pos):
                        resetAnimation(mainBoard, allMoves) # clicked on Reset button
                    elif NEW_RECT.collidepoint(event.pos):
                        mainBoard, solutionSeq = generateNewPuzzle(num_slides) 
                        LETTER_POSITIONS = generate_new_words()
                    elif SOLVE_RECT.collidepoint(event.pos):
                        resetAnimation(mainBoard, solutionSeq + allMoves) # clicked on Solve button
                    allMoves = []
                else:
                    # check if the clicked tile was next to the blank spot
                    blank_x, blank_y = getBlankPosition(mainBoard)
                    if spot_x == blank_x + 1 and spot_y == blank_y:
                        playRandom() 
                        slideTo = LEFT
                    elif spot_x == blank_x - 1 and spot_y == blank_y:
                        playRandom() 
                        slideTo = RIGHT
                    elif spot_x == blank_x and spot_y == blank_y + 1:
                        playRandom() 
                        if SOUND == True:
                            selectSound.play()
                        slideTo = UP
                    elif spot_x == blank_x and spot_y == blank_y - 1:
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
            slideAnimation(mainBoard, slideTo, 'Click near space or press arrow keys to slide.', 4) # show slide on screen
            makeMove(mainBoard, slideTo)
            allMoves.append(slideTo) # record the slide

        game.display.update()
        FPS_CLOCK.tick(FPS)


"""def ai_main(): 
    global  TEXT_FONT, X_MARGIN, T_MARGIN, LETTER_POSITIONS, TILE_FONT, TEXT_FONT, SMALL_FONT, RESET_RECT, RESET_SURF, \
            NEW_SURF, NEW_RECT, SOLVE_SURF, SOLVE_RECT, mainBoard, solutionSeq, SOLVED_BOARD, allMoves, FPS_CLOCK

    while True:
        slideTo = None # the direction, if any, a tile should slide
        msg = f"Click near space or press arrow keys to slide. Your current score is: {len(allMoves)}" 

        drawBoard(mainBoard, msg)
        checkForQuit()

        for event in game.event.get(): # event handling loop
            if event.type == MOUSEBUTTONUP:
                spot_x, spot_y = getSpotClicked(mainBoard, event.pos[0], event.pos[1])
                if (spot_x, spot_y) == (None, None):
                # check if the user clicked on an option button
                    if RESET_RECT.collidepoint(event.pos):
                        resetAnimation(mainBoard, allMoves) # clicked on Reset button
                    elif NEW_RECT.collidepoint(event.pos):
                        mainBoard, solutionSeq = generateNewPuzzle(num_slides) 
                        LETTER_POSITIONS = generate_new_words()
                    elif SOLVE_RECT.collidepoint(event.pos):
                        resetAnimation(mainBoard, solutionSeq + allMoves) # clicked on Solve button
                    allMoves = []
                else:
                    # check if the clicked tile was next to the blank spot
                    blank_x, blank_y = getBlankPosition(mainBoard)
                    if spot_x == blank_x + 1 and spot_y == blank_y:
                        playRandom() 
                        slideTo = LEFT
                    elif spot_x == blank_x - 1 and spot_y == blank_y:
                        playRandom() 
                        slideTo = RIGHT
                    elif spot_x == blank_x and spot_y == blank_y + 1:
                        playRandom() 
                        if SOUND == True:
                            selectSound.play()
                        slideTo = UP
                    elif spot_x == blank_x and spot_y == blank_y - 1:
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
            slideAnimation(mainBoard, slideTo, 'Click near space or press arrow keys to slide.', 4) # show slide on screen
            makeMove(mainBoard, slideTo)
            allMoves.append(slideTo) # record the slide

        game.display.update()
        FPS_CLOCK.tick(FPS)"""

def import_tile_colors(color):
    temp = {}
    letters = s.ascii_uppercase
    for i in range(26):
        temp_img = game.image.load(f'Assets/{color}_color_theme/{letters[i]}.png').convert_alpha() 
        temp_img = pygame.transform.smoothscale_by(temp_img, .32)
        temp[letters[i].lower()] = temp_img
    
    return temp

def generate_new_words():
    with open("Assets/dictionary/popular.txt", "r") as f:
        for line in f.readlines():
            line = line.strip()
            if len(line) == BOARD_WIDTH and not any(i.isupper() for i in line) and line.isalpha():
                WORDS_LEN_1.append(line.split("=")[-1].strip())
            elif len(line) == BOARD_WIDTH-1 and not any(i.isupper() for i in line) and line.isalpha():
                WORDS_LEN_2.append(line.split("=")[-1].strip()) 

    randomWords = []
    for i in range(BOARD_WIDTH-1):
        randomWords.append("".join(r.choice(WORDS_LEN_1)))
    randomWords.append("".join(r.choice(WORDS_LEN_2)))
    randomWords.append(" ")

    # gets the index of all the letters of each word after the list(randomWords) is combined in a string
    tempRandomWords = "".join(randomWords)
    LETTER_POSITIONS = dict(enumerate(tempRandomWords[:-1], start=1))
    LETTER_POSITIONS[None] = ""

    return LETTER_POSITIONS

def transpose_matrix(board):
    return [i for i in zip(*board)]

def get_inversion_count(board):
    transposed_matrix = transpose_matrix(board)
    arr = [j for i in transposed_matrix for j in i]
            
    inversion_count = 0
    for i in range(BOARD_HEIGHT * BOARD_HEIGHT - 1):
        for j in range(i + 1, BOARD_HEIGHT * BOARD_HEIGHT):
            if arr[j] and arr[i] and arr[i] > arr[j]:
                inversion_count += 1

    return inversion_count

def is_solvable(board):
    inversion_count = get_inversion_count(board)
    blank_row = getBlankPosition(board)[0]

    check = inversion_count & 1

    if BOARD_HEIGHT & 1:
        return ~check
    else:   
        if blank_row & 1:
            return ~check
        else:
            return check

def playRandom():
    if SOUND:
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
    # For example, if BOARD_WIDTH and BOARD_HEIGHT are both 3, this function
    # returns [[1, 4, 7], [2, 5, 8], [3, 6, BLANK]]
    counter = 1
    board = []
    for x in range(BOARD_WIDTH):
        column = []
        for y in range(BOARD_HEIGHT):
            column.append(counter)
            counter += BOARD_WIDTH
        board.append(column)
        counter -= BOARD_WIDTH * (BOARD_HEIGHT - 1) + BOARD_WIDTH - 1
    board[BOARD_WIDTH-1][BOARD_HEIGHT-1] = BLANK
    return board

def getBlankPosition(board):
    # Return the x and y of board coordinates of the blank space.
    for x in range(BOARD_WIDTH):
        for y in range(BOARD_HEIGHT):
            if board[x][y] is BLANK:
                return (x, y)

def makeMove(board, move):
    # This function does not check if the move is valid.
    blank_x, blank_y = getBlankPosition(board)

    if move == UP:
        board[blank_x][blank_y], board[blank_x][blank_y + 1] = board[blank_x][blank_y + 1], board[blank_x][blank_y]
    elif move == DOWN:
        board[blank_x][blank_y], board[blank_x][blank_y - 1] = board[blank_x][blank_y - 1], board[blank_x][blank_y]
    elif move == LEFT:
        board[blank_x][blank_y], board[blank_x + 1][blank_y] = board[blank_x + 1][blank_y], board[blank_x][blank_y]
    elif move == RIGHT:
        board[blank_x][blank_y], board[blank_x - 1][blank_y] = board[blank_x - 1][blank_y], board[blank_x][blank_y]

def isValidMove(board, move):
    blank_x, blank_y = getBlankPosition(board)
    return (move == UP and blank_y != len(board[0]) - 1) or \
           (move == DOWN and blank_y != 0) or \
           (move == LEFT and blank_x != len(board) - 1) or \
           (move == RIGHT and blank_x != 0)

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

def getLeftTopOfTile(tile_x, tile_y, ai=False):
    left = X_MARGIN + (tile_x * TILE_SIZE) + (tile_x - 1)
    top = T_MARGIN + (tile_y * TILE_SIZE) + (tile_y - 1)
    return (left, top)

def getSpotClicked(board, x, y):
    # from the x & y pixel coordinates, get the x & y board coordinates
    for tile_x in range(len(board)):
        for tile_y in range(len(board[0])):
            left, top = getLeftTopOfTile(tile_x, tile_y)
            tileRect = game.Rect(left, top, TILE_SIZE, TILE_SIZE)
            if tileRect.collidepoint(x, y):
                return (tile_x, tile_y)
    return (None, None)

def drawTile(tile_x, tile_y, number, adj_x=0, adj_y=0, ai=False):
    # draw a tile at board coordinates tile_x and tile_y, optionally a few
    # pixels over (determined by adj_x and adj_y).
    left, top = getLeftTopOfTile(tile_x, tile_y)
    letter = LETTER_POSITIONS.get(number)

    screen.blit(tile_colors_cherry[letter], (left + adj_x, top + adj_y, TILE_SIZE, TILE_SIZE))


def makeText(text, color, bgcolor, top, left):
    # create the Surface and Rect objects for some text.
    textSurf = TEXT_FONT.render(text, True, color, bgcolor)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    return (textSurf, textRect)

def draw_outline():
    left, top = getLeftTopOfTile(0, 0)
    width = BOARD_WIDTH * TILE_SIZE
    height = BOARD_HEIGHT * TILE_SIZE
    game.draw.rect(screen, BORDER_COLOR, (left - 5, top - 5, width + 11, height + 11), 4)

def drawBoard(board, message, ai=False):
    screen.fill(BACKGROUND_COLOR)
    if message:
        textSurf, textRect = makeText(message, MESSAGE_COLOR, BACKGROUND_COLOR, 5, 5)
        screen.blit(textSurf, textRect)

    for tile_x in range(len(board)):
        for tile_y in range(len(board[0])):
            if board[tile_x][tile_y]:
                drawTile(tile_x, tile_y, board[tile_x][tile_y])

    draw_outline()

    screen.blit(RESET_SURF, RESET_RECT)
    screen.blit(NEW_SURF, NEW_RECT)
    screen.blit(SOLVE_SURF, SOLVE_RECT)

    if game_back_button.draw(screen):
        main_menu()

def slideAnimation(board, direction, message, animationSpeed):
    # Note: This function does not check if the move is valid.

    blank_x, blank_y = getBlankPosition(board)
    if direction == UP:
        move_x = blank_x
        move_y = blank_y + 1
    elif direction == DOWN:
        move_x = blank_x
        move_y = blank_y - 1
    elif direction == LEFT:
        move_x = blank_x + 1
        move_y = blank_y
    elif direction == RIGHT:
        move_x = blank_x - 1
        move_y = blank_y

    # prepare the base surface
    drawBoard(board, message)
    baseSurf = screen.copy()
    # draw a blank space over the moving tile on the baseSurf Surface.
    moveLeft, moveTop = getLeftTopOfTile(move_x, move_y)
    game.draw.rect(baseSurf, BACKGROUND_COLOR, (moveLeft, moveTop, TILE_SIZE, TILE_SIZE))

    for i in range(0, TILE_SIZE, animationSpeed):
        print(i)
        # animate the tile sliding over
        checkForQuit()
        screen.blit(baseSurf, (0, 0))
        if direction == UP:
            drawTile(move_x, move_y, board[move_x][move_y], 0, -i)
        if direction == DOWN:
            drawTile(move_x, move_y, board[move_x][move_y], 0, i)
        if direction == LEFT:
            drawTile(move_x, move_y, board[move_x][move_y], -i, 0)
        if direction == RIGHT:
            drawTile(move_x, move_y, board[move_x][move_y], i, 0)

        game.display.update()
        FPS_CLOCK.tick(FPS)

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
        slideAnimation(board, move, 'Generating new puzzle...', animationSpeed=TILE_SIZE // 2)
        makeMove(board, move)
        sequence.append(move)
        lastMove = move
    
    if not is_solvable(board):
        generateNewPuzzle(numSlides)

    return (board, sequence)

def resetAnimation(board, allMoves):
    # make all of the moves in allMoves in reverse.

    for move in reversed(allMoves):
        if move == UP:
            oppositeMove = DOWN
        elif move == DOWN:
            oppositeMove = UP
        elif move == RIGHT:
            oppositeMove = LEFT
        elif move == LEFT:
            oppositeMove = RIGHT
        slideAnimation(board, oppositeMove, '', animationSpeed=TILE_SIZE // 2)
        makeMove(board, oppositeMove)
    
if __name__ == '__main__':
    # mixer.music.load("Assets/Sounds/main theme.wav") 
    # mixer.music.play(-1)  
    main_menu()