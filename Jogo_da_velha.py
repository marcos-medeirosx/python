import tkinter as tk
from tkinter import messagebox

class JogoDaVelha:
    def __init__(self, root):
        self.root = root
        self.root.title("Jogo da Velha - IA Invicta")
        self.tabuleiro = [' '] * 9
        self.jogador_atual = 'X'
        
        self.botoes = []
        for i in range(9):
            btn = tk.Button(
                root, text='', font=('Arial', 20), width=5, height=2,
                command=lambda idx=i: self.jogada_humano(idx)
            )
            btn.grid(row=i//3, column=i%3)
            self.botoes.append(btn)
        
        self.btn_reiniciar = tk.Button(
            root, text="Reiniciar", command=self.reiniciar_jogo
        )
        self.btn_reiniciar.grid(row=3, column=0, columnspan=3, sticky="we")
    
    def jogada_humano(self, posicao):
        if self.tabuleiro[posicao] == ' ' and self.jogador_atual == 'X':
            self.tabuleiro[posicao] = 'X'
            self.botoes[posicao].config(text='X', state='disabled', disabledforeground='blue')
            self.verificar_fim_jogo()
            
            if not self.jogo_acabou:
                self.jogador_atual = 'O'
                self.root.after(500, self.jogada_ia)
    
    def jogada_ia(self):
        melhor_pontuacao = -float('inf')
        melhor_jogada = -1
        
        for i in range(9):
            if self.tabuleiro[i] == ' ':
                self.tabuleiro[i] = 'O'
                pontuacao = self.minimax(False)
                self.tabuleiro[i] = ' '
                
                if pontuacao > melhor_pontuacao:
                    melhor_pontuacao = pontuacao
                    melhor_jogada = i
        
        if melhor_jogada != -1:
            self.tabuleiro[melhor_jogada] = 'O'
            self.botoes[melhor_jogada].config(text='O', state='disabled', disabledforeground='red')
            self.verificar_fim_jogo()
            self.jogador_atual = 'X'
    
    def minimax(self, maximizando):
        if self.verificar_vencedor('O'):
            return 1
        if self.verificar_vencedor('X'):
            return -1
        if ' ' not in self.tabuleiro:
            return 0
        
        if maximizando:
            melhor = -float('inf')
            for i in range(9):
                if self.tabuleiro[i] == ' ':
                    self.tabuleiro[i] = 'O'
                    pontuacao = self.minimax(False)
                    self.tabuleiro[i] = ' '
                    melhor = max(melhor, pontuacao)
            return melhor
        else:
            pior = float('inf')
            for i in range(9):
                if self.tabuleiro[i] == ' ':
                    self.tabuleiro[i] = 'X'
                    pontuacao = self.minimax(True)
                    self.tabuleiro[i] = ' '
                    pior = min(pior, pontuacao)
            return pior
    
    def verificar_vencedor(self, jogador):
        combinacoes = [
            [0,1,2], [3,4,5], [6,7,8],
            [0,3,6], [1,4,7], [2,5,8],
            [0,4,8], [2,4,6]
        ]
        return any(
            all(self.tabuleiro[pos] == jogador for pos in combo)
            for combo in combinacoes
        )
    
    @property
    def jogo_acabou(self):
        return self.verificar_vencedor('X') or self.verificar_vencedor('O') or ' ' not in self.tabuleiro
    
    def verificar_fim_jogo(self):
        if self.verificar_vencedor('X'):
            messagebox.showinfo("Fim do Jogo", "Você venceu! (Isso é um milagre!)")
            self.desabilitar_botoes()
        elif self.verificar_vencedor('O'):
            messagebox.showinfo("Fim do Jogo", "IA venceu! (Como esperado)")
            self.desabilitar_botoes()
        elif ' ' not in self.tabuleiro:
            messagebox.showinfo("Fim do Jogo", "Empate!")
    
    def desabilitar_botoes(self):
        for btn in self.botoes:
            btn.config(state='disabled')
    
    def reiniciar_jogo(self):
        self.tabuleiro = [' '] * 9
        self.jogador_atual = 'X'
        for btn in self.botoes:
            btn.config(text='', state='normal')

root = tk.Tk()
root.resizable(False, False)
jogo = JogoDaVelha(root)
root.mainloop()