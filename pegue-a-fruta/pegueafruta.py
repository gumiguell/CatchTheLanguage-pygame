import pygame
import random
import time
import easygui  # Adicione esta linha

# Configurações do jogo
LARGURA_TELA = 800
ALTURA_TELA = 600
FPS = 60

# Cores
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
AMARELO = (255, 255, 0)
CORES = [VERMELHO, AZUL, VERDE, AMARELO]

# Inicializa o Pygame
pygame.init()

# Cria a tela
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))

# Classe para a cesta
class Cesta(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill(VERMELHO)
        self.rect = self.image.get_rect()
        self.rect.center = (LARGURA_TELA / 2, ALTURA_TELA - 50)

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8  # Aumentamos a velocidade do jogador
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8  # Aumentamos a velocidade do jogador
        self.rect.x += self.speedx
        if self.rect.right > LARGURA_TELA:
            self.rect.right = LARGURA_TELA
        if self.rect.left < 0:
            self.rect.left = 0

# Classe para a fruta
class Fruta(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 30))
        self.image.fill(random.choice(CORES))  # As frutas agora têm cores diferentes
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

# Loop do jogo
jogar_novamente = True
while jogar_novamente:
    # Cria os grupos de sprites
    todos_sprites = pygame.sprite.Group()
    frutas = pygame.sprite.Group()

    # Cria a cesta
    cesta = Cesta()
    todos_sprites.add(cesta)

    # Cria as frutas
    for i in range(5):  # Reduzimos o número de frutas para 5
        f = Fruta()
        todos_sprites.add(f)
        frutas.add(f)

    # Contador de frutas
    contador_frutas = 0

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

        # Verifica se a cesta pegou a fruta
        colisoes = pygame.sprite.spritecollide(cesta, frutas, True)
        for colisao in colisoes:
            f = Fruta()
            todos_sprites.add(f)
            frutas.add(f)
            contador_frutas += 1  # Incrementa o contador de frutas

        # Verifica se o tempo acabou
        if time.time() - tempo_inicio > 30:  # 30 segundos
            rodando = False

        # Desenha / renderiza
        tela.fill((0, 0, 0))
        todos_sprites.draw(tela)

        # Mostra o contador de tempo na tela
        tempo_restante = 30 - int(time.time() - tempo_inicio)
        texto_tempo = fonte.render(f'Tempo restante: {tempo_restante}', True, BRANCO)
        tela.blit(texto_tempo, (10, 10))

        # Mostra a quantidade de frutas pegas na tela
        texto_frutas = fonte.render(f'Frutas pegas: {contador_frutas}', True, BRANCO)
        tela.blit(texto_frutas, (10, 50))

        # Depois de desenhar tudo, inverte o display
        pygame.display.flip()


    pygame.display.flip()

    # Aguarda antes de sair
    pygame.time.wait(2000)

    # Pergunta ao jogador se ele quer jogar novamente e pontuação
    jogar_novamente = easygui.ynbox('Você pegou ' + str(contador_frutas) + ' frutas em 30 segundos! Você quer jogar novamente?', 'Fim do Jogo', ('Sim', 'Não'))

pygame.quit()
