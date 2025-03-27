from Figures import Pawn, Rook, Knight, Bishop, Queen, King, Scandic, Dag, Technique


class Board(object):
    """
    Класс, представляющий шахматную доску.

    Attributes:
        grid (list): 8x8 массив, представляющий игровое поле.
        current_turn (str): Цвет игрока, который сейчас ходит
        move_count (int): Количество сделанных ходов.
    """
    def __init__(self):
        """Создает шахматную доску и расставляет фигуры."""
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        self.current_turn = "white"
        self.move_count = 0 
        if game_type == 1:
            self.place()
        if game_type == 2:
            self.place_special()




    def place(self):
        """Расставляет фигуры на стартовые позиции."""
        order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for col in range(8):
            self.grid[6][col] = Pawn("white")
            self.grid[1][col] = Pawn("black")
            self.grid[7][col] = order[col]("white")
            self.grid[0][col] = order[col]("black")

    def place_special(self):
        """Расставление специальных фигур"""
        for col in range(8):
            self.grid[6][col] = Pawn("white")
            self.grid[1][col] = Pawn("black")
        self.grid[0][0] = Scandic('black')
        self.grid[7][0] = Scandic('white')
        self.grid[0][7] = Dag('black')
        self.grid[7][7] = Dag('white')
        self.grid[0][1] = Technique('black')
        self.grid[7][1] = Technique('white')
        self.grid[0][6] = Technique('black')
        self.grid[7][6] = Technique('white')
        self.grid[0][2] = Bishop('black')
        self.grid[7][2] = Bishop('white')
        self.grid[0][3] = Queen('black')
        self.grid[7][3] = Queen('white')
        self.grid[0][4] = King('black')
        self.grid[7][4] = King('white')
        self.grid[0][5] = Bishop('black')
        self.grid[7][5] = Bishop('white')

    def move_piece(self, start, end):
        """
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
            print("На выбранной клетке нет фигуры.")
            return False

        if piece.color != self.current_turn:
            print(f"Сейчас ходят {self.current_turn}. Выбрана фигура другого цвета.")
            return False

        target = self.grid[row2][col2]

        if piece.move(start, end):
            if target and target.color != piece.color:
                print(f"{piece.symbol} {piece.color} берет {target.symbol} {target.color} на ({row2}, {col2})")
                target.is_on_board = False

                # Если съели короля - игра окончена
                if isinstance(target, King):
                    print(f"Король {target.color} побежден! Игра окончена.")
                    exit()

            self.grid[row2][col2] = piece
            self.grid[row1][col1] = None
            self.current_turn = "black" if self.current_turn == "white" else "white"
            self.move_count += 1
            return True
        else:
            print("Неверный ход.")
            return False

    def display(self):
        """Выводит шахматную доску в консоль."""
        print("  A B C D E F G H")
        print("  ---------------")
        for i, row in enumerate(self.grid):
            print(f"{i + 1}|", end=" ")
            print(" ".join(str(cell) if cell else "." for cell in row))
        print(f"\nХодят: {'Белые' if self.current_turn == 'white' else 'Черные'}\n")

    @staticmethod
    def chess_to_coords(chess_pos):
        """
        Конвертирует шахматные координаты

        Args:
            chess_pos (str): Шахматные координаты
        Returns:
            tuple: Индексы массива
        """
        col = ord(chess_pos[0].upper()) - ord("A")
        row = int(chess_pos[1]) - 1
        return row, col

    @staticmethod
    def coords_to_chess(coords):
        """
        Конвертирует индексы массива в шахматные координаты.

        Args:
            coords (tuple): Индексы массива

        Returns:
            str: Шахматные координаты.
        """
        col = chr(coords[1] + ord("A"))
        row = str(coords[0] + 1)
        return col + row
print("Выберите тип игры", "1 - Классические шахматы", "2 - Шахматы с изменными фигурами", sep="\n")
game_type = int(input())
board = Board()
board.display()

while True:
    move = input("Введите ход (например, A2 A3): ").upper().split()
    if len(move) != 2:
        print("Неверный формат.")
        continue

    try:
        start = board.chess_to_coords(move[0])
        end = board.chess_to_coords(move[1])
        if board.move_piece(start, end):
            board.display()
    except (IndexError, ValueError):
        print("Ошибка ввода. Введите координаты в формате A2.")
