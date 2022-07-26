# Author: Jeffrey Wang
# GitHub username: Jeffrey-Wang98
# Date: July 23, 2022
# Description:
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
            self._board[spaces + 1] = None
        self._a_home = ["a_p", "a_q"]
        self._a_row = {
            "A1": None,
            "A2": None,
            "A3": None,
            "A4": None,
            "A5": None,
            "A6": None
        }
        self._b_home = ["b_p", "b_q"]
        self._b_row = {
            "B1": None,
            "B2": None,
            "B3": None,
            "B4": None,
            "B5": None,
            "B6": None
        }
        self._c_home = ["c_p", "c_q"]
        self._d_row = {
            "C1": None,
            "C2": None,
            "C3": None,
            "C4": None,
            "C5": None,
            "C6": None
        }
        self._d_home = ["d_p", "d_q"]
        self._d_row = {
            "D1": None,
            "D2": None,
            "D3": None,
            "D4": None,
            "D5": None,
            "D6": None
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
        self._start = 1
        self._end = 50
        if position == "B":
            self._start = 15
            self._end = 8
        if position == "C":
            self._start = 29
            self._end = 22
        if position == "D":
            self._start = 43
            self._end = 36
        self._finished = False

    def get_completed(self):
        return self._finished

    def get_token_p_step_count(self):
        return self._p_steps

    def get_token_q_step_count(self):
        return self._q_steps

    def get_space_name(self, total_steps):
        current_position = (self._start + total_steps) % 56 + 1
        pass


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
