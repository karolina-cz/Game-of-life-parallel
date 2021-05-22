from rich import print
import numpy as np
import cell_utils
import process_utils

def display_board(board):
  n_rows = board.shape[0]
  n_cols = board.shape[1]
  for i in range(1, n_rows - 1):
    for j in range(1, n_cols - 1):
      if board[i][j] == 1:
        print('[bold green3]\u25A0 [/bold green3]', end = '')
      else: 
        print('[bold white]\u25A0 [/bold white]', end = '')
    print('\n', end = '')


def add_board_padding(board):
  return np.pad(board, pad_width=1, mode='constant', constant_values=0)


def generate_board(n_rows, n_cols):
  return np.random.randint(2, size=(n_rows, n_cols))


def get_next_iteration(board):
  n_rows = board.shape[0]
  n_cols = board.shape[1]
  new_board = np.zeros((n_rows, n_cols))
  for i in range(1, n_rows - 1):
    for j in range(1, n_cols - 1):
        new_board[i][j] = cell_utils.get_cell_next_state(i, j, board)
  return new_board

def remove_redundant_rows(board, id, size):
  if process_utils.is_master(id):
    board = board[:-1,:]
  elif process_utils.is_last_process(id, size):
    board = board[1:,:]
  else:
    board = board[1:-1,:]
  return board