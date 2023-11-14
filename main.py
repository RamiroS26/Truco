from game import Game
from player import Player

def run_game():
        print()
        print("Ingresa el nombre del jugador 1")
        p1 = input("-> ")
        print("Ingresa el nombre del jugador 2")
        p2 = input("-> ")
        game = Game(p1, p2)
        while not game.is_over():
            print()
            print("Inicia la mano.")
            game.reset_hands()
            game.start_hand()
            game.table()
    
if __name__ == "__main__":
    run_game()

