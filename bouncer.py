import pygame
import pika

class Bouncer():
    def __init__(self, init_pos, width=60, height=10):
        self.pos = init_pos
        self.width = width
        self.height = height
        self.curr_rect = self.get_rect_from_pos()
        self.direction = 0

    def update(self):
        # TODO attraper le lapin
        if self.direction <= -1:
            self.pos = [self.pos[0] - 10, self.pos[1]]
        if self.direction >= 1:
            self.pos = [self.pos[0] + 10, self.pos[1]]
        return

    def move_left(self):
        self.direction -= 1
        if self.direction < -1:
            self.direction = -1

    def move_right(self):
        self.direction += 1
        if self.direction > 1:
            self.direction = 1


    def draw(self, surface):
        rects = [self.curr_rect]
        new_rect = self.get_rect_from_pos()
        pygame.draw.rect(surface, (255,255,255), self.curr_rect)
        rects.append(new_rect)
        self.curr_rect = new_rect
        pygame.draw.rect(surface, (0,0,0), self.curr_rect)
        return rects

    def check_collisions(self, ball):
        if self.curr_rect.colliderect(ball.curr_rect):
            self.send_message_bounce()
            ball.pos[1] -= 6 # Fix better

    def send_message_bounce(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(
                host='localhost'))
        channel = connection.channel()
        channel.exchange_declare(exchange='bounce',
                                 exchange_type='fanout')
        message = "1" # 1 for vertical, 0 for horizontal
        channel.basic_publish(exchange='bounce',
                              routing_key='',
                              body=message)
        return


    def get_rect_from_pos(self):
        return pygame.Rect(self.pos[0] - self.width / 2, self.pos[1] - self.height / 2, \
                           self.width, self.height)