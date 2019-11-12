from Pieces import *
from Network import Network
from Game import *

pygame.init()


def interaction():
    global chosenPiece, board, waiting, sent_move

    if not waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            pres = pygame.mouse.get_pressed()
            if pres[0]:
                tempx, tempy = pygame.mouse.get_pos()
                posx = tempx // dist
                posy = tempy // dist
                if chosenPiece:
                    chosenColor, chosenInd = chosenPiece[0]
                    piece = chosenColor.ownPieces[chosenInd]
                    if (posx, posy) in piece.valid_space(board):
                        sent_move.nature = 'moving'
                        sent_move.origin = (piece.x, piece.y)
                        sent_move.destination = (posx, posy)
                        waiting = True
                    piece.chosen = False
                    chosenPiece = []
                else:
                    color, ind = board[posx][posy]
                    if color != empty:
                        chosenPiece = [(color, board[posx][posy][1])]
                        color.ownPieces[ind].chosen = True
            if pres[2]:
                tempx, tempy = pygame.mouse.get_pos()
                posx = tempx // dist
                posy = tempy // dist
                if chosenPiece:
                    chosenColor, chosenInd = chosenPiece[0]
                    piece = chosenColor.ownPieces[chosenInd]
                    if type(piece) == Shooter:
                        ownx = piece.x
                        owny = piece.y
                        if (posx - ownx, posy - owny) in piece.aimingSpots:
                            if piece.ammo > 0:
                                ownBullet.dirnx = (posx - ownx)
                                ownBullet.dirny = (posy - owny)
                                ownBullet.x = ownx * dist + ownBullet.biais()[0]
                                ownBullet.y = owny * dist + ownBullet.biais()[1]
                                ownBullet.colliding_position(board)
                                sent_move.nature = 'shooting'
                                sent_move.origin = (piece.x, piece.y)
                                sent_move.destination = (ownBullet.colx, ownBullet.coly)
                                waiting = True
                        piece.chosen = False
                        chosenPiece = []
                        chosenColor.ownPieces[chosenInd] = piece

def update(g):
    global board, moving, player, ownBullet, oppositeBullet

    white_move = g.moves[0]
    w_originx, w_originy = white_move.origin
    _, w_ind = board[w_originx][w_originy]
    w_destx, w_desty = white_move.destination
    piece = white.ownPieces[w_ind]
    if white_move.nature == 'moving':
        piece.move(w_destx, w_desty, board)
        if board[w_destx][w_desty][0] == black:
            b_killedPiece = black.ownPieces[board[w_destx][w_desty][1]]
            if type(b_killedPiece) == King:
                g.king1Alive = False
    elif white_move.nature == 'shooting':
        piece.ammo -= 1
        if player == 0:
            ownBullet.triggered = True
        else:
            print('We are setting opposite\'s bullet parameters')
            oppositeBullet.dirnx = normalize(w_destx - w_originx)
            oppositeBullet.dirny = normalize(w_desty - w_originy)
            oppositeBullet.x = w_originx * dist + oppositeBullet.biais()[0]
            oppositeBullet.y = w_originy * dist + oppositeBullet.biais()[1]
            oppositeBullet.colx = w_destx
            oppositeBullet.coly = w_desty
            oppositeBullet.triggered = True
        moving = True

    black_move = g.moves[1]
    b_originx, b_originy = black_move.origin
    _, b_ind = board[b_originx][b_originy]
    b_destx, b_desty = black_move.destination
    piece = black.ownPieces[b_ind]
    if black_move.nature == 'moving':
        piece.move(b_destx, b_desty, board)
        if board[b_destx][b_desty][0] == white:
            w_killedPiece = white.ownPieces[board[b_destx][b_desty][1]]
            if type(w_killedPiece) == King:
                g.king0Alive = False
    elif black_move.nature == 'shooting':
        piece.ammo -= 1
        if player == 1:
            ownBullet.triggered = True
        else:
            print('We are setting opposite\'s bullet parameters')
            oppositeBullet.dirnx = normalize(b_destx - b_originx)
            oppositeBullet.dirny = normalize(b_desty - b_originy)
            oppositeBullet.x = b_originx * dist + oppositeBullet.biais()[0]
            oppositeBullet.y = b_originy * dist + oppositeBullet.biais()[1]
            oppositeBullet.colx = b_destx
            oppositeBullet.coly = b_desty
            oppositeBullet.triggered = True
        moving = True



