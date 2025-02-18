import tkinter as tk
from tkinter import messagebox
import random
import shelve

# Listas de palavras por tema
temas = {
    'Desenvolvimento Web': ['javascript', 'css', 'html', 'navegador', 'programar', 'internet', 'computador', 'teclado', 'mouse', 'monitor', 'python'],
    'Animais': ['gato', 'cachorro', 'elefante', 'girafa', 'tigre', 'leao', 'zebra', 'macaco', 'panda', 'urso'],
    'Paises': ['brasil', 'argentina', 'canada', 'japao', 'australia', 'franca', 'alemanha', 'italia', 'espanha', 'russia'],
    'Comidas': ['pizza', 'hamburguer', 'sushi', 'lasanha', 'churrasco', 'salada', 'sorvete', 'bolo', 'pao', 'queijo']
}

# Variáveis globais de controle do jogo
palavras = []  # Lista de palavras do tema escolhido
palavra_secreta = ''  # Palavra secreta a ser adivinhada
letras_descobertas = []  # Lista de letras descobertas
erros = 0  # Número de erros cometidos
acertos = 0  # Número de acertos
max_erros = 7  # Número máximo de erros permitidos
pontuacao = 0  # Pontuação do jogador
indice_palavra = 0  # Índice da palavra atual

# Carrega a pontuação e o índice da palavra do banco de dados
with shelve.open('pontuacao_db') as db:
    pontuacao = db.get('pontuacao', 0)
    indice_palavra = db.get('indice_palavra', 0)

# Função para escolher o tema e iniciar o jogo
def escolher_tema(tema):
    global palavras, palavra_secreta, letras_descobertas, erros, acertos
    palavras = temas[tema]  # Define as palavras do tema escolhido
    erros = 0  # Reseta o número de erros
    acertos = 0  # Reseta o número de acertos
    escolher_palavra_secreta()  # Escolhe uma palavra secreta
    atualizar_palavra_secreta()  # Atualiza a palavra na tela
    criar_botoes_alfabeto()  # Cria os botões do alfabeto
    canvas.delete('boneco')  # Limpa o boneco da forca
    desenhar_forca()  # Desenha a forca inicial
    janela_tema.destroy()  # Fecha a janela de escolha de tema
    janela.deiconify()  # Mostra a janela principal após escolher o tema

# Função para abrir a janela de escolha de tema
def abrir_janela_tema():
    global janela_tema
    janela_tema = tk.Toplevel(janela)  # Cria uma nova janela
    janela_tema.title("Escolha o Tema")
    # Cria um botão para cada tema
    for tema in temas.keys():
        btn = tk.Button(janela_tema, text=tema, command=lambda t=tema: escolher_tema(t))
        btn.pack(pady=5)
    janela.withdraw()  # Esconde a janela principal até a escolha do tema

# Função para escolher a palavra secreta
def escolher_palavra_secreta():
    global palavra_secreta, letras_descobertas, indice_palavra
    # Se ainda houver palavras no tema, escolhe a próxima; senão, escolhe uma aleatória
    if indice_palavra < len(palavras):
        palavra_secreta = palavras[indice_palavra]
    else:
        palavra_secreta = random.choice(palavras)
    letras_descobertas = ['_' for _ in palavra_secreta]  # Inicia as letras descobertas com "_"

# Função para desenhar a forca
def desenhar_forca():
    canvas.delete('boneco')  # Limpa a forca anterior
    # Desenha a base da forca e outros elementos do desenho
    canvas.create_line(50, 250, 150, 250, width=2)
    canvas.create_line(100, 250, 100, 50, width=2)
    canvas.create_line(100, 50, 200, 50, width=2)
    canvas.create_line(200, 50, 200, 70, width=2)
    # Adiciona o corpo do boneco conforme o número de erros
    if erros >= 1:
        canvas.create_oval(180, 70, 220, 110, width=2, tags='boneco')
    if erros >= 2:
        canvas.create_line(200, 110, 200, 170, width=2, tags='boneco')
    if erros >= 3:
        canvas.create_line(200, 120, 170, 150, width=2, tags='boneco')
    if erros >= 4:
        canvas.create_line(200, 120, 230, 150, width=2, tags='boneco')
    if erros >= 5:
        canvas.create_line(200, 170, 180, 210, width=2, tags='boneco')
    if erros >= 6:
        canvas.create_line(200, 170, 220, 210, width=2, tags='boneco')
    if erros >= 7:
        canvas.create_line(190, 80, 195, 85, width=2, tags='boneco')
        canvas.create_line(195, 80, 190, 85, width=2, tags='boneco')
        canvas.create_line(205, 80, 210, 85, width=2, tags='boneco')
        canvas.create_line(210, 80, 205, 85, width=2, tags='boneco')

