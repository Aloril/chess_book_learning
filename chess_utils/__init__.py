# -*- coding: utf-8 -*-
import time

PAUSE_FLAG = "pause.flag"
GO_COMMAND = "go infinite"
HASH_SIZE = 1024
NODES = 10**6
INFINITE_SCORE = 10**9
MATE_SCORE = 10**6
COUNTER_END = chr(27) + "[K\r"

def score2no(score_type, score):
    score = int(score)
    if score_type=="mate":
        if score<0: return -MATE_SCORE-score
        else: return MATE_SCORE-score
    return score

def get_time_str():
    return time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(time.time()))

def fen2key(fen):
    l = fen.split()
    return " ".join(l[:4])

def load_evaluations(filename):
    d = {}
    for line in open(filename):
        key = fen2key(line)
        l = line.strip().split()
        fen = " ".join(l[:6])
        score_type = l[6]
        score = l[7]
        pv = " ".join(l[8:])
        d[key] = (fen, score_type, score, pv)
    return d

log_fp = None
def print_log(s=""):
    global log_fp
    if log_fp:
        log_fp.write(s + "\n")
        log_fp.flush()
    print(s)
