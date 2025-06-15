from raylib import *
from pyray import *
from settings import *

from player import Player
from meteor import Meteor
from laser import Laser

import time
from random import randint, choice
import os


class Game:
    def __init__(self):
        init_window(WIDTH, HEIGHT, TITLE)
        init_audio_device()

        self.player = Player()
        self.meteors: list[Meteor] = []
        self.lasers: list[Laser] = []

        self.last_spawn = time.time()
        self.lives = 3
        self.score = time.time()

        self.game_music = load_sound(os.path.join("07.SpaceShooter", "audio", "game_music.wav"))
        self.shoot_sound = load_sound(os.path.join("07.SpaceShooter", "audio", "laser.wav"))
        self.explosion_sound = load_sound(os.path.join("07.SpaceShooter", "audio", "explosion.wav"))
        self.damage_sound = load_sound(os.path.join("07.SpaceShooter", "audio", "damage.ogg"))

        play_sound(self.game_music)

        self.run()

    def spawn_meteor(self):
        x = randint(0, WIDTH)
        y = randint(-200, -50)
        direction = Vector2(randint(-1, 1), 1)
        speed = randint(300, 800)
        rotation = randint(0, 360)
        meteor = Meteor(x, y, direction, speed, rotation)
        self.meteors.append(meteor)

    def draw_meteors(self):
        # Draw
        for meteor in self.meteors:
            meteor.update()
            meteor.draw()

        # Destroy if too below
        meteors = []
        for m in self.meteors:
            if not m.pos.y >= HEIGHT:
                meteors.append(m)
        self.meteors = meteors[:]

        # Player Collide with it
        for m in self.meteors:
            rec_m = Rectangle(m.pos.x, m.pos.y, m.texture.width, m.texture.height)
            rec_player = Rectangle(self.player.pos.x, self.player.pos.y, self.player.texture.width, self.player.texture.height)
            if check_collision_recs(rec_m, rec_player):
                self.meteors.remove(m)
                self.lives -= 1
                play_sound(self.damage_sound)
                break
        
        if self.lives <= 0:
            close_window()
                
    def draw_lasers(self):
        # Span Laser - Shoot
        if is_key_pressed(KEY_SPACE):
            x, y = self.player.pos.x + self.player.texture.width / 2 - 5, self.player.pos.y - 10
            laser = Laser(x, y)
            self.lasers.append(laser)
            play_sound(self.shoot_sound)

        # Draw
        for laser in self.lasers:
            laser.update()
            laser.draw()

        # Too Up - Destroy
        lasers = []
        for l in self.lasers:
            if not l.pos.y <= -100:
                lasers.append(l)
        self.lasers = lasers[:]

        # Collide with meteor
        for m in self.meteors:
            for l in self.lasers:
                rec_m = Rectangle(m.pos.x, m.pos.y, m.texture.width, m.texture.height)
                rec_l = Rectangle(l.pos.x, l.pos.y, l.texture.width, l.texture.height)
                if check_collision_recs(rec_m, rec_l):
                    self.meteors.remove(m)
                    self.lasers.remove(l)
                    play_sound(self.explosion_sound)
                    return
                
    def draw_texts(self):
        draw_text(f"Lives: {self.lives}", 10, 10, 36, WHITE)
        draw_text(f"Score: {int((time.time() - self.score) * 10)}", WIDTH - 250, 10, 36, WHITE)

    def run(self):
        while not window_should_close():
            begin_drawing()

            clear_background(BLACK)

            self.player.update()
            self.player.draw()

            if time.time() - self.last_spawn >= METEOR_SPAWN_DURATION:
                self.spawn_meteor()
                self.last_spawn = time.time()

            self.draw_meteors()
            self.draw_lasers()
            self.draw_texts()

            end_drawing()
        
        unload_sound(self.game_music)
        unload_sound(self.shoot_sound)
        unload_sound(self.explosion_sound)
        unload_sound(self.damage_sound)
        close_audio_device()
        close_window()


if __name__ == "__main__":
    game = Game()
