from facilitator_credentials import Facilitator
from game_table import TableTop
from player_chair import *
from announcer_chair import Announcer

class Referee(Facilitator):

    def __init__(self, table_top, player1, player2):
        self.announcer = Announcer()
        self.table_top = table_top
        self.player1 = player1
        self.player2 = player2
        self.whos_turn = self.player1

    def show_board(self):
        board = self.announcer.render_board(self.table_top.board)
        self.announcer.show(board)

    def start_game(self):
        self.announcer.show(self.announcer.start)
        self.show_board()
        self.facilitate_turns()
        
    def facilitate_turns(self):
        self.whos_turn.move(self.board)
        self.show_board()
        the_game_is_over = check_for_game_over()
        if the_game_is_over != False:
            game_over(the_game_is_over)
        else:
            self.prep_next_turn()
            self.facilitate_turns()

    def prep_next_turn(self):
        if self.whos_turn == self.player1:
            self.whos_turn = self.player2
        elif self.whos_turn == self.player2:
            self.whos_turn = self.player1
        
    def game_over(self, winner): 
        self.show_board()
        if winner == "tie":
            self.announcer.show(self.announcer.tie)
        elif winner == "computer":
            self.announcer.show(self.announcer.computer)
        elif winner == "human":
            self.announcer.show(self.announcer.human)

    def check_for_game_over(self):
        if check_for_tie() == True:
            return "tie"
        elif check_for_winner() == True:
            return self.players_turn.id
        else:
            return False

    def check_for_tie(self):
        if 0 in self.table_top.board:
            return False
        else:
            return True

    def check_for_winner(self):
        board = self.table_top.board
        p1_win = self.get_board_size(board)
        p2_win = p1_win * 10
        win_list = self.get_win_list()
        did_they_win = False
        for i in range(0, len(win_list)):
            win_factor = 0
            for j in win_list[i]:
                win_factor += board[j]
            if win_factor == p1_win or win_factor == p2_win:
                did_they_win = True
        return did_they_win

    def get_win_list(self):
        board = self.table_top.board
        board_size = self.get_board_size(board)
        win_list = []
        win_list.extend(self.get_winning_rows(board_size))
        win_list.extend(self.get_winning_cols(board_size))
        win_list.extend(self.get_winning_diags(board_size))
        print win_list
        return win_list

    def get_winning_rows(self, board_size):
        winning_rows = self.get_empty_list(board_size)
        start = 0
        for i in range(0, board_size):
            stop = start + board_size
            for j in range(start, stop):
                 winning_rows[i].append(j)
            start += board_size
        return winning_rows

    def get_winning_cols(self, board_size):
        all_squares = board_size * board_size
        winning_cols = self.get_empty_list(board_size)
        col = 0
        for i in range(0, board_size):
            for j in range(col, all_squares, board_size):
                 winning_cols[i].append(j)
            col += 1
        return winning_cols
 
    def get_empty_list(self, board_size):
        empty_list = []
        for i in range(0, board_size):
            empty_list.append([])
        return empty_list

    def get_winning_diags(self, board_size):
        winning_diags = []
        winning_diags.append(self.get_NW_SE_diag(board_size))
        winning_diags.append(self.get_SW_NE_diag(board_size))
        return winning_diags

    def get_NW_SE_diag(self, board_size):
        diag = []
        coord = 0
        for i in range(0, board_size):
            diag.append(coord)
            coord += board_size + 1
        return diag

    def get_SW_NE_diag(self, board_size):
        diag = []
        coord = board_size -1
        for i in range(0, board_size):
            diag.append(coord)
            coord += board_size - 1
        return diag
