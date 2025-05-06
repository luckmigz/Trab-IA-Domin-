from colors import Color

class DominoGame:
    """Classe principal para gerenciar o jogo de dominó."""
    
    def __init__(self, player1, player2, stock):
        self.board = []
        self.ends = (None, None)  # (extremidade esquerda, extremidade direita)
        self.players = [player1, player2]
        self.stock = stock
        self.current_player_idx = 0
        self.pass_count = 0
        self.game_over = False
    
    @property
    def current_player(self):
        """Retorna o jogador atual."""
        return self.players[self.current_player_idx]
    
    def get_opponent(self, player):
        """Retorna o oponente do jogador fornecido."""
        return self.players[0] if player == self.players[1] else self.players[1]
    
    def next_player(self):
        """Troca para o próximo jogador."""
        self.current_player_idx = 1 - self.current_player_idx
    
    def find_starting_player(self):
        """Determina o jogador e a peça que iniciam o jogo."""
        # Procura por duplas
        doubles = []
        for player_idx, player in enumerate(self.players):
            for piece in player.pieces:
                if piece.is_double():
                    doubles.append((player_idx, piece, piece.left))
        
        # Se houver duplas, a maior começa
        if doubles:
            doubles.sort(key=lambda x: x[2], reverse=True)
            player_idx, piece, _ = doubles[0]
            return player_idx, piece
        
        # Se não houver duplas, a peça de maior valor começa
        highest = (-1, None, -1)
        for player_idx, player in enumerate(self.players):
            for piece in player.pieces:
                value = piece.get_value()
                if value > highest[2]:
                    highest = (player_idx, piece, value)
        
        return highest[0], highest[1]
    
    def update_ends(self):
        """Atualiza as extremidades do tabuleiro após uma jogada."""
        if not self.board:
            self.ends = (None, None)
        elif len(self.board) == 1:
            self.ends = (self.board[0].left, self.board[0].right)
        else:
            self.ends = (self.board[0].left, self.board[-1].right)
    
    def apply_move(self, piece, side):
        """Aplica uma jogada no tabuleiro."""
        if side == 'left':
            if self.ends[0] is None:  # Primeira peça
                self.board.append(piece)
            elif piece.right == self.ends[0]:
                self.board.insert(0, piece)
            else:
                self.board.insert(0, piece.flipped())
        else:  # lado direito
            if self.ends[1] is None:  # Primeira peça
                self.board.append(piece)
            elif piece.left == self.ends[1]:
                self.board.append(piece)
            else:
                self.board.append(piece.flipped())
        
        self.update_ends()
    
    def display_board(self):
        """Exibe o tabuleiro atual."""
        if not self.board:
            print("\nO tabuleiro está vazio.")
            return
        
        print(f"\n{Color.CYAN}Tabuleiro:{Color.RESET}", end=" ")
        
        # Para tabuleiros longos, adiciona reticências no meio
        if len(self.board) > 10:
            for piece in self.board[:5]:
                print(piece, end=" ")
            print(f"{Color.YELLOW}...{Color.RESET}", end=" ")
            for piece in self.board[-5:]:
                print(piece, end=" ")
        else:
            for piece in self.board:
                print(piece, end=" ")
        
        print(f"\n{Color.CYAN}Extremidades:{Color.RESET} Esquerda={self.ends[0]}, Direita={self.ends[1]}")
    
    def display_game_state(self):
        """Exibe o estado completo do jogo."""
        print(f"\n{Color.MAGENTA}{'='*50}{Color.RESET}")
        self.display_board()
        print(f"\n{Color.YELLOW}Monte:{Color.RESET} {len(self.stock)} peças restantes")
        
        for player in self.players:
            if player == self.current_player:
                print(f"{Color.GREEN}➤ {player.name}:{Color.RESET} {len(player.pieces)} peças")
            else:
                print(f"  {player.name}: {len(player.pieces)} peças")
        
        print(f"{Color.MAGENTA}{'='*50}{Color.RESET}\n")
    
    def check_win_condition(self):
        """Verifica se o jogo foi vencido ou está travado."""
        # Verifica se algum jogador ficou sem peças
        for player in self.players:
            if not player.pieces:
                print(f"\n{Color.GREEN}🏆 {player.name} venceu! Ficou sem peças.{Color.RESET}")
                return True
        
        # Verifica se o jogo está travado (ninguém pode jogar e o monte acabou)
        if self.pass_count >= len(self.players) and not self.stock:
            print(f"\n{Color.YELLOW}Jogo travado. Calculando vencedor...{Color.RESET}")
            
            # Soma os pontos de cada jogador
            scores = [(player, sum(p.get_value() for p in player.pieces)) for player in self.players]
            scores.sort(key=lambda x: x[1])
            
            print(f"\nPontuações finais:")
            for player, score in scores:
                print(f"{player.name}: {score} pontos")
            
            print(f"\n{Color.GREEN}🏆 {scores[0][0].name} venceu com {scores[0][1]} pontos!{Color.RESET}")
            return True
        
        return False
    
    def start(self):
        """Inicia e executa o jogo."""
        print(f"{Color.GREEN}Iniciando o jogo de dominó!{Color.RESET}")
        
        # Determina o jogador e peça iniciais
        player_idx, starting_piece = self.find_starting_player()
        self.current_player_idx = player_idx
        
        # Coloca a peça inicial no tabuleiro e remove da mão do jogador
        self.current_player.remove_piece(starting_piece)
        self.apply_move(starting_piece, 'esquerda')
        
        print(f"\n{Color.YELLOW}{self.current_player.name} começa com {starting_piece}{Color.RESET}")
        
        # Troca para o próximo jogador
        self.next_player()
        
        # Loop principal do jogo
        while not self.game_over:
            self.display_game_state()
            
            if not self.current_player.has_valid_move(self.ends):
                print(f"{Color.YELLOW}{self.current_player.name} não tem jogadas válidas.{Color.RESET}")
                
                if self.stock:
                    # Compra uma peça do monte
                    drawn_piece = self.stock.pop()
                    self.current_player.add_piece(drawn_piece)
                    print(f"{self.current_player.name} compra uma peça do monte.")
                    
                    # Verifica se pode jogar com a peça comprada
                    if drawn_piece.matches(self.ends[0]) or drawn_piece.matches(self.ends[1]):
                        self.display_game_state()
                        piece, side = self.current_player.make_move(self)
                        
                        if piece:
                            self.current_player.remove_piece(piece)
                            self.apply_move(piece, side)
                            if side == 'left':
                                print(f"{self.current_player.name} joga {piece} no lado esquedo.")
                            else:   
                                print(f"{self.current_player.name} joga {piece} no lado direito.")
                            
                            self.pass_count = 0
                        else:
                            print(f"{self.current_player.name} passa a vez.")
                            self.pass_count += 1
                    else:
                        print(f"{self.current_player.name} passa a vez.")
                        self.pass_count += 1
                else:
                    # Sem peças no monte, jogador passa
                    print(f"{self.current_player.name} passa a vez.")
                    self.pass_count += 1
            else:
                # Jogador faz uma jogada
                piece, side = self.current_player.make_move(self)
                
                if piece:
                    self.current_player.remove_piece(piece)
                    self.apply_move(piece, side)
                    if side == 'left':
                        print(f"{self.current_player.name} joga {piece} no lado esquedo.")
                    else:   
                        print(f"{self.current_player.name} joga {piece} no lado direito.")
                    self.pass_count = 0
            
            # Verifica condição de vitória
            self.game_over = self.check_win_condition()
            
            if not self.game_over:
                # Próxima rodada
                self.next_player()
                input(f"{Color.GREEN}Pressione Enter para o próximo turno...{Color.RESET}")
      