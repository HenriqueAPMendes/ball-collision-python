# ============================================================================== #
#                 Simulador de colisoes - Fisica 1                               #
# ============================================================================== #
#  Autor: Henrique Mendes                                                        #
# ============================================================================== #

from numpy import full, sqrt
import pygame
from pygame.locals import *
from random import randint

# Variáveis Globais
N_BOLAS = 200
RAIO = 15
COR = 0x040404
TELA = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
LARGURA, ALTURA = TELA.get_size()

pygame.init()

# Vetor referencia para cada bola e seus atributos
lista = []


class Bolas:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

# =========================================================================== #
            # Define matrizes posição e velocidade iniciais #

vel = full((2, N_BOLAS), 1)
pos = full((2, N_BOLAS), 1)

# Atualiza matriz velocidade para valores aleatórios
for i in range(2):
    for j in range(N_BOLAS):
        vel[i, j] = randint(-10, 10)

ncolunas = int(LARGURA/(3*RAIO))
nlinhas = int(ALTURA/(3*RAIO))

if ncolunas*nlinhas < N_BOLAS:
    print("Numero max de bolinhas excedido")
    exit(0)

# Define posições iniciais de todas as bolas de forma matricial #
# Ex: |o o o o o o o|
#     |o o o o o    |
#     |             |

i = 0
while i < N_BOLAS:
    j = 0
    while j < nlinhas and i < N_BOLAS:
        k = 0
        while k < ncolunas and i < N_BOLAS:
            pos[0, i] = (k+1)*(3*RAIO)
            pos[1, i] = (j+1)*(3*RAIO)
            i += 1
            k += 1
        j += 1
    i += 1


# ============================================================================ #
        # Funcoes que serao chamadas no loop principal do simulador #

def check_collision(o1, o2):
    dist_x = lista[o2].x - lista[o1].x
    dist_y = lista[o2].y - lista[o1].y
    distance = dist_x**2 + dist_y**2
    if distance < 4*RAIO*RAIO:
        return True
    return False


def draw(idx):
    pygame.draw.circle(TELA, COR, (lista[idx].x, lista[idx].y), RAIO)


# Retorna um vetor velocidade na direcao da colisao em suas componentes X e Y #
def proj(i1, i2):
    dx = lista[i2].x - lista[i1].x
    dy = lista[i2].y - lista[i1].y

    # Projeção ortogonal geometria analítica #
    v = (lista[i1].vx*dx + lista[i1].vy*dy) / (dx**2 + dy**2)
    vcol = [v * dx, v * dy]
    return vcol


def wall_collision(idx):
    if lista[idx].x <= RAIO and lista[idx].vx < 0:
        lista[idx].vx *= -1
    elif lista[idx].x >= LARGURA - RAIO and lista[idx].vx > 0:
        lista[idx].vx *= -1

    if lista[idx].y <= RAIO and lista[idx].vy < 0:
        lista[idx].vy *= -1
    elif lista[idx].y >= ALTURA - RAIO and lista[idx].vy > 0:
        lista[idx].vy *= -1


def atualiza_pos(i1):
    lista[i1].x += lista[i1].vx
    lista[i1].y += lista[i1].vy


# =============================================================================== #
            # Cria os objetos e as referências no vetor 'lista' #
for i in range(N_BOLAS):
    lista.append(Bolas(pos[0, i], pos[1, i], vel[0, i], vel[1, i]))


# =============================================================================== #
                    # Loop principal do simulador #
relogio = pygame.time.Clock()
while True:
    TELA.fill(0xAAAAAA)
    relogio.tick(60)

    for event in pygame.event.get():
        if event.type == QUIT:
            exit(0)

    LARGURA, ALTURA = TELA.get_size()

    # Calcula energia cinética a cada frame para verificar sua conservação
    ec = 0
    for i in range(N_BOLAS):
        ec += lista[i].vx**2 + lista[i].vy**2

    pygame.display.set_caption('K total = %s' % str(ec))

    # ======================================================================================== #
    # Chamada das funcoes para desenhar, checar colisao com a parede e atualizar suas posicoes #

    for i in range(N_BOLAS):
        draw(i)

    for i in range(N_BOLAS):
        wall_collision(i)

    for i in range(N_BOLAS):
        atualiza_pos(i)

    # ======================================================================================== #
                                 # Checar colisao entre bolinhas #

    for i in range(N_BOLAS-1):

        for j in range(i+1, N_BOLAS):
            if check_collision(i, j):
                v1col = proj(i, j)
                v2col = proj(j, i)

                # Para colisoes elasticas entre dois corpos de mesma massa:
                # v1f = v2i
                # v2f = v1i
                lista[i].vx += - v1col[0] + v2col[0]
                lista[i].vy += - v1col[1] + v2col[1]

                lista[j].vx += - v2col[0] + v1col[0]
                lista[j].vy += - v2col[1] + v1col[1]

                # Forçar saida de uma bola de dentro da outra manualmente
                atualiza_pos(i)
                atualiza_pos(j)
                while check_collision(i, j):
                    atualiza_pos(i)
                    atualiza_pos(j)

    pygame.display.update()
