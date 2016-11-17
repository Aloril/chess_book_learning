#!/usr/bin/env python3
import chess
from chess_utils import *

def show_book_line(b, book_dict):
    score = None
    while True:
        key = fen2key(b.fen())
        if key not in book_dict:
            break
        score, move, all_moves = book_dict[key]
        #print(" ".join(map(str, b.move_stack)), score, move, all_moves)
        b.push_uci(move)
    print_log("%s %s" % (" ".join(map(str, b.move_stack)), score))

def best_book_line(book_dict_name, fen=None, other_moves = ("e2e4", "d2d4")):
    if not fen:
        fen = chess.STARTING_FEN
    book_dict = eval(open(book_dict_name).read())
    b = chess.Board(fen)
    show_book_line(b, book_dict)
    move1 = str(b.move_stack[0])
    #print("@"*60)
    for move in other_moves:
        if move1!=move:
            b = chess.Board(fen)
            if move in list(map(str, b.legal_moves)):
                b.push_uci(move)
                show_book_line(b, book_dict)
