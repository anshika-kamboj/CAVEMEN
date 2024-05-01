import numpy as np
import tkinter as tk
import copy
import pickle as pickle
import tkinter.messagebox as messagebox
from tkinter import ttk
class Game:
    def __init__(self, master, player1, player2, Q_learn=None, Q={}, alpha=0.3, gamma=0.9):
        frame = tk.Frame()
        frame.grid()
        self.master = master
        master.title("Tic Tac Toe")

        self.player1 = player1
        self.player2 = player2
        self.current_player = player1
        self.other_player = player2
        self.empty_text = ""
        self.board = Board()

        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(frame, height=3, width=6, text=self.empty_text, font=("Helvetica", 24), command=lambda i=i, j=j: self.callback(self.buttons[i][j]))
                self.buttons[i][j].grid(row=i, column=j, padx=5, pady=5)

        self.reset_button = tk.Button(text="Reset and Play Again", font=("Helvetica", 14), command=self.reset)
        self.reset_button.grid(row=3, columnspan=3, pady=10)

        self.Q_learn = Q_learn
        if self.Q_learn:
            self.Q = Q
            self.alpha = alpha
            self.gamma = gamma
            self.share_Q_with_players()

    @property
    def Q_learn(self):
        if self._Q_learn is not None:
            return self._Q_learn
        if isinstance(self.player1, QPlayer) or isinstance(self.player2, QPlayer):
            return True

    @Q_learn.setter
    def Q_learn(self, _Q_learn):
        self._Q_learn = _Q_learn

    def share_Q_with_players(self):
        if isinstance(self.player1, QPlayer):
            self.player1.Q = self.Q
        if isinstance(self.player2, QPlayer):
            self.player2.Q = self.Q

    def callback(self, button):
        if self.board.over():
            pass
        else:
            if isinstance(self.current_player, HumanPlayer) and isinstance(self.other_player, HumanPlayer):
                if self.empty(button):
                    move = self.get_move(button)
                    self.handle_move(move)
            elif isinstance(self.current_player, HumanPlayer) and isinstance(self.other_player, ComputerPlayer):
                computer_player = self.other_player
                if self.empty(button):
                    human_move = self.get_move(button)
                    self.handle_move(human_move)
                    if not self.board.over():
                        computer_move = computer_player.get_move(self.board)
                        self.handle_move(computer_move)

    def empty(self, button):
        return button["text"] == self.empty_text

    def get_move(self, button):
        info = button.grid_info()
        move = (int(info["row"]), int(info["column"]))
        return move

    def handle_move(self, move):
        if self.Q_learn:
            self.learn_Q(move)
        i, j = move
        self.buttons[i][j].configure(text=self.current_player.mark)
        self.board.place_mark(move, self.current_player.mark)
        if self.board.over():
            self.declare_outcome()
        else:
            self.switch_players()

    # def declare_outcome(self):
    #     if self.board.winner() is None:
    #         print("Drawn out...\n")
    #         print("Reset and Try Again...")
    #     else:
    #         print(("🎉🎉Hurray!!!🎉🎉\nPlayer {mark} won!!!🥳🥳".format(mark=self.current_player.mark)))

    def declare_outcome(self):
        if self.board.winner() is None:
            messagebox.showinfo("Game Over", "It's a draw!")
            print("Game Over", "It's a draw!\n")
            print("Reset and Try Again...")
        else:
            winner = self.board.winner()
            messagebox.showinfo("Game Over\n", f"🎉🎉Hurray!!!🎉🎉\nPlayer {winner} won!")  
            print(("🎉🎉Hurray!!!🎉🎉\nPlayer {mark} won!!!🥳🥳".format(mark=self.current_player.mark)))
    # def declare_outcome(self):
    #         outcome = "It's a draw!" if self.board.winner() is None else f"Player {self.board.winner()} won!"

    #         # Create a new Toplevel window for the game result
    #         result_window = tk.Toplevel(self.master)
    #         result_window.title("Game Result")

    #         # Add a label to display the outcome
    #         label = ttk.Label(result_window, text=outcome, font=("Helvetica", 16))
    #         label.pack(padx=20, pady=10)

    #         # Add a button to close the window
    #         close_button = ttk.Button(result_window, text="Close", command=result_window.destroy)
    #         close_button.pack(pady=10)

    def reset(self):
        print("Resetting...")
        print("Now Play...")
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].configure(text=self.empty_text)
        self.board = Board(grid=np.ones((3,3))*np.nan)
        self.current_player = self.player1
        self.other_player = self.player2
        self.play()

    def switch_players(self):
        if self.current_player == self.player1:
            self.current_player = self.player2
            self.other_player = self.player1
        else:
            self.current_player = self.player1
            self.other_player = self.player2

    def play(self):
        if isinstance(self.player1, HumanPlayer) and isinstance(self.player2, HumanPlayer):
            pass
        elif isinstance(self.player1, HumanPlayer) and isinstance(self.player2, ComputerPlayer):
            pass
        elif isinstance(self.player1, ComputerPlayer) and isinstance(self.player2, HumanPlayer):
            first_computer_move = player1.get_move(self.board)
            self.handle_move(first_computer_move)
        elif isinstance(self.player1, ComputerPlayer) and isinstance(self.player2, ComputerPlayer):
            while not self.board.over():
                self.play_turn()

    def play_turn(self):
        move = self.current_player.get_move(self.board)
        self.handle_move(move)

    def learn_Q(self, move):
        state_key = QPlayer.make_and_maybe_add_key(self.board, self.current_player.mark, self.Q)
        next_board = self.board.get_next_board(move, self.current_player.mark)
        reward = next_board.give_reward()
        next_state_key = QPlayer.make_and_maybe_add_key(next_board, self.other_player.mark, self.Q)
        if next_board.over():
            expected = reward
        else:
            next_Qs = self.Q[next_state_key]
            if self.current_player.mark == "X":
                expected = reward + (self.gamma * min(next_Qs.values()))
            elif self.current_player.mark == "O":
                expected = reward + (self.gamma * max(next_Qs.values()))
        change = self.alpha * (expected - self.Q[state_key][move])
        self.Q[state_key][move] += change

