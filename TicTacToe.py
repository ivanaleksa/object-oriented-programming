from random import choice
import os

class TicTacToe:
    FREE_CELL = 0  # свободная клетка
    HUMAN_X = 1  # крестик (игрок - человек)
    COMPUTER_O = 2  # нолик (игрок - компьютер)

    def __init__(self):
        self.pole_size = 3
        self.init()

    def check_init(self):
        if not ("pole" in self.__dict__.keys() and "free_cells" in self.__dict__.keys()):
            raise AttributeError("Необходимо проинициализировать поле")

    def __getitem__(self, item):
        self.check_init()
        r, c = item
        if type(r) is not int or type(c) is not int or r < 0 or c < 0 or r >= self.pole_size or c >= self.pole_size:
            raise IndexError('некорректно указанные индексы')
        return self.pole[r][c].value

    def __setitem__(self, key, value):
        self.check_init()
        r, c = key
        if type(r) is not int or type(c) is not int or r < 0 or c < 0 or r >= self.pole_size or c >= self.pole_size:
            raise IndexError('некорректно указанные индексы')
        if value not in (0, 1, 2):
            return ValueError("Не корректное значение")
        self.pole[r][c].value = value

    def init(self):
        setattr(self, "pole", [[Cell() for _ in range(self.pole_size)] for _ in range(self.pole_size)])
        setattr(self, "free_cells", [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)])

    def show(self):
        self.check_init()
        d = {0: "#", 1: "X", 2: "O"}
        for i in range(self.pole_size):
            for j in range(self.pole_size):
                print(d[self.pole[i][j].value], end=" ")
            print()

    def human_go(self):
        x, y = map(int, input().split())
        self.check_init()
        if self.pole[x][y].value != 0:
            raise IndexError("Клетка уже занята")
        self.pole[x][y].value = 1
        del self.free_cells[self.free_cells.index((x, y))]

    def computer_go(self):
        self.check_init()
        x, y = choice(self.free_cells)
        self.pole[x][y].value = 2
        del self.free_cells[self.free_cells.index((x, y))]

    @property
    def is_human_win(self):
        all_win_comb = [((0, 0), (0, 1), (0, 2)), ((0, 0), (1, 1), (2, 2)), ((0, 0), (1, 0), (2, 0)),
                        ((0, 1), (1, 1), (2, 1)),
                        ((0, 2), (1, 1), (2, 0)), ((0, 2), (1, 2), (2, 2)),
                        ((1, 0), (1, 1), (1, 2)),
                        ((2, 0), (2, 1), (2, 2))]
        for comb in all_win_comb:
            a, b, c = comb
            if self.pole[a[0]][a[1]].value == self.pole[b[0]][b[1]].value == self.pole[c[0]][c[1]].value == TicTacToe.HUMAN_X:
                return True
        return False

    @property
    def is_computer_win(self):
        all_win_comb = [((0, 0), (0, 1), (0, 2)), ((0, 0), (1, 1), (2, 2)), ((0, 0), (1, 0), (2, 0)),
                        ((0, 1), (1, 1), (2, 1)),
                        ((0, 2), (1, 1), (2, 0)), ((0, 2), (1, 2), (2, 2)),
                        ((1, 0), (1, 1), (1, 2)),
                        ((2, 0), (2, 1), (2, 2))]
        for comb in all_win_comb:
            a, b, c = comb
            if self.pole[a[0]][a[1]].value == self.pole[b[0]][b[1]].value == self.pole[c[0]][c[1]].value == TicTacToe.COMPUTER_O:
                return True
        return False

    @property
    def is_draw(self):
        return all([all([not bool(elem) for elem in l]) for l in self.pole])

class Cell:
    def __init__(self):
        self.value = 0

    def __bool__(self):
        return self.value == 0

def main():
    game = TicTacToe()
    game.init()

    while True:
        os.system("cls")
        game.show()

        game.human_go()
        if game.is_human_win:
            os.system("cls")
            print("Вы выиграли")
            game.show()
            break
        if game.is_draw:
            os.system("cls")
            print("Ничья")
            game.show()
            break

        game.computer_go()
        if game.is_computer_win:
            os.system("cls")
            print("Компьютер выиграл")
            game.show()
            break
        if game.is_draw:
            os.system("cls")
            print("Ничья")
            game.show()
            break

if "__main__" == __name__:
    main()


# game = TicTacToe()
# game.init()
# while True:
#     os.system("cls")
#     game.show()
#     game.human_go()
#     if game.is_human_win:
#         os.system("cls")
#         print("Вы выиграли")
#         game.show()
#         break
#     if game.is_draw:
#         os.system("cls")
#         print("Ничья")
#         game.show()
#         break
#     game.computer_go()
#     if game.is_computer_win:
#         os.system("cls")
#         print("Компьютер выиграл")
#         game.show()
#         break
#     if game.is_draw:
#         os.system("cls")
#         print("Ничья")
#         game.show()
#         break
