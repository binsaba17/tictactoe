import tkinter as tk
## importo il modulo tkinter per creare un'interfaccia grafica per l'utente
from tkinter import messagebox
import random


class Board:
    def __init__(self, size=4):
        self.size = size
        self.board = [[' ' for _ in range(size)] for _ in range(size)]
        ### creo la griglia di dimensioni 4x4 ( lista dentro una lista)

    def is_full(self):
        for row in self.board:
            if ' ' in row:
                return False
        return True
        ### la griglia è piena? ci sono ancora spazi vuoti?
    def is_winner(self, player):
        # controllo le righe e le colonne
        for i in range(self.size):
            if all(self.board[i][j] == player for j in range(self.size)) or \
               all(self.board[j][i] == player for j in range(self.size)):
                return True

        # Controllo le diagonali
        if all(self.board[i][i] == player for i in range(self.size)) or \
           all(self.board[i][self.size - i - 1] == player for i in range(self.size)):
            return True
        
        return False
        ##solo le combinazioni vincenti,che verranno usate per capire quando il giocatore
        ## o il suo avversario vince
    def make_move(self, move, player):
        if self.board[move[0]][move[1]] == ' ':
            self.board[move[0]][move[1]] = player
            return True
        return False
    ### se la casella desiderata è vuota inserisco la mossa del giocatore in quella posizione
    def undo_move(self, move):
        self.board[move[0]][move[1]] = ' '
        ### annullo la mossa (serve per il giocatore computer)
    def print_board(self):
        for row in self.board:
            print(" | ".join(row))
            print("-" * (4 * self.size - 1))
        ### stampo la griglia

class Player:
    def __init__(self, symbol):
        self.symbol = symbol

    def make_move(self, board):
        pass
### implemento la classe giocatore, 
### make move verrà implementata nelle sottoclassi

class GUI: #grafical user interface
    def __init__(self, master):
        self.master = master
        self.master.title("Tris 4X4") #titolo
        self.board = Board() #griglia
        self.player1 = HumanPlayer('X')
        self.player2 = ComputerPlayer('O')
        self.current_player = self.player1

        self.buttons = [[None for _ in range(self.board.size)] for _ in range(self.board.size)]
        for i in range(self.board.size):
            for j in range(self.board.size):
                self.buttons[i][j] = tk.Button(self.master, text="", font=('Arial', 20), width=4, height=4,
                                                command=lambda i=i, j=j: self.make_move(i, j))
                self.buttons[i][j].grid(row=i, column=j)
        ### vengono creati i pulsanti ed "command " permette di collegare ogni pulsante con
        ### il metodo make_move così da poter gestire le mosse dei giocatori
                
    def make_move(self, row, col):
        if self.board.make_move((row, col), self.current_player.symbol):
            self.buttons[row][col].config(text=self.current_player.symbol)
            if self.board.is_winner(self.current_player.symbol):
                self.display_winner(self.current_player.symbol)
                self.reset_game()
            elif self.board.is_full():
                messagebox.showinfo("Game Over", "It's a draw!")
                self.reset_game()
            else:
                self.current_player = self.player2 if self.current_player == self.player1 else self.player1
                if isinstance(self.current_player, ComputerPlayer):
                    self.make_computer_move()
        ### viene chiamato quando un giocatore fa un click su una cella, viene verificato se la mossa è valida
        ### viene controllato se c'è un vincitore oppure un pareggio,viene aggiornata la griglia
    def make_computer_move(self):
        move = self.current_player.make_move(self.board)
        self.make_move(move[0], move[1])
        #### chiama make_move per il computer
    def display_winner(self, symbol):
        winner = "Player X" if symbol == 'X' else "Player O"
        messagebox.showinfo("Game Over", f"{winner} wins!")
        ### mostra se abbiamo un vincitore 
    def reset_game(self):
        self.board = Board()
        self.current_player = self.player1
        for i in range(self.board.size):
            for j in range(self.board.size):
                self.buttons[i][j].config(text="")
        ### reimposta il gioco per una nuova partita

class HumanPlayer(Player):
    def make_move(self, board):
        valid_move = False
        while not valid_move:
            row = int(input("Inserisci la riga: ")) - 1
            col = int(input("Inserisci la colonna: ")) - 1
            if 0 <= row < board.size and 0 <= col < board.size and board.board[row][col] == ' ':
                valid_move = True
        return row, col
### classe per il giocatore utente( non il computer), inserisce le mosse

class ComputerPlayer(Player):
    def __init__(self, symbol):
        super().__init__(symbol)
        

    def make_move(self, board):
        random_choice_probability = random.random()
        if random_choice_probability > 0.8:
            return self.make_random_move(board)
        elif random_choice_probability > 0.4:
            depth = 2
        else:
            depth = 4

        _, move = self.minimax(board, depth, self.symbol, float('-inf'), float('inf'), True)
        return move
        
    def make_random_move(self, board):
        available_moves = [(i, j) for i in range(board.size) for j in range(board.size) if board.board[i][j] == ' ']
        return random.choice(available_moves)
    ### classe per il giocatore computer, in seguito viene implementato l'algoritmo minimax per la scelta della mossa migliore con la 
    ### potatura alfa beta che serve a ridurre sensibilmente il numero delle possibili mosse che non sono utili alla
    ### riuscita del gioco
    def minimax(self, board, depth, player, alpha, beta, maximizing_player):
        if depth == 0 or board.is_full() or board.is_winner(self.symbol) or board.is_winner('X' if self.symbol == 'O' else 'O'):
            return self.evaluate(board), None

        available_moves = [(i, j) for i in range(board.size) for j in range(board.size) if board.board[i][j] == ' ']

        if maximizing_player:
            max_eval = float('-inf')
            best_move = None
            for move in available_moves:
                board.make_move(move, player)
                eval, _ = self.minimax(board, depth - 1, player, alpha, beta, False)
                board.undo_move(move)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, max_eval)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            best_move = None
            for move in available_moves:
                board.make_move(move, 'X' if player == 'O' else 'O')
                eval, _ = self.minimax(board, depth - 1, player, alpha, beta, True)
                board.undo_move(move)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, min_eval)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def evaluate(self, board):
        if board.is_winner(self.symbol):
            return 10
        elif board.is_winner('X' if self.symbol == 'O' else 'O'):
            return -10
        return 0


def play_game():
    board = Board()
    player1 = HumanPlayer('X')
    player2 = ComputerPlayer('O')

    current_player = player1

    while not board.is_full() and not board.is_winner(player1.symbol) and not board.is_winner(player2.symbol):
        move = current_player.make_move(board)
        board.make_move(move, current_player.symbol)

        if current_player == player1:
            current_player = player2
        else:
            current_player = player1

    board.print_board()
    if board.is_winner(player1.symbol):
        print("Player X wins!")
    elif board.is_winner(player2.symbol):
        print("Player O wins!")
    else:
        print("It's a draw!")


if __name__ == "__main__":
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()
