import numpy as np
import tkinter as tk
import copy
import pickle
from Q_Learning_Tic_Tac_Toe import Game,Gametrain, QPlayer   

root = tk.Tk()
epsilon = 0.9
player1 = QPlayer(mark="X", epsilon=epsilon)
player2 = QPlayer(mark="O", epsilon=epsilon)
game = Gametrain(root, player1, player2)

count_games = 2000
for episodes in range(count_games):
    game.play()
    game.reset()

Q = game.Q

filename = "Q_values_{:.2f}_{}.p".format(epsilon, count_games)
pickle.dump(Q, open(filename, "wb"))
