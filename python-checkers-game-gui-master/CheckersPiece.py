class CheckersPiece(object):
    player_id = 0
    piece_id = 0
    row = 0
    col = 0
    color = ""
    king = False

    def __init__(self, row_, col_, color_, king_, piece_id_, player_id_):
        self.row = row_
        self.col = col_
        self.king = king_
        self.color = color_
        self.piece_id = piece_id_
        self.player_id = player_id_

    def __str__(self):
        str_representation = '{} {} {} {} {} {} {} {} {} {} {} {}'.format(
            'Player ID =', self.player_id,
            '\nPiece ID =', self.piece_id,
            '\nrow =', self.row,
            '\ncol =', self.col,
            '\ncolor =', self.color,
            '\nis king?', self.king)
        return str_representation