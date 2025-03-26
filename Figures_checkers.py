class Checker:
    """
    Класс, представляющий шашку.

    Attributes:
        color (str): Цвет шашки
    """
    def __init__(self, color):
        self.color = color
        self.symbol = "●" if color == "white" else "○"

    def move(self, start, end):
        """
        Проверяет возможность хода.

        Args:
            start (tuple): Координаты начальной клетки (row, col).
            end (tuple): Координаты целевой клетки (row, col).

        Returns:
            bool: Может ли шашка сделать такой ход.
        """
        row1, col1 = start
        row2, col2 = end
        direction = -1 if self.color == "white" else 1  # Белые идут вниз, черные вверх
        return abs(row2 - row1) == 1 and abs(col2 - col1) == 1 and row2 - row1 == direction

    def can_capture(self, start, end, board):
        """
        Проверяет возможность взятия шашки.

        Args:
            start (tuple): Координаты начальной клетки (row, col).
            end (tuple): Координаты целевой клетки (row, col).
            board (Board): Игровая доска.

        Returns:
            bool: Можно ли выполнить взятие.
        """
        row1, col1 = start
        row2, col2 = end

        if abs(row2 - row1) == 2 and abs(col2 - col1) == 2:
            middle_row = (row1 + row2) // 2
            middle_col = (col1 + col2) // 2
            middle_piece = board.grid[middle_row][middle_col]
            if middle_piece and middle_piece.color != self.color:
                return True
        return False

    def __str__(self):
        return self.symbol


class Board:
    """
    Класс, представляющий игровую доску для шашек.
    """
    def __init__(self):
        """Создает игровую доску и расставляет шашки."""
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        self.current_turn = "white"
        self.place_checkers()

    def place_checkers(self):
        """Расставляет шашки на стартовые позиции."""
        for row in range(3):
            for col in range(8):
                if (row + col) % 2 == 1:
                    self.grid[row][col] = Checker("black")

        for row in range(5, 8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    self.grid[row][col] = Checker("white")

    def move_piece(self, start, end):
        """
        Перемещает шашку, если ход корректен.

        Args:
            start (tuple): Координаты начальной клетки
            end (tuple): Координаты целевой клетки

        Returns:
            bool: Успешность хода.
        """
        row1, col1 = start
        row2, col2 = end
        piece = self.grid[row1][col1]

        if piece is None:
            print("На выбранной клетке нет шашки.")
            return False

        if piece.color != self.current_turn:
            print(f"Сейчас ходят {self.current_turn}. Выбрана шашка другого цвета.")
            return False

        if piece.move(start, end) and self.grid[row2][col2] is None:
            # Обычный ход
            self.grid[row2][col2] = piece
            self.grid[row1][col1] = None
            self.current_turn = "black" if self.current_turn == "white" else "white"
            return True

        if piece.can_capture(start, end, self):
            # Удаляем съеденную шашку
            middle_row = (row1 + row2) // 2
            middle_col = (col1 + col2) // 2
            self.grid[middle_row][middle_col] = None

            # Перемещаем шашку
            self.grid[row2][col2] = piece
            self.grid[row1][col1] = None

            # Проверка на победу
            if not any(cell for row in self.grid for cell in row if cell and cell.color != self.current_turn):
                print(f"{self.current_turn.capitalize()} winner!")
                exit()

            self.current_turn = "black" if self.current_turn == "white" else "white"
            return True

        print("Неверный ход.")
        return False

    def display(self):
        """Выводит доску в консоль."""
        print("  A B C D E F G H")
        print("  ---------------")
        for i, row in enumerate(self.grid):
            print(f"{i + 1}|", end=" ")
            print(" ".join(str(cell) if cell else "." for cell in row))
        print(f"\nХодят: {'Белые' if self.current_turn == 'white' else 'Черные'}\n")

    @staticmethod
    def chess_to_coords(chess_pos):
        """Конвертирует шахматные координаты"""
        col = ord(chess_pos[0].upper()) - ord("A")
        row = int(chess_pos[1]) - 1
        return row, col

    @staticmethod
    def coords_to_chess(coords):
        """Конвертирует индексы массива"""
        col = chr(coords[1] + ord("A"))
        row = str(coords[0] + 1)
        return col + row



board = Board()
board.display()

while True:
    move = input("Введите ход (например, A3 B4): ").upper().split()
    if len(move) != 2:
        print("Неверный формат.")
        continue

    try:
        start = board.chess_to_coords(move[0])
        end = board.chess_to_coords(move[1])
        if board.move_piece(start, end):
            board.display()
    except (IndexError, ValueError):
        print("Ошибка ввода. Введите координаты в формате A3.")
