from classes import *
import copy
import tkMessageBox
from Tkinter import *
from CheckersPiece import CheckersPiece
from CheckersBoard import CheckersBoard


class CheckersBoardUI(object):
    """The gui implementation of checkers board for two human players.
    holds CheckersBoard as a class member and uses its logic methods \ routines."""
    _game_board = CheckersBoard
    game = Game
    _game_board_ui = []
    _white_pieces_ui = []
    _red_pieces_ui = []
    _tile_width = 31
    _tile_height = 31
    _tile_border = .75
    _highlighted_tiles = []
    _last_clicked_tile_id = None
    _current_clicked_tile_id = None
    _is_light_on = True
    _checker_border = 4
    _selected_ui_piece = CheckersPiece
    _red_pieces_counter = 12
    _white_pieces_counter = 12
    _new_game_button = Button
    _forfeit_button = Button
    _turn_indicator_label = Label
    _canvas_offset = 25

    def __init__(self, master):
        self.master = master
        self.master.title("Checkers Game")
        self._game_board = CheckersBoard()
        self.set_pieces_counters_labels()
        self.set_turn_indicator_label()
        self.set_canvas()
        self.create_board_tiles()
        self.set_game_buttons()
        self.set_pieces_counter_labels_initial_text()
        self.set_turn_indicator_label_initial_text()

    def start_new_game(self):
        if self._game_board is None:
            self._game_board = CheckersBoard()

        #game = Game()
        self.game = Game()
        self.create_board_checkers()
        self._new_game_button.config(state=DISABLED)
        self._forfeit_button.config(state='normal')
        self.update_pieces_counters_labels_text()
        self.update_turn_label_text()

    def forfeit_game(self):
        self._new_game_button.config(state='normal')
        self._forfeit_button.config(state=DISABLED)
        winner = self._game_board.forfeit_game()
        self.declare_winner_popup(winner)
        self._on_game_over()

    def _on_game_over(self):
        self._new_game_button.config(state='normal')
        self._forfeit_button.config(state=DISABLED)
        self.clean_up_ui_board()
        self._game_board = None
        self.set_pieces_counter_labels_initial_text()
        self.set_turn_indicator_label_initial_text()

    def clean_up_ui_board(self):
        self._clear_highlighted_tiles()
        canvas_ui_pieces = self._red_pieces_ui + self._white_pieces_ui
        for canvas_ui_piece in canvas_ui_pieces:
            self.canvas.delete(canvas_ui_piece[0])
            if canvas_ui_piece[1].color == "Red":
                self._red_pieces_ui.remove(canvas_ui_piece)
            elif canvas_ui_piece[1].color == "Beige":
                self._white_pieces_ui.remove(canvas_ui_piece)

    def declare_tie_popup(self):
        tkMessageBox.showinfo("Game Over!", "It's A Tie!")

    def declare_winner_popup(self, winner):
        winning_msg = '{} {}'.format(winner, 'Wins!')
        tkMessageBox.showinfo("Game Over!", winning_msg)

    def set_game_buttons(self):
        self._new_game_button = Button(self.master, text="New Game", command=self.start_new_game)
        self._forfeit_button = Button(self.master, text="Forfeit", command=self.forfeit_game, state=DISABLED)
        self._new_game_button.pack()
        self._forfeit_button.pack()

    def set_turn_indicator_label(self):
        self._turn_indicator_label = Label(self.master)
        self._turn_indicator_label.pack()

    def set_canvas(self):
        self.canvas = Canvas(self.master, bg = "beige", height = 300, width = 300)
        self.canvas.pack()

    def set_pieces_counters_labels(self):
        self._red_pieces_counter = Label(self.master)
        self._white_pieces_counter = Label(self.master)
        self._red_pieces_counter.pack()
        self._white_pieces_counter.pack()

    def update_turn_label_text(self):
        current_turn_text = "{}{}".format(self._game_board.current_player_color, "\'s Turn!")
        self._turn_indicator_label.config(text = current_turn_text)

    def update_pieces_counters_labels_text(self):
        self._red_pieces_counter.config(text="Red: %i" % self._game_board.red_pieces_count)
        self._white_pieces_counter.config(text="Beige: %i" % self._game_board.white_pieces_count)

    def set_pieces_counter_labels_initial_text(self):
        self._red_pieces_counter.config(text="Red:")
        self._white_pieces_counter.config(text="Beige:")

    def set_turn_indicator_label_initial_text(self):
        self._turn_indicator_label.config(text = "")

    def create_board_tiles(self):
        width = self._tile_width
        height = self._tile_height

        for i in range(self._game_board.Rows):
            top_left_x = (i * width + self._tile_border) + self._canvas_offset
            bottom_right_x = ((i + 1) * width - self._tile_border) + self._canvas_offset
            for j in range(self._game_board.Cols):
                top_left_y = (j * height + self._tile_border) + self._canvas_offset
                bottom_right_y = ((j + 1) * height - self._tile_border) + self._canvas_offset
                tile_unique_id = 0
                if (i + j) % 2 == 0:
                    tile_unique_id = self.canvas.create_rectangle(top_left_x, top_left_y, bottom_right_x,
                                                                  bottom_right_y, fill="red")
                else:
                    tile_unique_id = self.canvas.create_rectangle(top_left_x, top_left_y, bottom_right_x,
                                                                  bottom_right_y, fill="black")

                if tile_unique_id != 0:
                    self._game_board_ui.append(
                        (tile_unique_id, j, i, top_left_x, bottom_right_x, top_left_y, bottom_right_y))

    def create_board_checkers(self):
        checker_border = self._checker_border
        max_white_pieces_row = 3

        white_pieces = self._game_board.get_white_pieces()
        red_pieces = self._game_board.get_red_pieces()
        all_pieces = white_pieces + red_pieces

        for piece in all_pieces:
            # x1 and x2 coords of the oval checkers piece's form
            x1 = ((piece.col * self._tile_width) + checker_border) + self._canvas_offset
            x2 = ((piece.col + 1) * self._tile_width - checker_border) + self._canvas_offset

            # y1 and y2 coords of the oval checkers piece's form
            y1 = (piece.row * self._tile_width + checker_border) + self._canvas_offset
            y2 = ((piece.row + 1) * self._tile_width - checker_border) + self._canvas_offset

            # Draw the checker on the board, giving it a color tag and an id tag
            piece_id_tag = self.canvas.create_oval(x1, y1, x2, y2, fill = piece.color)
            self.canvas.tag_bind(piece_id_tag, "<ButtonPress-1>", self._analyze_checker_click)

            if piece.color == "Red":
                self._red_pieces_ui.append((piece_id_tag, piece))
            elif piece.color == "Beige":
                self._white_pieces_ui.append((piece_id_tag, piece))

    def get_tile_id(self, row_, col_):
        found_tile_id = 0
        row = row_
        col = col_
        ui_board_length = len(self._game_board_ui)
        for i in range(ui_board_length):
            if row == self._game_board_ui[i][1] and col == self._game_board_ui[i][2]:
                found_tile_id = self._game_board_ui[i][0]
                break

        return found_tile_id

    def _analyze_highlighted_tile_click(self, event):
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        id_tag = self.canvas.find_closest(x, y)[0]

        # get the new board position where the selected checker is about to be placed.
        new_row = -1
        new_col = -1
        for tile in self._game_board_ui:
            is_position_found = tile[0] == id_tag
            if is_position_found:
                new_row = tile[1]
                new_col = tile[2]

        is_position_valid = self._game_board.is_board_position_valid(new_row, new_col)
        if is_position_valid:
            new_position = (new_row, new_col)
            selected_checkers_piece_tag, selected_checkers_piece = self._selected_ui_piece

            piece_royalty_state_before_movement = selected_checkers_piece.king
            updated_moved_piece = self._game_board.make_move(selected_checkers_piece, new_position)
            self._selected_ui_piece = (selected_checkers_piece_tag, copy.copy(updated_moved_piece))
            self._turn_tiles_light_off()

            # placing the piece in its new position on the gui board
            # x1 and x2 coords of the oval checkers piece's form
            x1 = ((self._selected_ui_piece[1].col * self._tile_width) + self._checker_border) + self._canvas_offset
            x2 = ((self._selected_ui_piece[1].col + 1) * self._tile_width - self._checker_border) + self._canvas_offset

            # y1 and y2 coords of the oval checkers piece's form
            y1 = (self._selected_ui_piece[1].row * self._tile_width + self._checker_border) + self._canvas_offset
            y2 = ((self._selected_ui_piece[1].row + 1) * self._tile_width - self._checker_border) + self._canvas_offset

            # draw the piece in its new position
            self.canvas.coords(selected_checkers_piece_tag, (x1, y1, x2, y2))

            self._handle_ui_game_state()
            # handle piece royalty
            if updated_moved_piece.king and not piece_royalty_state_before_movement:
                self.canvas.itemconfig(selected_checkers_piece_tag, outline="cyan")
                if updated_moved_piece.color == "Red":
                    for r_piece in self._red_pieces_ui:
                        if r_piece[1].piece_id == updated_moved_piece.piece_id:
                            r_piece[1].king = True
                elif updated_moved_piece.color == "Beige":
                    for w_piece in self._white_pieces_ui:
                        if w_piece[1].piece_id == updated_moved_piece.piece_id:
                            w_piece[1].king = True

            # updating the piece in its corresponding list
            self._update_piece_location_in_list()
            last_move_eaten_piece = None
            if self._game_board is not None:
                last_move_eaten_piece = self._game_board.get_eaten_piece()
            eaten_ui_piece_tag = None
            if last_move_eaten_piece is not None:
                eaten_ui_piece_tag = self._find_ui_piece_tag(last_move_eaten_piece)
                self.update_pieces_counters_labels_text()
                if eaten_ui_piece_tag is not None:
                    self.canvas.delete(eaten_ui_piece_tag)

            if self._game_board is not None:
                self.update_turn_label_text()

    def _handle_ui_game_state(self):
        if self._game_board.is_game_over:
            winner = self._game_board.winner
            if winner is not None:
                self.declare_winner_popup(winner)
            else:
                self.declare_tie_popup()

            self._on_game_over()

    # Description: searches for the specified piece tag. if found, returns the found tag, else: returns None.
    def _find_ui_piece_tag(self, checker_piece):
        ui_piece_tag = None
        for r_piece in self._red_pieces_ui:
            if r_piece[1].piece_id == checker_piece.piece_id:
                ui_piece_tag = r_piece[0]
                break

        if ui_piece_tag is None:
            for w_piece in self._white_pieces_ui:
                if w_piece[1].piece_id == checker_piece.piece_id:
                    ui_piece_tag = w_piece[0]
                    break

        return ui_piece_tag

    # Description: updates ui piece in its corresponding list
    def _update_piece_location_in_list(self):
        is_piece_found = False

        for r_piece in self._red_pieces_ui:
            if r_piece[1].piece_id == self._selected_ui_piece[1].piece_id:
                r_piece[1].row = self._selected_ui_piece[1].row
                r_piece[1].col = self._selected_ui_piece[1].col
                is_piece_found = True
                break

        if not is_piece_found:
            for w_piece in self._white_pieces_ui:
                if w_piece[1].piece_id == self._selected_ui_piece[1].piece_id:
                    w_piece[1].row = self._selected_ui_piece[1].row
                    w_piece[1].col = self._selected_ui_piece[1].col
                    is_piece_found = True
                    break

    def _turn_tiles_light_off(self):
        self._is_light_on = True
        self._toggle_highlighted_tiles_light()

    # Description: sets the specified board positions borders' color to yellow.
    def _highlight_tiles(self):
        for move_position in self._highlighted_tiles:
            x, y = move_position
            highlighted_tile_id = self.get_tile_id(x, y)
            self.canvas.itemconfig(highlighted_tile_id, outline = "yellow")
            self.canvas.tag_bind(highlighted_tile_id, "<ButtonPress-1>", self._analyze_highlighted_tile_click)

    def _clear_highlighted_tiles(self):
        for highlighted_tile in self._highlighted_tiles:
            x, y = highlighted_tile
            highlighted_tile_id = self.get_tile_id(x, y)
            self.canvas.itemconfig(highlighted_tile_id, outline = "black")

    # Description: toggles highlighted tiles light
    def _toggle_highlighted_tiles_light(self):
        for tile in self._highlighted_tiles:
            x, y = tile
            tile_id = self.get_tile_id(x, y)
            if self._is_light_on:
                self.canvas.itemconfig(tile_id, outline = "black")
            else:
                self.canvas.itemconfig(tile_id, outline = "yellow")

        self._is_light_on = not self._is_light_on

    def unbind_highlighted_tiles_events(self):
        for tile in self._highlighted_tiles:
            x, y = tile
            tile_id = self.get_tile_id(x, y)
            self.canvas.tag_unbind(tile_id, "<ButtonPress-1>")

    # Description: Once a checker piece is clicked, highlights its allowed moves
    def _analyze_checker_click(self, event):
        self._clear_highlighted_tiles()
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        checker_id_tag = self.canvas.find_closest(x, y)[0]
        found_ui_piece = self._get_checker_piece(checker_id_tag)
        found_piece = found_ui_piece[1]
        self._selected_ui_piece = found_ui_piece
        self._current_clicked_tile_id = self.get_tile_id(found_piece.row, found_piece.col)

        if self._current_clicked_tile_id != self._last_clicked_tile_id:
            self.unbind_highlighted_tiles_events()
            allowed_moves = self._game_board.get_allowed_moves(found_piece)
            self._highlighted_tiles = allowed_moves
            self._highlight_tiles()
            self._last_clicked_tile_id = self._current_clicked_tile_id
        else:
            self._toggle_highlighted_tiles_light()

    def _get_checker_piece(self, id_tag):
        found_piece = 0
        for w_piece in self._white_pieces_ui:
            if w_piece[0] == id_tag:
                found_piece = w_piece
                break

        if found_piece == 0:
            for r_piece in self._red_pieces_ui:
                if r_piece[0] == id_tag:
                    found_piece = r_piece
                    break;

        return found_piece
