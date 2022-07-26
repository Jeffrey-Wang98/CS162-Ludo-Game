# Author: Jeffrey Wang
# GitHub username: Jeffrey-Wang98
# Date: July 23, 2022
# Description:

class InvalidPositionError(Exception):
    pass


class InvalidToken(Exception):
    pass


class InvalidTokenPositionError(Exception):
    pass


class Board:
    def __init__(self):
        self._board = {}
        for spaces in range(56):
            self._board[str(spaces + 1)] = []
        for char in ["A", "B", "C", "D"]:
            for num in range(1, 7):
                self._board[char + str(num)] = []
        self._finish = []
        self._occupied_spaces = []

    def set_finish_tokens(self, token):
        self._finish.append(token)

    def remove_token(self, pos, token):
        self._board[pos].remove(token)

    def move_piece(self, token, start_pos, end_pos):
        if end_pos == "E":
            self._finish.append(token)
            self._board[start_pos].remove(token)
        else:
            self._board[end_pos].append(token)
            self._board[start_pos].remove(token)


class Player:
    def __init__(self, position):
        try:
            self._player_pos = position.upper()
        except AttributeError:
            print("That's not a character from A - D.")
        self._p_status = "HOME"
        self._q_status = "HOME"
        self._p_steps = -1
        self._q_steps = -1
        if self._player_pos == "A":
            self._start = 0
            self._end = 49
        elif self._player_pos == "B":
            self._start = 14
            self._end = 7
        elif self._player_pos == "C":
            self._start = 28
            self._end = 21
        elif self._player_pos == "D":
            self._start = 42
            self._end = 35
        else:
            raise InvalidPositionError
        self._finished = False

    def get_completed(self):
        return self._finished

    def get_player_pos(self):
        return self._player_pos

    def get_token_p_step_count(self):
        return self._p_steps

    def set_token_p_step_count(self, new_steps):
        self._p_steps = new_steps

    def get_token_q_step_count(self):
        return self._q_steps

    def set_token_q_step_count(self, new_steps):
        self._q_steps = new_steps

    def get_space_name(self, total_steps):
        current_position = (self._start + total_steps) % 56
        if total_steps == -1:  # when the piece is still in Home
            return "H"
        if total_steps == 0:  # when the piece is on the ready space
            return "R"
        if total_steps == 56:  # when the piece hits the finish line
            return "F"
        if total_steps > 56:  # when the piece goes past the finish line
            return 56 - total_steps
        if self._player_pos != "A":  # if the player is B - D
            if self._start > current_position > self._end:  # if the piece is on the home row
                return self._player_pos + str(current_position - self._end)
            else:  # if the piece is on the shared board spaces
                return str(current_position + 1)
        else:  # if the player is A
            if current_position > self._end:  # if the piece is on the home row
                return self._player_pos + str(current_position - self._end)
            else:  # if the piece is on the shared board spaces
                return str(current_position + 1)


class LudoGame:
    def __init__(self):
        player_a = Player("A")
        player_b = Player("B")
        player_c = Player("C")
        player_d = Player("D")
        self._players = {
            "A": player_a,
            "B": player_b,
            "C": player_c,
            "D": player_d
        }

    def get_player_by_position(self, player_position):
        try:
            if player_position.upper() in self._players:
                return self._players[player_position.upper()]
            else:
                return "Player not found!"
        except AttributeError:
            return "Player not found!"

    def move_token(self, board, player, token, steps):
        try:
            if token.upper() == "P":
                token_name = "{}_p".format(player.get_player_pos().lower())
                token_steps = player.get_token_p_step_count()
            elif token.upper() == "Q":
                token_name = "{}_q".format(player.get_player_pos().lower())
                token_steps = player.get_token_q_step_count()
            else:
                raise InvalidToken
        except AttributeError:
            raise InvalidToken
        start_pos = player.get_space_name(token_steps)
        end_steps = token_steps + steps
        if start_pos == "E" or "H" or "F" or "R":  # spaces that the token cannot move from
            raise InvalidToken
        end_pos = player.get_space_name(end_steps)
        try:
            if end_pos < 0:
                end_steps += end_pos
        except TypeError:
            if end_pos == "E":
                board.move_piece(token_name, start_pos, end_pos)

    def play_game(self, players_list, turns_list):
        board = Board()
        pass
