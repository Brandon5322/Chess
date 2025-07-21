# address 
# int x = 0 在記憶體的某個地方我們把它取名為 x ，並且給他一個為 0 的值。0000 0000
# int y 在記憶體的某個地方我們把它取名為 y ，並且沒給他值
# 0Xc0 bb12

# 直接給 y x 的值
# y = x

# 我直接想要從取名為 x 的抽屜參考他的值。
# pass by value / pass by address
# call by value / call by address
# y -> x

import copy

# 棋盤座標
columns = "abcdefgh"
rows = "12345678"
valid_positions = [c + r for c in columns for r in rows]

# 棋子走法邏輯（可擴充）
def is_valid_move(piece, start, end, board):
    col_s, row_s = start[0], int(start[1])
    col_e, row_e = end[0], int(end[1])
    dx = abs(ord(col_s) - ord(col_e))
    dy = abs(row_s - row_e)
    target = next((p for p in board if p[2] == end), None)

    def path_clear(path):
        return not any(p[2] in path for p in board)

    if piece[0] == "pawn":
        direction = 1 if piece[1] == "white" else -1
        start_row = 2 if piece[1] == "white" else 7
        diff_col = ord(col_e) - ord(col_s)
        diff_row = row_e - row_s

        # 一格前進
        if diff_col == 0 and diff_row == direction and not target:
            return True

        # 初始兩格
        if diff_col == 0 and row_s == start_row and diff_row == 2 * direction:
            mid_pos = col_s + str(row_s + direction)
            if not any(p[2] in [mid_pos, end] for p in board):
                return True

        # 吃子（斜走）
        if abs(diff_col) == 1 and diff_row == direction and target and target[1] != piece[1]:
            return True

    elif piece[0] == "rook":
        if col_s != col_e and row_s != row_e:
            return False
        path = []
        if col_s == col_e:
            step = 1 if row_e > row_s else -1
            for r in range(row_s + step, row_e, step):
                path.append(col_s + str(r))
        else:
            step = 1 if ord(col_e) > ord(col_s) else -1
            for c in range(ord(col_s) + step, ord(col_e), step):
                path.append(chr(c) + str(row_s))
        return path_clear(path) and (not target or target[1] != piece[1])

    elif piece[0] == "bishop":
        if dx != dy:
            return False
        step_col = 1 if col_e > col_s else -1
        step_row = 1 if row_e > row_s else -1
        path = []
        for i in range(1, dx):
            path.append(chr(ord(col_s) + i * step_col) + str(row_s + i * step_row))
        return path_clear(path) and (not target or target[1] != piece[1])

    elif piece[0] == "knight":
        return (dx, dy) in [(1, 2), (2, 1)] and (not target or target[1] != piece[1])

    elif piece[0] == "queen":
        if col_s == col_e or row_s == row_e:
            path = []
            if col_s == col_e:
                step = 1 if row_e > row_s else -1
                for r in range(row_s + step, row_e, step):
                    path.append(col_s + str(r))
            else:
                step = 1 if ord(col_e) > ord(col_s) else -1
                for c in range(ord(col_s) + step, ord(col_e), step):
                    path.append(chr(c) + str(row_s))
            return path_clear(path) and (not target or target[1] != piece[1])
        elif dx == dy:
            step_col = 1 if col_e > col_s else -1
            step_row = 1 if row_e > row_s else -1
            path = []
            for i in range(1, dx):
                path.append(chr(ord(col_s) + i * step_col) + str(row_s + i * step_row))
            return path_clear(path) and (not target or target[1] != piece[1])
        else:
            return False

    elif piece[0] == "king":
        return max(dx, dy) == 1 and (not target or target[1] != piece[1])

    return False


