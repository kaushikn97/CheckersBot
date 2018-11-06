from CheckersPiece import CheckersPiece
import copy


class CheckersBoard(object):
    """Checkers Game Board Logic"""
    __rows = 8
    __cols = 8
    __white_pieces = list()
    __redPieces = list()
    __board = [[CheckersPiece for x in range(__rows)] for y in range(__cols)]
    __red_pieces_count = 12
    __white_pieces_count = 12
    __whitePlayerID = 0
    __red_player_id = 1
    _current_player = 1
    __is_last_move_is_jump = False
    __last_move_eaten_piece = None
    __winner = None
    __is_game_over = False

    # Description: Initializes a new Board with its initial settings.
    def __init__(self):
        self.__initRedPieces()
        self.__initWhitePieces()
        self.__initBoard()

    # Description: Prints the board current state. used for debugging.
    def print_board_state(self):
        for i in range(self.__rows):
            for j in range(self.__cols):
                piece = self.__board[i][j]
                print "board[", i, "]", "[", j, "]=", piece.color, "ID =", piece.piece_id

    # Description: returns the current board state
    def get_board_state(self):
        board = self.__board
        return board

    # Description: Initalizes the red pieces dict to its initial state:
    # holding 12 pieces: each piece is represented by a unique id key and the
    # the piece's value is its starting position on the board.
    def __initWhitePieces(self):
        maxWhiteRow = 3
        uniqueID = 13
        isKing = False
        for i in range(maxWhiteRow):
            for j in range(self.__cols):
                isPlacedByRedPiece = (i + j) % 2 == 1
                if (isPlacedByRedPiece):
                    piece = CheckersPiece(i, j, "Beige", isKing, uniqueID, self.__whitePlayerID)
                    self.__white_pieces.append(piece)
                    uniqueID += 1

    # Description: Initalizes the red pieces dict to its initial state:
    # holding 12 pieces: each piece is represented by a unique id key and the
    # the piece's value is its starting position on the board.
    def __initRedPieces(self):
        minRedRow = 5
        uniqueID = 1
        isKing = False
        for i in range(minRedRow, self.__rows):
            for j in range(self.__cols):
                isPlacedByRedPiece = (i + j) % 2 == 1
                if (isPlacedByRedPiece):
                    piece = CheckersPiece(i, j, "Red", isKing, uniqueID, self.__red_player_id)
                    self.__redPieces.append(piece)
                    uniqueID += 1

    def get_white_pieces(self):
        white_pieces = []
        for piece in self.__white_pieces:
            white_pieces.append(piece)

        return white_pieces

    def get_red_pieces(self):
        red_pieces = []
        for piece in self.__redPieces:
            red_pieces.append(piece)

        return red_pieces

    # region: public API

    # Description: Initializes a new board and sets it ready for a new game.
    def __initBoard(self):
        self.__board = [[CheckersPiece for x in xrange(self.__rows)] for y in xrange(self.__cols)]
        # placing the red & white pieces on the board
        for i in range(len(self.__redPieces)):
            redX, redY = self.__redPieces[i].row, self.__redPieces[i].col
            whiteX, whiteY = self.__white_pieces[i].row, self.__white_pieces[i].col
            self.__board[redX][redY] = self.__redPieces[i]
            self.__board[whiteX][whiteY] = self.__white_pieces[i]

    # Description: returns string Red or White.
    @property
    def red_pieces_count(self):
        return self.__red_pieces_count

    @property
    def white_pieces_count(self):
        return self.__white_pieces_count

    @property
    def current_player_color(self):
        return "Red" if self._current_player == self.__red_player_id else "Beige"

    # Description: Board matrix rows length
    @property
    def Rows(self):
        return self.__rows

    # Description: Board matrix cols length
    @property
    def Cols(self):
        return self.__cols

    # Description: Red playerID
    @property
    def RedPlayerID(self):
        return self.__red_player_id

    # Description: White playerID
    @property
    def WhitePlayerID(self):
        return self.__whitePlayerID

    # Description: returns the piece which is placed in the given board-key.
    def __getitem__(self, key):
        x, y = key
        return self.__board[x][y]

        # Description: returns a list containing the allowed jumps regarding the specified piece.

    def getAllowedJumps(self, piece_, occupied_positions):
        returned_jumps = []
        color = piece_.color
        for position in occupied_positions:
            x, y = position
            occupying_piece = self.__board[x][y]
            if occupying_piece.color != piece_.color:
                # check if piece can jump over occupying piece.
                # if true, append this jumped x, y position to returned_jumps
                jumped_x_coord = occupying_piece.row - (piece_.row - occupying_piece.row)
                jumped_y_coord = occupying_piece.col - (piece_.col - occupying_piece.col)
                if self.is_board_position_valid(jumped_x_coord, jumped_y_coord):
                    is_diagonal_position_free = not (self.isOccupied(jumped_x_coord, jumped_y_coord))
                    if is_diagonal_position_free:
                        returned_jumps.append((jumped_x_coord, jumped_y_coord))

        return returned_jumps

    # Description: returns a list containing the neighbors' positions.
    # the length of the list will be ranging from 1 to 4.
    def get_neighbors_positions(self, row_, col_):
        returned_neighbors = []
        if not (self.is_board_position_valid(row_, col_)):
            raise ValueError("position is out of board!")
        else:
            is_not_on_edge = row_ > 0 and row_ < self.__rows - 1 and col_ > 0 and col_ < self.__cols - 1
            is_on_bottom_left = row_ == self.__rows - 1 and col_ == 0
            is_on_top_right = row_ == 0 and col_ == self.__cols - 1
            is_on_first_line = row_ == 0 and col_ > 0 and col_ < self.__cols - 1
            is_on_last_line = row_ == self.__rows - 1 and col_ > 0 and col_ < self.__cols - 1
            is_on_left_col = row_ > 0 and row_ < self.__rows - 1 and col_ == 0
            is_on_right_col = row_ > 0 and row_ < self.__rows - 1 and col_ == self.__cols - 1
            if is_not_on_edge:
                returned_neighbors.append((row_ - 1, col_ + 1))
                returned_neighbors.append((row_ - 1, col_ - 1))
                returned_neighbors.append((row_ + 1, col_ + 1))
                returned_neighbors.append((row_ + 1, col_ - 1))
            elif is_on_first_line:
                returned_neighbors.append((row_ + 1, col_ + 1))
                returned_neighbors.append((row_ + 1, col_ - 1))
            elif is_on_last_line:
                returned_neighbors.append((row_ - 1, col_ + 1))
                returned_neighbors.append((row_ - 1, col_ - 1))
            elif is_on_top_right:
                returned_neighbors.append((row_ + 1, col_ - 1))
            elif is_on_bottom_left:
                returned_neighbors.append((row_ - 1, col_ + 1))
            elif is_on_left_col:
                returned_neighbors.append((row_ - 1, col_ + 1))
                returned_neighbors.append((row_ + 1, col_ + 1))
            elif is_on_right_col:
                returned_neighbors.append((row_ - 1, col_ - 1))
                returned_neighbors.append((row_ + 1, col_ - 1))

            return returned_neighbors

    def __find_piece(self, piece_, pieces_list):
        piece_id = piece_.piece_id
        found_piece = None
        for colored_piece in pieces_list:
            if colored_piece.piece_id == piece_id:
                found_piece = colored_piece
                break

        return found_piece

    def get_occupied_free_neighbors_positions(self, piece, neighbors_):
        free_positions = []
        occupied_positions = []
        player_id_ = piece.player_id
        row, col = piece.row, piece.col

        for neighbor in neighbors_:
            x, y = neighbor
            if not (self.isOccupied(x, y)):
                free_positions.append((x, y))
            else:
                occupied_positions.append((x,y))
                if piece.king:
                    occupied_positions.append((x, y))
                elif player_id_ == self.__red_player_id and x < row:
                    occupied_positions.append((x, y))
                elif player_id_ == self.__whitePlayerID and x > row:
                    occupied_positions.append((x, y))

        return occupied_positions, free_positions

    # Description: returns the allowed positions one can go to on the board from the specified position.
    def get_allowed_moves(self, piece_):
        player_id_ = piece_.player_id
        piece = self.__find_piece(piece_, self.__redPieces) if self.__red_player_id == player_id_ else self.__find_piece(
            piece_, self.__white_pieces)
        row, col = piece.row, piece.col
        neighbors = self.get_neighbors_positions(row, col)
        allowed_jumps = []
        free_positions = []
        occupied_positions = []
        allowed_regular_moves = []
        allowed_moves = []

        # 1. nothing is available: the chosen piece color does not belong to the player who owns the current turn.
        is_not_chosen_piece_player_turn = piece_.color != self.current_player_color
        if is_not_chosen_piece_player_turn:
            return allowed_moves

        occupied_positions, free_positions = self.get_occupied_free_neighbors_positions(piece_, neighbors)

        if not piece_.king:
            for position in free_positions:
                x, y = position
                if player_id_ == self.__red_player_id and x < row:
                    allowed_regular_moves.append(position)
                if player_id_ == self.__whitePlayerID and x > row:
                    allowed_regular_moves.append(position)
        else:
            # a king can walk in all directions
            allowed_regular_moves = free_positions

        allowed_jumps = self.getAllowedJumps(piece, occupied_positions)
        if len(allowed_jumps) > 0:
            # if any jump is available, then it must be taken.
            allowed_moves = allowed_jumps + allowed_regular_moves
        else:
            # there is no jump available per this piece.
            allowed_moves = allowed_regular_moves
            skip_id = piece_.piece_id
            pieces_list = self.__redPieces if piece_.color == "Red" else self.__white_pieces
            #is_any_jump_available_for_other_player_piece = self.is_any_jump_available_for_player(skip_id, pieces_list)
            """if is_any_jump_available_for_other_player_piece:
                # this player must take a jump move with another piece,
                # therefore the player's chosen piece has no moves available.
                del allowed_moves
                allowed_moves = []"""

        return allowed_moves

        """def is_any_jump_available_for_player(self, skip_id, pieces_list):
        is_any_jump_found = False
        for current_piece in pieces_list:
            if current_piece.piece_id == skip_id:
                continue

            current_piece_neighbors = self.get_neighbors_positions(current_piece.row, current_piece.col)
            current_piece_occupied_positions = self.get_occupied_free_neighbors_positions(current_piece, current_piece_neighbors)[0]
            self.get_occupied_free_neighbors_positions(current_piece, current_piece_neighbors)[0]
            allowed_jumps = self.getAllowedJumps(current_piece, current_piece_occupied_positions)
            if len(allowed_jumps) > 0:
                is_any_jump_found = True
                break

        return is_any_jump_found"""

    # Description: returns the eaten piece if the last taken move was a jump, else: returns None.
    def get_eaten_piece(self):
        eaten_piece = None
        if self.__is_last_move_is_jump:
            eaten_piece = self.__last_move_eaten_piece

        return eaten_piece

    # Description: moves the specified player's(red or white) pieceID to the specified position.
    def make_move(self, piece_, new_board_position_):
        if self.is_game_over:
            return None

        self.__is_last_move_is_jump = False
        self.__last_move_eaten_piece = None
        is_move_allowed = False
        all_allowed_moves = self.get_allowed_moves(piece_)
        for allowed_position in all_allowed_moves:
            if new_board_position_ == allowed_position:
                is_move_allowed = True
                break

        if is_move_allowed:
            piece_old_row = piece_.row
            piece_old_col = piece_.col
            # getting new row,col position and placing piece in its new position
            piece_new_row, piece_new_col = new_board_position_
            copied_piece = copy.copy(piece_)
            copied_piece.row = piece_new_row
            copied_piece.col = piece_new_col
            if not (copied_piece.king):
                self._determine_moved_piece_royality(copied_piece)
            self.__board[piece_new_row][piece_new_col] = copied_piece

            # removing the playing piece from its old position on the board.
            self.__board[piece_old_row][piece_old_col] = CheckersPiece

            # if this move is a jump, then one of the opponent's pieces has been eaten.
            # remove it from the board and update the counters.
            is_jump_taken = abs(piece_old_row - piece_new_row) > 1 and abs(piece_old_col - piece_new_col) > 1
            if is_jump_taken:
                self.__is_last_move_is_jump = True
                factor_x = -1 if piece_old_row - piece_new_row < 0 else 1
                factor_y = -1 if piece_old_col - piece_new_col < 0 else 1
                last_eaten_x = piece_old_row - factor_x
                last_eaten_y = piece_old_col - factor_y
                self.__last_move_eaten_piece = copy.copy(self.__board[last_eaten_x][last_eaten_y])
                self.__board[last_eaten_x][last_eaten_y] = CheckersPiece
                container_eaten_piece_list = self.__redPieces if self.__last_move_eaten_piece.color == "Red" else self.__white_pieces
                self.remove_eaten_piece_from_its_container(self.__last_move_eaten_piece, container_eaten_piece_list)
                self.__update_eaten_player_pieces_counter()

            self.__handle_game_state()
            if not self.__is_game_over:
                self._determine_next_turn_owner(copied_piece, is_jump_taken)

            return copied_piece
        else:
            old_position = (piece_old_row, piece_old_col)
            error_msg = '{} {} {} {}'.format('forbidden move!', new_board_position_, 'from', old_position)
            raise ValueError(error_msg)

    def _determine_next_turn_owner(self, moved_piece, is_jump_taken):
        """if not (is_jump_taken):
            self._current_player = not (self._current_player)
        else:
            # if the specified moved piece can make another jump, then it must be taken
            allowed_jumps = []
            moved_piece_neighbors = self.get_neighbors_positions(moved_piece.row, moved_piece.col)
            moved_piece_occupied_positions = \
            self.get_occupied_free_neighbors_positions(moved_piece, moved_piece_neighbors)[0]
            allowed_jumps = self.getAllowedJumps(moved_piece, moved_piece_occupied_positions)
            if len(allowed_jumps) == 0:
                self._current_player = not (self._current_player)"""
        self._current_player = not (self._current_player)

    def remove_eaten_piece_from_its_container(self, piece_to_remove, container_list):
        for current_piece in container_list:
            if current_piece.piece_id == piece_to_remove.piece_id:
                container_list.remove(current_piece)
                break

    def _determine_moved_piece_royality(self, moved_piece):
        is_piece_reached_opponent_inner_row = False

        if moved_piece.color == "Red":
            is_piece_reached_opponent_inner_row = moved_piece.row == 0
            moved_piece.king = is_piece_reached_opponent_inner_row
            if moved_piece.king:
                for r_piece in self.__redPieces:
                    if r_piece.piece_id == moved_piece.piece_id:
                        r_piece.king == True

        elif moved_piece.color == "Beige":
            is_piece_reached_opponent_inner_row = moved_piece.row == self.__rows - 1
            moved_piece.king = is_piece_reached_opponent_inner_row
            if moved_piece.king:
                for w_piece in self.__white_pieces:
                    if w_piece.piece_id == moved_piece.piece_id:
                        w_piece.king == True

    # Description: updates the eaten player's pieces counter
    def __update_eaten_player_pieces_counter(self):
        if self.__last_move_eaten_piece is not None:
            eaten_piece = self.__last_move_eaten_piece
            if eaten_piece.color == "Beige":
                self.__white_pieces_count -= 1 if self.__white_pieces_count - 1 >= 0 else 0
            elif eaten_piece.color == "Red":
                self.__red_pieces_count -= 1 if self.__red_pieces_count - 1 >= 0 else 0

    # Description: Determines whether the game is over: win is detected or its a tie.
    def __handle_game_state(self):
        is_win = self._is_win_detected()
        self.__is_game_over = is_win
        if self.is_game_over:
            self.__on_game_over()

    @property
    def winner(self):
        return self.__winner

    @property
    def is_game_over(self):
        return self.__is_game_over

    def forfeit_game(self):
        self.__is_game_over = True
        self.__winner = "Red" if self._current_player == self.__whitePlayerID else "Beige"
        self.__on_game_over()
        return self.__winner

    # endregion: public API

    def __on_game_over(self):
        for i in range(len(self.__white_pieces)):
            self.__white_pieces.pop()
        for i in range(len(self.__redPieces)):
            self.__redPieces.pop()

    # Description: a naive approach according to which a win is detected once one of the players has no pieces left.
    def _is_win_detected(self):
        self.__winner = None
        is_red_wins = self.__red_pieces_count > 0 and self.__white_pieces_count == 0
        is_white_wins = self.__white_pieces_count > 0 and self.__red_pieces_count == 0
        if is_red_wins:
            self.__winner = "Red"
        elif is_white_wins:
            self.__winner = "Beige"

        self.__is_game_over = self.__winner != None
        return self.__is_game_over

    # Description: Determines whether the specified position is occupied by any
    # piece.  returns false if its empty\free.
    def isOccupied(self, row_, col_):
        return isinstance(self.__board[row_][col_], CheckersPiece)

    # Description: Determines whether the specified position(row & col) is
    # within the board's range.  used for validating positions where pieces are
    # placed.
    def is_board_position_valid(self, row_, col_):
        return self.__isRowValid(row_) and self.__isColValid(col_)

    # Description: Determines whether the specified row index is within the
    # board's rows range.
    def __isRowValid(self, _row):
        return _row >= 0 and _row < self.__rows

    # Description: Determines whether the specified col index is within the
    # board's cols range.
    def __isColValid(self, _col):
        return _col >= 0 and _col < self.__cols
