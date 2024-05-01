import numpy as np
import tkinter as tk
import copy
import pickle as pickle    

from Q_Learning_Tic_Tac_Toe import Game, HumanPlayer, QPlayer


Q = pickle.load(open("Q_values_0.90_2000.p", "rb"))

root = tk.Tk()
player1 = HumanPlayer(mark="X")
# player2 = QPlayer(mark="O", epsilon=0)
# player1 = QPlayer(mark="X", epsilon=0)
player2 = QPlayer(mark="O", epsilon=0)
game = Game(root, player1, player2, Q=Q)

game.play()
root.mainloop()