# 初始棋盤
def initialize_board():
    board = [
        ['rook', 'white', 'a1'], ['knight', 'white', 'b1'], ['bishop', 'white', 'c1'], ['queen', 'white', 'd1'],
        ['king', 'white', 'e1'], ['bishop', 'white', 'f1'], ['knight', 'white', 'g1'], ['rook', 'white', 'h1'],
        ['pawn', 'white', 'a2'], ['pawn', 'white', 'b2'], ['pawn', 'white', 'c2'], ['pawn', 'white', 'd2'],
        ['pawn', 'white', 'e2'], ['pawn', 'white', 'f2'], ['pawn', 'white', 'g2'], ['pawn', 'white', 'h2'],
        ['pawn', 'black', 'a7'], ['pawn', 'black', 'b7'], ['pawn', 'black', 'c7'], ['pawn', 'black', 'd7'],
        ['pawn', 'black', 'e7'], ['pawn', 'black', 'f7'], ['pawn', 'black', 'g7'], ['pawn', 'black', 'h7'],
        ['rook', 'black', 'a8'], ['knight', 'black', 'b8'], ['bishop', 'black', 'c8'], ['queen', 'black', 'd8'],
        ['king', 'black', 'e8'], ['bishop', 'black', 'f8'], ['knight', 'black', 'g8'], ['rook', 'black', 'h8'],
    ]
    return board

# 輸出棋盤
def print_board(board):
    board_map = {pos: None for pos in valid_positions}
    
    piece_symbols = {
        "pawn": "P",
        "rook": "R",
        "knight": "N",
        "bishop": "B",
        "queen": "Q",
        "king": "K"
    }

    for piece in board:
        symbol = piece_symbols[piece[0]]
        if piece[1] == 'black':
            symbol = symbol.lower()
        board_map[piece[2]] = symbol

    print("  " + " ".join(columns))
    for r in reversed(rows):
        row_str = r + " "
        for c in columns:
            symbol = board_map[c + r] if board_map[c + r] else '.'
            row_str += symbol + " "
        print(row_str)


# 移動棋子
def move_piece(start, end, board, move_stack):
    piece = next((p for p in board if p[2] == start), None)
    if not piece:
        print("無棋子在該位置")
        return board
    if not is_valid_move(piece, start, end, board):
        print("此移動不合法")
        return board
    new_board = copy.deepcopy(board)
    new_board = [p for p in new_board if p[2] != end and p[2] != start]
    new_board.append([piece[0], piece[1], end])
    move_stack.append(copy.deepcopy(board))
    return new_board


# Undo
def undo(move_stack):
    if move_stack:
        return move_stack.pop()
    else:
        print("無法 undo")
        return None

# 主流程
def is_king_alive(color, board):
    return any(p[0] == "king" and p[1] == color for p in board)

def main():
    board = initialize_board()
    move_stack = []
    turn = "white"  # 先手是白方

    while True:
        print_board(board)
        print(f"輪到 {turn} 方")

        # 國王是否被吃
        if not is_king_alive("white", board):
            print("黑方獲勝！白方國王已被吃掉")
            break
        if not is_king_alive("black", board):
            print("白方獲勝！黑方國王已被吃掉")
            break

        cmd = input("請輸入指令（格式 a2 a4 或 undo 或 exit）: ").strip()
        if cmd == "exit":
            break
        elif cmd == "undo":
            prev = undo(move_stack)
            if prev:
                board = prev
                turn = "black" if turn == "white" else "white"
        else:
            try:
                start, end = cmd.split()
                if start in valid_positions and end in valid_positions:
                    piece = next((p for p in board if p[2] == start), None)
                    if not piece:
                        print("該位置沒有你的棋子")
                        continue
                    if piece[1] != turn:
                        print(f"現在是 {turn} 方回合，不能操作對方棋子")
                        continue
                    new_board = move_piece(start, end, board, move_stack)
                    if new_board != board:
                        board = new_board
                        turn = "black" if turn == "white" else "white"  # 成功才換回合
                else:
                    print("無效位置")
            except:
                print("格式錯誤")

if __name__ == "__main__":
    main()
