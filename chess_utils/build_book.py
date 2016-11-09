#!/usr/bin/env python3
import chess
from chess_utils import *

def add_link(link_dict, move, pos1, pos2):
    d = link_dict.get(pos1, {})
    d[pos2] = move
    link_dict[pos1] = d

#debug_b = chess.Board()
def minmax(existing_evaluations, book_dict, link_dict, key, move_history):
    #global debug_b
    if key in move_history:
        return
    move_history.add(key)
    if key in book_dict:
        return book_dict[key]
    if key not in link_dict:
        if key in existing_evaluations:
            fen, score_type, score, pv = existing_evaluations[key]
            return score2no(score_type, score), None, False
        return None
    d = link_dict[key]
    best_score = -INFINITE_SCORE
    best_move = None
    all_moves = bool(d)
    for key2 in d:
        move = d[key2]
        #debug_b.push(move)
        res = minmax(existing_evaluations, book_dict, link_dict, key2, move_history)
        #debug_b.pop()
        if not res:
            all_moves = False
            continue
        score = -res[0]
        if score > best_score:
            best_score = score
            best_move = move
    move_history.remove(key)
    if best_move:
        result = best_score, str(best_move), all_moves
        #print(" ".join(map(str, debug_b.move_stack)), result)
        book_dict[key] = result
        return result

def build_book(evaluations_filename, game_log_filename, book_dict_filename):
    existing_evaluations = load_evaluations(evaluations_filename)
    print_log("%i evaluations loaded" % (len(existing_evaluations),))
    minmax_positions = {}
    link_dict = {}
    for line in open(game_log_filename):
        move_lst = line.strip().split()
        b = chess.Board()
        for move in move_lst:
            if len(move) > 1: #first entry is colour, but ignore it and analyse opening position
                b.push_uci(move)
            key1 = fen2key(b.fen())
            if key1 not in link_dict:
                for move in b.legal_moves:
                    b.push(move)
                    key2 = fen2key(b.fen())
                    add_link(link_dict, move, key1, key2)
                    b.pop()
        #print(line.strip())
    print_log("%i links created" % (len(link_dict),))
    book_dict = {}
    move_history = set()
    minmax(existing_evaluations, book_dict, link_dict, fen2key(chess.STARTING_FEN), move_history)
    print_log("%i book entries created" % (len(book_dict),))
    if book_dict_filename:
        fp = open(book_dict_filename, "w")
        fp.write(repr(book_dict))
        fp.close()
    return book_dict
