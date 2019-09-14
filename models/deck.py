import random
from models import Card


class Deck:
    def __init__(self, type):
        self.type = type
        self.cards = []
        self.make_deck()

    def shuffle(self):
        if len(self.cards) > 1:
            random.shuffle(self.cards)

    def deal(self):
        if len(self.cards) > 1:
            return self.cards.pop(0)

    def deal_hand(self):
        if len(self.cards) > 7:
            new_hand = self.cards[:7]
            del self.cards[:7]
            return new_hand

    def make_deck(self):
        file_path = "txt/" + str(self.type) + "_cards.txt"
        f = open(file_path)
        cards = f.readlines()
        for card in cards:
            card_arr = card.split('-', 1)
            new_card = Card(
                value=card_arr[0].strip(),
                description=card_arr[1].strip()
            )
            self.cards.append(new_card)
