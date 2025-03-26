class Piece(object):
    """
    Базовый класс для шахматных фигур.

    Attributes:
        color (str): Цвет фигуры.
        symbol (str): Символ фигуры.
        is_on_board (bool): Находится ли фигура на доске.
    """
    def __init__(self, color, symbol):
        self.color = color
        self.symbol = symbol
        self.is_on_board = True

    def move(self, start, end):
        """
        Абстрактный метод для передвижения фигуры.

        Args:
            start (tuple): Начальная позиция (row, col).
            end (tuple): Конечная позиция (row, col).

        Returns:
            bool: Может ли фигура сделать ход.
        """
        pass

    def __str__(self):
        return self.symbol

class Pawn(Piece):
    """
    Пешка двигается вперед на одну клетку, а бьет по диагонали.
    """

    def __init__(self, color):
        """
        Инициализирует пешку.

        Args:
            color (str): Цвет фигуры ('white' или 'black').
        """
        symbol = "P"
        super().__init__(color, symbol)

    def move(self, start, end):
        """Пешка двигается вперед на 1 клетку, бьет по диагонали"""
        row1, col1 = start
        row2, col2 = end
        direction = -1 if self.color == "white" else 1  # Белые двигаются вниз
        # Обычный ход
        if col1 == col2 and row2 == row1 + direction:
            return True
        # Взятие по диагонали
        if abs(col2 - col1) == 1 and row2 == row1 + direction:
            return True
        return False

class Rook(Piece):
    """
    Ладья двигается по горизонтали или вертикали.
    """

    def __init__(self, color):
        """
        Инициализирует ладью.

        Args:
            color (str): Цвет фигуры.
        """
        symbol = "R"
        super().__init__(color, symbol)

    def move(self, start, end):
        row1, col1 = start
        row2, col2 = end
        return row1 == row2 or col1 == col2

class Knight(Piece):
    """
    Конь ходит буквой "Г"
    """
    def __init__(self, color):
        symbol = "N"
        super().__init__(color, symbol)

    def move(self, start, end):
        row1, col1 = start
        row2, col2 = end
        return (abs(row1 - row2), abs(col1 - col2)) in [(2, 1), (1, 2)]


class Bishop(Piece):
    """
    Слон ходит только по диагоналям.
    """

    def __init__(self, color):
        symbol = "B"
        super().__init__(color, symbol)

    def move(self, start, end):
        row1, col1 = start
        row2, col2 = end
        return abs(row1 - row2) == abs(col1 - col2)


class Queen(Piece):
    """
    Ферзь ходит как слон и конь
    """
    def __init__(self, color):
        symbol = "Q"
        super().__init__(color, symbol)

    def move(self, start, end):
        return Rook(self.color).move(start, end) or Bishop(self.color).move(start, end)


class King(Piece):
    """
    Король двигается на одну клетку в любом направлении.
    """
    def __init__(self, color):
        symbol = "K"
        super().__init__(color, symbol)

    def move(self, start, end):
        row1, col1 = start
        row2, col2 = end
        return max(abs(row1 - row2), abs(col1 - col2)) == 1


class Scandic(Piece):
    """Ходит ровно на 2 клетки по диагонали"""

    def __init__(self, color):
        symbol = "S"
        super().__init__(color, symbol)

    def move(self, start, end):
        row1, col1 = start
        row2, col2 = end
        return abs(row1 - row2) == 2 and abs(col1 - col2) == 2


class Dag(Piece):
    """Ходит ровно на 1 клетку по вертикали/горизонтали"""

    def __init__(self, color):
        symbol = "D"
        super().__init__(color, symbol)

    def move(self, start, end):
        row1, col1 = start
        row2, col2 = end
        return (row1 == row2 and abs(col1 - col2) == 1) or (col1 == col2 and abs(row1 - row2) == 1)

class Technique(Piece):
    """Ходит как конь, только на 1 клетку в сторону длиннее"""
    def __init__(self, color):
        symbol = "T"
        super().__init__(color, symbol)

    def move(self, start, end):
        row1, col1 = start
        row2, col2 = end
        return (abs(row1 - row2) == 2 and abs(col1 - col2) == 2)