import numpy as np

def get_cell_next_state(row, col, board): 
  cell = board[row][col]
  live_neigh = get_live_neighbors(row, col, board)
  if cell == 0:
    if live_neigh == 3:
      return 1
    else:
      return 0
  else:
    if live_neigh == 2 or live_neigh == 3:
      return 1
    else: 
      return 0


def get_live_neighbors(row, col, board): 
  neighbors = []
  for i in range(row-1, row+2):
    for j in range(col-1, col+2):
      neighbors = np.append(neighbors, board[i][j])
  neighbors = np.delete(neighbors, 4)
  return np.sum(neighbors)