def normalize(x):
    if x == 0:
        return 0
    else:
        return x//abs(x)

def drawBoard(surface):
    for i in range(rows):
        for j in range(rows):
            if (i + j) % 2 == 0:
                pygame.draw.rect(surface, backWhite, (i * dist, j * dist, dist, dist))
            else:
                pygame.draw.rect(surface, backBrown, (i * dist, j * dist, dist, dist))


def redrawWindow(surface):
    drawBoard(surface)
    for white_item in white.ownPieces:
        if white_item.chosen:
            white_item.drawPossibleMoves(surface, board)
            if type(white_item) == Shooter:
                white_item.drawAiming(surface)
    for black_item in black.ownPieces:
        if black_item.chosen:
            black_item.drawPossibleMoves(surface, board)
            if type(black_item) == Shooter:
                black_item.drawAiming(surface)
    for white_item in white.ownPieces:
        white_item.draw(surface)
    for black_item in black.ownPieces:
        black_item.draw(surface)
    if ownBullet.triggered:
        ownBullet.draw(surface)
    if oppositeBullet.triggered:
        oppositeBullet.draw(surface)
    if player == 0 and game.p0Went:
        pygame.draw.rect(surface, (255, 0, 0), (0, 0, 10, 10))
    elif player == 1 and game.p1Went:
        pygame.draw.rect(surface, (255, 0, 0), (0, 0, 10, 10))
    pygame.display.update()


def main():
    global whiteKing, whiteSquire1, whiteSquire2, whiteShooter1, whiteShooter2, blackKing, blackSquire1, blackSquire2, \
        blackShooter1, blackShooter2, chosenPiece, ownBullet, oppositeBullet, board, waiting, sent_move, moving, player, game

    win = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()

    whiteKing = King(4, 7, white, whiteKingImg)
    whiteSquire1 = Squire(3, 6, white, whiteSquireImg)
    whiteSquire2 = Squire(5, 6, white, whiteSquireImg)
    whiteShooter1 = Shooter(3, 7, white, whiteShooterImg)
    whiteShooter2 = Shooter(5, 7, white, whiteShooterImg)
    blackKing = King(4, 0, black, blackKingImg)
    blackSquire1 = Squire(3, 1, black, blackSquireImg)
    blackSquire2 = Squire(5, 1, black, blackSquireImg)
    blackShooter1 = Shooter(3, 0, black, blackShooterImg)
    blackShooter2 = Shooter(5, 0, black, blackShooterImg)

    chosenPiece = []

    board = [[(empty, 0)] * rows for k in range(rows)]
    for wInd, whiteItem in enumerate(white.ownPieces):
        board[whiteItem.x][whiteItem.y] = (white, wInd)
    for bInd, blackItem in enumerate(black.ownPieces):
        board[blackItem.x][blackItem.y] = (black, bInd)

    sent_move = Movement('unknown', (-1, -1), (-1, -1))

    run = True
    waiting = False
    moving = False
    n = Network()
    player = int(n.getP())
    pColor = white
    if player == 1:
        pColor = black
    ownBullet = Bullet(0, 0, 0, 0, pColor, bulletImg)
    oppositeBullet = Bullet(0, 0, 0, 0, pColor.opposite, bulletImg)
    counter = 0

    while run:
        counter += 1
        clock.tick(60)
        if not moving:
            try:
                game = n.send(sent_move)
                if not sent_move.primordial():
                    sent_move.resetMove()
            except:
                run = False
                print('Could not get game')
                break
            interaction()
            if game.bothWent():
                print('Both players went')
                update(game)
                waiting = False
                sent_move.reset = True
        else:
            if ownBullet.triggered:
                ownBullet.move()
            if oppositeBullet.triggered:
                oppositeBullet.move()
            if ownBullet.collided:
                ownBullet.collide(board)
            if oppositeBullet.collided:
                oppositeBullet.collide(board)
            if (not ownBullet.triggered) and (not oppositeBullet.triggered):
                moving = False
        redrawWindow(win)

    pygame.quit()


main()
