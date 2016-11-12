#!/usr/bin/env python3
import struct
import chess.polyglot
from chess_utils import *

ENTRY_STRUCT = struct.Struct(">QHHi")
castling2chess960 = {chess.G1: chess.H1,
                     chess.C1: chess.A1,
                     chess.G8: chess.H8,
                     chess.C8: chess.A8}

def dict2polyglot(book_dict, book_filename):
    book_lst = []
    for key in book_dict:
        score, move, all_moves = book_dict[key]
        if all_moves:
            b = chess.Board(key + " 0 1")
            zhash = b.zobrist_hash()
            move = b.parse_uci(move)
            move_from = move.from_square
            move_to = move.to_square
            if b.is_castling(move):
                move_to = castling2chess960[move_to]
            move_raw = (move_from << 6) | move_to
            if move.promotion:
                move_raw |= (move.promotion-1) << 12
            book_lst.append((zhash, move_raw, score))
    book_lst.sort()
    count = 0
    with open(book_filename, "wb") as fp:
        for zhash, move, score in book_lst:
            weight = 1
            learn = score
            fp.write(ENTRY_STRUCT.pack(zhash, move, weight, learn))
            count += 1
    print_log("%i entries in dictionary, added %i complete entries to polyglot book %s" % (
        len(book_dict), count, book_filename))
    if 0:
        pg = chess.polyglot.open_reader(book_filename)
        for key in book_dict:
            score, move, all_moves = book_dict[key]
            if all_moves:
                b = chess.Board(key + " 0 1")
                results = tuple(pg.find_all(b))
                assert(len(results)==1 and results[0].move()==b.parse_uci(move))
