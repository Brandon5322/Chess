#  1. 引入模組與基本變數初始化
import copy  # 為了做「undo」功能要複製整份棋盤

columns = "abcdefgh"  # 棋盤直行
rows = "12345678"     # 棋盤橫列

# 產生所有合法棋盤座標 ['a1', 'a2', ..., 'h8']
valid_positions = []

for c in columns:
    for r in rows:
        position = c + r
        valid_positions.append(position)


#  2. 初始化棋盤（初始擺放所有棋子）
'''
board = [
  ['rook', 'white', 'a1'], ['pawn', 'white', 'a2'], ['pawn', 'black', 'a7'], ['rook', 'black', 'a8'],
  ['knight', 'white', 'b1'], ['pawn', 'white', 'b2'], ['pawn', 'black', 'b7'], ['knight', 'black', 'b8'],
  ['bishop', 'white', 'c1'], ['pawn', 'white', 'c2'], ['pawn', 'black', 'c7'], ['bishop', 'black', 'c8'],
  ['queen', 'white', 'd1'], ['pawn', 'white', 'd2'], ['pawn', 'black', 'd7'], ['queen', 'black', 'd8'],
  ['king', 'white', 'e1'], ['pawn', 'white', 'e2'], ['pawn', 'black', 'e7'], ['king', 'black', 'e8'],
  ['bishop', 'white', 'f1'], ['pawn', 'white', 'f2'], ['pawn', 'black', 'f7'], ['bishop', 'black', 'f8'],
  ['knight', 'white', 'g1'], ['pawn', 'white', 'g2'], ['pawn', 'black', 'g7'], ['knight', 'black', 'g8'],
  ['rook', 'white', 'h1'], ['pawn', 'white', 'h2'], ['pawn', 'black', 'h7'], ['rook', 'black', 'h8']
]
'''

def initialize_board():
    board = []
    piece_order = ["rook", "knight", "bishop", "queen", "king", "bishop", "knight", "rook"]
    for i in range(8):
        # 白方底排 + 白兵
        board.append([piece_order[i], "white", columns[i] + "1"])
        board.append(["pawn", "white", columns[i] + "2"])
        # 黑方兵 + 黑方底排
        board.append(["pawn", "black", columns[i] + "7"])
        board.append([piece_order[i], "black", columns[i] + "8"])
    return board

#  3. 工具函式：取得某位置的棋子（若有）# 特別為 knight 使用 'N'（避免與 king 同樣是 'K'）
abbr_dict = {
    "pawn": "P",
    "rook": "R",
    "knight": "N",  # <-- 注意這裡
    "bishop": "B",
    "queen": "Q",
    "king": "K"
}

def get_piece_at(pos):
    for p in board: # 遍歷
        if p[2] == pos:
            return p # p['rook', 'white', 'a1']
    return None

#  4. 判斷某路徑是否中間有擋路（for rook, bishop, queen）
def is_path_clear(start, end):
    x1, y1 = columns.index(start[0]), int(start[1])
    x2, y2 = columns.index(end[0]), int(end[1])
    dx = x2 - x1
    dy = y2 - y1

    # 根據移動方向設定步進方向
    step_x = 0 if dx == 0 else (1 if dx > 0 else -1)
    step_y = 0 if dy == 0 else (1 if dy > 0 else -1)

    curr_x = x1 + step_x
    curr_y = y1 + step_y

    # 循序檢查每一格是否有棋子擋住
    while curr_x != x2 or curr_y != y2:
        pos = columns[curr_x] + str(curr_y)
        if get_piece_at(pos) is not None:
            return False
        curr_x += step_x
        curr_y += step_y

    return True

