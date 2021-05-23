from rich import print
import argparse
import board_utils
import args_parser
import numpy as np
import os
from IPython.display import clear_output

def main():
  args = args_parser.register_arg_parser()
  iterations = args_parser.get_iterations(args)
  board = args_parser.get_board(args)

  if args.d == "yes":
    board = game_loop_with_display(board, iterations)
  else: 
    board = game_loop_no_display(board, iterations)
  
  if args.file_out is not None:
      np.savetxt(args.file_out, board, delimiter=",")


def game_loop_no_display(board, iterations):
  for i in range (0, iterations):
    print("computing iteration {}".format(i))
    board = board_utils.get_next_iteration(board)
  return board


def game_loop_with_display(board, iterations):
  for i in range (0, iterations):
    print("computing iteration {}".format(i))
    board = board_utils.get_next_iteration(board)
    board_utils.display_board(board)
  return board


main()