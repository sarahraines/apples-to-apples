class Hand:
    def __init__(self, name, cards):
        self.name = name
        self.cards = cards

    def choose_card(self, keyword):
        print('-----------------------------------------')
        count = 1
        print(
            self.name.capitalize() +
            '\'s turn!'
        )
        print(
            'Select a card that best fits the adjective ' +
            keyword.get_value() +
            '\n'
        )
        for card in self.cards:
            print('Card: ' + card.get_value())
            print('Description: ' + card.get_description())
            print('Type ' + str(count) + ' to select this card.\n')
            count += 1

        prompt = \
            'Please select your card by choosing a number between 1-7. '
        prompt_again = \
            'Not a valid input. Please enter a number between 1-7. '

        card_index = input(prompt).strip()
        while card_index not in ['1', '2', '3', '4', '5', '6', '7']:
            card_index = input(prompt_again).strip()

        chosen_card = self.cards.pop(int(card_index)-1)
        return chosen_card

    def add_card(self, card):
        self.cards.append(card)
