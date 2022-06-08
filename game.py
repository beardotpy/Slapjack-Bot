import os
import random

class Game:
    def __init__(self, players):
        self.players = players
        self.user_list = [player.user for player in players]
        self.num_of_players = len(players)
        self.deck = []
        self.turn = 0

    @property
    def winner(self):
        for player in self.players:
            if player.hand_length < 52:
                return None
            else:
                return player

    @property
    def current_player(self):
        return self.players[self.turn%self.num_of_players]
    
    @property
    def current_player_index(self):
        return self.turn%self.num_of_players

    @property
    def turn_order_str(self):
        players = self.players
        for player in players:
            if player.hand_length == 0:
                players.remove(player)
        players = [[player.user.name, str(player.hand_length)] for player in players]
        players[self.current_player_index][0] = f"**{players[self.current_player_index][0]}**"
        return ", ".join([":".join(player) for player in players])

    def next_turn(self):
        self.turn += 1

    def check_if_slap(self):
        try:
            is_jack = self.deck[0].split("_")[0] == "jack"
        except:
            return False
        try:
            is_doubles = self.deck[0].split("_")[0] == self.deck[1].split("_")[0]
        except:
            return False
        try:
            is_sandwich = self.deck[0].split("_")[0] == self.deck[2].split("_")[0]
        except:
            return False
        return is_jack or is_doubles or is_sandwich

    def add_to_deck(self, card):
        self.deck.insert(0, card)

    def empty_deck(self):
        self.deck.clear()

    def deal_cards(self):
        players = self.players
        cards = os.listdir("cards")
        random.shuffle(cards)
        for i, card in enumerate(cards):
            players[i%self.num_of_players].hand.append(card)