# Função para atualizar a palavra secreta na interface
def atualizar_palavra_secreta():
    lbl_palavra.config(text=' '.join(letras_descobertas))  # Exibe as letras descobertas

# Função para criar os botões do alfabeto
def criar_botoes_alfabeto():
    for widget in frame_botoes.winfo_children():
        widget.destroy()  # Limpa os botões anteriores
    keyboard_layout = ['qwertyuiop', 'asdfghjkl', 'zxcvbnm']  # Layout do teclado
    # Cria os botões para cada linha do teclado
    for row in keyboard_layout:
        frame_row = tk.Frame(frame_botoes)
        frame_row.pack()
        for letra in row:
            btn = tk.Button(frame_row, text=letra.upper(), width=4, command=lambda l=letra: escolher_letra(l))
            btn.pack(side='left', padx=2, pady=2)

# Função para lidar com a escolha de uma letra
def escolher_letra(letra):
    global erros, acertos, pontuacao
    acertou = False
    # Verifica se a letra escolhida está na palavra secreta
    for idx, char in enumerate(palavra_secreta):
        if char == letra:
            letras_descobertas[idx] = letra.upper()
            acertou = True
            acertos += 1
    atualizar_palavra_secreta()  # Atualiza a palavra na tela
    # Desabilita o botão de letra e altera a cor dependendo de acerto ou erro
    for frame in frame_botoes.winfo_children():
        for btn in frame.winfo_children():
            if btn['text'].lower() == letra:
                if acertou:
                    btn.config(state='disabled', bg='blue', fg='white')
                else:
                    btn.config(state='disabled', bg='gray')
                break
    if not acertou:
        erros += 1
        desenhar_forca()  # Desenha a forca a cada erro
    verificar_fim_de_jogo()  # Verifica se o jogo terminou

# Função para verificar se o jogo terminou
def verificar_fim_de_jogo():
    global pontuacao, indice_palavra
    # Verifica se o jogador perdeu
    if erros == max_erros:
        messagebox.showinfo('Jogo da Forca', 'Você perdeu! A palavra era: {}'.format(palavra_secreta.upper()))
        reiniciar_jogo_automatico()  # Reinicia o jogo automaticamente
        salvar_pontuacao()  # Salva a pontuação
    # Verifica se o jogador venceu
    elif acertos == len(palavra_secreta):
        messagebox.showinfo('Jogo da Forca', 'Você venceu!')
        pontuacao += 1
        indice_palavra += 1  # Avança para a próxima palavra
        lbl_pontuacao.config(text='Pontuação: {}'.format(pontuacao))
        salvar_pontuacao()  # Salva a pontuação
        reiniciar_jogo_automatico()  # Reinicia o jogo automaticamente

# Função para reiniciar o jogo automaticamente
def reiniciar_jogo_automatico():
    global erros, acertos
    erros = 0  # Reseta os erros
    acertos = 0  # Reseta os acertos
    escolher_palavra_secreta()  # Escolhe uma nova palavra secreta
    atualizar_palavra_secreta()  # Atualiza a palavra na tela
    criar_botoes_alfabeto()  # Cria os botões novamente
    canvas.delete('boneco')  # Limpa o boneco da forca
    desenhar_forca()  # Desenha a forca novamente

# Função para reiniciar o jogo manualmente
def reiniciar_jogo():
    reiniciar_jogo_automatico()  # Reinicia o jogo

# Função para salvar a pontuação no banco de dados
def salvar_pontuacao():
    with shelve.open('pontuacao_db') as db:
        db['pontuacao'] = pontuacao
        db['indice_palavra'] = indice_palavra

# Configuração da interface gráfica
janela = tk.Tk()
janela.title('Jogo da Forca')

lbl_pontuacao = tk.Label(janela, text='Pontuação: {}'.format(pontuacao), font=('Arial', 16))
lbl_pontuacao.pack(pady=10)

canvas = tk.Canvas(janela, width=300, height=300)
canvas.pack()

lbl_palavra = tk.Label(janela, text='', font=('Arial', 24))
lbl_palavra.pack(pady=10)

frame_botoes = tk.Frame(janela)
frame_botoes.pack()

btn_reiniciar = tk.Button(janela, text='Reiniciar Jogo', command=reiniciar_jogo)
btn_reiniciar.pack(pady=10)

abrir_janela_tema()  # Abre a janela de escolha de tema

janela.mainloop()  # Inicia o loop principal da interface gráfica
