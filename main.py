import pygame

turn = int(input("Who's going first? (1 = Blue, 2 = Red, 3 = Green)"))
players = int(input("How many players / teams? (2 or 3)"))
col = int(input("Who are you? (1 = Blue, 2 = Red, 3 = Green)"))
pygame.init()
gameDisplay = pygame.display.set_mode((800,693))
pygame.display.set_caption('Sequence Assistant')
clock = pygame.time.Clock()

boardImg = pygame.image.load('board.png')

class card:
    def __init__(self, id, team, left, inhand):
        self.id = id
        self.team = team
        self.left = left
        self.inhand = inhand

idArray = [
    [0 ,17,18,19,20,21,22,23,24,0 ],
    [16,47,48,1 ,2 ,3 ,4 ,5 ,6 ,25],
    [15,46,23,24,25,26,27,28,7 ,26],
    [14,45,22,39,40,41,42,29,8 ,27],
    [13,44,21,38,47,48,43,30,9 ,28],
    [12,43,20,37,46,45,44,31,10,29],
    [11,42,19,36,35,34,33,32,11,30],
    [10,41,18,17,16,15,14,13,12,31],
    [9 ,40,39,38,37,36,35,34,33,32],
    [0 ,8 ,7 ,6 ,5 ,4 ,3 ,2 ,1 ,0 ]]

def text_objects(text, font, colour):
    textSurface = font.render(text, True, colour)
    return textSurface, textSurface.get_rect()

def message_display(text, x, y, colour):
    largeText = pygame.font.Font('freesansbold.ttf',20)
    TextSurf, TextRect = text_objects(text, largeText, colour)
    TextRect.center = (x,y)
    gameDisplay.blit(TextSurf, TextRect)

cardArray = [[0 for x in range(10)] for y in range(10)] 

onejacks = 4
twojacks = 4
cards = 104

def ToggleInhand(x,y):
    if cardArray[x][y].left == 1:
         if cardArray[x][y].inhand and cardArray[x][y].team == col:
             cardArray[x][y].inhand = False
             cardArray[x][y].team = 0
         else:
             cardArray[x][y].inhand = True
             cardArray[x][y].team = col
    else:
        for arr in cardArray:
            for c in arr:
                if c.id == cardArray[x][y].id:
                    if c.inhand and c.team == col:
                        c.inhand = False
                        c.team = 0
                    else:
                        c.inhand = True
                        c.team = col
def DrawLines(x,y):
    directions = [[0,1],[0,-1],[1,0],[-1,0],[1,1],[1,-1],[-1,1],[-1,-1],]
    for dir in directions:
        x2 = dir[0]
        y2 = dir[1]
        fail = False
        b = False
        r = False
        g = False
        teams = 0
        row = 0
        colour4 = (0,0,0)
        for n in range(0, 5):
            if x+(n*x2) < 0 or x+(n*x2) > 9 or y+(n*y2) < 0 or y+(n*y2) > 9:
                fail = True
                break
            if cardArray[x+(n*x2)][y+(n*y2)].id == 0:
                row += 1
            elif cardArray[x+(n*x2)][y+(n*y2)].team == 1 and not b:
                teams += 1
                b = True
            elif cardArray[x+(n*x2)][y+(n*y2)].team == 2 and not r:
                teams += 1
                r = True
            elif cardArray[x+(n*x2)][y+(n*y2)].team == 3 and not g:
                teams += 1
                g = True
            elif cardArray[x+(n*x2)][y+(n*y2)].team == 1 and b:
                row += 1
            elif cardArray[x+(n*x2)][y+(n*y2)].team == 2 and r:
                row += 1
            elif cardArray[x+(n*x2)][y+(n*y2)].team == 3 and g:
                row += 1
            if teams > 1:
                fail = True
                break
        if teams == 0:
            fail = True
        if row == 0:
            fail = True
        if not fail:
            if b:
                colour4 = (0,0,255)
            if r:
                colour4 = (255,0,0)
            if g:
                colour4 = (255,0,255)
            pygame.draw.line(gameDisplay, colour4, ((x*69)+35,(y*69)+35), ((x+4*x2)*69+35,(y+4*y2)*69+35), row)

for y in range(0, 10):
    for x in range(0, 10):
        cardArray[x][y] = card(idArray[y][x], 0, 2, False)

end = False

while not end:
    gameDisplay.fill((0,0,0))
    gameDisplay.blit(boardImg, (0,0))
    for y in range(0, 10):
        for x in range(0, 10):
            if cardArray[x][y].id != 0:
                text = cardArray[x][y].left
                if text == 2:
                    colour = pygame.Color(0,255,0)
                elif text == 1:
                    colour = pygame.Color(255,255,0)
                else:
                    colour = pygame.Color(255,0,0)
                team = cardArray[x][y].team
                if team == 1:
                    colour2 = pygame.Color(0,0,255)
                elif team == 2:
                    colour2 = pygame.Color(255,0,0)
                elif team == 3:
                    colour2 = pygame.Color(0,255,0)
                s = pygame.Surface((70,70))
                s.set_alpha(128)
                s.fill((255,255,255))
                if not cardArray[x][y].inhand:
                    pygame.draw.rect(s,colour,(0,0,70,70),0)
                else:
                    pygame.draw.rect(s,(255,0,255),(0,0,70,70),0)
                gameDisplay.blit(s, (x*69,y*69))
                if team != 0 and not cardArray[x][y].inhand:
                    pygame.draw.circle(gameDisplay, colour2, ((x*69)+35,(y*69)+35), 15)
                DrawLines(x,y)
    message_display("1EJ: " + str(onejacks), 730, 50, (255,255,255))
    msg = f"{onejacks/cards:.4f}"
    message_display(f"{str(100*float(msg))[0:4]}%", 730, 75, (255,255,255))
    msg = f"{twojacks/cards:.4f}"
    message_display("2EJ: " + str(twojacks), 730, 200, (255,255,255))
    message_display(f"{str(100*float(msg))[0:4]}%", 730, 225, (255,255,255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            end = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            l, m, r = pygame.mouse.get_pressed()
            if l == 1:
                x, y = pygame.mouse.get_pos()
                x = x // 69
                y = y // 69
                cards -= 1
                if cardArray[x][y].id == 0:
                    continue
                if cardArray[x][y].inhand:
                    ToggleInhand(x,y)
                if cardArray[x][y].team != 0:
                    cardArray[x][y].team = 0
                    onejacks -= 1
                else:
                    cardArray[x][y].team = ((turn-1) % players) + 1
                    for arr in cardArray:
                        for c in arr:
                            if c.id == cardArray[x][y].id:
                                c.left -= 1
                turn += 1
            elif r == 1:
                x, y = pygame.mouse.get_pos()
                x = x // 69
                y = y // 69
                cards -= 1
                if cardArray[x][y].id == 0:
                    continue
                if cardArray[x][y].inhand:
                    ToggleInhand(x,y)
                if cardArray[x][y].team != 0:
                    cardArray[x][y].team = 0
                    onejacks -= 1
                else:
                    cardArray[x][y].team = ((turn-1) % players) + 1
                    twojacks -= 1
                turn += 1
            elif m == 1:
                x, y = pygame.mouse.get_pos()
                x = x // 69
                y = y // 69
                ToggleInhand(x,y)

    pygame.display.update()
    clock.tick(60)