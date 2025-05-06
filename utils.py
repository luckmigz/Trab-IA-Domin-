import random
from piece import DominoPiece

def generate_domino_set(max_dots=6):
    """Gera um conjunto completo de peças de dominó."""
    dominoes = []
    for i in range(max_dots + 1):
        for j in range(i, max_dots + 1):
            dominoes.append(DominoPiece(i, j))
    return dominoes

def shuffle_and_distribute(dominoes, player_count=2, pieces_per_player=7):
    """Embaralha as peças e distribui entre os jogadores."""
    # Cria uma cópia para evitar modificar o original
    dominoes = dominoes.copy()
    random.shuffle(dominoes)
    
    # Distribui as peças para os jogadores
    hands = []
    for i in range(player_count):
        start_idx = i * pieces_per_player
        end_idx = start_idx + pieces_per_player
        hands.append(dominoes[start_idx:end_idx])
    
    # As peças restantes formam o estoque
    stock = dominoes[player_count * pieces_per_player:]
    
    return hands, stock
