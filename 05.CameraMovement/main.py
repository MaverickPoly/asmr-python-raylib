from pyray import *
from raylib import *
from random import randint, choice

WIDTH, HEIGHT = 1400, 900
PLAYER_W, PLAYER_H = 100, 100
SPEED = 600

init_window(WIDTH, HEIGHT, "Camera Movement")

circles = [
    (
        randint(-1000, 1000),
        randint(-1000, 1000),
        randint(10, 150),
        choice([RED, YELLOW, ORANGE, BLUE, GREEN, PURPLE, BROWN, PINK, GRAY])

    )
    for _ in range(100)
]

player = Rectangle(WIDTH / 2 - PLAYER_W / 2, HEIGHT / 2 - PLAYER_H / 2, PLAYER_W, PLAYER_H)
direction = Vector2()

camera = Camera2D()
camera.zoom = 1.0
camera.target.x = player.x
camera.target.y = player.y
camera.offset.x = player.x - player.width / 2
camera.offset.y = player.y - player.height / 2

while not window_should_close():
    # Updating
    camera.target.x = player.x
    camera.target.y = player.y
    
    direction.x = is_key_down(KEY_RIGHT) - is_key_down(KEY_LEFT)
    direction.y = is_key_down(KEY_DOWN) - is_key_down(KEY_UP)

    dt = get_frame_time()

    if is_key_down(KEY_M) and camera.zoom <= 4.0:
        camera.zoom += 0.5 * dt
    if is_key_down(KEY_N) and camera.zoom >= 0.1:
        camera.zoom -= 0.5 * dt

    player.x += direction.x * dt * SPEED
    player.y += direction.y * dt * SPEED
    
    # Drawing

    begin_drawing()
    begin_mode_2d(camera)
    clear_background(WHITE)

    for circle in circles:
        draw_circle(*circle)
    draw_rectangle_rec(player, BLACK)

    end_mode_2d()
    end_drawing()

close_window()
