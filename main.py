import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Automatically get your phone's screen size
info = pygame.display.Info()
WIDTH = info.current_w
HEIGHT = info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Biking Game")

# Colors
GREEN = (34, 139, 34)
ROAD_GRAY = (80, 80, 80)
WHITE = (255, 255, 255)
BLUE = (0, 120, 255)
RED = (200, 30, 30)
BLACK = (0, 0, 0)

# Clock and FPS
clock = pygame.time.Clock()
FPS = 60

# Center the road on the phone screen
ROAD_WIDTH = min(450, WIDTH - 40)
road_x = (WIDTH - ROAD_WIDTH) // 2

# Player (Biker) Setup
player_width = 30
player_height = 50
player_x = road_x + ROAD_WIDTH // 2 - player_width // 2
player_y = HEIGHT - 180
player_speed = 8

# Obstacles Setup
obstacle_width = 40
obstacle_height = 40
obstacle_speed = 6
obstacles = []
SPAWNEVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWNEVENT, 900)  # Spawn a new rock every 0.9 seconds

# Score and Font
score = 0
font = pygame.font.SysFont(None, 40)

def draw_biker(x, y):
    # Draw simple bike body & rider
    pygame.draw.rect(screen, BLUE, (x, y + 10, player_width, 30))  # Body
    pygame.draw.circle(screen, BLACK, (x + 5, y + 45), 8)        # Back wheel
    pygame.draw.circle(screen, BLACK, (x + player_width - 5, y + 45), 8) # Front wheel
    pygame.draw.circle(screen, WHITE, (x + player_width // 2, y + 5), 8) # Helmet

def show_game_over():
    screen.fill(BLACK)
    over_text = font.render("GAME OVER", True, RED)
    score_text = font.render(f"Final Score: {score}", True, WHITE)
    restart_text = font.render("Tap screen to restart", True, WHITE)
    
    screen.blit(over_text, (WIDTH // 2 - over_text.get_width() // 2, HEIGHT // 2 - 60))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 60))
    pygame.display.flip()

# Main Game Loop
running = True
game_over = False

while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == SPAWNEVENT and not game_over:
            # Spawn new obstacle inside the road boundaries
            obs_x = random.randint(road_x + 10, road_x + ROAD_WIDTH - 10 - obstacle_width)
            obstacles.append(pygame.Rect(obs_x, -obstacle_height, obstacle_width, obstacle_height))
            
        if game_over and event.type == pygame.MOUSEBUTTONDOWN:
            # Reset game on tap after game over
            game_over = False
            obstacles.clear()
            score = 0
            player_x = road_x + ROAD_WIDTH // 2 - player_width // 2

    if not game_over:
        # Touch controls (Left half of screen = move left, Right half = move right)
        mouse_pressed = pygame.mouse.get_pressed()
        keys = pygame.key.get_pressed()

        if mouse_pressed[0]:  # Screen touched
            touch_x, _ = pygame.mouse.get_pos()
            if touch_x < WIDTH // 2 and player_x > road_x + 5:
                player_x -= player_speed
            elif touch_x >= WIDTH // 2 and player_x < road_x + ROAD_WIDTH - 5 - player_width:
                player_x += player_speed
                
        # Keyboard controls support
        if keys[pygame.K_LEFT] and player_x > road_x + 5:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < road_x + ROAD_WIDTH - 5 - player_width:
            player_x += player_speed

        # Move obstacles down
        for obs in obstacles[:]:
            obs.y += obstacle_speed
            if obs.y > HEIGHT:
                obstacles.remove(obs)
                score += 10  # Increase score for dodging

        # Collision detection
        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
        for obs in obstacles:
            if player_rect.colliderect(obs):
                game_over = True

        # Draw Background (Grass & Centered Road)
        screen.fill(GREEN)
        pygame.draw.rect(screen, ROAD_GRAY, (road_x, 0, ROAD_WIDTH, HEIGHT))
        
        # Draw Road Lines
        pygame.draw.line(screen, WHITE, (road_x, 0), (road_x, HEIGHT), 6)
        pygame.draw.line(screen, WHITE, (road_x + ROAD_WIDTH, 0), (road_x + ROAD_WIDTH, HEIGHT), 6)

        # Draw Player & Obstacles
        draw_biker(player_x, player_y)
        for obs in obstacles:
            pygame.draw.rect(screen, RED, obs, border_radius=6)

        # Draw Score
        score_surface = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_surface, (30, 30))

        pygame.display.flip()
    else:
        show_game_over()

pygame.quit()
sys.exit()
