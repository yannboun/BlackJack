import random
import numpy as np


class Card:
    def __init__(self, face, kind, game):
        self.face = face
        self.kind = kind
        self.value = game.values[face]


class Deck:
    def __init__(self, game):
        self.game = game
        faces = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        kinds = ['S', 'H', 'C', 'D']
        self.new_deck = [Card(face=face, kind=kind, game=self.game) for face in faces for kind in kinds]
        self.cards = self.new_deck.copy()
        random.shuffle(self.cards)

    def draw(self):
        try:
            return self.cards.pop()
        except IndexError:
            self.cards = self.new_deck.copy()
            random.shuffle(self.cards)
            return self.cards.pop()


class Hand:
    def __init__(self):
        self.cards = []
        self.value = [0]

    def add(self, card):
        self.cards.append(card)
        self.value = [actual + new for actual in self.value for new in card.value]
        self.value = [y for y in self.value if y < 22]

    def reset(self):
        self.cards = []
        self.value = [0]


class Blackjack:
    def __init__(self):
        self.values = {
            '2': [2],
            '3': [3],
            '4': [4],
            '5': [5],
            '6': [6],
            '7': [7],
            '8': [8],
            '9': [9],
            '10': [10],
            'J': [10],
            'Q': [10],
            'K': [10],
            'A': [1, 11]
        }
        self.deck = Deck(self)
        self.dealer = Hand()
        self.player = Hand()
        self.player_score = 0
        self.dealer_score = 0
        plays = {'H': 0, 'S': 0}
        self.q = {}
        for x in range(22):
            for y in range(22):
                self.q[True, x, y] = plays.copy()
                self.q[False, x, y] = plays.copy()

    def new_hand(self):
        self.dealer.reset()
        self.player.reset()
        self.player.add(self.deck.draw())
        self.dealer.add(self.deck.draw())
        self.player.add(self.deck.draw())
        self.dealer.add(self.deck.draw())

    def play(self):
        self.new_hand()
        print('Player : {} , Dealer : {} , *'.format(self.player.value, self.dealer.cards[0].value[0]))

        # Players turn
        while len(self.player.value) > 0: #there is at least 1 value <= 21:
            answer = None
            while (answer != 'Y') and (answer != 'N'):
                answer = input('Hit ? Y/N ').upper()
            if answer == 'Y':
                self.player.add(self.deck.draw())
                print('Player : {} , Dealer : {} , *'.format(self.player.value, self.dealer.cards[0].value[0]))
            if answer == 'N':
                break
        if len(self.player.value) == 0:
            print('Busted')
            self.dealer_score = self.dealer_score + 10
            return self.player_score, self.dealer_score

        # Dealers turn
        print('Player : {} , Dealer : {}'.format(max(self.player.value), self.dealer.value))
        while len([y for y in self.dealer.value if y >= 17]) == 0 and len(self.dealer.value) > 0:
            self.dealer.add(self.deck.draw())
            print('Player : {} , Dealer : {}'.format(max(self.player.value), self.dealer.value))

        if len(self.dealer.value) == 0:
            print('Dealer Busted')
            self.player_score = self.player_score + 10
            return self.player_score, self.dealer_score

        if max(self.player.value) > max(self.dealer.value):
            print("Player Wins")
            self.player_score = self.player_score + 10
            return self.player_score, self.dealer_score

        elif max(self.player.value) < max(self.dealer.value):
            print("Dealer Wins")
            self.dealer_score = self.dealer_score + 10
            return self.player_score, self.dealer_score

        else:
            print('Push')
            return self.player_score, self.dealer_score

    # functions for RL, returns a ACE marker, best player score, dealer visible card, game finished flag

    def first_step_play(self):
        self.new_hand()
        return [len(self.player.value) > 1, max(self.player.value), self.dealer.cards[0].value[0], 0]

    def step_play(self, action):

        if action == 'H':
            self.player.add(self.deck.draw())
            if len(self.player.value) > 0:
                return [len(self.player.value) > 1, max(self.player.value), self.dealer.cards[0].value[0], 0, False]
            else:
                # Player Busts
                self.new_hand()
                return [len(self.player.value) > 1, max(self.player.value), self.dealer.cards[0].value[0], -10, True]

        # Dealers turn
        if action == 'S':

            while len([y for y in self.dealer.value if y >= 17]) == 0 and len(self.dealer.value) > 0:
                self.dealer.add(self.deck.draw())

            if len(self.dealer.value) == 0:
                # Dealer Busts
                self.new_hand()
                return [len(self.player.value) > 1, max(self.player.value), self.dealer.cards[0].value[0], 12, True]

            if max(self.player.value) > max(self.dealer.value):
                # Player Win
                self.new_hand()
                return [len(self.player.value) > 1, max(self.player.value), self.dealer.cards[0].value[0], 12, True]

            elif max(self.player.value) < max(self.dealer.value):
                # Dealer Win
                self.new_hand()
                return [len(self.player.value) > 1, max(self.player.value), self.dealer.cards[0].value[0], -10, True]

            else:
                # Push
                self.new_hand()
                return [len(self.player.value) > 1, max(self.player.value), self.dealer.cards[0].value[0], 0, True]

    def play_ai(self):
        self.new_hand()
        print('Player : {} , Dealer : {} , *'.format(self.player.value, self.dealer.cards[0].value[0]))

        # Players turn
        while len(self.player.value) > 0:  # there is at least 1 value <= 21:
            state = [len(self.player.value) > 1, max(self.player.value), self.dealer.cards[0].value[0]]
            answer = max(self.q[state[0], state[1], state[2]], key=self.q[state[0], state[1], state[2]].get)
            if answer == 'H':
                self.player.add(self.deck.draw())
                print("AI Hits")
                if len(self.player.value) == 0:
                    print('Busted')
                    self.dealer_score = self.dealer_score + 10
                    return self.player_score, self.dealer_score
                print('Player : {} , Dealer : {} , *'.format(self.player.value, self.dealer.cards[0].value[0]))
            if answer == 'S':
                print("AI Stays")
                break

        # Dealers turn
        print('Player : {} , Dealer : {}'.format(max(self.player.value), self.dealer.value))
        while len([y for y in self.dealer.value if y >= 17]) == 0 and len(self.dealer.value) > 0:
            self.dealer.add(self.deck.draw())
            print('Player : {} , Dealer : {}'.format(max(self.player.value), self.dealer.value))

        if len(self.dealer.value) == 0:
            print('Dealer Busted')
            self.player_score = self.player_score + 10
            return self.player_score, self.dealer_score

        if max(self.player.value) > max(self.dealer.value):
            print("Player Wins")
            self.player_score = self.player_score + 10
            return self.player_score, self.dealer_score

        elif max(self.player.value) < max(self.dealer.value):
            print("Dealer Wins")
            self.dealer_score = self.dealer_score + 10
            return self.player_score, self.dealer_score

        else:
            print('Push')
            return self.player_score, self.dealer_score

    def train_ai(self, niter=10000, lr=0.02, df=0.5):
        player_wallet = []
        outcome = self.first_step_play()
        for k in range(niter):
            next_move = max(self.q[outcome[0], outcome[1], outcome[2]],
                            key=self.q[outcome[0], outcome[1], outcome[2]].get)
            previous = outcome.copy()
            previous_move = max(self.q[previous[0], previous[1], previous[2]],
                                key=self.q[previous[0], previous[1], previous[2]].get)
            outcome = self.step_play(next_move)
            self.q[previous[0], previous[1], previous[2]][previous_move] = \
                self.q[previous[0], previous[1], previous[2]][previous_move] * (1 - lr) + \
                lr * (outcome[3] + df * max(self.q[outcome[0], outcome[1], outcome[2]].values()))
            if outcome[4]:
                player_wallet.append(outcome[3])
        return np.cumsum(player_wallet)