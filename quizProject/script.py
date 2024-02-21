import sys, random
import pygame
from pygame.locals import *
from pygame import *
import time
from classes import questions
mixer.init()

FPS = 60
fpsClock = pygame.time.Clock()
WINDOW_WIDTH = 700
WINDOW_HEIGHT = 600

YES_BUTTON = pygame.Rect(WINDOW_WIDTH - 130, WINDOW_HEIGHT - 70, 110, 50)
SHORT_VER = pygame.Rect(25, WINDOW_HEIGHT//2 + 20, 140, 70)
MEDIUM_VER = pygame.Rect(270, WINDOW_HEIGHT//2 + 20, 150, 70)
LONG_VER = pygame.Rect(535, WINDOW_HEIGHT//2 + 20, 140, 70)
START_BUTTON = pygame.Rect(100, WINDOW_HEIGHT//2, 140, 70)
QUIT_BUTTON = pygame.Rect(460, WINDOW_HEIGHT//2, 140, 70)

CLICK_SOUND = pygame.mixer.Sound('sounds/click.mp3')
QUESTION_SOUND = pygame.mixer.Sound('sounds/next_question.mp3')
SCORE_SOUND = pygame.mixer.Sound('sounds/score.mp3')
TIME_SOUND = pygame.mixer.Sound('sounds/timer.mp3')

WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('*** QUIZ GAME ***')

# [index_of_the_answer, the_height_of_the_text]
ans_nums = {
    'a': [0, 140],
    'b': [1, 190],
    'c': [2, 240],
    'd': [3, 290]
    }


def read_text_from_file(file_name):
    """unused function but seems cool"""
    with open(file_name, 'r', encoding='utf-8') as file:
        return file.read()


def write_wrapped(text, font, colour, height, sleep_seconds):
    """function for writing the wrapped text"""
    _, lower = font.size(text[0])
    for element in text:
        text = font.render(element, True, colour)
        WINDOW.blit(text, [20, height])
        height += lower
    pygame.display.update()
    time.sleep(sleep_seconds)


def wrapped_text(text, font):
    """text wrapping function"""
    words = text.split()
    lines = []
    current_line = words[0]

    for word in words[1:]:
        help_len = len(word)
        test_line = current_line + " " + word
        test_width, _ = font.size(test_line)
        # font.size(test_line) returns two values: width and height of the area occupied by the given text
        # here test_width represents the width and the _ means that we won't use the height

        if test_width <= WINDOW_WIDTH - 20:
            current_line = test_line
        else:
            test_line = test_line[:len(test_line)-help_len-1]
            lines.append(test_line)
            current_line = word

    lines.append(current_line)
    return lines


def show_rules():
    hello_font = pygame.font.SysFont('georgia', 40, False, False)
    hello_font.set_underline(True)
    font = pygame.font.SysFont('georgia', 30, False, False)
    rule_font = pygame.font.SysFont('georgia', 25, False, False)

    hello_text = wrapped_text("Welcome to the ultimate quiz game!", hello_font)
    rules_text = wrapped_text("I want you, Player, to read some basic rules before you start. Let's go!", font)
    rule_1 = wrapped_text("1. You have only 10 seconds to answer the question", rule_font)
    rule_2 = wrapped_text("2. There is only ONE correct answer", rule_font)
    rule_3 = wrapped_text("3. To choose the answer press a, b, c or d", rule_font)
    rule_4 = wrapped_text("4. If you don't know the answer - press n - the next question will appear", rule_font)
    rule_5 = wrapped_text("5. You cannot go back to the previous question, so think wisely", rule_font)
    rule_6 = wrapped_text("6. If you want to quit - press q", rule_font)
    rules_end = wrapped_text("You see - it is not complicated. If you are ready, press START. Good luck Player!", font)

    write_wrapped(hello_text, hello_font, 'whitesmoke', 20, 2)
    write_wrapped(rules_text, font, 'whitesmoke', 100, 0)
    write_wrapped(rule_1, rule_font, 'lightcoral', 185, 0)
    write_wrapped(rule_2, rule_font, 'burlywood', 220, 0)
    write_wrapped(rule_3, rule_font, 'khaki2', 255, 0)
    write_wrapped(rule_4, rule_font, 'lightgreen', 290, 0)
    write_wrapped(rule_5, rule_font, 'aquamarine3', 355, 0)
    write_wrapped(rule_6, rule_font, 'mediumpurple2', 420, 0)
    write_wrapped(rules_end, font, 'whitesmoke', 465, 0)

    pygame.draw.rect(WINDOW, 'whitesmoke', YES_BUTTON, 1)
    yes_text = font.render("START", True, 'mediumpurple2')
    WINDOW.blit(yes_text, yes_text.get_rect(center=YES_BUTTON.center))


def choose_version():
    random.shuffle(questions)

    title_font = pygame.font.SysFont('georgia', 60, False, False)
    font = pygame.font.SysFont('georgia', 30, False, False)

    choice = wrapped_text("Choose the game version", title_font)
    text = wrapped_text("The short, medium and long versions have 10, 15 and 20 questions respectively. \
    What challenge will you take up?", font)

    write_wrapped(choice, title_font, 'whitesmoke', 20, 0)
    write_wrapped(text, font, 'whitesmoke', 100, 0)

    short_text = font.render("SHORT", True, 'lightgreen')
    med_text = font.render("MEDIUM", True, 'aquamarine3')
    long_text = font.render("LONG", True, 'mediumpurple2')

    pygame.draw.rect(WINDOW, 'whitesmoke', SHORT_VER, 1)
    pygame.draw.rect(WINDOW, 'whitesmoke', MEDIUM_VER, 1)
    pygame.draw.rect(WINDOW, 'whitesmoke', LONG_VER, 1)

    WINDOW.blit(short_text, short_text.get_rect(center=SHORT_VER.center))
    WINDOW.blit(med_text, med_text.get_rect(center=MEDIUM_VER.center))
    WINDOW.blit(long_text, long_text.get_rect(center=LONG_VER.center))


def question_num_screen(number):
    font = pygame.font.SysFont('georgia', 60, False, True)
    text = font.render(f'Question {number+1}', True, 'grey85')

    QUESTION_SOUND.play()
    WINDOW.blit(text, [WINDOW_WIDTH/2 - 145, WINDOW_HEIGHT/2 - 40])
    pygame.display.update()
    time.sleep(2)
    WINDOW.fill('black')
    pygame.display.update()


def show_question(number):
    font = pygame.font.SysFont('georgia', 44, False, False)
    font.set_underline(True)
    contests = wrapped_text(questions[number].question, font)
    write_wrapped(contests, font, 'grey85', 20, 2)
    show_answers(number)


def show_answers(number):
    font = pygame.font.SysFont('georgia', 35)

    answer_a = wrapped_text(questions[number].options[0], font)
    answer_b = wrapped_text(questions[number].options[1], font)
    answer_c = wrapped_text(questions[number].options[2], font)
    answer_d = wrapped_text(questions[number].options[3], font)

    write_wrapped(answer_a, font, 'grey85', 140, 1)
    write_wrapped(answer_b, font, 'grey85', 190, 1)
    write_wrapped(answer_c, font, 'grey85', 240, 1)
    write_wrapped(answer_d, font, 'grey85', 290, 1)


def correct_answer(number, user_answer, screen_look, score):
    font = pygame.font.SysFont('georgia', 35)
    correct = (questions[number].answer.lower()).strip()  # it is the letter a, b, c or d
    WINDOW.blit(screen_look, (0, 0))

    if correct != user_answer and user_answer != 'x':
        user_option = ans_nums[user_answer][0]
        height = ans_nums[user_answer][1]
        red_text = wrapped_text(questions[number].options[user_option], font)
        write_wrapped(red_text, font, 'dark red', height, 0)

    if correct == user_answer:
        score += 1

    correct_option = ans_nums[correct][0]
    correct_height = ans_nums[correct][1]
    green_text = wrapped_text(questions[number].options[correct_option], font)
    write_wrapped(green_text, font, 'mediumseagreen', correct_height, 0)

    time.sleep(2)
    WINDOW.fill('black')
    return score


def timer(index):
    font = pygame.font.SysFont('georgia', 45, False, True)
    screen_look = WINDOW.copy()
    PAUSED = False
    user_answer = 'x'

    for i in range(10, -1, -1):
        TIME_SOUND.play()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_q:
                    pygame.quit()
                    sys.exit()
                elif event.key == K_n:
                    PAUSED = True
                elif event.key in [K_a, K_b, K_c, K_d]:
                    PAUSED = True
                    user_answer = chr(event.key)

        if not PAUSED:
            WINDOW.blit(screen_look, (0, 0))
            sec = font.render(str(i), True, 'grey85')
            WINDOW.blit(sec, [WINDOW_WIDTH-80, WINDOW_HEIGHT-80])
        else:
            TIME_SOUND.stop()
            break

        pygame.display.update()
        time.sleep(1)

    TIME_SOUND.stop()
    WINDOW.fill('black')
    index += 1
    return index, user_answer


def show_score(score, NUM_OF_QUESTIONS):
    font1 = pygame.font.SysFont('georgia', 70, False, True)
    font2 = pygame.font.SysFont('georgia', 80, False, True)

    text_score = font2.render('SCORE', True, 'mediumseagreen')
    user_score = font1.render(f'{score}/{NUM_OF_QUESTIONS}', True, 'grey85')

    score_width = user_score.get_width()
    score_height = user_score.get_height()

    text_width = text_score.get_width()
    text_height = text_score.get_height()

    SCORE_SOUND.play()
    WINDOW.blit(text_score, [(WINDOW_WIDTH - text_width)//2, (WINDOW_HEIGHT - text_height)//2 - 100])
    WINDOW.blit(user_score, [(WINDOW_WIDTH - score_width)//2, (WINDOW_HEIGHT - score_height)//2])
    pygame.display.update()

    time.sleep(3)


def game_continue():
    WINDOW.fill('black')
    pygame.display.update()

    title_font = pygame.font.SysFont('georgia', 60, False, False)
    font = pygame.font.SysFont('georgia', 30, False, False)

    title = wrapped_text("What comes next?", title_font)
    text = wrapped_text("Do you want to start a new game or quit? Choose the right button below:", font)

    write_wrapped(title, title_font, 'whitesmoke', 20, 0)
    write_wrapped(text, font, 'whitesmoke', 100, 0)

    start_text = font.render("START", True, 'mediumseagreen')
    quit_text = font.render("QUIT", True, 'dark red')

    pygame.draw.rect(WINDOW, 'whitesmoke', START_BUTTON, 1)
    pygame.draw.rect(WINDOW, 'whitesmoke', QUIT_BUTTON, 1)

    WINDOW.blit(start_text, start_text.get_rect(center=START_BUTTON.center))
    WINDOW.blit(quit_text, quit_text.get_rect(center=QUIT_BUTTON.center))

    pygame.display.update()

    GAME_CONTINUE = False
    LEAVE_LOOP = False
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                CLICK_SOUND.play()
                if event.button == 1 and START_BUTTON.collidepoint(event.pos):
                    GAME_CONTINUE = True
                    LEAVE_LOOP = True
                    break
                elif event.button == 1 and QUIT_BUTTON.collidepoint(event.pos):
                    LEAVE_LOOP = True
                    break
        if LEAVE_LOOP:
            break

    if GAME_CONTINUE:
        return True
    if not GAME_CONTINUE:
        pygame.quit()
        sys.exit()


def starting_window():
    CLICK_SOUND.play()
    WINDOW.fill('black')
    time.sleep(1)
    return 0, True
