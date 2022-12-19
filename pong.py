'''Dhruv Gupta

Classic twist on Pong video game

3.25.2020
'''

import random, pygame, sys, time
from pygame.locals import *
from Vector2 import Vector2
from random import randint

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BALL_SIZE = 20
BORDER_SIZE = 5

PADDLE_WIDTH = 20
PADDLE_HEIGHT = 80

PADDLE_SPEED = 250

GAME_OVER = 'game_over'
GAME_PLAY = 'game_play'
GAME_START = 'game_start'

WHITE = (255, 255, 255) 
BLACK = (0, 0, 0)

PLAYER1_START = (50, WINDOW_HEIGHT // 2 - PADDLE_HEIGHT // 2)
PLAYER2_START = (WINDOW_WIDTH - PADDLE_WIDTH - 50, WINDOW_HEIGHT // 2 - PADDLE_HEIGHT // 2)
BALL_START = (WINDOW_WIDTH // 2 - BALL_SIZE // 2, WINDOW_HEIGHT // 2 - BALL_SIZE // 2)
ball_x_change = 0
ball_y_change = 0


def main():
    global DISPLAY_SURF, pong_font, instructions_font, ball_x_change, ball_y_change
    
    pygame.init()
    
    game_state = GAME_START  

    player1 = pygame.Rect(*PLAYER1_START, PADDLE_WIDTH, PADDLE_HEIGHT)
    player2 = pygame.Rect(*PLAYER2_START, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = pygame.Rect(*BALL_START, BALL_SIZE, BALL_SIZE)
    
    player1_vector = Vector2()
    player2_vector = Vector2()
    ball_vector = Vector2()

    player1_score = 0
    player2_score = 0

    ball_speed = 250
    
    DISPLAY_SURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)
    pygame.display.set_caption("PONG")
    background = pygame.image.load('background.png')
    pong_font = pygame.font.Font('freesansbold.ttf', 40)
    instructions_font = pygame.font.Font('freesansbold.ttf', 24)
    score_font = pygame.font.Font('freesansbold.ttf', 18)
    clock = pygame.time.Clock()

    while True:
        DISPLAY_SURF.fill(BLACK)

        p1_score = score_font.render('Player 1: ' + str(player1_score),
                                            True, WHITE)
        p1_score_rect = p1_score.get_rect()
        p1_score_rect.center = (WINDOW_WIDTH//2 - 100, 75)

        p2_score = score_font.render('Player 2: ' + str(player2_score),
                                            True, WHITE)
        p2_score_rect = p2_score.get_rect()
        p2_score_rect.center = (WINDOW_WIDTH//2 + 100, 75)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_s:
                    player1_vector += Vector2(0, 1)
                    player1_vector.normalize()
                elif event.key == K_w:
                    player1_vector += Vector2(0, -1)
                    player1_vector.normalize()
                elif event.key == K_DOWN:
                    player2_vector += Vector2(0, 1)
                    player2_vector.normalize()
                elif event.key == K_UP:
                    player2_vector += Vector2(0, -1)
                    player2_vector.normalize()
          
            elif event.type == KEYUP:
                if event.key == K_s:
                    player1_vector -= Vector2(0, 1)
                    player1_vector.normalize()
                elif event.key == K_w:
                    player1_vector -= Vector2(0, -1)
                    player1_vector.normalize()
                elif event.key == K_DOWN:
                    player2_vector -= Vector2(0, 1)
                    player2_vector.normalize()
                elif event.key == K_UP:
                    player2_vector -= Vector2(0, -1)
                    player2_vector.normalize()

            elif event.type == MOUSEBUTTONUP:
                if game_state == GAME_START:
                    player1.topleft = PLAYER1_START
                    player2.topleft = PLAYER2_START
                    ball.topleft = BALL_START
                    game_state = GAME_PLAY
                    player1_score, player2_score = 0, 0
                    ball_vector = Vector2(1,0)
                    ball_speed = 250
                    clock.tick() #initial "snapshot" of time
                elif game_state == GAME_OVER:
                    game_state = GAME_START

        if game_state == GAME_START:
            display_pong_screen()

        if game_state == GAME_PLAY:
            DISPLAY_SURF.blit(background, (0,0))
            DISPLAY_SURF.blit(p1_score, p1_score_rect)
            DISPLAY_SURF.blit(p2_score, p2_score_rect)

            time_passed_seconds = clock.tick() / 1000
            player_distance = time_passed_seconds * PADDLE_SPEED 

            p1_y_change = int((player1_vector * player_distance).y)
            p2_y_change = int(player2_vector.y * player_distance)
            
            if player1.top + p1_y_change >= BORDER_SIZE and \
               player1.bottom + p1_y_change < WINDOW_HEIGHT - BORDER_SIZE:
                player1.top += p1_y_change
            if player2.top + p2_y_change >= BORDER_SIZE and \
               player2.bottom + p2_y_change < WINDOW_HEIGHT - BORDER_SIZE:
                player2.top = player2.top + p2_y_change

            #If ball currently colliding with paddle, change before moving x-value
            if ball.colliderect(player1) and ball_vector.x < 0:
                ball_speed += 25
                ball_vector.x *= -1
                player1_expanded = player1_vector * PADDLE_SPEED
                ball_expanded = ball_vector * ball_speed
                ball_vector = ball_expanded + player1_expanded
                ball_vector.normalize()
            elif ball.colliderect(player2) and ball_vector.x > 0:
                ball_speed += 25
                ball_vector.x *= -1
                player2_expanded = player2_vector * PADDLE_SPEED
                ball_expanded = ball_vector * ball_speed
                ball_vector = ball_expanded + player2_expanded
                ball_vector.normalize()
            
            #now let's get ready to move the ball
            ball_distance = time_passed_seconds * ball_speed

            ball_y_change = int(ball_vector.y * ball_distance)
            ball_x_change = int(ball_vector.x * ball_distance)

            ball.left = ball.left + ball_x_change

            #if the ball would collide with top or bottom -- go other way and invert y
            if ball.top + ball_y_change >= BORDER_SIZE and \
               ball.bottom + ball_y_change < WINDOW_HEIGHT - BORDER_SIZE:
                ball.top = ball.top + ball_y_change
            else:
                ball.top = ball.top - ball_y_change
                ball_vector.y *= -1

            #checking for a score
            if ball.left < 0:
                player2_score += 1
                player1.topleft = PLAYER1_START
                player2.topleft = PLAYER2_START
                ball.topleft = BALL_START
                ball_speed = 250
                time.sleep(2)
                clock.tick()
                ball_vector = Vector2(randint(50, 100), randint(20, 100))
                ball_vector.normalize()
                if randint(0, 1) == 1:
                    ball_vector.x *= -1
            if ball.right > WINDOW_WIDTH:
                player1_score += 1
                player1.topleft = PLAYER1_START
                player2.topleft = PLAYER2_START
                ball.topleft = BALL_START
                ball_speed = 250
                time.sleep(2)
                clock.tick()
                ball_vector = Vector2(randint(50, 100), randint(20, 100))
                ball_vector.normalize()
                if randint(0, 1) == 1:
                    ball_vector.x += -1

            if player2_score == 10:
                    game_state = GAME_OVER
                    winner = 'Player 2'
            elif player1_score == 10:
                    game_state = GAME_OVER
                    winner = 'Player 1'

            if game_state == GAME_OVER:
                DISPLAY_SURF.fill((0, 0, 0))

                winner_text = instructions_font.render(winner + ' wins!', True, WHITE)
                winner_rect = winner_text.get_rect()
                winner_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//3 - 50)

                game_over_text = pong_font.render("GAME OVER", True, WHITE)
                game_over_rect = game_over_text.get_rect()
                game_over_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//3 - 20)

                instructions = instructions_font.render('Click Mouse to Play', True, WHITE)
                instructions_rect = instructions.get_rect()
                instructions_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

                DISPLAY_SURF.blit(winner_text, winner_rect)
                DISPLAY_SURF.blit(game_over_text, game_over_rect)
                DISPLAY_SURF.blit(instructions, instructions_rect)

            #redraw the objects on the screen
            pygame.draw.rect(DISPLAY_SURF, WHITE, player1)
            pygame.draw.rect(DISPLAY_SURF, WHITE, player2)
            pygame.draw.rect(DISPLAY_SURF, WHITE, ball)

        pygame.display.update()


def display_pong_screen():    
    pong_text = pong_font.render("PONG", True, WHITE)
    pong_rect = pong_text.get_rect()
    pong_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//3 - 20)

    instructions = instructions_font.render('Click Mouse to Play', True, WHITE)
    instructions_rect = instructions.get_rect()
    instructions_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

    DISPLAY_SURF.blit(pong_text, pong_rect)
    DISPLAY_SURF.blit(instructions, instructions_rect)


if __name__ == '__main__':
    main()
