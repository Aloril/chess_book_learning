#!/usr/bin/env python3
import sys, os, re
import chess_utils

if __name__=="__main__":
    filename_fmt = sys.argv[1]
    chess_utils.log_fp = open("tournament.log", "a")
    print_log = chess_utils.print_log
    i = 1
    total_win = total_lost = total_draw = 0
    while True:
        filename = filename_fmt % i
        if not os.path.exists(filename):
            break
        win, lost, draw = 0, 0, 0
        for line in open(filename):
            m = re.match(r"Score of (.+) vs (.+): (\d+) - (\d+) - (\d+)", line)
            if m:
                prog1, prog2, win, lost, draw = m.groups()
                win = int(win)
                lost = int(lost)
                draw = int(draw)
        total_win += win
        total_lost += lost
        total_draw += draw
        #print("%i: SF8 vs SF8U: %i - %i - %i" % (i, total_win, total_lost, total_draw))
        i += 1
    print_log("%i(%i): %s vs %s: +%i -%i =%i" % (i-1, (i-1)*2, prog1, prog2, total_win, total_lost, total_draw))
