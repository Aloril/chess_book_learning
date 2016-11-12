#!/usr/bin/env python3
import os, sys, argparse
from chess_utils import init_log, print_log, PAUSE_FLAG
from chess_utils.book_learning_lib import book_learning_args, do_book_learning
from chess_utils.result_summary import result_summary
from chess_utils.book_line import best_book_line

DEFAULT_TOURNAMENT_LOG = "tournament.log"
DEFAULT_EXTERNAL_EVALUATIONS = "evaluations_everything.lst"
DEFAULT_TOURNAMENT_SCRIPT = "./round.sh"

if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Play given number of rounds using cutechess-cli: each round first play 2 games, then analyse games and update book. Default log argument is tournament.log")
    parser.add_argument('rounds', type=int, help="Number of rounds to be played, analysed and book updated. Will play each round 2 games, both engines play white and black.")
    parser.add_argument('-t', '--tournament_script', default=DEFAULT_TOURNAMENT_SCRIPT, help="Tournament script/bat/etc..: this calls cuteches-cli with wanted argument, edit script to suit your need, default is "+DEFAULT_TOURNAMENT_SCRIPT)
    book_learning_args(parser, name_required=True)
    args = parser.parse_args()
    if not args.log:
        args.log = DEFAULT_TOURNAMENT_LOG
    init_log(args.log)

    if not os.path.exists(args.book):
        fp = open(args.book, "w")
        fp.close()

    if args.external_evaluations==None and os.path.exists(DEFAULT_EXTERNAL_EVALUATIONS):
        args.external_evaluations = DEFAULT_EXTERNAL_EVALUATIONS
    
    pgn_fmt = "tournament%i_games2.pgn"
    book_dict_fmt = "book_dict%i.dat"
    tournament_log_fmt = "tournament%i_games2.log"
    tournament_result_fmt = "tournament%i_games2.res"
    engine_log_fmt = "tournament%i_games2_eval.log"

    i = 0
    while i<args.rounds:
        i += 1
        done_flag = False
        for filename_fmt in (pgn_fmt, book_dict_fmt,
                            tournament_log_fmt, tournament_result_fmt,
                             engine_log_fmt):
            filename = filename_fmt % i
            if os.path.exists(filename):
                done_flag = True
                break
        if done_flag:
            continue
        print_log("Round %i(%i)/%i(%i):" % (i, i*2, args.rounds, args.rounds*2))
        os.system('%s %i "%s"' % (args.tournament_script, i, args.name))
        with open(tournament_result_fmt % i, "w") as result_fp:
            for line in open(tournament_log_fmt % i):
                if line.find("<")>=0 or line.find(">")>=0:
                    continue
                result_fp.write(line)
                print_log(line.strip())
        result_summary(tournament_result_fmt)
        print_log()

        args.pgn = pgn_fmt % i
        args.engine_log = engine_log_fmt % i
        args.book_dict = book_dict_fmt % i
        do_book_learning(args)
        best_book_line(args.book_dict)
        
        print_log()
        print_log("@"*60)
        if os.path.exists(PAUSE_FLAG):
            os.remove(PAUSE_FLAG)
            input("Press enter to continue...")
        print_log()
