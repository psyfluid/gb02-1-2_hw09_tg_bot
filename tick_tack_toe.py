import random

EMPTY_SYMBOL = '\U0001F532'
X_SYMBOL = '\U0000274E'
O_SYMBOL = '\U0001F17E\uFE0F'


class Game(object):
    def __init__(self):
        super().__init__()
        self.restart_game()

    @staticmethod
    def _default_buttons():
        return [(i, j) for i in range(3) for j in range(3)]

    def restart_game(self):
        self.buttons = [[EMPTY_SYMBOL for _ in range(3)] for _ in range(3)]
        self.winner = ''
        self.winner_text = ''
        self.available_buttons = self._default_buttons()
        self.player_turn = random.choice((False, True))
        if not self.player_turn:
            self.bot_move()

    def toggle_field(self, i, j):
        self.buttons[i][j] = X_SYMBOL if self.player_turn else O_SYMBOL
        self.available_buttons.remove((i, j))

        self.check_win()
        if self.winner or not self.available_buttons:
            if not self.winner:
                self.winner = 'nobody'
            self.show_winner()
            return

        self.player_turn = not self.player_turn
        if not self.player_turn:
            self.bot_move()

    def bot_move(self):
        i, j = random.choice(self.available_buttons)
        self.toggle_field(i, j)

    def check_win(self):
        player_diag_1 = 0
        player_diag_2 = 0
        bot_diag_1 = 0
        bot_diag_2 = 0
        for i in range(3):
            player_win = 3 in (
                [btn for btn in self.buttons[i]].count(X_SYMBOL),
                [row[i] for row in self.buttons].count(X_SYMBOL)
            )
            bot_win = 3 in (
                [btn for btn in self.buttons[i]].count(O_SYMBOL),
                [row[i] for row in self.buttons].count(O_SYMBOL)
            )
            if player_win:
                self.winner = 'player'
                return
            elif bot_win:
                self.winner = 'bot'
                return

            if self.buttons[i][i] == X_SYMBOL:
                player_diag_1 += 1
            elif self.buttons[i][i] == O_SYMBOL:
                bot_diag_1 += 1

            if self.buttons[i][-1 - i] == X_SYMBOL:
                player_diag_2 += 1
            elif self.buttons[i][-1 - i] == O_SYMBOL:
                bot_diag_2 += 1

        if player_diag_1 == 3 or player_diag_2 == 3:
            self.winner = 'player'
        elif bot_diag_1 == 3 or bot_diag_2 == 3:
            self.winner = 'bot'

    def show_winner(self):
        if self.winner == 'player':
            self.winner_text = 'Вы победили! \U0001F642'
        elif self.winner == 'bot':
            self.winner_text = 'Вы проиграли... \U0001F615'
        else:
            self.winner_text = 'Ничья \U0001F610'
