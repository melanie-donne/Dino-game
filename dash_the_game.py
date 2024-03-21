import pygame
import sys
import random

# Initialisation de Pygame
pygame.init()

# Paramètres de l'écran
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
GROUND_HEIGHT = 50
SCREEN_COLOR = (255, 255, 255)
GROUND_COLOR = (150, 150, 150)

# Paramètres du dinosaure
DINO_WIDTH = 60
DINO_HEIGHT = 60
DINO_JUMP_SPEED = 12         
DINO_GRAVITY = 0.5

# Paramètres des cactus
CACTUS_WIDTH = 30
CACTUS_HEIGHT = 50
CACTUS_SPEED = 4

# Paramètres de la police de caractères
FONT_SIZE = 36
FONT_COLOR = (255, 0, 0)

# Création de l'écran
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jeu du Dinosaure")

clock = pygame.time.Clock()

# Chargement des images
dino_img = pygame.image.load('dino.gif')
dino_img = pygame.transform.scale(dino_img, (DINO_WIDTH, DINO_HEIGHT))
cactus_img = pygame.image.load('bush.png')
cactus_img = pygame.transform.scale(cactus_img, (CACTUS_WIDTH, CACTUS_HEIGHT))

# Chargement de la police de caractères
font = pygame.font.Font(None, FONT_SIZE)

# Fonction pour afficher le message
def show_message(message):
    text = font.render(message, True, FONT_COLOR)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))

# Fonction pour afficher le bouton
def show_button():
    button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50, 200, 50)
    pygame.draw.rect(screen, (0, 0, 255), button_rect)
    text = font.render("Recommencer", True, (255, 255, 255))
    screen.blit(text, (button_rect.centerx - text.get_width() // 2, button_rect.centery - text.get_height() // 2))
    return button_rect

# Classe pour le dinosaure
class Dino(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = dino_img
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH // 4
        self.rect.y = SCREEN_HEIGHT - GROUND_HEIGHT - DINO_HEIGHT
        self.velocity = 0

    def jump(self):
        if self.rect.bottom == SCREEN_HEIGHT - GROUND_HEIGHT:
            self.velocity = -DINO_JUMP_SPEED

    def update(self):
        if self.rect.bottom < SCREEN_HEIGHT - GROUND_HEIGHT:
            self.velocity += DINO_GRAVITY
        self.rect.y += self.velocity
        if self.rect.bottom >= SCREEN_HEIGHT - GROUND_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT - GROUND_HEIGHT   
            self.velocity = 0

# Classe pour les cactus
class Cactus(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = cactus_img
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = SCREEN_HEIGHT - GROUND_HEIGHT - CACTUS_HEIGHT

    def update(self):
        self.rect.x -= CACTUS_SPEED

# Fonction pour le jeu
def run_game():
    dino = Dino()
    all_sprites = pygame.sprite.Group()
    cactuses = pygame.sprite.Group()

    all_sprites.add(dino)

    next_cactus_time = pygame.time.get_ticks() + random.randint(500, 1500)  # Intervalles aléatoires
    game_over = False
    retry_button_rect = None

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    dino.jump()
            elif event.type == pygame.MOUSEBUTTONDOWN and game_over:
                if retry_button_rect and retry_button_rect.collidepoint(event.pos):
                    run_game()

        # Génération des cactus
        if pygame.time.get_ticks() > next_cactus_time and not game_over:
            cactus = Cactus()
            all_sprites.add(cactus)
            cactuses.add(cactus)
            next_cactus_time = pygame.time.get_ticks() + random.randint(500, 1500)  # Nouvel intervalle aléatoire

        # Mise à jour de l'écran
        screen.fill(SCREEN_COLOR)
        pygame.draw.rect(screen, GROUND_COLOR, (0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT))

        all_sprites.update()
        all_sprites.draw(screen)

        # Vérification des collisions
        if pygame.sprite.spritecollide(dino, cactuses, False):
            game_over = True

        # Mise à jour du message de fin
        if game_over:
            show_message("Vous avez perdu")

            # Affichage du bouton "Recommencer"
            retry_button_rect = show_button()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

# Lancement du jeu
run_game()