#  5. 判斷是否為合法走法（依據棋種決定）
def is_valid_move(piece, start, end):
    piece_type = piece[0]  # 棋種
    x1, y1 = columns.index(start[0]), int(start[1])
    x2, y2 = columns.index(end[0]), int(end[1])
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    if start == end:
        return False
    # 兵：只能往前直走，不處理吃子或升變
    if piece_type == "pawn":
        direction = 1 if piece[1] == "white" else -1
        if x1 == x2 and ((y2 - y1) == direction or
            (y1 == (2 if piece[1] == "white" else 7) and (y2 - y1) == 2 * direction)):
            return True
        return False

    # 馬：L 型
    if piece_type == "knight":
        return (dx, dy) in [(1, 2), (2, 1)]

    # 車：橫直方向，需通過擋路檢查
    if piece_type == "rook":
        if dx == 0 or dy == 0:
            return is_path_clear(start, end)
        return False

    # 象：斜線走法
    if piece_type == "bishop":
        if dx == dy:
            return is_path_clear(start, end)
        return False

    # 后：橫直斜皆可
    if piece_type == "queen":
        if dx == dy or dx == 0 or dy == 0:
            return is_path_clear(start, end)
        return False

    # 王：走一步
    if piece_type == "king":
        return max(dx, dy) == 1

    return False

#  6. 顯示棋盤（列印 8×8 盤面）
def print_board():
    print("\n  a  b  c  d  e  f  g  h")
    for r in range(8, 0, -1):
        line = str(r) + " "
        for c in columns:  #columns = "abcdefgh"
            pos = c + str(r)
            p = get_piece_at(pos)
            if p == None:
                line += "-- "
            else:
                # 特別為 knight 使用 'N'（避免與 king 同樣是 'K'）
                abbr_dict = {
                    "pawn": "P",
                    "rook": "R",
                    "knight": "N",  
                    "bishop": "B",
                    "queen": "Q",
                    "king": "K"
                }
                abbrev = p[1][0] + abbr_dict[p[0][:]]
                line += abbrev + " "
        print(line)
    print()

#  7. 遊戲主迴圈：玩家輸入與控制整體流程
board = initialize_board()
move_stack = []       # 儲存歷史狀態，用於 undo
turn = "white"        # 目前輪到誰
game_over = False     # 是否結束遊戲

while not game_over:
    print("===============================")
    print_board()
    print("現在輪到", turn, "方")

    cmd = input("請輸入起點與終點（例如 e2,e4），或輸入 undo： ").strip()

    # === undo 指令：還原上一手 ===
    if cmd == "undo":
        if len(move_stack) > 0:
            last = move_stack.pop()
            board = copy.deepcopy(last[0])
            turn = last[1]
            print("已還原上一步")
        else:
            print("無可還原步驟")
        continue

    # === 檢查輸入格式 ===
    if "," not in cmd:
        print("格式錯誤，請輸入 start,end")
        continue

    start, end = [x.strip() for x in cmd.split(",")]

    if start not in valid_positions or end not in valid_positions:
        print("此非合法走法，請再輸入一次。")
        continue

    piece = get_piece_at(start)
    if piece == None:
        print("該位置無棋子，請再輸入一次。")
        continue
    if piece[1] != turn:
        print("不能移動對方棋子，請再輸入一次。")
        continue
    if not is_valid_move(piece, start, end):
        print("此非合法走法，請再輸入一次。")
        continue

    target = get_piece_at(end)
    if target != None and target[1] == turn:
        print("終點已有己方棋子，請再輸入一次。")
        continue

    # === 儲存目前狀態（for undo） ===
    move_stack.append([copy.deepcopy(board), turn])

    # === 吃掉對方棋子 ===
    if target:
        board.remove(target)
        print(f"成功吃掉 {target[1]} 的 {target[0]}")

    # === 移動棋子 ===
    piece[2] = end
    print("移動完成")

    #  8. 判斷勝負（只看國王是否存在）
    white_king = any(p for p in board if p[0] == "king" and p[1] == "white")
    black_king = any(p for p in board if p[0] == "king" and p[1] == "black")
    if not white_king:
        print("黑方勝利！")
        game_over = True
    elif not black_king:
        print("白方勝利！")
        game_over = True
    else:
        turn = "black" if turn == "white" else "white"
