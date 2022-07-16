from random import randint
import os

class Cell:
    """ Класс клетки поля. Имеет локальные атрибуты: around_mines - количество мин вокруг,
     mine - булево значение True мина False обычная клетка, fl_open - булево значение (показывать или нет клетку) """
    
    def __init__(self, around_mines=0, mine=False):
        self.around_mines = around_mines
        self.mine = mine
        self.fl_open = False

class GamePole:
    """ Класс игрового поля. Представляет собой матрицу размера N x N объектов класса Cell """

    def __init__(self, n, m):
        self.n = n
        self.m = m
        self.pole = self.init()

    def init(self):
        r = [[Cell() for _ in range(self.n)] for _ in range(self.n)]
        m_ = 0

        # расстановака мин
        while m_ < self.m:
            i = randint(0, self.n - 1)
            j = randint(0, self.n - 1)
            if r[i][j].mine:
                continue
            r[i][j].mine = True
            m_ += 1

        # проверка кол-ва мин рядом
        indx = (-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)
        for i in range(self.n):
            for j in range(self.n):
                if r[i][j].mine == False:
                    r[i][j].around_mines = sum((r[x + i][y + j].mine for x, y in indx if 0 <= x + i < self.n and 0 <= y + j < self.n))

        return r

    def show(self):
        """ метод отображения игрового поля """

        for i in range(self.n):
            for j in range(self.n):
                if self.pole[i][j].fl_open and not self.pole[i][j].mine:
                    print(self.pole[i][j].around_mines, end=" ")
                elif self.pole[i][j].fl_open and self.pole[i][j].mine:
                    print("*", end=" ")
                elif not self.pole[i][j].fl_open:
                    print("#", end=" ")
            print()

    def click(self, x, y):
        """ Нажатие на ячейку x y """
        self.pole[x - 1][y - 1].fl_open = True


n, m = map(int, input("Enter size and count mines: ").split())
pole_game = GamePole(n, m)
check = 0

while True:
    try:
        pole_game.show()
        x, y = map(int, input().split())
        pole_game.click(x, y)
        os.system("cls")
        if pole_game.pole[x - 1][y - 1].mine:
            pole_game.show()
            print("You lose!")
            break
        check += 1
        if n**2 - check == m:
            pole_game.show()
            print("You won")
            break
    except:
        print("Few arguments")