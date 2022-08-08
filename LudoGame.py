# Author: Jeffrey Wang
# GitHub username: Jeffrey-Wang98
# Date: July 23, 2022
# Description:
class InvalidPositionError(Exception):
    """
    Error for when a position other than A, B, C, or D is entered. Will not be handled since Player construction was not
    meant to be done outside LudoGame.
    """
    pass


class InvalidTokenError(Exception):
    """
    Error for move_token() when an invalid token is chosen for movement. Will be handled by play_game() to skip
    that turn
    """
    pass


class InvalidPlayerError(Exception):
    """
    Error for when something other than A, B, C, or D is given for a turn that's not theirs to move. Will be handled by
    play_game() to skip that turn.
    """
    pass


class Board:
    """
    This class controls the board state and stores each piece in a dictionary with the pace names as the keys and the
    tokens occupying those spaces as the values. Values are a list because more than one token can be on one space.
    Also knows which pieces are in the finish and which positions on the board are occupied. LudoGame will create one
    and recreate it for each new game. Will call move_piece() to update the Board each turn.
    """
    def __init__(self):
        self._board = {}
        for spaces in range(56):  # creation of the dictionary board
            self._board[str(spaces + 1)] = []
        for char in ["A", "B", "C", "D"]:  # adding in the home rows
            for num in range(1, 7):
                self._board[char + str(num)] = []
        self._finish = []  # to remember which pieces are done
        self._occupied_spaces = []  # to remember which spaces are occupied for faster search

    def get_occupied_spaces(self):
        """
        Returns the spaces on the board that have at least one token on it.

        :return: list of strings
        """
        return self._occupied_spaces

    def get_finish(self):
        """
        Returns the tokens that have reached the finish space.

        :return: list of strings
        """
        return self._finish

    def set_finish_tokens(self, token):
        """
        Allows other functions to assign tokens to self._finish.

        :param token: str. Name of the token that moves to the finish space.
        :return: None
        """
        self._finish.append(token)

    def remove_token(self, pos, token):
        """
        To remove a token from a specified board space name.

        :param pos: str. The space name.
        :param token: str. The token name to remove
        :return: None
        """
        self._board[pos].remove(token)

    def move_piece(self, token, start_pos, end_pos):
        """
        Does everything to move a piece to a new space. Kicks out pieces that are already occupying the space. Removes
        the previous occupying space from occupied spaces list. Adds pieces to the finish zone when it reaches it. Will
        move doubled pieces. When more than one token is occupying a space, occupied space only has the space name once
        in the list.

        :param token: str. Desired token to move.
        :param start_pos: str. Space name for the starting position of the token.
        :param end_pos: str. Space name for the ending position of the token.
        :return: None, list of str, str. Depends on if we need to reset a token or to make a doubled status.
        """
        print(self._occupied_spaces)
        if end_pos in self._occupied_spaces:  # going to an occupied space
            if token[0] in self._board[end_pos][0]:
                if start_pos == "R":  # when the token is brought out of ready
                    self._board[end_pos].append(token)
                    self._occupied_spaces.append(end_pos)
                else:  # when the token is moved to a space with friendly token
                    self._board[end_pos].append(token)
                    self._board[start_pos].remove(token)
                    self._occupied_spaces.remove(start_pos)
                    self._occupied_spaces.append(end_pos)
                print("DOUBLE!")
                return "DOUBLE"
            else:  # when a token is moved to a space with hostile token(s)
                if start_pos == "R":  # when the token is brought out of ready
                    removed_tokens = self._board[end_pos]
                    for _ in removed_tokens:
                        self._occupied_spaces.remove(end_pos)
                    self._board[end_pos] = []  # need to remove all tokens that were occupying that space
                    self._board[end_pos].append(token)
                    self._occupied_spaces.append(end_pos)
                    return removed_tokens  # returns the list of tokens that need to be reset
                else:
                    removed_tokens = self._board[end_pos]
                    for _ in removed_tokens:
                        self._occupied_spaces.remove(end_pos)
                    self._board[end_pos] = []  # need to remove all tokens that were occupying that space
                    self._board[end_pos].append(token)
                    self._board[start_pos].remove(token)
                    self._occupied_spaces.remove(start_pos)
                    self._occupied_spaces.append(end_pos)
                    return removed_tokens  # returns the list of tokens that need to be reset
        else:  # going to an empty space
            if end_pos == "E":  # when the token makes it to the end
                self._finish.append(token)
                self._board[start_pos].remove(token)
                self._occupied_spaces.remove(start_pos)
            elif end_pos == "H":  # when the token is sent back to home
                self._board[start_pos].remove(token)
                self._occupied_spaces.remove(start_pos)
            elif start_pos == "R":
                self._board[end_pos].append(token)  # when the token is brought out of home
                self._occupied_spaces.append(end_pos)
            else:  # when the token is moved to a new space on the board
                self._board[end_pos].append(token)
                self._board[start_pos].remove(token)
                self._occupied_spaces.remove(start_pos)
                self._occupied_spaces.append(end_pos)

    def reset_board(self):
        """
        Resets all data members to its default state for a new game.

        :return: None
        """
        for space in self._board:
            self._board[space] = []
        self._finish = []
        self._occupied_spaces = []

    def get_board(self):
        """
        Returns the board dictionary to check board state.

        :return: dict with str as keys and list of str as values
        """
        return self._board


