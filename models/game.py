from models import Deck, Hand


class Game:
    def __init__(self):
        self.scores = {}
        self.player_names = []
        self.hands = {}
        self.green_deck = Deck('green')
        self.green_deck.shuffle()
        self.red_deck = Deck('red')
        self.red_deck.shuffle()

    def play(self):
        self.ascii_art_title()
        self.set_num_players()
        self.set_points_threshold()
        self.name_players()
        self.deal_hands()
        playing = True
        round = 0
        judge = self.player_names[0]

        while playing:
            print('*****************************************')
            print(judge.capitalize() + ' is the judge for this round.')
            # choose a new green card
            green_card = self.green_deck.deal()
            print('\nThe green card is ' + green_card.get_value())
            print('Description: ' + green_card.get_description())

            self.show_scores()
            choices = self.pick_cards(judge, green_card)
            self.judge_round(judge, green_card, choices)

            winner = self.check_win()
            if winner is not None:
                playing = False
                print('\n' + winner.capitalize() + ' JUST WON THE GAME!')
                self.show_scores()
                self.ascii_art_end()

            round += 1
            judge = list(self.scores.keys())[round % int(self.num_players)]

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
        print('by SARAH RAINES')

    def set_num_players(self):
        print('\nSET UP A NEW GAME:')
        prompt = \
            'Please select the number of players between 3-6. '
        prompt_again = \
            'Not a valid input. Please enter a number between 3-6. '

        self.num_players = input(prompt).strip()
        while self.num_players not in ['3', '4', '5', '6']:
            self.num_players = input(prompt_again).strip()

    def set_points_threshold(self):
        points_prompt = \
            'Please select a winning points threshold between 1-100. '
        points_prompt_again = \
            'Not a valid input. Please enter a number between 1-100. '

        self.points_threshold = input(points_prompt).strip()
        while not self.points_threshold.isdigit():
            self.points_threshold = input(points_prompt_again).strip()
        while int(self.points_threshold) > 100 or int(self.points_threshold) < 1:
            self.points_threshold = input(points_prompt_again).strip()

    def name_players(self):
        name_prompt = \
            'Please enter a name for Player '
        name_repeat_prompt = \
            'Cannot use the same name for two players.\n' +  \
            'Please enter a new name for Player '

        for i in range(int(self.num_players)):
            player_name = input(name_prompt + str(i+1) + ' ').strip().lower()
            while player_name == '':
                player_name = \
                    input(name_prompt + str(i+1) + ' ').strip().lower()
            while player_name in self.player_names:
                player_name = \
                    input(name_repeat_prompt + str(i+1) + ' ').strip().lower()
            self.player_names.append(player_name)

    def deal_hands(self):
        for player in self.player_names:
            self.scores[player] = 0
            dealt_hand = self.red_deck.deal_hand()
            new_hand = Hand(player.lower(), dealt_hand)
            self.hands[player] = new_hand

    def pick_cards(self, judge, green_card):
        choices = {}
        for hand in self.hands.items():
            player_name = hand[0]
            # select a card for every non-dealer hand
            if player_name != judge:
                chosen_card = hand[1].choose_card(green_card)
                choices[player_name] = chosen_card
                # deal a new card to every non-dealer hand
                card_drawn = self.red_deck.deal()
                hand[1].add_card(card_drawn)

        return choices

    def judge_round(self, judge, green_card, choices):
        round_winner = ''
        card_winner = ''
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

        non_judges = self.player_names.copy()
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
        self.scores[round_winner] += 1
        print(
            round_winner.capitalize() +
            ' won the round with the card ' +
            card_winner +
            '!'
        )

    def check_win(self):
        for score in self.scores.items():
            if score[1] >= int(self.points_threshold):
                return(score[0])
        return None

    def show_scores(self):
        print('\nSCORES:')
        for score in self.scores.items():
            print(score[0].capitalize() + ': ' + str(score[1]))

    def ascii_art_end(self):
        print(
            ' _____ _   _ _____   _____ _   _ ____\n' +
            '|_   _| | | | ____| | ____| \\ | |  _ \\\n' +
            '  | | | |_| |  _|   |  _| |  \\| | | | |\n' +
            '  | | |  _  | |___  | |___| |\\  | |_| |\n' +
            '  |_| |_| |_|_____| |_____|_| \\_|____/\n'
        )
