from random import randint

class Game:
    def __init__(self):
        self.p0Went = False
        self.p1Went = False
        self.moves = [None, None]
        self.ready = False
        self.king0Alive = True
        self.king1Alive = True
        self.preference = randint(0, 1)

    def get_player_move(self, player):
        return self.moves[player]

    def play(self, player, move):
        self.moves[player] = move
        if player == 0:
            self.p0Went = True
        else:
            self.p1Went = True
        self.preference = randint(0, 1)

    def connected(self):
        return self.ready

    def bothWent(self):
        return self.p0Went and self.p1Went

    def noneWent(self):
        return (not self.p0Went) and (not self.p1Went)

    def winner(self):
        if not self.king0Alive:
            return 1
        elif not self.king1Alive:
            return 0

    def resetWent(self):
        self.p0Went = False
        self.p1Went = False
        self.moves = [None, None]
        print('We are resetting the moves in the game')

    def reset(self):
        self.p0Went = False
        self.p1Went = False
        self.moves = [None, None]
        self.ready = False
        self.king0Alive = True
        self.king1Alive = True


class Movement:

    def __init__(self, nature, origin, destination):
        self.nature = nature
        self.origin = origin
        self.destination = destination
        self.reset = False

    def print_move(self, color):
        if self.nature == 'moving':
            print(color + ': Piece located at ' + str(self.origin) + ' is moving to ' + str(self.destination))
        elif self.nature == 'shooting':
            print(color + ': Piece located at ' + str(self.origin) + ' is shooting at ' + str(self.destination))
        else:
            print('Movement\'s nature is unknown')

    def resetMove(self):
        self.nature = 'unknown'
        self.origin = (-1, -1)
        self.destination = (-1, -1)
        self.reset = False
        print('We are resetting the move')

    def primordial(self):
        return (self.nature == 'unknown') and (self.origin == (-1, -1)) and (self.destination == (-1, -1)) and (self.reset == False)
