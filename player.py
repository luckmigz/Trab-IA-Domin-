from piece import DominoPiece
from colors import Color

class Player:
    """Classe base de jogador com funcionalidades comuns."""
    
    def __init__(self, name, pieces):
        self.name = name
        self.pieces = pieces
    
    def has_valid_move(self, ends):
        """Verifica se o jogador tem jogadas válidas com as pontas atuais do tabuleiro."""
        for piece in self.pieces:
            if piece.matches(ends[0]) or piece.matches(ends[1]):
                return True
        return False
    
    def remove_piece(self, piece):
        """Remove uma peça da mão do jogador."""
        for i, p in enumerate(self.pieces):
            if p == piece:
                return self.pieces.pop(i)
        raise ValueError("Peça não encontrada na mão do jogador")
    
    def add_piece(self, piece):
        """Adiciona uma peça à mão do jogador."""
        self.pieces.append(piece)
    
    def get_valid_moves(self, ends):
        """Retorna todas as jogadas válidas com base nas pontas atuais do tabuleiro."""
        jogadas_validas = []
        for i, piece in enumerate(self.pieces):
            if piece.matches(ends[0]):
                jogadas_validas.append((i, piece, 'left'))
            if piece.matches(ends[1]) and ends[0] != ends[1]:  # Evita duplicatas na primeira jogada
                jogadas_validas.append((i, piece, 'right'))
        return jogadas_validas
    
    def __repr__(self):
        return f"{self.name} - {len(self.pieces)} peças"

class HumanPlayer(Player):
    """Jogador humano com seleção de jogada interativa."""
    
    def make_move(self, game):
        """Permite ao jogador humano escolher interativamente sua jogada."""
        jogadas_validas = self.get_valid_moves(game.ends)
        
        if not jogadas_validas:
            print(f"{Color.YELLOW}Nenhuma jogada válida disponível. Comprando do monte ou passando.{Color.RESET}")
            return None, None
        
        print(f"\n{Color.CYAN}Sua mão:{Color.RESET}")
        for i, piece in enumerate(self.pieces):
            print(f"  {i}: {piece}")
        
        print(f"\n{Color.CYAN}Jogadas válidas:{Color.RESET}")
        for i, (idx, piece, side) in enumerate(jogadas_validas):
            if side == 'left':
                print(f"  {i}: Jogar {piece} no lado esquerdo")
            else:   
                print(f"  {i}: Jogar {piece} no lado direito")
           
        
        while True:
            try:
                escolha = input(f"\n{Color.GREEN}Escolha a jogada (0-{len(jogadas_validas)-1}): {Color.RESET}")
                escolha = int(escolha)
                
                if 0 <= escolha < len(jogadas_validas):
                    idx, piece, side = jogadas_validas[escolha]
                    return piece, side
                else:
                    print(f"{Color.RED}Escolha inválida. Tente novamente.{Color.RESET}")
            except ValueError:
                print(f"{Color.RED}Por favor, insira um número.{Color.RESET}")
            except (KeyboardInterrupt, EOFError):
                raise KeyboardInterrupt("Jogo encerrado pelo usuário")

class AIPlayer(Player):
    """Jogador IA que utiliza o algoritmo minimax para escolher jogadas."""
    
    def __init__(self, name, pieces, difficulty=2):
        super().__init__(name, pieces)
        self.difficulty = difficulty
    
    def make_move(self, game):
        """Utiliza o algoritmo minimax para escolher a melhor jogada."""
        from ai import find_best_move, DifficultyLevel
        
        # Mapeia o nível de dificuldade
        mapa_dificuldade = {
            1: DifficultyLevel.EASY,
            2: DifficultyLevel.MEDIUM,
            3: DifficultyLevel.HARD
        }
        
        # Obtém a melhor jogada usando minimax
        piece, side = find_best_move(
            game.board[:], 
            game.ends, 
            self.pieces[:], 
            game.get_opponent(self).pieces[:], 
            difficulty=mapa_dificuldade[self.difficulty]
        )
        
        return piece, side
