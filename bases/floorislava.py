import pygame
import sys
import random
import time

pygame.init()

# Configurações do jogo
WIDTH, HEIGHT = 800, 600  # Aumentando a proporção da tela
RED = (255, 0, 0)
GREEN = (0, 255, 0)
player_size = 50
lava_size = 100
player_position = [random.randint(0, WIDTH - player_size), random.randint(0, HEIGHT - player_size)]  # Posição inicial do jogador aleatória
lava_position = [random.randint(0, WIDTH - lava_size), random.randint(0, HEIGHT - lava_size)]  # Posição inicial da lava aleatória
clock = pygame.time.Clock()
level = 1
time_limit = 5  # Tempo limite para cada fase em segundos
game_time = 0  # Contador de tempo total do jogo
lava_time = 0  # Contador de tempo para o aparecimento da lava
lava_color = (196, 77, 77)  # Cor inicial da lava
lava_colors = [(190, 41, 41), (187, 11, 11), (162, 2, 2), (128, 0, 0)]  # Cores intermediárias da lava
lava_index = 0  # Índice da cor atual da lava
lava_delay = 5  # Tempo para a lava mudar de cor em segundos
lava_kill = False  # Indica se a lava pode matar o jogador
game_over = False
restart_game = False

screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Carregar a imagem da logo
logo = pygame.image.load('logo.jpeg')  # Substitua 'caminho/para/sua/imagem/logo.png' pelo caminho correto da sua imagem

# Obtendo as dimensões da tela
screen_width, screen_height = screen.get_size()

# Redimensionar a logo mantendo a proporção
aspect_ratio = logo.get_width() / logo.get_height()
new_width = int(screen_width * 0.5)  # Definindo a largura desejada para a logo
new_height = int(new_width / aspect_ratio)
logo = pygame.transform.scale(logo, (new_width, new_height))

# Posicionando a logo no centro da tela
logo_x = (screen_width - new_width) // 2
logo_y = (screen_height - new_height) // 2

show_logo = True
game_started = False

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)
    
# Loop para exibir a logo
while show_logo:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                show_logo = False
                game_started = True

    # Desenhar a logo na tela
    screen.blit(logo, (logo_x, logo_y))
    pygame.display.flip()

    clock.tick(60)

cont = time.time()
while not game_over:    
    time_now = time.time()

    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_position[0] -= 10  # Aumentando a velocidade do jogador
    if keys[pygame.K_RIGHT]:
        player_position[0] += 10
    if keys[pygame.K_UP]:
        player_position[1] -= 10
    if keys[pygame.K_DOWN]:
        player_position[1] += 10

    # Limitando o jogador dentro da tela
    if player_position[0] < 0:
        player_position[0] = 0
    if player_position[0] > WIDTH - player_size:
        player_position[0] = WIDTH - player_size
    if player_position[1] < 0:
        player_position[1] = 0
    if player_position[1] > HEIGHT - player_size:
        player_position[1] = HEIGHT - player_size

    # Desenhar o jogador
    pygame.draw.rect(screen, GREEN, (player_position[0], player_position[1], player_size, player_size))

    # Contadores de tempo
    game_time += clock.get_rawtime() / 1000  # Tempo total do jogo
    lava_time += clock.get_rawtime() / 1000  # Tempo para o aparecimento da lava
    
    
    # Verifica se é hora de aumentar a dificuldade
    if lava_time > time_limit:
        level += 1
        lava_time = 0
        lava_position = [random.randint(0, WIDTH - lava_size * level), random.randint(0, HEIGHT - lava_size * level)]  # Nova posição da lava aleatória
        lava_color = (196, 77, 77)  # Cor inicial da lava
        lava_index = 0  # Índice da cor atual da lava
        lava_kill = False  # Indica se a lava pode matar o jogador

    # Verifica se é hora de mudar a cor da lava
    if lava_time % lava_delay < 0.1 and lava_index < len(lava_colors):
        lava_color = lava_colors[lava_index]
        lava_index += 1
        if lava_index == len(lava_colors):  # Se a lava atingiu a cor máxima
            lava_kill = True  # A lava pode matar o jogador
            lava_time = time_limit - 2  # A lava vai desaparecer em 2 segundos

    # Desenhar a lava
    pygame.draw.rect(screen, lava_color, (lava_position[0], lava_position[1], lava_size * level, lava_size * level))

    # Verificar colisão com a lava
    if (player_position[0] < lava_position[0] + lava_size * level and
            player_position[0] + player_size > lava_position[0] and
            player_position[1] < lava_position[1] + lava_size * level and
            player_position[1] + player_size > lava_position[1]) and lava_kill:
        font = pygame.font.SysFont(None, 55)
        draw_text("Você foi pego pela lava! Pressione R para reiniciar.", font, (255, 255, 255), screen, WIDTH // 2 - 280, HEIGHT // 2)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            player_position = [random.randint(0, WIDTH - player_size), random.randint(0, HEIGHT - player_size)]  # Nova posição do jogador aleatória
            level = 1
            game_time = 0
            lava_time = 0
            lava_color = (196, 77, 77)  # Cor inicial da lava
            lava_index = 0  # Índice da cor atual da lava
            lava_kill = False  # Indica se a lava pode matar o jogador

    # Exibir contadores de tempo na tela
    
    font = pygame.font.SysFont(None, 35)
    draw_text(f"Tempo para a lava: {int(time_limit - lava_time)}s", font, (255, 255, 255), screen, 10, 10)
    draw_text(f"Tempo total: {int(game_time)}s", font, (255, 255, 255), screen, 10, 40)
    draw_text(f"Cont: {int((cont-time_now)%60)}s", font, (255, 255, 255), screen, 10, 80)
        
    if game_time >= 5 * time_limit:  # Exemplo de condição para finalizar o jogo após 5 fases
        restart_game = True
        break

    pygame.display.flip()
    clock.tick(60)

# Tela de parabéns ao terminar o jogo
while restart_game:
    screen.fill((0, 0, 0))
    draw_text("Parabéns, você concluiu o jogo!", pygame.font.SysFont(None, 60), (255, 255, 255), screen, WIDTH // 2 - 300, HEIGHT // 2 - 100)
    draw_text("Pressione R para reiniciar ou Q para sair.", pygame.font.SysFont(None, 40), (255, 255, 255), screen, WIDTH // 2 - 250, HEIGHT // 2 + 50)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_r]:
        restart_game = False
        game_over = False
        player_position = [random.randint(0, WIDTH - player_size), random.randint(0, HEIGHT - player_size)]  # Nova posição do jogador aleatória
        level = 1
        game_time = 0
        lava_time = 0
        lava_color = (196, 77, 77)  # Cor inicial da lava
        lava_index = 0  # Índice da cor atual da lava
        lava_kill = False  # Indica se a lava pode matar o jogador
    elif keys[pygame.K_q]:
        pygame.quit()
        sys.exit()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
