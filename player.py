class Player:
    def __init__(self, user):
        self.user = user
        self.hand = []
        self.strikes = 0

    @property
    def hand_length(self):
        return len(self.hand)

    def __getattr__(self, attribute):
        return getattr(self.user, attribute)
    
    def pickup_deck(self, deck):
        self.hand += deck

    def lose_card(self):
        return self.hand.pop()