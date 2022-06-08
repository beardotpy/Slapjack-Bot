import os
import random

class Game:
    def __init__(self, players):
        self.players = players
        self.num_of_players = len(players)
        self.deck = []
        self.turn = 0

    @property
    def is_won(self):
        for player in self.players:
            if player.hand_length < 52:
                return False
            else:
                return True

    @property
    def current_player(self):
        return self.turn_order[self.turn%self.num_of_players]

    @property
    def turn_order_str(self):
        players = self.players
        for player in players:
            if player.hand_length == 0:
                players.remove(player)
        players = [[player.name, player.hand_length] for player in players]
        players[self.current_player_index][0] = f"**{players[self.current_player_index]}**"

        return ", ".join([":".join(player) for player in players])

    def next_turn(self):
        self.turn += 1

    def add_to_deck(self, card):
        self.deck.inser(0, card)

    def deal_cards(self):
        players = self.players
        cards = os.listdir("cards")
        random.shuffle(cards)
        for i, card in enumerate(cards):
            players[i%self.num_of_players].hand.append(card)