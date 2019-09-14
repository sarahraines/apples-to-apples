from models import Deck, Hand


class Game:
    def __init__(self):
        self.scores = {}

    def play(self):
        self.ascii_art_title()
        print('by SARAH RAINES')
        playing = True
        round = 0

        green_deck = Deck('green')
        green_deck.shuffle()

        red_deck = Deck('red')
        red_deck.shuffle()

        print('\nSET UP A NEW GAME:')

        prompt = \
            'Please select the number of players between 3-6. '
        prompt_again = \
            'Not a valid input. Please enter a number between 3-6. '

        num_players = input(prompt).strip()
        while num_players not in ['3', '4', '5', '6']:
            num_players = input(prompt_again).strip()

        points_prompt = \
            'Please select a winning points threshold between 1-100. '
        points_prompt_again = \
            'Not a valid input. Please enter a number between 1-100. '

        points_threshold = input(points_prompt).strip()
        while not points_threshold.isdigit():
            points_threshold = input(points_prompt_again).strip()
        while int(points_threshold) > 100 or int(points_threshold) < 1:
            points_threshold = input(points_prompt_again).strip()

        hands = {}
        player_names = []

        name_prompt = \
            'Please enter a name for Player '
        name_repeat_prompt = \
            'Cannot use the same name for two players.\n' +  \
            'Please enter a new name for Player '

        for i in range(int(num_players)):
            player_name = input(name_prompt + str(i+1) + ' ').strip().lower()
            while player_name == '':
                player_name = \
                    input(name_prompt + str(i+1) + ' ').strip().lower()
            while player_name in player_names:
                player_name = \
                    input(name_repeat_prompt + str(i+1) + ' ').strip().lower()
            player_names.append(player_name)

        for player in player_names:
            self.scores[player] = 0
            dealt_hand = red_deck.deal_hand()
            new_hand = Hand(player.lower(), dealt_hand)
            hands[player] = new_hand

        judge = player_names[0]

        while playing:
            # choose a new green card
            print('*****************************************')
            green_card = green_deck.deal()
            choices = {}
            round_winner = ''
            card_winner = ''

            print(judge.capitalize() + ' is the judge for this round.')

            print('\nThe green card is ' + green_card.get_value())
            print('Description: ' + green_card.get_description())

            print('\nSCORES:')
            for score in self.scores.items():
                print(score[0].capitalize() + ': ' + str(score[1]))

            for hand in hands.items():
                player_name = hand[0]

                # select a card for every non-dealer hand
                if player_name != judge:
                    chosen_card = hand[1].choose_card(green_card)
                    candidate = {player_name: chosen_card}
                    choices.update(candidate)

                    # deal a new card to every non-dealer hand
                    card_drawn = red_deck.deal()
                    hand[1].add_card(card_drawn)

            print('-----------------------------------------')
            print('Time to judge, ' + judge.capitalize() + '!')
            print(
                'Select a card that best fits the adjective ' +
                green_card.get_value() +
                '\n'
            )
            for choice in choices.items():
                print(
                    choice[0].capitalize()
                    + ' selected the card '
                    + choice[1].get_value()
                )
                print('Description: ' + choice[1].get_description())
                print('Type ' + choice[0] + ' to select this card.\n')

            non_judges = player_names.copy()
            non_judges.remove(judge)

            prompt = 'Please choose [ ' + ' / '.join(non_judges) + ' ] '

            prompt_again = \
                'Not a valid input. Please enter one of [ ' + \
                ' / '.join(non_judges) + \
                ' ] '

            round_winner = input(prompt).strip().lower()
            while round_winner not in non_judges:
                round_winner = input(prompt_again).strip().lower()

            card_winner = choices[round_winner].get_value()
            self.scores[round_winner] = \
                self.scores[round_winner] + 1

            print(
                round_winner.capitalize() +
                ' won the round with the card ' +
                card_winner +
                '!'
            )

            winner = self.check_win(int(points_threshold))
            if winner is not None:
                playing = False
                print('\n' + winner.capitalize() + ' JUST WON THE GAME!')
                print('\nSCORES:')
                for score in self.scores.items():
                    print(score[0].capitalize() + ': ' + str(score[1]))
                self.ascii_art_end()

            round += 1
            judge = list(self.scores.keys())[round % int(num_players)]

    def check_win(self, points_threshold):
        for score in self.scores.items():
            if score[1] >= points_threshold:
                return(score[0])
        return None

    def ascii_art_title(self):
        print(
            '     _                _\n' +
            '    / \\   _ __  _ __ | | ___  ___\n' +
            '   / _ \\ | \'_ \\| \'_ \\| |/ _ \\/ __|\n' +
            '  / ___ \\| |_) | |_) | |  __/\\__ \\\n' +
            ' /_/   \\_\\ .__/| .__/|_|\\___||___/\n' +
            '         |_| _ |_|\n' +
            '            | |_ ___\n' +
            '            | __/ _ \\\n' +
            '            | || (_) |\n' +
            '     _       \\__\\___/ _\n' +
            '    / \\   _ __  _ __ | | ___  ___\n' +
            '   / _ \\ | \'_ \\| \'_ \\| |/ _ \\/ __|\n' +
            '  / ___ \\| |_) | |_) | |  __/\\__ \\\n' +
            ' /_/   \\_\\ .__/| .__/|_|\\___||___/\n' +
            '         |_|   |_|\n'
        )

    def ascii_art_end(self):
        print(
            ' _____ _   _ _____   _____ _   _ ____\n' +
            '|_   _| | | | ____| | ____| \\ | |  _ \\\n' +
            '  | | | |_| |  _|   |  _| |  \\| | | | |\n' +
            '  | | |  _  | |___  | |___| |\\  | |_| |\n' +
            '  |_| |_| |_|_____| |_____|_| \\_|____/\n'
        )