class Player:
    """
    Contains the status of token "P" and token "Q" and where the starting and ending position for this player is. Also
    contains the status of the player for finished or not finished. Also tracks if player's pieces are doubled up.
    Will be created for each new game by LudoGame.
    """
    def __init__(self, position):
        try:
            self._player_pos = position.upper()
        except AttributeError:
            raise InvalidPositionError
        self._p_status = "HOME"  # "HOME", "READY", "ON BOARD", "FINISHED"
        self._q_status = "HOME"  # "HOME", "READY", "ON BOARD", "FINISHED"
        self._p_steps = -1
        self._q_steps = -1
        if self._player_pos == "A":
            self._start = 1
            self._end = 50
        elif self._player_pos == "B":
            self._start = 15
            self._end = 8
        elif self._player_pos == "C":
            self._start = 29
            self._end = 22
        elif self._player_pos == "D":
            self._start = 43
            self._end = 36
        else:
            raise InvalidPositionError
        self._finished = False
        self._doubled = False  # if the pieces are on the same space and will move together
        self._in_play = False

    def start(self):
        """
        Puts this Player in play. Sets self._in_play to True.

        :return: None
        """
        self._in_play = True

    def get_in_play(self):
        """
        Returns the in_play status of this Player.

        :return: True/False
        """
        return self._in_play

    def get_doubled(self):
        """
        Returns True/False if the Player's pieces are doubled.

        :return: True/False
        """
        return self._doubled

    def set_doubled(self):
        """
        Will set self._doubled to be True so that pieces will be moved together rather than individually.

        :return: None
        """
        self._doubled = True

    def get_completed(self):
        """
        Returns True or False for the player's finished status.

        :return: True/False
        """
        complete = False
        if self._finished or (self._p_status == "FINISHED" and self._q_status == "FINISHED"):
            complete = True
        return complete

    def set_completed(self):
        """
        Sets the Player self._finished to True

        :return: None
        """
        self._finished = True

    def reset_player(self):
        """
        Resets data members to its default for a new game.

        :return: None
        """
        self.reset_status_and_steps("p")
        self.reset_status_and_steps("q")
        self._in_play = False
        self._finished = False

    def reset_status_and_steps(self, token):
        """
        When a token is sent back to home, it resets the token's step count and status to "HOME". Will reset both tokens
        for the player if the player is doubled.

        :param token: str. The token that is being reset.
        :return: None
        """
        if self._doubled is True:
            self._p_steps = -1
            self._p_status = "HOME"
            self._q_steps = -1
            self._q_status = "HOME"
            self._doubled = False
        else:
            if token.upper() == "P":
                self._p_steps = -1
                self._p_status = "HOME"
            else:
                self._q_steps = -1
                self._q_status = "HOME"

    def get_player_pos(self):
        """
        Returns the position the player occupies at the table. "A", "B", "C", or "D".

        :return: str. 1 char long.
        """
        return self._player_pos

    def get_token_p_step_count(self):
        """
        Returns the step count of token p for this player. Allows for checking of its current position and next position
        on the board.

        :return: int
        """
        return self._p_steps

    def set_token_p_step_count(self, new_steps):
        """
        Sets the step count of token p for this player. Updates the token's current position after a move.

        :param new_steps: int
        :return: None
        """
        self._p_steps = new_steps

    def get_token_q_step_count(self):
        """
        Returns the step count of token q for this player. Allows for checking of its current position and next position
        on the board.

        :return: int
        """
        return self._q_steps

    def set_token_q_step_count(self, new_steps):
        """
        Sets the step count of token q for this player. Updates the token's current position after a move.

        :param new_steps: int
        :return: None
        """
        self._q_steps = new_steps

    def get_start(self):
        """
        Returns the starting position of this player. Doesn't give the actual space name, but the int for step count
        calculations.

        :return: int
        """
        return self._start

    def get_end(self):
        """
        Returns the ending position for this player. Doesn't give the actual space name, but the int for step count
        calculations.

        :return: int
        """
        return self._end

    def get_p_status(self):
        """
        Returns the status of token p. Either "HOME", "READY", "ON BOARD", or "FINISHED".

        :return: str
        """
        return self._p_status

    def set_p_status(self, new_status):
        """
        Sets the status of token p. Either "HOME", "READY", "ON BOARD", or "FINISHED".

        :param new_status: str. Must be either "HOME", "READY", "ON BOARD", or "FINISHED".
        :return: None
        """
        self._p_status = new_status

    def get_q_status(self):
        """
        Returns the status of token q. Either "HOME", "READY", "ON BOARD", or "FINISHED".

        :return: str
        """
        return self._q_status

    def set_q_status(self, new_status):
        """
        Sets the status of token q. Either "HOME", "READY", "ON BOARD", or "FINISHED".

        :param new_status: str. Must be either "HOME", "READY", "ON BOARD", or "FINISHED".
        :return: None
        """
        self._q_status = new_status

    def get_space_name(self, total_steps):
        """
        Uses a step count as a parameter or the step count for a future move. Will calculate the exact space name for
        either the current position or the future position of a token. If total_steps is more than 57, it will return
        a negative int for the number of steps a token must go back on.

        :param total_steps: int
        :return: str or int.
        """
        current_position = (self._start + total_steps - 1) % 56
        if total_steps == -1:  # when the piece is still in Home
            return "H"
        if total_steps == 0:  # when the piece is on the ready space
            return "R"
        if total_steps == 57:  # when the piece hits the finish line
            return "E"
        if total_steps > 57:  # when the piece goes past the finish line
            return 57 - total_steps
        if self._player_pos != "A":  # if the player is B - D
            if self._start > current_position > self._end:  # if the piece is on the home row
                return self._player_pos + str(current_position - self._end)
            else:  # if the piece is on the shared board spaces
                return str(current_position)
        else:  # if the player is A
            if current_position > self._end:  # if the piece is on the home row
                return self._player_pos + str(current_position - self._end)
            elif current_position == 0:
                return self._player_pos + "6"
            else:  # if the piece is on the shared board spaces
                return str(current_position)


