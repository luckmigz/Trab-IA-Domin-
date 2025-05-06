import random
from piece import DominoPiece
from player import Player, AIPlayer, HumanPlayer
from game import DominoGame
from utils import generate_domino_set, shuffle_and_distribute
from colors import Color

def get_difficulty_choice():
    """Obtém o nível de dificuldade da IA escolhido pelo usuário."""
    while True:
        print(f"\n{Color.CYAN}Escolha a dificuldade da IA:{Color.RESET}")
        print(f"  1: {Color.GREEN}Fácil{Color.RESET}")
        print(f"  2: {Color.YELLOW}Médio{Color.RESET}")
        print(f"  3: {Color.RED}Difícil{Color.RESET}")
        
        try:
            choice = int(input("\nDigite a dificuldade (1-3): "))
            if 1 <= choice <= 3:
                return choice
            print(f"{Color.RED}Escolha inválida. Por favor, digite 1, 2 ou 3.{Color.RESET}")
        except ValueError:
            print(f"{Color.RED}Por favor, digite um número.{Color.RESET}")

def main():
    print(f"\n{Color.MAGENTA}===== JOGO DE DOMINÓ ====={Color.RESET}\n")
    print(f"{Color.CYAN}Bem-vindo ao jogo de dominó no terminal!{Color.RESET}")
    
    # Obtém a dificuldade da IA
    difficulty = get_difficulty_choice()
    
    # Gera e distribui as peças de dominó
    dominoes = generate_domino_set()
    hands, stock = shuffle_and_distribute(dominoes)
    
    # Cria os jogadores
    human_player = HumanPlayer("Jogador", hands[0])
    ai_player = AIPlayer("Computador", hands[1], difficulty=difficulty)
    
    # Cria e inicia o jogo
    game = DominoGame(human_player, ai_player, stock)
    game.start()
    
    print(f"\n{Color.GREEN}Obrigado por jogar!{Color.RESET}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Color.YELLOW}Jogo encerrado pelo usuário. Até logo!{Color.RESET}")
    except Exception as e:
        print(f"\n{Color.RED}Ocorreu um erro: {e}{Color.RESET}")
