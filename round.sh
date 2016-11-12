#!/bin/bash
ROUND=$1
NAME="$2"
cutechess-cli -debug -fcp name="$NAME" cmd=stockfish book=book_learning.bin proto=uci option.SyzygyPath=/usr/games/syzygy option."Move Overhead"=100 tc=10+0.1 -scp name="Stockfish 8" cmd=stockfish proto=uci option.SyzygyPath=/usr/games/syzygy option."Move Overhead"=100 tc=10+0.1 -games 2 -pgnout tournament${ROUND}_games2.pgn >> tournament${ROUND}_games2.log
