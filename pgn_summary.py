#!/usr/bin/env python3
import os, sys
import chess.pgn

if __name__=="__main__":
    name = sys.argv[1]
    for colour in chess.WHITE, chess.BLACK:
        if colour==chess.WHITE:
            print("White:")
        else:
            print("Black:")
        i = 1
        while True:
            filename = "tournament%i_games2.pgn" % i
            if not os.path.exists(filename):
                break
            fp = open(filename)
            while True:
                game = chess.pgn.read_game(fp)
                if not game:
                    break
                white = game.headers["White"]
                black = game.headers["Black"]
                result = game.headers["Result"]
                if white==name:
                    analyse_colour = chess.WHITE
                elif black==name:
                    analyse_colour = chess.BLACK
                if analyse_colour!=colour:
                    continue
                b = chess.Board()
                variation = game.variations
                result = result[:3]
                print("%2i: %s" % (i, result), end=" ")
                while True:
                    move_postfix = ""
                    if b.turn==analyse_colour:
                        move_postfix = "" #"_"
                    if not variation:
                        break
                    move = variation[0].move
                    comment = variation[0].comment
                    if comment.find("book")>=0:
                        move_postfix = "@"
                    if b.turn==chess.WHITE:
                        print("%i." % (len(b.move_stack)//2+1,), end=" ")
                    print("%-5s" % (b.san(move) + move_postfix,), end=" ")
                    b.push(move)
                    if len(b.move_stack)>=22:
                        break
                    variation = variation[0].variations
                print()
            i += 1

