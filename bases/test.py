import pygame
import sys
import time

# Inicialização do Pygame
pygame.init()

# Configurações da janela
largura = 800
altura = 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Contador de Tempo')

# Cores
branco = (255, 255, 255)
preto = (0, 0, 0)

# Fonte
fonte = pygame.font.Font(None, 36)

# Função para exibir o tempo na tela
def mostrar_tempo(segundos):
    minutos = segundos // 60
    segundos_restantes = segundos % 60
    tempo_formatado = f'Tempo: {minutos} minutos e {segundos_restantes} segundos'
    texto = fonte.render(tempo_formatado, True, preto)
    tela.blit(texto, (10, 10))

# Função principal
def main():
    # Variáveis do contador de tempo
    tempo_inicial = time.time()
    segundos_passados = 0

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Lógica do contador de tempo
        tempo_atual = time.time()
        segundos_passados = int(tempo_atual - tempo_inicial)

        # Limpa a tela
        tela.fill(branco)

        # Exibe o tempo na tela
        mostrar_tempo(segundos_passados)

        # Atualiza a tela
        pygame.display.flip()

        # Controla a taxa de quadros por segundo
        pygame.time.Clock().tick(60)

if __name__ == "__main__":
    main()
