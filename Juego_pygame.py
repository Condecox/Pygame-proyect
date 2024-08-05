import pygame
import random
import sys

# Inicialización de Pygame
pygame.init()

# Constantes
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Configuración de la pantalla
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Resistencia espacial")

# Fondo del espacio
background = pygame.image.load('space_background.jpg')

# Cargar imágenes de enemigos y eliminar fondo blanco
enemy_images = [
    pygame.image.load('enemy.png').convert_alpha(),
    pygame.image.load('brick.png').convert_alpha(),
    pygame.image.load('meteor.png').convert_alpha()
]

# Redimensionar imágenes de enemigos
enemy_images = [pygame.transform.scale(img, (50, 50)) for img in enemy_images]

# Establecer color clave (transparencia) para eliminar fondo blanco
for img in enemy_images:
    img.set_colorkey(WHITE)

# Cargar imagen de vida
life_image = pygame.image.load('heart.jpg')
life_image = pygame.transform.scale(life_image, (30, 30))

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("player.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speed_x = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.speed_x = -5
        elif keys[pygame.K_d]:
            self.speed_x = 5
        else:
            self.speed_x = 0

        self.rect.x += self.speed_x

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = random.choice(enemy_images)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed_y = random.randint(1, 5)

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randint(-100, -40)
            self.speed_y = random.randint(1, 5)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 20))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed_y = -10

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.bottom < 0:
            self.kill()

def show_menu(screen):
    font = pygame.font.Font(None, 74)
    title = font.render("Resistencia espacial", True, WHITE)
    screen.fill(BLACK)
    screen.blit(title, (150, 100))

    font = pygame.font.Font(None, 36)
    options = ["1. Iniciar Juego", "2. Instrucciones", "3. Comandos", "4. Creditos"]
    for i, option in enumerate(options):
        text = font.render(option, True, WHITE)
        screen.blit(text, (150, 200 + i * 50))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    select_difficulty(screen)
                    waiting = False
                elif event.key == pygame.K_2:
                    show_instructions(screen)
                elif event.key == pygame.K_3:
                    show_commands(screen)
                elif event.key == pygame.K_4:
                    show_credits(screen)

def select_difficulty(screen):
    font = pygame.font.Font(None, 74)
    title = font.render("Seleccione la dificultad", True, WHITE)
    screen.fill(BLACK)
    screen.blit(title, (150, 100))

    font = pygame.font.Font(None, 36)
    options = ["1. Facil", "2. Dificil"]
    for i, option in enumerate(options):
        text = font.render(option, True, WHITE)
        screen.blit(text, (150, 200 + i * 50))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    main('Fácil')
                    waiting = False
                elif event.key == pygame.K_2:
                    main('Dificil')
                    waiting = False

def show_credits(screen):
    font = pygame.font.Font(None, 74)
    title = font.render("Credits", True, WHITE)
    screen.fill(BLACK)
    screen.blit(title, (150, 100))

    font = pygame.font.Font(None, 36)
    text = font.render("Creado por: Diego Chacon", True, WHITE)
    screen.blit(text, (150, 200))

    font = pygame.font.Font(None, 36)
    back_option = font.render("Presione M para regresar al menu", True, WHITE)
    screen.blit(back_option, (150, 300))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    show_menu(screen)
                    waiting = False

def show_instructions(screen):
    font = pygame.font.Font(None, 74)
    title = font.render("Instrucciones", True, WHITE)
    screen.fill(BLACK)
    screen.blit(title, (150, 100))

    font = pygame.font.Font(None, 36)
    instructions = [
        "Evita los enemigos y obstáculos.",
        "Dispara con la tecla SPACE.",
        "Muevete con A (izquierda) y D (derecha)."
    ]
    for i, instruction in enumerate(instructions):
        text = font.render(instruction, True, WHITE)
        screen.blit(text, (50, 200 + i * 50))

    font = pygame.font.Font(None, 36)
    back_option = font.render("Presione M para regresar al menu", True, WHITE)
    screen.blit(back_option, (150, 400))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    show_menu(screen)
                    waiting = False

def show_commands(screen):
    font = pygame.font.Font(None, 74)
    title = font.render("Comandos", True, WHITE)
    screen.fill(BLACK)
    screen.blit(title, (150, 100))

    font = pygame.font.Font(None, 36)
    commands = [
        "A: Moverse a la izquierda",
        "D: Moverse a la derecha",
        "SPACE: Disparar"
    ]
    for i, command in enumerate(commands):
        text = font.render(command, True, WHITE)
        screen.blit(text, (50, 200 + i * 50))

    font = pygame.font.Font(None, 36)
    back_option = font.render("Presione M para regresar al menu", True, WHITE)
    screen.blit(back_option, (150, 400))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    show_menu(screen)
                    waiting = False

def show_game_over(screen):
    font = pygame.font.Font(None, 74)
    title = font.render("Game Over", True, WHITE)
    screen.fill(BLACK)
    screen.blit(title, (150, 100))

    font = pygame.font.Font(None, 36)
    options = ["1. Volver a Empezar", "2. Menu Principal"]
    for i, option in enumerate(options):
        text = font.render(option, True, WHITE)
        screen.blit(text, (150, 200 + i * 50))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    select_difficulty(screen)
                    waiting = False
                elif event.key == pygame.K_2:
                    show_menu(screen)
                    waiting = False

# Función principal del juego
def main(difficulty):
    clock = pygame.time.Clock()
    
    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()

    player = Player()
    all_sprites.add(player)

    if difficulty == 'Fácil':
        num_enemies = 5
    else:
        num_enemies = 15
    
    for i in range(num_enemies):
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

    score = 0
    lives = 3

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet = Bullet(player.rect.centerx, player.rect.top)
                    all_sprites.add(bullet)
                    bullets.add(bullet)

        all_sprites.update()

        for bullet in bullets:
            hits = pygame.sprite.spritecollide(bullet, enemies, True)
            for hit in hits:
                all_sprites.remove(bullet)
                bullets.remove(bullet)
                score += 10
                enemy = Enemy()
                all_sprites.add(enemy)
                enemies.add(enemy)

        hits = pygame.sprite.spritecollide(player, enemies, True)
        for hit in hits:
            lives -= 1
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)
            if lives == 0:
                show_game_over(screen)
                running = False

        screen.blit(background, (0, 0))
        all_sprites.draw(screen)

        # Dibujar vidas restantes
        for i in range(lives):
            screen.blit(life_image, (10 + i * 35, 10))

        # Mostrar puntaje
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Puntaje: {score}", True, WHITE)
        screen.blit(score_text, (SCREEN_WIDTH - 150, 10))

        pygame.display.flip()

if __name__ == "__main__":
    show_menu(screen)
    pygame.quit()
