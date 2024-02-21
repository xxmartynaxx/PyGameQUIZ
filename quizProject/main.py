import pygame, sys, time
from pygame.locals import *
from script import show_rules, question_num_screen, show_question, timer, correct_answer, show_score, \
                   choose_version, game_continue, starting_window
from script import WINDOW, fpsClock, FPS, YES_BUTTON, SHORT_VER, MEDIUM_VER, LONG_VER, CLICK_SOUND

pygame.init()


def main(CHOICE):

    index = 0
    score = 0
    GAME_BEGAN = False

    while True:

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN:
                if event.key == K_q:
                    pygame.quit()
                    sys.exit()

            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1 and YES_BUTTON.collidepoint(event.pos):
                    CLICK_SOUND.play()
                    WINDOW.fill('black')
                    CHOICE = True
                if event.button == 1 and SHORT_VER.collidepoint(event.pos):
                    NUM_OF_QUESTIONS = 10
                    index, GAME_BEGAN = starting_window()
                elif event.button == 1 and MEDIUM_VER.collidepoint(event.pos):
                    NUM_OF_QUESTIONS = 15
                    index, GAME_BEGAN = starting_window()
                elif event.button == 1 and LONG_VER.collidepoint(event.pos):
                    NUM_OF_QUESTIONS = 20
                    index, GAME_BEGAN = starting_window()

        if CHOICE:
            choose_version()
            CHOICE = False

        if GAME_BEGAN:
            question_num_screen(index)
            show_question(index)

            screen_look = WINDOW.copy()

            index, user_answer = timer(index)
            time.sleep(1)

            score = correct_answer(index-1, user_answer, screen_look, score)

            if index == NUM_OF_QUESTIONS:
                WINDOW.fill('black')
                pygame.display.update()
                show_score(score, NUM_OF_QUESTIONS)
                break

        pygame.display.update()
        fpsClock.tick(FPS)


"""main program"""
WINDOW.fill('black')
show_rules()
main(CHOICE=False)
while True:
    if game_continue():
        WINDOW.fill('black')
        pygame.display.update()
        main(CHOICE=True)
