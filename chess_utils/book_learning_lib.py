import chess_utils
from chess_utils.analyse_games import analyse_pgn
from chess_utils.build_book import build_book
from chess_utils.dict2polyglot import dict2polyglot

DEFAULT_EVALUATIONS_POS = "evaluations.pos"
DEFAULT_GAME_LOG = "game.log"
DEFAULT_BOOK = "book_learning.bin"
DEFAULT_ENGINE_EXECUTABLE = "/usr/local/bin/stockfish"
DEFAULT_SYZYGY_PATH = "/usr/games/syzygy"

def book_learning_args(parser, name_required=False):
    parser.add_argument('-p', '--pgn', help="PGN file to analyse, if not given, then analysis is skipped")
    parser.add_argument('-n', '--name', required=name_required, help="Name of engine used in pgn file White and/or Black headers, if not given, analysis is skipped")
    parser.add_argument('-e', '--evaluations', default=DEFAULT_EVALUATIONS_POS, help="Positions, evaluations and moves read if exists and new evaluations appended to "+DEFAULT_EVALUATIONS_POS)
    parser.add_argument('-a', '--external_evaluations', help="Not used for building opening book unless position is seen in analysis")
    parser.add_argument('-x', '--engine_executable', default=DEFAULT_ENGINE_EXECUTABLE, help="Engine executable including path to it, default is "+DEFAULT_ENGINE_EXECUTABLE)
    parser.add_argument('-s', '--syzygy_path', default=DEFAULT_SYZYGY_PATH, help="SyzygyPath option for engine, default is "+DEFAULT_SYZYGY_PATH)
    parser.add_argument('-o', '--engine_log', help="Log file for engine input and output")
    parser.add_argument('-m', '--nodes', default=chess_utils.NODES, help="Amount of nodes used in analysis, k/M/G/T accepted in addition to plain numbers, default is " + str(chess_utils.NODES))
    parser.add_argument('-g', '--game_log', default=DEFAULT_GAME_LOG, help="Moves from games analysed, append if already exists, default is "+DEFAULT_GAME_LOG)
    parser.add_argument('-d', '--book_dict', help="Python version of book dictionary")
    parser.add_argument('-f', '--fen', help="Start book building from this position, default is standard starting position")
    parser.add_argument('-i', '--fixed_lines', help="Fixed opening lines that won't be altered")
    parser.add_argument('-b', '--book', default=DEFAULT_BOOK, help="Polyglot book, will overwrite if exists, default is "+DEFAULT_BOOK)
    parser.add_argument('-l', '--log', help="Log file")

def do_book_learning(args):
    chess_utils.init_log(args.log)
    chess_utils.print_log(str(args))
    if args.pgn and args.name:
        analyse_pgn(args.pgn, args.name,
                    args.evaluations, args.external_evaluations,
                    args.engine_executable, args.syzygy_path,
                    chess_utils.nodes_str2nodes(args.nodes),
                    args.engine_log, args.game_log)
    
    book_dict = build_book(args.evaluations, args.game_log, args.book_dict, args.fen)
    dict2polyglot(book_dict, args.book, args.fen, args.fixed_lines)
