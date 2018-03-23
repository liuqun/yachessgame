# -*- encoding:utf-8 -*-

class ChessboardSandbox:
    def __init__(self):
        self.data = {}
        self.empty()

    def empty(self):
        for y_str in '1', '2', '3', '4', '5', '6', '7', '8':
            for x_str in 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H':
                coordinate_str = x_str + y_str
                coordinate = parse_coordinate_str(coordinate_str)
                self.data[coordinate] = None

    def print_status(self):
        print('   A B C D E F G H')
        for y_str in '8', '7', '6', '5', '4', '3', '2', '1':
            print('%s:' % y_str, end='')
            for x_str in 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H':
                coordinate_str = x_str + y_str
                coordinate = parse_coordinate_str(coordinate_str)
                piece_symbol = '-'
                piece_id = self.data[coordinate]
                if piece_id:
                    piece_symbol = '@'
                print(' %s' % piece_symbol, end='')
            print()
        print('   A B C D E F G H')

    def mark(self, coordinate_str, piece_id):
        coordinate = parse_coordinate_str(coordinate_str)
        self.data[coordinate] = piece_id
        return

    def erase(self, coordinate_str):
        self.mark(coordinate_str, None)
        return

    def get_piece_id(self, coordinate_str):
        coordinate = parse_coordinate_str(coordinate_str)
        id = self.data[coordinate]
        return id


def parse_coordinate_str(coordinate_str):
    """坐标解析

    将字符串"A1"～"H8"转换为二维坐标(x, y), 要求字符串第一个字符必须是[a-h|A-H], 第二个字符必须是[1-8].
    否则抛出一个 ValueError 异常.
    :return 坐标位置 (x, y)
    :rtype : tuple
    :type coordinate_str: str
    """
    if len(coordinate_str) < 2:
        raise ValueError('Invalid coordinate str %r' % (coordinate_str))
    x = ord(coordinate_str[0].upper()) - ord('A')
    y = ord(coordinate_str[1]) - ord('1')
    if x >= 0 and x < 8 and y >= 0 and y < 8:
        return x, y
    raise ValueError('Invalid coordinate str %r' % (coordinate_str))


class Piece:
    id = None
    owner_id = None
    move_directions = set()
    range_limit = 0  # 棋子最大移动格数, 用正整数 N 代表棋子最大移动距离(倍数 N). 例如王只能移动1格(N=1), 车象后可以移动7格(N=7)

    def __repr__(self):
        id = self.id or -1
        owner_id = self.owner_id or -1
        s = '<%s id=%d,owner_id=%d>' % (type(self).__name__, id, owner_id)
        return s

    def get_fire_coverage(self, coordinate, chessboard_data):
        """棋子火力范围, 包括棋子所防守的友方棋子所在的格子

        :rtype : {(0,0), (7,7)}
        """
        nodes = set()
        for dx, dy in self.move_directions:
            x = coordinate[0] + dx
            y = coordinate[1] + dy
            for i in range(self.range_limit):
                if x < 0 or x >= 8 or y < 0 or y >= 8:
                    break
                nodes.add((x, y))
                target = chessboard_data[(x, y)]
                if target is None:
                    x += dx
                    y += dy
                    continue
                else:
                    break
        return nodes


class King(Piece):
    move_directions = {(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)}
    range_limit = 1


class Queen(Piece):
    move_directions = {(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)}
    range_limit = 7


class Rook(Piece):
    move_directions = {(1, 0), (0, 1), (-1, 0), (0, -1)}
    range_limit = 7


class Knight(Piece):
    move_directions = {(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)}
    range_limit = 1


class Bishop(Piece):
    move_directions = {(1, 1), (-1, 1), (-1, -1), (1, -1)}
    range_limit = 7


class Pawn(Piece):
    def get_fire_coverage(self, coordinate, chessboard_data):
        nodes = set()
        return nodes


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

    # “福斯夫-爱德华兹记号法”[Forsyth-Edwards Notation](https://en.wikipedia.org/wiki/Forsyth–Edwards_Notation)
    # 表示开局状态的 FEN 字符串为: 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'
    # FEN 为每种棋子规定了一个字母、用大小写表示黑棋或者白棋、用斜线分割不同的行、用数字表示空白
    @property
    def fen_piece_placement(self) -> str:
        fen_list = []
        for y_str in '8', '7', '6', '5', '4', '3', '2', '1':
            cnt = 0  # 统计同一行上有多少个连续空格
            for x_str in 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H':
                coordinate_str = x_str + y_str
                piece_id = self.chessboard.get_piece_id(coordinate_str)
                if piece_id is None:
                    cnt += 1
                    continue
                if cnt >= 1:
                    fen_list.append('%d' % cnt)
                    cnt = 0
                piece = self.piece_list[piece_id]
                piece_symbol = piece_symbol_from_instance(piece).upper()
                if piece.owner_id >= 2:
                    piece_symbol = piece_symbol.lower()
                # 白棋用大写字母表示, 黑棋用小写字母表示
                fen_list.append(piece_symbol)
            if cnt >= 1:
                fen_list.append('%d' % cnt)
            fen_list.append('/')
        fen_list.pop(-1)
        return ''.join(fen_list)

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

    def get_valid_destinations_of_piece_at(self, from_coordinate_str):
        piece_id = self.chessboard.get_piece_id(from_coordinate_str)
        if piece_id is None:
            raise Game.InvalidMove('There is no piece at %r' % from_coordinate_str)
        piece = self.piece_list[piece_id]
        fire_coverage = self.get_fire_coverage_of_piece_at(from_coordinate_str)
        destination_coordinates = set()
        for x, y in fire_coverage:
            target_piece_id = self.chessboard.data[(x, y)]
            if target_piece_id is None:
                pass
            else:
                target_piece = self.piece_list[target_piece_id]
                if target_piece.owner_id == piece.owner_id:  # 目的地棋盘格子上不能有己方棋子阻挡
                    continue
            destination_coordinates.add((x, y))
        # 将(x,y)坐标转换为输出字符串列表
        result = []
        for x, y in destination_coordinates:
            result.append('%c%c' % (chr(ord('A') + x), chr(ord('1') + y)))
        return sorted(result)

    def get_fire_coverage_of_piece_at(self, coordinate_str):
        piece_id = self.chessboard.get_piece_id(coordinate_str)
        if piece_id is None:
            raise Game.InvalidMove('There is no piece at %r' % coordinate_str)
        piece = self.piece_list[piece_id]
        coordinate = parse_coordinate_str(coordinate_str)
        return piece.get_fire_coverage(coordinate, chessboard_data=self.chessboard.data)


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
    # 棋子走法求解展示:
    print('Check available moves of the black queen at D5:')
    black_queen_move_selections = game.get_valid_destinations_of_piece_at('D5')
    print(sorted(black_queen_move_selections))
    print()
    print('Check available moves of the white knight at C3:')
    white_knight_c3_move_selections = game.get_valid_destinations_of_piece_at('C3')
    print(sorted(white_knight_c3_move_selections))
    print()
