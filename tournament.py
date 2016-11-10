#!/usr/bin/env python3
import os, sys
import chess_utils
chess_utils.log_fp = open("tournament.log", "a")
from chess_utils import *

BOOK_FILE = "book_learning.bin"

if __name__=="__main__":
    rounds = int(sys.argv[1])
    if not os.path.exists(BOOK_FILE):
        fp = open(BOOK_FILE, "w")
        fp.close()
    i = 0
    while i<rounds:
        i += 1
        done_flag = False
        for filename_fmt in ("tournament%i_games2.pgn", "book_dict%i.dat",
                             "tournament%i_games2.log", "tournament%i_games2.res",
                             "tournament%i_games2_eval.log"):
            filename = filename_fmt % i
            if os.path.exists(filename):
                done_flag = True
                break
        if done_flag:
            continue
        print_log("Round %i(%i)/%i(%i):" % (i, i*2, rounds, rounds*2))
        os.system("./round.sh %i" % i)
        print_log()
        print_log("@"*60)
        if os.path.exists(PAUSE_FLAG):
            os.remove(PAUSE_FLAG)
            input("Press enter to continue...")
        print_log()