class LudoGame:
    """
    Contains the Player and Board objects for each game session. Has the functions to return the Player object with
    the position name, to return the Board object, to move a piece for a turn, and a main recursive function to play
    the game according to the rules and the lists of players and turns for the game. Please look up the game Ludo for
    a complete set of rules for this game.
    """
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
        self._board = Board()

    def get_board(self):
        """
        Returns the Board object that LudoGame uses to remember board states.

        :return: Board
        """
        return self._board

    def get_player_by_position(self, player_position):
        """
        Returns the Player object by its name "A", "B", "C", or "D". Raises an exception if player_position is anything
        but those 4 characters.

        :param player_position: str. Must be "A", "B", "C", or "D".
        :return: Player
        """
        try:
            if player_position.upper() in self._players:
                if self._players[player_position.upper()].get_in_play() is False:
                    return "Player not found!"
                else:
                    return self._players[player_position.upper()]
            else:
                return "Player not found!"
        except AttributeError:
            return "Player not found!"

    def move_token(self, player, token, steps):
        """
        Moves the specific token for a specific player for a specific # of steps. Will raise InvalidTokenError if the
        wrong token is given. Calls Board.move_piece() in order to properly update the board state. Will update token
        step counts and token statuses for Player.

        :param player: Player. Takes the Player object, not player name.
        :param token: str. "P" or "Q" token for Player, not token name on board.
        :param steps: int. The steps for a player's turn.
        :return: str or None. If we double a player's tokens, will return "DOUBLE".
        """
        try:
            if token.upper() == "P":
                token_name = "{}_p".format(player.get_player_pos().lower())
                token_steps = player.get_token_p_step_count()
                set_token_steps = player.set_token_p_step_count  # to set "P" token step count
                set_status = player.set_p_status  # to set "P" token status
            elif token.upper() == "Q":
                token_name = "{}_q".format(player.get_player_pos().lower())
                token_steps = player.get_token_q_step_count()
                set_token_steps = player.set_token_q_step_count  # to set "Q" token step count
                set_status = player.set_q_status  # to set "Q" token status
            else:
                raise InvalidTokenError
        except AttributeError:
            raise InvalidTokenError
        start_pos = player.get_space_name(token_steps)
        end_steps = token_steps + steps
        if start_pos == "H" and steps == 6:  # we need a 6 to move this piece
            set_token_steps(0)
            set_status("READY")
            return
        if start_pos == "H" or start_pos == "E":  # space that the token cannot move from
            raise InvalidTokenError
        end_pos = player.get_space_name(end_steps)
        result = None  # assigns it a base value of None
        try:
            if end_pos < 0:
                result = self._board.move_piece(token_name, start_pos, player.get_space_name(57 + end_pos))
                set_token_steps(57 + end_pos)
        except TypeError:
            if end_pos == "E":  # if the token lands on finish
                result = self._board.move_piece(token_name, start_pos, end_pos)
                set_token_steps(57)
                set_status("FINISHED")
            elif start_pos == "R":  # if the token was on ready position
                result = self._board.move_piece(token_name, start_pos, end_pos)
                set_token_steps(end_steps)
                set_status("ON BOARD")
            else:  # if the token was anywhere else
                result = self._board.move_piece(token_name, start_pos, end_pos)
                set_token_steps(end_steps)
        if result is not None:  # resets the opponent's token(s) if it lands on something or doubles a player
            if result == "DOUBLE":  # if result is set to "DOUBLE", we landed on a friendly token
                return "DOUBLE"
            else:
                print(result)
                reset_player = self.get_player_by_position(result[0][0])
                for token in result:
                    reset_player.reset_status_and_steps(token[2])

    def rec_play_game(self, players_list, turns_list, pos):
        """
        Recursive function that loops through the turns_list and players_list to alternate turns and skip turns if the
        move is invalid. Will NOT do this for the assignment but for the future "finished" state of the game for the
        portfolio. For the assignment, it will go through the turns_list without caring for multiple turns in a row.

        :param players_list: list of str. List of "A", "B", "C", or "D" players.
        :param turns_list: list of tuples. Tuple is (player char, step count) for that turn.
        :param pos: int. Position in turns_list.
        :return: None
        """
        print("Move {}".format(pos + 1))
        print(self._board.get_occupied_spaces())
        if pos >= len(turns_list):  # base case for stopping the game
            return
        player_char, steps = turns_list[pos]  # assigning the tuple variables

        try:  # is this turn a valid player turn?
            player = self.get_player_by_position(player_char)
            print(player.get_doubled())
        except AttributeError:  # skip this turn if not
            return self.rec_play_game(players_list, turns_list, pos + 1)  # done with this turn

        if player.get_in_play() is False:  # is this Player in the game?
            return self.rec_play_game(players_list, turns_list, pos + 1)  # done with this turn

        if player.get_completed():  # if this player is all done
            return self.rec_play_game(players_list, turns_list, pos + 1)  # done with this turn

        if player.get_p_status == "FINISHED" or player.get_q_status == "FINISHED":
            if player.get_p_status == "FINISHED" and player.get_q_status == "FINISHED":
                player.set_completed()
                return self.rec_play_game(players_list, turns_list, pos + 1)  # done with this turn
            else:
                if player.get_p_status == "FINISHED":  # p is already done
                    try:
                        self.move_token(player, "q", steps)
                        return self.rec_play_game(players_list, turns_list, pos + 1)  # done with this turn
                    except InvalidTokenError:  # can't move this token
                        return self.rec_play_game(players_list, turns_list, pos + 1)  # done with this turn
                else:  # q is already done
                    try:
                        self.move_token(player, "p", steps)
                        return self.rec_play_game(players_list, turns_list, pos + 1)  # done with this turn
                    except InvalidTokenError:  # can't move this token
                        return self.rec_play_game(players_list, turns_list, pos + 1)  # done with this turn

        if player.get_doubled():  # if we just move both tokens together
            self.move_token(player, "p", steps)
            self.move_token(player, "q", steps)
            return self.rec_play_game(players_list, turns_list, pos + 1)  # done with this turn

        if steps == 6:  # checking of there are any tokens in Home
            if player.get_p_status() == "HOME":
                self.move_token(player, "p", steps)
                return self.rec_play_game(players_list, turns_list, pos + 1)  # done with this turn
            if player.get_q_status() == "HOME":
                self.move_token(player, "q", steps)
                return self.rec_play_game(players_list, turns_list, pos + 1)  # done with this turn

        p_steps = player.get_token_p_step_count()
        q_steps = player.get_token_q_step_count()

        p_future_space = player.get_space_name(p_steps + steps)
        q_future_space = player.get_space_name(q_steps + steps)
        if p_future_space == "E":  # if this will move "p" to the end
            print("We're checking if p can reach the end.")
            self.move_token(player, "p", steps)
            return self.rec_play_game(players_list, turns_list, pos + 1)  # done with this turn
        if q_future_space == "E":  # if this will move "q" to the end.
            print("We're checking if q can reach the end.")
            self.move_token(player, "q", steps)
            return self.rec_play_game(players_list, turns_list, pos + 1)  # done with this turn

        occupied_spaces = self._board.get_occupied_spaces()
        if p_future_space in occupied_spaces or q_future_space in occupied_spaces:  # check to kick opponent out
            print("We're checking if they can kick opponents")
            p_kick = False
            q_kick = False
            if p_steps + steps != q_steps and p_future_space in occupied_spaces:  # will kick opponent not double
                print(p_future_space)
                print("We can kick with p")
                p_kick = True
            if q_steps + steps != p_steps and q_future_space in occupied_spaces:  # will kick opponent not double
                print(q_future_space)
                print("We can kick with q")
                q_kick = True
            if p_kick and q_kick:  # find the furthest token if both can kick opponents out
                if p_steps < q_steps:  # p is further back than q
                    try:
                        self.move_token(player, "p", steps)
                        return self.rec_play_game(players_list, turns_list, pos + 1)  # done with this turn
                    except InvalidTokenError:
                        pass
                else:  # q is further back than p
                    try:
                        self.move_token(player, "q", steps)
                        return self.rec_play_game(players_list, turns_list, pos + 1)  # done with this turn
                    except InvalidTokenError:
                        pass
            else:  # only one of them can kick an opponent out
                if p_kick:  # p will kick opponent out
                    try:
                        self.move_token(player, "p", steps)
                        return self.rec_play_game(players_list, turns_list, pos + 1)  # done with this turn
                    except InvalidTokenError:
                        pass
                if q_kick:  # q will kick opponent out
                    try:
                        self.move_token(player, "q", steps)
                        return self.rec_play_game(players_list, turns_list, pos + 1)  # done with this turn
                    except InvalidTokenError:
                        pass

        print("p steps = {}".format(p_steps))
        print("q steps = {}".format(q_steps))
        if p_steps < q_steps:  # p token is the furthest behind
            try:
                print("We moved p")
                results = self.move_token(player, "p", steps)
                if results == "DOUBLE":  # will double up the player if this makes them doubled
                    player.set_doubled()
                return self.rec_play_game(players_list, turns_list, pos + 1)  # done with this turn
            except InvalidTokenError:
                try:
                    print("We moved q")
                    results = self.move_token(player, "q", steps)
                    if results == "DOUBLE":  # will double up the player if this makes them doubled
                        player.set_doubled()
                    return self.rec_play_game(players_list, turns_list, pos + 1)  # done with this turn
                except InvalidTokenError:
                    pass
        else:  # q token is the furthest behind
            try:
                print("We moved q")
                results = self.move_token(player, "q", steps)
                if results == "DOUBLE":  # will double up the player if this makes them doubled
                    player.set_doubled()
                return self.rec_play_game(players_list, turns_list, pos + 1)  # done with this turn
            except InvalidTokenError:
                try:
                    print("We moved p")
                    results = self.move_token(player, "p", steps)
                    if results == "DOUBLE":  # will double up the player if this makes them doubled
                        player.set_doubled()
                    return self.rec_play_game(players_list, turns_list, pos + 1)  # done with this turn
                except InvalidTokenError:
                    pass

        # Last check to see if Player is done after doing all these moves
        if player.get_p_status == "FINISHED" and player.get_q_status == "FINISHED":
            player.set_completed()

        return self.rec_play_game(players_list, turns_list, pos + 1)  # if all else can't be done

    def play_game(self, players_list, turns_list):
        """
        Uses a list of players "A", "B", "C", or "D" and a list of tuples for turns (player name, int steps) to move
        pieces on a Board. Will call rec_play_game() to play through the game. If play_game() is called after a previous
        game, it will reset the board state and player token statuses to start a new game. Will set a player to doubled
        if their pieces occupy the same space. Returns a list of str space names for every space a token is occupying.
        With be either "H" for home space, "R" for the ready position, "E" for a finished position, or a string for the
        specific space names on the board a token is occupying.

        :param players_list: list of str. List of "A", "B", "C", or "D" players.
        :param turns_list: list of tuples. Tuple is (player char, step count) for that turn.
        :return: list of str.
        """
        self._board.reset_board()
        for player in self._players:
            self._players[player].reset_player()
        players_list.sort()
        for char in players_list:
            self._players[char.upper()].start()
        self.rec_play_game(players_list, turns_list, 0)  # starts the game
        # now we start to compile the board state to return the occupied board spaces.
        positions = []
        for char in players_list:
            p_steps = self._players[char].get_token_p_step_count()
            q_steps = self._players[char].get_token_q_step_count()
            positions.append(self._players[char].get_space_name(p_steps))
            positions.append(self._players[char].get_space_name(q_steps))
        return positions
