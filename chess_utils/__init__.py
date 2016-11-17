# -*- coding: utf-8 -*-
import time, bz2, string

PAUSE_FLAG = "pause.flag"
GO_COMMAND = "go infinite"
HASH_SIZE = 1024
NODES = "1M"
INFINITE_SCORE = 10**9
MATE_SCORE = 10**6
COUNTER_END = chr(27) + "[K\r"

def nodes_str2nodes(nodes_str):
    if nodes_str[-1] not in string.digits:
        multiplier = {"k":10**3, "M":10**6, "G":10**9, "T":10**12}[nodes_str[-1]]
        nodes_str = nodes_str[:-1]
    else:
        multiplier = 1
    return int(nodes_str) * multiplier
    

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
    if filename.endswith(".bz2"):
        fp = bz2.open(filename, "rt")
    else:
        fp = open(filename)
    for line in fp:
        key = fen2key(line)
        l = line.strip().split()
        fen = " ".join(l[:6])
        score_type = l[6]
        score = l[7]
        pv = " ".join(l[8:])
        d[key] = (fen, score_type, score, pv)
    return d

log_fp = None
def init_log(logname):
    global log_fp
    if log_fp==None and logname:
        log_fp = open(logname, "a")
    
def print_log(s=""):
    global log_fp
    if log_fp:
        log_fp.write(s + "\n")
        log_fp.flush()
    print(s)
