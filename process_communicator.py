import numpy as np
from mpi4py import MPI
import process_utils

comm = MPI.COMM_WORLD
id = comm.Get_rank()
size = comm.Get_size()

def add_redundant_rows(sub_board, right, left):
  if process_utils.is_master(id):
    sub_board = add_redundant_bottom_row(sub_board, right)
  elif process_utils.is_last_process(id, size):
    sub_board = add_redundant_top_row(sub_board, left)
  else:
    sub_board = add_redundant_both_rows(sub_board, left, right)

  return sub_board

def exchange_data(sub_board, right, left):
  if process_utils.is_master(id):
    sub_board = exchange_bottom_row(sub_board, right)
  elif process_utils.is_last_process(id, size):
    sub_board = exchange_top_row(sub_board, left)
  else:
    sub_board = exchange_both_rows(sub_board, right, left)

  return sub_board


def send_row(row, dest_proc):
  comm.send(row, dest=dest_proc)

def receive_row(src_proc):
  return comm.recv(source=src_proc)

def concatenate_board_row(board, top_row, bottom_row):
  if bottom_row is None:
    return np.concatenate(([top_row], board), axis=0)
  elif top_row is None:
    return np.concatenate((board,[bottom_row]), axis=0)
  else:
   board = np.concatenate(([top_row], board), axis=0)
   return np.concatenate((board,[bottom_row]), axis=0)

def add_redundant_bottom_row(sub_board, right):
  req = comm.irecv(source=right)
  comm.send(sub_board[-1], dest=right)
  bottom_row = req.wait()
  # send_row(sub_board[-1], right)
  # bottom_row = receive_row(right)
  sub_board = concatenate_board_row(sub_board, None, bottom_row)
  return sub_board


def add_redundant_top_row(sub_board, left):
  req = comm.irecv(source=left)
  comm.send(sub_board[0], dest=left)
  top_row = req.wait()
  # send_row(sub_board[0], left)
  # top_row = receive_row(left)
  sub_board = concatenate_board_row(sub_board, top_row, None)
  return sub_board

def add_redundant_both_rows(sub_board, left, right):
  req1 = comm.irecv(source=left)
  req2 = comm.irecv(source=right)
  comm.send(sub_board[-1], dest=right)
  comm.send(sub_board[0], dest=left)
  top_row = req1.wait()
  bottom_row = req2.wait()
  # send_row(sub_board[0], left)
  # send_row(sub_board[-1], right)
  # top_row = receive_row(left)
  # bottom_row = receive_row(right)
  sub_board = concatenate_board_row(sub_board, top_row, bottom_row)
  return sub_board

def exchange_bottom_row(sub_board, right):
  req = comm.irecv(source=right)
  comm.send(sub_board[-2], dest=right)
  bottom_row = req.wait()

  # send_row(sub_board[-2], right)
  # bottom_row = receive_row(right)
  sub_board[-1] = bottom_row
  return sub_board

def exchange_top_row(sub_board, left):
  # send_row(sub_board[1], left)
  # top_row = receive_row(left)

  req = comm.irecv(source=left)
  comm.send(sub_board[1], dest=left)
  top_row = req.wait()

  sub_board[0] = top_row
  return sub_board

def exchange_both_rows(sub_board, right, left):

  # send_row(sub_board[-2], right)
  # send_row(sub_board[1], left)
  # top_row = receive_row(left)
  # bottom_row = receive_row(right)

  req1 = comm.irecv(source=left)
  req2 = comm.irecv(source=right)
  comm.send(sub_board[-2], dest=right)
  comm.send(sub_board[1], dest=left)
  top_row = req1.wait()
  bottom_row = req2.wait()

  sub_board[0] = top_row
  sub_board[-1] = bottom_row
  return sub_board