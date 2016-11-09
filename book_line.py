#!/usr/bin/env python3
import sys
import chess
import chess_utils
chess_utils.log_fp = open("tournament.log", "a")
from chess_utils import *

def show_book_line(b):
    score = None
    while True:
        key = fen2key(b.fen())
        if key not in book_dict:
            break
        score, move, all_moves = book_dict[key]
        #print(" ".join(map(str, b.move_stack)), score, move, all_moves)
        b.push_uci(move)
    print_log("%s %s" % (" ".join(map(str, b.move_stack)), score))

if __name__=="__main__":
    book_dict = eval(open(sys.argv[1]).read())
    b = chess.Board()
    show_book_line(b)
    move1 = str(b.move_stack[0])
    #print("@"*60)
    for move in ("e2e4", "d2d4"):
        if move1!=move:
            b = chess.Board()
            b.push_uci(move)
            show_book_line(b)
