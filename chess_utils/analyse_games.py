#!/usr/bin/env python3
import sys, subprocess, os
import chess.pgn

from chess_utils import *

class Engine:
    def __init__(self, log_filename, syzygy_path):
        self.engine = subprocess.Popen(["/usr/local/bin/stockfish"], bufsize=1, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        if log_filename:
            self.log_out = open(log_filename, "a")
        else:
            self.log_out = None
        self.write("uci\n")
        self.write("setoption name Hash value %i\n" % HASH_SIZE)
        self.write("setoption name SyzygyPath value %s\n" % syzygy_path)
        
    def write(self, s):
        if self.log_out:
            self.log_out.write(get_time_str() + " " + s)
        self.engine.stdin.write(s)
        self.engine.stdin.flush()
        
    def readline(self):
        line = self.engine.stdout.readline()
        if self.log_out:
            self.log_out.write(get_time_str() + " " + line)
        return line

    def analyse(self, fen):
        self.write("setoption name Clear Hash\n")
        self.write("isready\n")
        while True:
            res = self.readline()
            if res.find("readyok")>=0:
                break
        self.write("position fen %s\n" % (fen,))
        self.write(GO_COMMAND + "\n")
        stop_flag = False
        while True:
            res = self.readline()
            if res.find("info depth 0 score mate 0") >= 0:
                self.write("stop\n")
                stop_flag = True
                info = res + " pv (none)"
            if res.find("seldepth")>0 and res.find("bound")<0 and not stop_flag:
                info = res
                l = info.split()
                if int(l[l.index("nodes")+1]) >= NODES or int(l[l.index("depth")+1])>=127:
                    self.write("stop\n")
                    stop_flag = True
            elif res.startswith("bestmove"):
                break
        info_lst = info.strip().split()
        for i in range(len(info_lst)):
            if info_lst[i]=="score":
                score_type = info_lst[i+1]
                score = info_lst[i+2]
            elif info_lst[i]=="pv":
                pv = " ".join(info_lst[i+1:])
        return score_type, score, pv

def analyse_pgn(pgn_name,
                engine_id,
                evaluations_filename,
                external_evaluations_filename,
                syzygy_path,
                engine_log_filename,
                game_log_filename):
    print_log('analyse games from %s by "%s"' % (pgn_name, engine_id))
    if external_evaluations_filename:
        external_evaluations = load_evaluations(external_evaluations_filename)
        print_log("%i external evaluations loaded from %s" % (
            len(external_evaluations), external_evaluations_filename))
    else:
        external_evaluations = {}
    if os.path.exists(evaluations_filename):
        existing_evaluations = load_evaluations(evaluations_filename)
        print_log("%i existing evaluations read from %s" % (
            len(existing_evaluations), evaluations_filename))
    else:
        existing_evaluations = {}
    engine = Engine(engine_log_filename, syzygy_path)
    eval_out = open(evaluations_filename, "a")
    game_log_out = open(game_log_filename, "a")
    eval_start_pos = eval_out.tell()
    game_log_pos = game_log_out.tell()
    eval_lines = 0
    game_log_lines = 0
    print("new evaluations appended to %s, game moves appended to %s" % (evaluations_filename, game_log_filename))
    print_log()
    fp = open(pgn_name)
    count = 0
    while True:
        game = chess.pgn.read_game(fp)
        if not game:
            break
        white = game.headers["White"]
        black = game.headers["Black"]
        result = game.headers["Result"]
        analyse_colour = None
        if white.find(engine_id)>=0:
            analyse_colour = chess.WHITE
        elif black.find(engine_id)>=0:
            analyse_colour = chess.BLACK
        if analyse_colour==None:
            continue
        count += 1
        print_log("%i: %s-%s %s" % (count, white, black, result))
        b = chess.Board()
        variation = game.variations
        while True:
            best_move = None
            all_new = True
            if b.turn==analyse_colour:
                best_score = -INFINITE_SCORE
                ttable_count = everything_count = eval_count = 0
                #print(b.fen(), " ".join(map(str, b.move_stack)))
                game_moves = " ".join(map(str, b.move_stack))
                for move in b.legal_moves:
                    b.push(move)
                    fen = b.fen()
                    key = fen2key(fen)
                    if key in existing_evaluations:
                        fen, score_type, score, pv = existing_evaluations[key]
                        source = "ttable"
                        ttable_count += 1
                        all_new = False
                    else:
                        if key in external_evaluations:
                            fen, score_type, score, pv = external_evaluations[key]
                            source = "everything ttable"
                            everything_count += 1
                        else:
                            score_type, score, pv = engine.analyse(fen)
                            existing_evaluations[key] = (fen, score_type, score, pv)
                            source = "eval"
                            eval_count += 1
                        s = "%s %s %s %s" % (fen, score_type, score, pv)
                        eval_out.write(s + "\n")
                        eval_out.flush()
                        eval_lines += 1
                        sys.stderr.write("%i %s : %.2f %s TT:%i TTE:%i Eval:%i%s" % (len(b.move_stack), game_moves[:150], int(score)/100.0, move, ttable_count, everything_count, eval_count, COUNTER_END))
                    #treat all mate scores
                    score_no = -score2no(score_type, score)
                    if score_no > best_score:
                        best_score = score_no
                        best_move = move
                    #print(source, move, b.fen(), score_type, score, pv)
                    b.pop()
                sys.stderr.write(COUNTER_END)
                print_log("%i %s best: %.2f %s ttable/everything_tt/eval: %s/%s/%s" % (
                    len(b.move_stack), game_moves, best_score/100.0, best_move,
                    ttable_count, everything_count, eval_count))
                #print()
                if abs(best_score) > 200:
                    print_log("score differs too much from 0")
                    #print("@"*60)
                    print_log()
                    variation = None
            if not variation:
                break
            move = variation[0].move
            if all_new and best_move and move!=best_move:
                print_log("game move (%s) and best move (%s) differs" % (move, best_move))
                #print("@"*60)
                print_log()
                break
            b.push(move)
            variation = variation[0].variations
        colour_str = {chess.WHITE:"w", chess.BLACK:"b"}[analyse_colour]
        game_log_out.write("%s %s\n" % (colour_str, " ".join(map(str, b.move_stack))))
        game_log_out.flush()
        game_log_lines += 1
    print_log("%s size:%i->%i, %i lines written" % (
        evaluations_filename, eval_start_pos, eval_out.tell(), eval_lines))
    print_log("%s size:%i->%i, %i lines written" % (
        game_log_filename, game_log_pos, game_log_out.tell(), game_log_lines))
    
    return existing_evaluations
