class DominoPiece:
    """Representa uma peça de dominó com valores esquerdo e direito."""
    
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def flipped(self):
        """Retorna uma nova peça com os valores invertidos."""
        return DominoPiece(self.right, self.left)
    
    def matches(self, number):
        """Verifica se a peça combina com um número fornecido."""
        if number is None:  # A primeira peça pode ser qualquer uma
            return True
        return self.left == number or self.right == number
    
    def is_double(self):
        """Verifica se a peça é uma dupla (mesmo valor nos dois lados)."""
        return self.left == self.right
    
    def get_value(self):
        """Retorna o valor total da peça."""
        return self.left + self.right
    
    def __eq__(self, other):
        """Compara duas peças para ver se são iguais."""
        if not isinstance(other, DominoPiece):
            return False
        return (self.left == other.left and self.right == other.right) or \
               (self.left == other.right and self.right == other.left)
    
    def __repr__(self):
        """Representação em string da peça."""
        return f"[{self.left}|{self.right}]"
