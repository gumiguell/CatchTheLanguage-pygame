import pygame
import random
import time
import easygui

# Configurações do jogo
LARGURA_TELA = 800
ALTURA_TELA = 600
FPS = 60

# Carrega as imagens
cesta_img = pygame.transform.scale(pygame.image.load('vscode.png'), (50, 50))
linguagem_imgs = [
    pygame.transform.scale(pygame.image.load('python.png'), (80, 50)),
    pygame.transform.scale(pygame.image.load('javascript.png'), (50, 50)),
    pygame.transform.scale(pygame.image.load('java.jpeg'), (80, 50)),
    pygame.transform.scale(pygame.image.load('csharp.png'), (50, 50)),
    pygame.transform.scale(pygame.image.load('c++.png'), (50, 50))
]

# Inicializa o Pygame
pygame.init()

# Cria a tela
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))


# Classe para a cesta (VSCode)
class Cesta(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = cesta_img
        self.rect = self.image.get_rect()
        self.rect.center = (LARGURA_TELA / 2, ALTURA_TELA - 50)

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        self.rect.x += self.speedx
        if self.rect.right > LARGURA_TELA:
            self.rect.right = LARGURA_TELA
        if self.rect.left < 0:
            self.rect.left = 0

# Classe para a linguagem (logos das linguagens de programação)
class Linguagem(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = random.choice(linguagem_imgs)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(LARGURA_TELA - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > ALTURA_TELA + 10:
            self.rect.x = random.randrange(LARGURA_TELA - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)

# Fonte para o texto na tela
fonte = pygame.font.Font(None, 36)
BRANCO = (255, 255, 255)

# Loop do jogo
jogar_novamente = True
while jogar_novamente:
    # Pergunta ao jogador quanto tempo ele quer jogar
    tempo_jogo = easygui.choicebox('Por quanto tempo você quer jogar?', 'Escolha o tempo de jogo', ['15 segundos', '30 segundos', '50 segundos'])
    if tempo_jogo is None:  # O usuário clicou em cancelar
        break
    elif tempo_jogo == '15 segundos':
        tempo_jogo = 15
    elif tempo_jogo == '30 segundos':
        tempo_jogo = 30
    elif tempo_jogo == '50 segundos':
        tempo_jogo = 50
    else:
        tempo_jogo = 30  # Valor padrão

    # Cria os grupos de sprites
    todos_sprites = pygame.sprite.Group()
    linguagens = pygame.sprite.Group()

    # Cria a cesta
    cesta = Cesta()
    todos_sprites.add(cesta)

    # Cria as linguagens
    for i in range(5):  # Reduzimos o número de linguagens para 5
        l = Linguagem()
        todos_sprites.add(l)
        linguagens.add(l)

    # Contador de linguagens
    contador_linguagens = 0

    # Tempo de início
    tempo_inicio = time.time()

    # Loop do jogo
    rodando = True
    clock = pygame.time.Clock()
    while rodando:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False
                jogar_novamente = False

        # Atualiza
        todos_sprites.update()

        # Verifica se a cesta pegou a linguagem
        colisoes = pygame.sprite.spritecollide(cesta, linguagens, True)
        for colisao in colisoes:
            l = Linguagem()
            todos_sprites.add(l)
            linguagens.add(l)
            contador_linguagens += 1  # Incrementa o contador de linguagens

        # Verifica se o tempo acabou
        if time.time() - tempo_inicio > tempo_jogo:  # Usa o tempo de jogo escolhido pelo jogador
            rodando = False

        # Desenha / renderiza
        tela.fill((0, 0, 0))
        todos_sprites.draw(tela)

        # Mostra o contador de tempo na tela
        tempo_restante = tempo_jogo - int(time.time() - tempo_inicio)
        texto_tempo = fonte.render(f'Tempo restante: {tempo_restante}', True, BRANCO)
        tela.blit(texto_tempo, (10, 10))

        # Mostra a quantidade de linguagens pegas na tela
        texto_linguagens = fonte.render(f'Linguagens pegas: {contador_linguagens}', True, BRANCO)
        tela.blit(texto_linguagens, (10, 50))

        # Depois de desenhar tudo, inverte o display
        pygame.display.flip()

    # Aguarda antes de sair
    pygame.time.wait(2000)

    # Pergunta ao jogador se ele quer jogar novamente
    jogar_novamente = easygui.ynbox('Você pegou ' + str(contador_linguagens) + ' linguagens em ' + str(tempo_jogo) + ' segundos! Você quer jogar novamente?', 'Fim do Jogo', ('Sim', 'Não'))

pygame.quit()
