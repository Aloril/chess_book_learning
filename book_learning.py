#!/usr/bin/env python3
import argparse
from chess_utils.book_learning_lib import *

if __name__ == '__main__':
    #do evaluation of pgn:
    #input:
    #  engine name
    #  games.pgn: games by engine name are read from it
    #  evaluations: evaluations.pos (optinal, assumed none if not given)
    #output:
    #  evaluations: evaluations.pos or other file
    #  engine logs: evaluations.log or optinally none: default none
    #  moves: game.log
    #do evaluations of positions from pgn
    #do minmax
    #output:
    #  opening dictionary in python dictionary format: default none
    #  polyglot book: default book_learning.bin
    parser = argparse.ArgumentParser(description="Analyse input pgn file and create opening book resulting analysis from it, can append to existing analysis, evaluations and game log is used to build opening book")
    book_learning_args(parser)
    args = parser.parse_args()
    do_book_learning(args)
    
