WIN_COMBINATIONS = [
    (0,1,2),(3,4,5),(6,7,8),
    (0,3,6),(1,4,7),(2,5,8),
    (0,4,8),(2,4,6)
]


class GameState:
    def __init__(self, p1_symbol="X"):
        # ---------------- BOARD STATE ----------------
        self.board = [[None] * 9 for _ in range(9)]
        self.smallBoardStatus = [None] * 9
        self.nextBoard = -1

        # ---------------- PLAYERS ----------------
        self.player1 = p1_symbol
        self.player2 = "O" if p1_symbol == "X" else "X"

        self.human = self.player1
        self.ai = None  # set only in AI mode

        # 🔑 Player 1 ALWAYS starts
        self.current_player = self.player1

    # ---------------- SMALL BOARD ----------------
    def check_small_board(self, cells):
        for a, b, c in WIN_COMBINATIONS:
            if cells[a] and cells[a] == cells[b] == cells[c]:
                return cells[a]

        if all(cells):
            return "D"

        return None

    def update_small_board(self, board_index):
        if self.smallBoardStatus[board_index] is None:
            self.smallBoardStatus[board_index] = self.check_small_board(
                self.board[board_index]
            )

    # ---------------- GLOBAL BOARD ----------------
    def check_global_win(self):
        for a, b, c in WIN_COMBINATIONS:
            if (
                self.smallBoardStatus[a]
                and self.smallBoardStatus[a] == self.smallBoardStatus[b] == self.smallBoardStatus[c]
                and self.smallBoardStatus[a] != "D"
            ):
                return self.smallBoardStatus[a]

        if all(x is not None for x in self.smallBoardStatus):
            return "D"

        return None

    # ---------------- MOVE VALIDATION ----------------
    def is_valid_move(self, board_index, cell_index):
        if self.nextBoard != -1 and board_index != self.nextBoard:
            return False

        if self.smallBoardStatus[board_index] is not None:
            return False

        if self.board[board_index][cell_index] is not None:
            return False

        return True

    # ---------------- MAKE MOVE ----------------
    def make_move(self, board_index, cell_index, player):
        # ❌ Wrong turn
        if player != self.current_player:
            return False

        if not self.is_valid_move(board_index, cell_index):
            return False

        # Place move
        self.board[board_index][cell_index] = player
        self.update_small_board(board_index)

        # Decide next active board
        if self.smallBoardStatus[cell_index] is None:
            self.nextBoard = cell_index
        else:
            self.nextBoard = -1

        # 🔁 Switch turn
        self.current_player = self.player2 if self.current_player == self.player1 else self.player1

        return True
