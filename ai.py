import copy

class DifficultyLevel:
    EASY = 1
    MEDIUM = 2
    HARD = 3

def evaluate_state(player_pieces, opponent_pieces, difficulty):
    """
    Avalia o estado do jogo com heurísticas avançadas baseadas no nível de dificuldade.
    """
    player_sum = sum(p.get_value() for p in player_pieces)
    opponent_sum = sum(p.get_value() for p in opponent_pieces)
    
    if difficulty == DifficultyLevel.EASY:
        # Avaliação simples - considera apenas os valores das peças
        return opponent_sum - player_sum
    
    elif difficulty == DifficultyLevel.MEDIUM:
        # Avaliação média - considera quantidade de peças e valores
        player_count_factor = len(player_pieces) * 3
        opponent_count_factor = len(opponent_pieces) * 3
        doubles_bonus = sum(5 for p in player_pieces if p.is_double())
        return (opponent_sum + opponent_count_factor) - (player_sum + player_count_factor + doubles_bonus)
    
    else:  # HARD
        # Avaliação avançada - considera múltiplos fatores estratégicos
        player_count_factor = len(player_pieces) * 4
        opponent_count_factor = len(opponent_pieces) * 4
        
        # Bônus por ter duplas (estrategicamente valiosas)
        doubles_bonus = sum(8 for p in player_pieces if p.is_double())
        
        # Penalidade por ter peças de valor alto
        high_value_penalty = sum(2 for p in player_pieces if p.get_value() > 8)
        
        # Bônus por ter números diversos (mais opções de jogada)
        player_numbers = set()
        for p in player_pieces:
            player_numbers.add(p.left)
            player_numbers.add(p.right)
        diversity_bonus = len(player_numbers) * 3
        
        return (opponent_sum + opponent_count_factor) - \
               (player_sum + player_count_factor + doubles_bonus - high_value_penalty + diversity_bonus)

def get_valid_moves(pieces, ends):
    """Retorna as jogadas válidas para as peças e extremidades fornecidas."""
    valid_moves = []
    
    for piece in pieces:
        if ends[0] is None or piece.matches(ends[0]):
            valid_moves.append((piece, 'left'))
        if ends[1] is None or (piece.matches(ends[1]) and ends[0] != ends[1]):
            valid_moves.append((piece, 'right'))
    
    return valid_moves

def apply_move(board, piece, side, ends):
    """Simula a aplicação de uma jogada e retorna o novo tabuleiro e extremidades."""
    board = board.copy()
    new_piece = piece
    
    if side == 'left':
        if ends[0] is None:  # Primeira peça
            board.append(new_piece)
        elif piece.right == ends[0]:
            board.insert(0, new_piece)
        else:
            board.insert(0, new_piece.flipped())
    else:  # right
        if ends[1] is None:  # Primeira peça
            board.append(new_piece)
        elif piece.left == ends[1]:
            board.append(new_piece)
        else:
            board.append(new_piece.flipped())
    
    if not board:
        new_ends = (None, None)
    elif len(board) == 1:
        new_ends = (board[0].left, board[0].right)
    else:
        new_ends = (board[0].left, board[-1].right)
    
    return board, new_ends

def minimax(board, ends, player_pieces, opponent_pieces, depth, alpha, beta, maximizing_player, difficulty):
    """Algoritmo Minimax com poda alfa-beta e suporte a níveis de dificuldade."""
    # Condições de parada
    if depth == 0 or not player_pieces or not opponent_pieces:
        return evaluate_state(player_pieces, opponent_pieces, difficulty), None
    
    valid_moves = get_valid_moves(player_pieces, ends)
    
    if not valid_moves:
        # Passa a vez - troca os jogadores e continua
        return minimax(board, ends, opponent_pieces, player_pieces, 
                      depth - 1, alpha, beta, not maximizing_player, difficulty)[0], None
    
    if maximizing_player:
        max_eval = float('-inf')
        best_move = None
        
        # Para dificuldade fácil, ignora algumas jogadas aleatoriamente para decisões subótimas
        if difficulty == DifficultyLevel.EASY:
            import random
            valid_moves = random.sample(valid_moves, max(1, len(valid_moves) // 2))
        
        for piece, side in valid_moves:
            new_board, new_ends = apply_move(board[:], piece, side, ends)
            new_player_pieces = player_pieces[:]
            new_player_pieces.remove(piece)
            
            eval_score, _ = minimax(new_board, new_ends, opponent_pieces, new_player_pieces, 
                                  depth - 1, alpha, beta, False, difficulty)
            
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = (piece, side)
            
            alpha = max(alpha, max_eval)
            if beta <= alpha and difficulty != DifficultyLevel.EASY:  # Sem poda no modo fácil
                break
                
        return max_eval, best_move
    else:
        min_eval = float('inf')
        best_move = None
        
        for piece, side in valid_moves:
            new_board, new_ends = apply_move(board[:], piece, side, ends)
            new_player_pieces = player_pieces[:]
            new_player_pieces.remove(piece)
            
            eval_score, _ = minimax(new_board, new_ends, opponent_pieces, new_player_pieces, 
                                  depth - 1, alpha, beta, True, difficulty)
            
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = (piece, side)
            
            beta = min(beta, min_eval)
            if beta <= alpha and difficulty != DifficultyLevel.EASY:  # Sem poda no modo fácil
                break
                
        return min_eval, best_move

def get_search_depth(difficulty):
    """Retorna a profundidade da busca com base no nível de dificuldade."""
    if difficulty == DifficultyLevel.EASY:
        return 2
    elif difficulty == DifficultyLevel.MEDIUM:
        return 3
    else:  # HARD
        return 4

def find_best_move(board, ends, player_pieces, opponent_pieces, difficulty=DifficultyLevel.MEDIUM):
    """Encontra a melhor jogada usando o minimax com poda alfa-beta."""
    depth = get_search_depth(difficulty)
    _, best_move = minimax(board, ends, player_pieces, opponent_pieces, 
                          depth, float('-inf'), float('inf'), True, difficulty)
    return best_move
