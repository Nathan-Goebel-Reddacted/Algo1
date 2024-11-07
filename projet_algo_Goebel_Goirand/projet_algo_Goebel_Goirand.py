import os
class GameBoard:
    def __init__(self, n):
        # Si n n'est pas un multiple de 4, on force à en être un
        if n % 4 != 0:
            n += 4 - n % 4
        self.__board_size = n
        self.__board = self.board_init()

    def get_board_size(self):
        return self.__board_size

    def get_board(self):
        return self.__board

    def get_tile_state(self, x, y):
        return self.get_board()[y][x]


    def set_tile_state(self, x, y, value):
        self.get_board()[y][x] = value

    def board_init(self):
        __hound_number = 1
        __board = []
        # Crée une map vide
        for y in range(self.get_board_size()):
            __board.append([0] * self.get_board_size())
        # Placer les chiens
        for y in range(1, self.get_board_size(), 2):
            __board[0][y] = __hound_number
            __hound_number += 1
        # Placer le renard
        __board[self.get_board_size() - 1][self.get_board_size() // 2] = -1
        return __board

    def print_board(self):
        #clear terminal
        os.system('cls' if os.name == 'nt' else 'clear')
        #board layout
        print("   ",end="")
        for x in range(1,self.get_board_size()+1):
            print(x,"",end="")
        print("\n   ",end="")
        __a_print="--"*self.get_board_size()
        print(__a_print)
        #board
        for y in range(self.get_board_size()):
            print(y+1,end=" |")
            for x in range(self.get_board_size()):
                if self.get_tile_state(x, y) == 0:
                    print(".", end=" ")
                elif self.get_tile_state(x, y) == -1:
                    print("F", end=" ")
                else:
                    print(self.get_tile_state(x, y), end=" ")
            print()


class Hound:
    def __init__(self, x=0, y=0):
        self._token_x = int(x)
        self._token_y = int(y)

    def can_move_to(self, board, x, y):
        # Vérifie que la case est dans les limites et que c'est une diagonale valide
        if 0 <= y < board.get_board_size() and y == self._token_y + 1:
            if 0 <= x < board.get_board_size() and x in [self._token_x - 1, self._token_x + 1]:
                if board.get_tile_state(x,y)==0:# La case doit être vide
                    return True
        return False

    def move(self, board):
        while True:
            try:
                new_col = int(input("Saisir la colonne:")) - 1
                new_row = int(input("Saisir la ligne:")) - 1
                if self.can_move_to(board,new_col,new_row):
                    # Placer le hound à la nouvelle position
                    board.set_tile_state(
                        new_col,
                        new_row,
                        board.get_tile_state(self._token_x, self._token_y)
                        )
                    # Libérer l'ancienne position
                    board.set_tile_state(self._token_x, self._token_y, 0)
                    self._token_x,self._token_y = new_col,new_row
                    break
                else:
                    print("Déplacement non valide, réessayez.")
            except (IndexError,ValueError):
                print("Veuillez saisir des coordonnées valides.")

    def can_move(self,board):
        return (self.can_move_to(board, self._token_x - 1, self._token_y + 1) or
                self.can_move_to(board, self._token_x + 1, self._token_y + 1))


class Fox(Hound):
    def can_move_to(self, board, x, y):
        # Vérifie que la case est dans les limites et que c'est une diagonale valide
        if 0 <= y < board.get_board_size() and y in [self._token_y+1 , self._token_y-1]:
            if 0 <= x < board.get_board_size() and x in [self._token_x - 1, self._token_x + 1]:
                if board.get_tile_state(x,y)==0:# La case doit être vide
                    return True
        return False

    def can_move(self,board):
        return (self.can_move_to(board, self._token_x - 1, self._token_y + 1) or
                self.can_move_to(board, self._token_x + 1, self._token_y + 1) or
                self.can_move_to(board, self._token_x - 1, self._token_y - 1) or
                self.can_move_to(board, self._token_x + 1, self._token_y - 1))


    def win(self):
        return self._token_y == 0 # Si le fox atteint la première ligne, il gagne

class FoxAndHounds():
    def __init__(self,n=8):
        #initialisation du jeu
        self.__board=GameBoard(n)
        self.__fox=Fox(self.__board.get_board_size()/2 , self.__board.get_board_size()-1)
        self.__hound=[]
        for coord in range(1,self.__board.get_board_size(),2):
            self.__hound.append(Hound(coord,0))
        self.turn_sequence()

    def turn_sequence(self):
        while True:
            self.__board.print_board()
            if self.fox_turn() is True:
                print("fox a gagner!")
                break
            self.__board.print_board()
            if self.hound_turn() is True:
                print("hound a gagner!")
                break

    def fox_turn(self):
        print("Fox doit bouger:")
        self.__fox.move(self.__board)
        return self.__fox.win()

    def hound_turn(self):
        print("hound doit bouger:")
        while True:
            try:
                hound_selected=int(input("quel hound doit bouger?:"))-1
                if self.__hound[hound_selected].can_move(self.__board):
                    self.__hound[hound_selected].move(self.__board)
                    break
                else:
                    print("hound ne peut pas bouger")
            except (ValueError,IndexError):
                continue
        return self.__fox.can_move(self.__board) is False

if __name__ == "__main__":
    try:
        BOARD_SIZE = int(input("Entrez la taille du plateau: "))
    except ValueError:
        print("Entrée invalide,utilisation de la taille par défaut 8.")
        BOARD_SIZE = 8
    FoxAndHounds(BOARD_SIZE)
