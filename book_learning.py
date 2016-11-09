#!/usr/bin/env python3
import argparse
import chess_utils
from chess_utils.analyse_games import analyse_pgn
from chess_utils.build_book import build_book
from chess_utils.dict2polyglot import dict2polyglot

DEFAULT_EVALUATIONS_POS = "evaluations.pos"
DEFAULT_GAME_LOG = "game.log"
DEFAULT_BOOK = "book_learning.bin"
DEFAULT_ENGINE_EXECUTABLE = "/usr/local/bin/stockfish"
DEFAULT_SYZYGY_PATH = "/usr/games/syzygy"

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
    parser.add_argument('-p', '--pgn', help="PGN file to analyse, if not given, then analysis is skipped")
    parser.add_argument('-n', '--name', help="Name of engine used in pgn file White and/or Black headers, if not given, analysis is skipped")
    parser.add_argument('-e', '--evaluations', default=DEFAULT_EVALUATIONS_POS, help="Positions, evaluations and moves read if exists and new evaluations appended to "+DEFAULT_EVALUATIONS_POS)
    parser.add_argument('-a', '--external_evaluations', help="Not used for building opening book unless position is seen in analysis")
    parser.add_argument('-x', '--engine_executable', default=DEFAULT_ENGINE_EXECUTABLE, help="Engine executable including path to it, default is "+DEFAULT_ENGINE_EXECUTABLE)
    parser.add_argument('-s', '--syzygy_path', default=DEFAULT_SYZYGY_PATH, help="SyzygyPath option for engine, default is "+DEFAULT_SYZYGY_PATH)
    parser.add_argument('-o', '--engine_log', help="Log file for engine input and output")
    parser.add_argument('-g', '--game_log', default=DEFAULT_GAME_LOG, help="Moves from games analysed, append if already exists, default is "+DEFAULT_GAME_LOG)
    parser.add_argument('-d', '--book_dict', help="Python version of book dictionary")
    parser.add_argument('-b', '--book', default=DEFAULT_BOOK, help="Polyglot book, will overwrite if exists, default is "+DEFAULT_BOOK)
    parser.add_argument('-l', '--log', help="Log file")
    args = parser.parse_args()

    if args.log:
        chess_utils.log_fp = open(args.log, "a")
    chess_utils.print_log(str(args))
    if args.pgn and args.name:
        analyse_pgn(args.pgn, args.name,
                    args.evaluations, args.external_evaluations,
                    args.engine_executable, args.syzygy_path,
                    args.engine_log, args.game_log)
    
    book_dict = build_book(args.evaluations, args.game_log, args.book_dict)
    dict2polyglot(book_dict, args.book)