class Board:
    def __init__(self, grid=np.ones((3,3))*np.nan):
        self.grid = grid

    def winner(self):
        rows = [self.grid[i,:] for i in range(3)]
        cols = [self.grid[:,j] for j in range(3)]
        diag = [np.array([self.grid[i,i] for i in range(3)])]
        cross_diag = [np.array([self.grid[2-i,i] for i in range(3)])]
        lanes = np.concatenate((rows, cols, diag, cross_diag))

        any_lane = lambda x: any([np.array_equal(lane, x) for lane in lanes])
        if any_lane(np.ones(3)):
            return "X"
        elif any_lane(np.zeros(3)):
            return "O"

    def over(self):
        return (not np.any(np.isnan(self.grid))) or (self.winner() is not None)

    def place_mark(self, move, mark):
        num = Board.mark2num(mark)
        self.grid[tuple(move)] = num

    @staticmethod
    def mark2num(mark):
        d = {"X": 1, "O": 0}
        return d[mark]

    def available_moves(self):
        return [(i,j) for i in range(3) for j in range(3) if np.isnan(self.grid[i][j])]

    def get_next_board(self, move, mark):
        next_board = copy.deepcopy(self)
        next_board.place_mark(move, mark)
        return next_board

    def make_key(self, mark):
        fill_value = 9
        filled_grid = copy.deepcopy(self.grid)
        np.place(filled_grid, np.isnan(filled_grid), fill_value)
        return "".join(map(str, (list(map(int, filled_grid.flatten()))))) + mark

    def give_reward(self):
        if self.over():
            if self.winner() is not None:
                if self.winner() == "X":
                    return 1.0
                elif self.winner() == "O":
                    return -1.0
            else:
                return 0.5
        else:
            return 0.0

class Player(object):
    def __init__(self, mark):
        self.mark = mark

    @property
    def opponent_mark(self):
        if self.mark == 'X':
            return 'O'
        elif self.mark == 'O':
            return 'X'
        else:
            print("The player's mark must be either 'X' or 'O'.")

class HumanPlayer(Player):
    pass

class ComputerPlayer(Player):
    pass

class RandomPlayer(ComputerPlayer):
    @staticmethod
    def get_move(board):
        moves = board.available_moves()
        if moves:
            return moves[np.random.choice(len(moves))]

class THandPlayer(ComputerPlayer):
    def __init__(self, mark):
        super(THandPlayer, self).__init__(mark=mark)

    def get_move(self, board):
        moves = board.available_moves()
        if moves:
            for move in moves:
                if THandPlayer.next_move_winner(board, move, self.mark):
                    return move
                elif THandPlayer.next_move_winner(board, move, self.opponent_mark):
                    return move
            else:
                return RandomPlayer.get_move(board)

    @staticmethod
    def next_move_winner(board, move, mark):
        return board.get_next_board(move, mark).winner() == mark

class QPlayer(ComputerPlayer):
    def __init__(self, mark, Q={}, epsilon=0.2):
        super(QPlayer, self).__init__(mark=mark)
        self.Q = Q
        self.epsilon = epsilon

    def get_move(self, board):
        if np.random.uniform() < self.epsilon:
            return RandomPlayer.get_move(board)
        else:
            state_key = QPlayer.make_and_maybe_add_key(board, self.mark, self.Q)
            Qs = self.Q[state_key]

            if self.mark == "X":
                return QPlayer.stochastic_argminmax(Qs, max)
            elif self.mark == "O":
                return QPlayer.stochastic_argminmax(Qs, min)

    @staticmethod
    def make_and_maybe_add_key(board, mark, Q):
        default_Qvalue = 1.0
        state_key = board.make_key(mark)
        if Q.get(state_key) is None:
            moves = board.available_moves()
            Q[state_key] = {move: default_Qvalue for move in moves}
        return state_key

    @staticmethod
    def stochastic_argminmax(Qs, min_or_max):
        min_or_maxQ = min_or_max(list(Qs.values()))
        if list(Qs.values()).count(min_or_maxQ) > 1:
            best_options = [move for move in list(Qs.keys()) if Qs[move] == min_or_maxQ]
            move = best_options[np.random.choice(len(best_options))]
        else:
            move = min_or_max(Qs, key=Qs.get)
        return move
