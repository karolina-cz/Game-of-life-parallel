import argparse
import board_utils
import pandas as pd

def register_arg_parser():
  # TODO dodac parametr zapis do pliku 
  parser = argparse.ArgumentParser()
  parser.add_argument('--file_in', default=None)
  parser.add_argument('--file_out', default=None)
  parser.add_argument('--row', default=5)
  parser.add_argument('--col', default=5)
  parser.add_argument('--iter', default=5)
  parser.add_argument('--d', default="no") #display board 
  args = parser.parse_args()
  return args


def get_iterations(args):
  return int(args.iter)

def get_board(args):
  if args.file_in is not None:
    board = pd.read_csv(args.file_in, header=None).to_numpy()
  else:
    board = board_utils.generate_board(int(args.row), int(args.col))
  return board_utils.add_board_padding(board)

