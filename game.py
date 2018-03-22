# -*- encoding:utf-8 -*-

class ChessboardSandbox:
    def __init__(self):
        self.data = {}
        self.empty()

    def empty(self):
        for y_str in '1', '2', '3', '4', '5', '6', '7', '8':
            for x_str in 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H':
                coordinate_str = x_str + y_str
                coordinate = self.__parse(coordinate_str)
                self.data[coordinate] = None

    def print_status(self):
        print('   A B C D E F G H')
        for y_str in '8', '7', '6', '5', '4', '3', '2', '1':
            print('%s:' % y_str, end='')
            for x_str in 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H':
                coordinate_str = x_str + y_str
                coordinate = self.__parse(coordinate_str)
                piece_symbol = '-'
                piece_id = self.data[coordinate]
                if piece_id:
                    piece_symbol = '@'
                print(' %s' % piece_symbol, end='')
            print()
        print('   A B C D E F G H')

    def mark(self, coordinate_str, piece_id):
        coordinate = self.__parse(coordinate_str)
        self.data[coordinate] = piece_id
        return

    def erase(self, coordinate_str):
        self.mark(coordinate_str, None)
        return

    def get_piece_id(self, coordinate_str):
        coordinate = self.__parse(coordinate_str)
        id = self.data[coordinate]
        return id

    @staticmethod
    def __parse(coordinate_str) -> tuple:
        """坐标解析

        将字符串"A1"～"H8"转换为二维坐标(x, y), 要求字符串第一个字符必须是[a-h|A-H], 第二个字符必须是[1-8].
        否则抛出一个 ValueError 异常.
        :type coordinate_str: str
        :return 坐标位置 (x, y)
        """
        if len(coordinate_str) < 2:
            raise ValueError('Invalid coordinate str %r' % (coordinate_str))
        x = ord(coordinate_str[0].upper()) - ord('A')
        y = ord(coordinate_str[1]) - ord('1')
        if not x in range(8) or not y in range(8):
            raise ValueError('Invalid coordinate str %r' % (coordinate_str))
        return x, y


class Piece:
    id = None
    owner_id = None

    def __repr__(self):
        id = self.id or -1
        owner_id = self.owner_id or -1
        s = '<%s id=%d,owner_id=%d>' % (type(self).__name__, id, owner_id)
        return s


class King(Piece):
    pass


class Queen(Piece):
    pass


class Rook(Piece):
    pass


class Knight(Piece):
    pass


class Bishop(Piece):
    pass


class Pawn(Piece):
    pass


def piece_symbol_from_instance(piece_instance):
    table = {
        'King': 'K',
        'Queen': 'Q',
        'Rook': 'R',
        'Knight': 'N',
        'Bishop': 'B',
        'Pawn': 'P',
    }
    default_symbol = '?'
    symbol = table.get(type(piece_instance).__name__, default_symbol)
    return symbol


WHITE_PIECES = {
    'A1': Rook, 'H1': Rook,
    'B1': Knight, 'G1': Knight,
    'C1': Bishop, 'F1': Bishop,
    'D1': Queen,
    'E1': King,
    'A2': Pawn, 'B2': Pawn, 'C2': Pawn, 'D2': Pawn, 'E2': Pawn, 'F2': Pawn, 'G2': Pawn, 'H2': Pawn,
}
BLACK_PIECES = {
    'A8': Rook, 'H8': Rook,
    'B8': Knight, 'G8': Knight,
    'C8': Bishop, 'F8': Bishop,
    'D8': Queen,
    'E8': King,
    'A7': Pawn, 'B7': Pawn, 'C7': Pawn, 'D7': Pawn, 'E7': Pawn, 'F7': Pawn, 'G7': Pawn, 'H7': Pawn,
}


class Game():
    def __init__(self):
        self.chessboard = ChessboardSandbox()
        self.piece_list = []
        self.piece_list.append(None)
        i = 1  # 棋子编号从 1 开始, 跳过 0 值
        for coord, piece_class in WHITE_PIECES.items():
            piece = piece_class()
            piece.id = i
            piece.owner_id = 1  # 棋手编号从 1 开始, 1 代表白棋棋手, 2 代表黑棋棋手
            self.piece_list.append(piece)
            self.chessboard.mark(coord, piece.id)
            i += 1
        for coord, piece_class in BLACK_PIECES.items():
            piece = piece_class()
            piece.id = i
            piece.owner_id = 2  # 棋手编号从 1 开始, 1 代表白棋棋手, 2 代表黑棋棋手
            self.piece_list.append(piece)
            self.chessboard.mark(coord, piece.id)
            i += 1

    def print_status(self):
        print('   A B C D E F G H')
        for y_str in '8', '7', '6', '5', '4', '3', '2', '1':
            print('%s:' % y_str, end='')
            for x_str in 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H':
                coordinate_str = x_str + y_str
                piece_symbol = '-'
                piece_id = self.chessboard.get_piece_id(coordinate_str)
                if piece_id:
                    piece = self.piece_list[piece_id]
                    piece_symbol = piece_symbol_from_instance(piece).upper()
                    if piece.owner_id >= 2:
                        piece_symbol = piece_symbol.lower()
                # (默认白棋用大写字母表示, 黑棋用小写字母表示)
                print(' %s' % piece_symbol, end='')
            print()
        print('   A B C D E F G H')

    def has_piece_at(self, coordinate_str):
        piece_id = self.chessboard.get_piece_id(coordinate_str)
        return False if piece_id is None \
            else True

    def move_piece(self, from_coordinate_str, to_coordinate_str):
        piece_id = self.chessboard.get_piece_id(from_coordinate_str)
        if piece_id is None:
            raise Game.InvalidMove('There is no piece at %r' % from_coordinate_str)
        self.chessboard.erase(from_coordinate_str)
        self.chessboard.mark(to_coordinate_str, piece_id)
        # 当 from 和 to 恰好是同一个棋盘格子时, 执行上述代码后, 棋子将被放回原位置. 是否应该抛出 InvalidMove() 异常?
        return

    class InvalidMove(Exception):
        pass


if '__main__' == __name__:
    game = Game()
    # Pick up chess piece:
    selected_white_pawn = game.chessboard.get_piece_id('E2')
    selected_black_pawn = game.chessboard.get_piece_id('D7')
    # Sample moves:
    print('E2->E4')
    print()
    game.chessboard.mark('E4', selected_white_pawn)
    game.chessboard.erase('E2')
    game.print_status()
    print()
    print('D7->D5')
    print()
    game.chessboard.mark('D5', selected_black_pawn)
    game.chessboard.erase('D7')
    game.print_status()
    print()
    print('E4xD5')
    print()
    game.chessboard.mark('D5', selected_white_pawn)
    game.chessboard.erase('E4')
    game.print_status()
    print()
    # More moves:
    print('\n\nBlack queen D8xD5:\n')
    game.move_piece('D8', 'D5')
    game.print_status()
    print('\n\nWhite knight B1->C3:\n')
    game.move_piece('B1', 'C3')
    game.print_status()
