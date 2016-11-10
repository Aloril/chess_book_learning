Chess book learning for any chess engine or human.

Repeatedly analyse games played until it finds move
where it disagress with game move or abs(score)>5.0,
then score all positions including analysis of previous
games at same time with one minmax search
and (re)create opening book

Analysis part currently tested only with Stockfish,
but only minor changes if any should be needed 
to use any engine for analysis.


PyChess library needed, for example Ubuntu:
sudo apt-get install pychess


tournamet.py: Will run tournament 2 games at time until
file pause.flag is created in same directory or 
given number of rounds has been reached.
Edit round.sh before running this.
Example usage:
tournamet.py 100

book_learning.py: Used to create opening book from games played by engine or human.
Example usage:
book_learning.py --pgn some_tournament.pgn --name "Stockfish 8 Book learning"
This will analyse positions by player named "Stockfish 8 Book learning" until it
disagrees or absolute score becomes too big. Evaluations are stored in evaluations.pos
and games in game.log . Book is stored in book_learning.bin .

book_learning.py --help
will display help message with all options

round.sh also has more complete usage example
