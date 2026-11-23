from pico2d import get_canvas_width, load_image, draw_rectangle

import game_world
import game_framework

# 단위: 픽셀, 초
LAUNCH_SPEED_X = 300.0
LAUNCH_SPEED_Y = 300.0
GRAVITY = 9.8 * (10.0 / 0.3)  # 9.8 m/s²를 픽셀/s²로 변환
GROUND_Y = 40


class Ball:
    images = {}

    def __init__(self, x, y, direction, ball_type=1):
        if ball_type not in Ball.images:
            Ball.images[ball_type] = load_image(
                'ball21x21.png' if ball_type == 1 else 'ball41x41.png')
        self.image = Ball.images[ball_type]
        self.x, self.y = x, y
        self.velocity_x = direction * LAUNCH_SPEED_X
        self.velocity_y = LAUNCH_SPEED_Y
        self.radius = 10.5 if ball_type == 1 else 20.5
        self.stopped = (direction == 0)  # direction 이 0이면 바닥에 놓인 공

    def update(self):
        if self.stopped:
            return
        dt = game_framework.frame_time
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt - 0.5 * GRAVITY * dt ** 2
        self.velocity_y -= GRAVITY * dt
        if (self.x < -self.radius or self.x > get_canvas_width() + self.radius
                or self.y - self.radius <= GROUND_Y):
            game_world.remove_object(self)

    def draw(self):
        self.image.draw(self.x, self.y)
        draw_rectangle(*self.get_bb())  # 디버그용 바운딩 박스

    def get_bb(self):
        return (self.x - self.radius, self.y - self.radius,
                self.x + self.radius, self.y + self.radius)

    def get_bb(self):
        return self.x - self.radius, self.y - self.radius, self.x + self.radius, self.y + self.radius

    def handle_collision(self, collision_group, other):
        if collision_group == 'boy:ball':
            game_world.remove_object(self)
        if collision_group == 'grass:ball':
            self.stopped = True
            self.velocity_x = 0
            self.velocity_y = 0
            self.y = GROUND_Y + self.radius  # 공이 땅에 놓이도록 위치 조정