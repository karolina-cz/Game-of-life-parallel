from rich import print
import argparse
import board_utils
import args_parser
import numpy as np

def main():
  args = args_parser.register_arg_parser()
  iterations = args_parser.get_iterations(args)
  board = args_parser.get_board(args)

  for i in range (0, iterations):
    print("computing iteration {}".format(i))
    board = board_utils.get_next_iteration(board)

  if args.d == "yes":
    board_utils.display_board(board)
  
  if args.file_out is not None:
      np.savetxt(args.file_out, board, delimiter=",")

main()