#!/bin/sh
NAME="Stockfish 8 Book learning"
cutechess-cli -debug -fcp name="$NAME" cmd=stockfish book=book_learning.bin proto=uci option.SyzygyPath=/usr/games/syzygy option."Move Overhead"=100 tc=10+0.1 -scp name="Brainfish 081116" cmd=brainfish proto=uci option.SyzygyPath=/usr/games/syzygy option."Move Overhead"=100 option."Book Move2 Probability"=50 option.BookPath=/usr/local/lib/Cerebellum_Light.bin tc=10+0.1 -games 2 -pgnout tournament$1_games2.pgn >> tournament$1_games2.log
cat tournament$1_games2.log|grep -v "<"|grep -v ">" > tournament$1_games2.res
cat tournament$1_games2.res
cat tournament$1_games2.res >> tournament.log
./result_summary.py
echo
echo >> tournament.log

./book_learning.py --pgn tournament$1_games2.pgn --name "$NAME" --engine_log tournament$1_games2_eval.log --log tournament.log --external_evaluations evaluations_everything.lst --book_dict book_dict$1.dat
./book_line.py book_dict$1.dat
