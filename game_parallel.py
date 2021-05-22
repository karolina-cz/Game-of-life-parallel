# from mpi4py import MPI
from rich import print
import numpy as np
import argparse
import board_utils
import args_parser
from mpi4py import MPI
import process_communicator
import process_utils

comm = MPI.COMM_WORLD
id = comm.Get_rank()
size = comm.Get_size()
cartesian = comm.Create_cart(dims = [size],periods =[False],reorder=False)
left,right = cartesian.Shift(direction = 0,disp=1)

def main():
  sub_board, iterations, can_display_board, file_out = init_game()
  print("initialized")
  sub_board = compute_iterations(sub_board, iterations)
  finalize(sub_board, can_display_board, file_out)


def init_game():
  if process_utils.is_master(id):
    args = args_parser.register_arg_parser()
    iterations = args_parser.get_iterations(args)
    board = args_parser.get_board(args)
    board = np.array_split(board,size, axis=0) # podziel tablice na tyle czesci ile jest procesow
    can_display_board = args.d
    file_out = args.file_out
  else:
    board = None
    iterations = None
    can_display_board = None
    file_out = None
  sub_board = comm.scatter(board, root=0)  # wyslij procesom ich czesci tablicy 
  iterations = comm.bcast(iterations, root=0)  #wyslij procesom liczbe iteracji
  return sub_board, iterations, can_display_board, file_out


def compute_iterations(sub_board, iterations):
  sub_board = process_communicator.add_redundant_rows(sub_board, right, left)  # wysylanie i dodawanie wierszy nadmiarowych
  print("exchanged")
  for i in range(0, iterations):
    if process_utils.is_master(id):
      print("iteration {}".format(i))
    sub_board = board_utils.get_next_iteration(sub_board)
    sub_board = process_communicator.exchange_data(sub_board, right, left)
    comm.barrier()

  sub_board = board_utils.remove_redundant_rows(sub_board, id, size) #usun nadmiarowe wiersze
  return sub_board

def finalize(sub_board, can_display_board, file_out):
  result = comm.gather(sub_board, root=0)
  if process_utils.is_master(id):
    result = np.concatenate(result[0:], axis=0)
    print("Plansza policzona rownolegle")
    if can_display_board == "yes":
      board_utils.display_board(result)
    if file_out is not None:
      np.savetxt(file_out, result, delimiter=",")


main()