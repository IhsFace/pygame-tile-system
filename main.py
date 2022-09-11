import pygame
import sys


class Player(): # usually a class should be in another file for organisation, which is why it has parameters
    def __init__(self, pos, tile_size):
        self.display = pygame.display.get_surface()
        self.image = pygame.Surface((tile_size, tile_size))
        self.rect = self.image.get_rect(center=pos)
        self.moving_left = False
        self.moving_right = False
        self.speed = 3
        self.gravity = 0

    def tile_collision_test(self, tiles):
        hit_list = []
        for tile in tiles:
            if self.rect.colliderect(tile):
                hit_list.append(tile)
        return hit_list

    def move(self, tiles):
        self.movement = pygame.math.Vector2(0, 0)
        if self.moving_left:
            self.movement.x -= self.speed
        if self.moving_right:
            self.movement.x += self.speed
        self.movement.y += self.gravity
        self.gravity += 0.5
        if self.gravity > 4:
            self.gravity = 4
        self.rect.x += self.movement.x
        hit_list = self.tile_collision_test(tiles)
        for tile in hit_list:
            if self.movement.x > 0:
                self.rect.right = tile.left
            elif self.movement.x < 0:
                self.rect.left = tile.right
        self.rect.y += self.movement.y
        hit_list = self.tile_collision_test(tiles)
        for tile in hit_list:
            if self.movement.y > 0:
                self.rect.bottom = tile.top
                self.gravity = 0
            elif self.movement.y < 0:
                self.rect.top = tile.bottom
                self.gravity = 0
        return self.rect

    def update(self, tiles, scroll):
        self.rect = self.move(tiles)
        self.display.blit(
            self.image, (self.rect.x - scroll.x, self.rect.y - scroll.y))


def draw_text(text, size, color, surface, pos):
    font = pygame.font.Font('assets/PressStart2P-Regular.ttf', size)
    text_render = font.render(text, True, color)
    text_rect = text_render.get_rect()
    text_rect.center = pos
    display.blit(text_render, text_rect)


def load_map(path):
    with open(f'{path}.txt', 'r') as f:
        data = f.read()
        data = data.split('\n')
        game_map = []
        for row in data:
            game_map.append(list(row))
        return game_map


def render_map(path, tiles):
    game_map = load_map(path)
    for y, row in enumerate(game_map):
        for x, tile in enumerate(row):
            if tile == '1':
                dirt_image = pygame.Surface((tile_size, tile_size))
                dirt_image.fill((100, 50, 50))
                display.blit(dirt_image, (x * tile_size -
                             scroll.x, y * tile_size - scroll.y))
                tiles.append(pygame.Rect(
                    x * tile_size, y * tile_size, tile_size, tile_size))
            if tile == '2':
                grass_image = pygame.Surface((tile_size, tile_size))
                grass_image.fill((0, 255, 0))
                display.blit(grass_image, (x * tile_size -
                             scroll.x, y * tile_size - scroll.y))
                tiles.append(pygame.Rect(
                    x * tile_size, y * tile_size, tile_size, tile_size))


def game():
    while True:
        tile_rects = []

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    if player.air_timer < 2:
                        player.gravity = -8
                if event.key == pygame.K_a:
                    player.moving_left = True
                if event.key == pygame.K_d:
                    player.moving_right = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    player.moving_left = False
                if event.key == pygame.K_d:
                    player.moving_right = False

        display.fill((146, 244, 255))

        pygame.draw.rect(display, (5, 80, 75), pygame.Rect(
            0, (window_size.y // 2), window_size.x, (window_size.y // 2)))

        scroll.x += (player.rect.x - scroll.x -
                     (window_size.x // 2) + (player.rect.width // 2)) // 20
        scroll.y += (player.rect.y - scroll.y -
                     (window_size.y // 2) + (player.rect.width // 2)) // 20

        render_map('map', tile_rects)

        player.update(tile_rects, scroll)

        draw_text(f'FPS: {str(int(clock.get_fps()))}', 16, (255, 255,
                  255), display, (window_size.x // 2, (window_size.y - 25)))

        pygame.display.update()
        clock.tick(60)


pygame.init()
pygame.display.set_caption('Mining Sim')
window_size = pygame.math.Vector2(600, 400)
display = pygame.display.set_mode(window_size)
clock = pygame.time.Clock()

tile_size = 32

scroll = pygame.math.Vector2(0, 0)

player = Player(pygame.math.Vector2(100, 100), tile_size)

if __name__ == '__main__':
    game_state = game()
