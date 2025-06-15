from raylib import *
from pyray import *
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRAVITY = 0.4
FLAP_STRENGTH = -10
PIPE_WIDTH = 80
PIPE_GAP = 200
PIPE_SPEED = 3

def check_collision(bird_y, pipes, bird_radius=20):
    bird_rect = Rectangle(SCREEN_WIDTH // 3 - bird_radius, bird_y - bird_radius, 
                            bird_radius * 2, bird_radius * 2)
    for pipe in pipes:
        top_pipe = Rectangle(pipe["x"], 0, PIPE_WIDTH, pipe["top_height"])
        bottom_pipe = Rectangle(pipe["x"], pipe["top_height"] + PIPE_GAP, 
                                  PIPE_WIDTH, SCREEN_HEIGHT)
        if (CheckCollisionRecs(bird_rect, top_pipe) or 
            CheckCollisionRecs(bird_rect, bottom_pipe)):
            return True
    return False

def main():
    InitWindow(SCREEN_WIDTH, SCREEN_HEIGHT, bytes("Flappy Bird".encode()))
    SetTargetFPS(60)

    bird_y = SCREEN_HEIGHT // 2
    bird_velocity = 0
    game_over = False
    score = 0
    pipes = []
    pipe_spawn_timer = 0

    while not WindowShouldClose():
        if not game_over:
            if IsKeyPressed(KEY_SPACE):
                bird_velocity = FLAP_STRENGTH
            bird_velocity += GRAVITY
            bird_y += bird_velocity

            pipe_spawn_timer += 1
            if pipe_spawn_timer >= 120:  # 2 seconds at 60 FPS
                pipe_height = random.randint(100, SCREEN_HEIGHT - PIPE_GAP - 100)
                pipes.append({"x": SCREEN_WIDTH, "top_height": pipe_height})
                pipe_spawn_timer = 0

            for pipe in pipes:
                pipe["x"] -= PIPE_SPEED

            for pipe in pipes[:]:
                if pipe["x"] < -PIPE_WIDTH:
                    pipes.remove(pipe)
                elif pipe["x"] + PIPE_WIDTH < SCREEN_WIDTH // 3 and not pipe.get("scored", False):
                    score += 1
                    pipe["scored"] = True

            if (bird_y >= SCREEN_HEIGHT or bird_y <= 0 or 
                check_collision(bird_y, pipes)):
                game_over = True

        if game_over and IsKeyPressed(KEY_R):
            bird_y = SCREEN_HEIGHT // 2
            bird_velocity = 0
            pipes = []
            score = 0
            game_over = False
            pipe_spawn_timer = 0

        BeginDrawing()
        ClearBackground(SKYBLUE)
        
        for pipe in pipes:
            DrawRectangle(pipe["x"], 0, PIPE_WIDTH, pipe["top_height"], GREEN)
            DrawRectangle(pipe["x"], pipe["top_height"] + PIPE_GAP, 
                            PIPE_WIDTH, SCREEN_HEIGHT, GREEN)

        DrawCircle(int(SCREEN_WIDTH // 3), int(bird_y), 20, YELLOW)
        
        draw_text (f"Score: {score}", 20, 20, 30, WHITE)
        
        if game_over:
            DrawText("GAME OVER", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 30, 40, RED)
            DrawText("Press R to restart", SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 30, 20, WHITE)

        EndDrawing()

    CloseWindow()

if __name__ == "__main__":
    main()