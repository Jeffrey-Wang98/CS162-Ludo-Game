# Author: Jeffrey Wang
# GitHub username: Jeffrey-Wang98
# Date: July 23, 2022
# Description:

class InvalidPositionError(Exception):
    pass


class Space:
    def __init__(self, position, next_space=None, home_row=None):
        self._name = position
        self._tokens = []
        self._next = next_space
        self._next_home = home_row


class Board:
    def __init__(self):
        self._board = {}
        for spaces in range(56):
            self._board[spaces] = []
        self._a_home = ["a_p", "a_q"]
        self._a_row = {
            "A1": [],
            "A2": [],
            "A3": [],
            "A4": [],
            "A5": [],
            "A6": []
        }
        self._b_home = ["b_p", "b_q"]
        self._b_row = {
            "B1": [],
            "B2": [],
            "B3": [],
            "B4": [],
            "B5": [],
            "B6": []
        }
        self._c_home = ["c_p", "c_q"]
        self._d_row = {
            "C1": [],
            "C2": [],
            "C3": [],
            "C4": [],
            "C5": [],
            "C6": []
        }
        self._d_home = ["d_p", "d_q"]
        self._d_row = {
            "D1": [],
            "D2": [],
            "D3": [],
            "D4": [],
            "D5": [],
            "D6": []
        }
        self._finish = []
        self._occupied_spaces = []

    def move_piece(self, player, spaces):

        pass


class Player:
    def __init__(self, position):
        self._player_pos = position.upper()
        self._p_status = "HOME"
        self._q_status = "HOME"
        self._p_steps = -1
        self._q_steps = -1
        if position == "A":
            self._start = 0
            self._end = 49
        if position == "B":
            self._start = 14
            self._end = 7
        elif position == "C":
            self._start = 28
            self._end = 21
        elif position == "D":
            self._start = 42
            self._end = 35
        else:
            raise InvalidPositionError
        self._finished = False

    def get_completed(self):
        return self._finished

    def get_token_p_step_count(self):
        return self._p_steps

    def get_token_q_step_count(self):
        return self._q_steps

    def get_space_name(self, total_steps):
        current_position = (self._start + total_steps) % 56
        if total_steps == -1:
            return "H"
        if total_steps == 0:
            return "R"
        if self._player_pos != "A":
            if self._start > current_position > self._end:
                return self._player_pos + str(current_position - self._end)
            else:
                return str(current_position + 1)
        else:
            if current_position > self._end:
                return self._player_pos + str(current_position - self._end)
            else:
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

    def move_token(self, player, token, steps):
        pass

    def play_game(self, players_list, turns_list):
        board = Board()
        pass
