"""
Играет один игрок, управление с помощью мыши одной ракеткой справа
и одновренменно элементом Prism типа ракетки для корректировки полета
мяча возле левой стенки.

Мячик, отскакивает от всего.
Ракетка, отбивает мячик, увеличивая его скорость.

Prism прозрачна для мяча, идущего влево и корректирует траэкторию мяча,
идущего вправо.

Движущиеся ворота слева, движутся хаотично изменяя направление движения.

При попадании в движущиеся ворота, очко засчитывается Игроку.
При попадании мяча мимо Ракетки в правую стенки, очко засчитывается Компьютеру.

Задача, забить противнику и не пропустить самому.
После гола сразу следует подача из случайной точки возле левой стороны вправо.

Игра идет до 11 очей. Сопровождается звуками игры в настольный теннис.
"""

from livewires import games, color
import pygame
import random

# определение цвета
YELLOW = (255, 255, 0)

pygame.init()

# загрузка звуков
wav_ping = pygame.mixer.Sound("pingpong1.wav")
wav_pingpong = pygame.mixer.Sound("pingpong3.wav")
wav_goal = pygame.mixer.Sound("pingpong_goal.wav")
wav_loss = pygame.mixer.Sound("pingpong_loss.wav")

games.init(screen_width = 720, screen_height = 480, fps = 70)


class Rakets(games.Sprite):
    """" Перемещаемая мышью ракетка. """

    rakets_image = games.load_image("rakets.jpg", transparent = False)
    def __init__(self):
        # Инициализирует объект Rakets

        super(Rakets, self).__init__(image = Rakets.rakets_image,
                                  y = games.mouse.y,
                                  right = games.screen.width - 20)

    def update(self):
        """ Перемещает объект в позицию указателя мыши по одной линии . """
        self.y = games.mouse.y
        self.touch()    # проверка касания к мячу

    def touch(self):
        """ Проверяет касание к мячу """
        # если касается, изменяет направление и скорость мяча
        for ball in self.overlapping_sprites:
            ball.recoil()

class Prism(games.Sprite):

    prism_image = games.load_image("prisma.jpg", transparent = False)
    def __init__(self):
        # Инициализирует объект Prism, родитель Rakets

        super(Prism, self).__init__(image = Prism.prism_image,
                                  y = games.mouse.y,
                                  left = 150)

    def update(self):
        """ Перемещает объект в позицию указателя мыши по одной линии . """
        self.y = games.mouse.y
        self.touch()    # проверка касания к мячу

    def touch(self):
        """ Проверяет касание к мячу """
        # если касается, преломляет направление и скорость мяча
        for ball in self.overlapping_sprites:
            ball.correct()


class Out(games.Sprite):
    # край стола, невидимый, фиксирует касание и считает очки
    out_image = games.load_image("line_bok.jpg", transparent = True)
    def __init__(self):
        # Инициализирует объект Out

        super(Out, self).__init__(image = Out.out_image,
                                  y = games.screen.height/2,
                                  right = games.screen.width-1)
        self.score = games.Text(value = 0, size = 42, color = YELLOW,
                                top = 10, right = games.screen.width/2 - 30)
        games.screen.add(self.score)

    def update(self):
        self.touch()    # проверка касания к мячу

    def touch(self):
        # Проверяет касание к мячу
        # если касается, уничтожает мяч и создает новый
        for ball in self.overlapping_sprites:
            wav_goal.play()
            self.add_score()
            ball.goal()
            ball.message()
            ball.destroy()
            new_ball=Ball()
            games.screen.add(new_ball)

    def add_score(self):
        # Добавляет очки, игра до 11
        self.score.value += 1
        self.score.right = games.screen.width/2 - 30
        if self.score.value == 11:
            self.end_game()

    def end_game(self):
        """ Завершает игру. """
        wav_loss.play()
        end_message = games.Message(value = "Ігру закінчено. Ви програли",
                                    size = 60,
                                    color = color.red,
                                    x = games.screen.width/2,
                                    y = games.screen.height/3,
                                    lifetime = 5 * games.screen.fps,
                                    after_death = games.screen.quit)
        games.screen.add(end_message)


class Goal(games.Sprite):
    # левые ворота, фиксирует касание и считает очки
    goal_image = games.load_image("rakets.jpg", transparent = False)
    def __init__(self, y = games.screen.height/2, speed = 2, odds_change = 200):
        # Инициализирует объект Out

        super(Goal, self).__init__(image = Goal.goal_image,
                                  y = y,
                                  left = 0,
                                  dy = speed)
        self.score = games.Text(value = 0, size = 42, color = YELLOW,
                                top = 10, left = games.screen.width/2 + 30)
        self.odds_change = odds_change
        games.screen.add(self.score)

    def update(self):
        # меняет направление на краях и хаотично
        if self.top <= 0 or self.bottom >= games.screen.height:
            self.dy = -self.dy
        elif random.randrange(self.odds_change) == 100:
            self.dy = -self.dy
        self.touch()    # проверка касания к мячу

    def touch(self):
        # Проверяет касание к мячу
        # если касается, уничтожает мяч и создает новый
        for ball in self.overlapping_sprites:
            wav_goal.play()
            self.add_score()
            ball.goal()
            ball.message()
            ball.destroy()
            new_ball=Ball()
            games.screen.add(new_ball)

    def add_score(self):
        # Добавляет очки, игра до 11
        self.score.value += 1
        self.score.left = games.screen.width/2 + 30
        if self.score.value == 11:
            self.end_game()

    def end_game(self):
        """ Завершает игру. """
        wav_loss.play()
        end_message = games.Message(value = "Ігру закінчено. Ви перемогли",
                                    size = 60,
                                    color = color.red,
                                    x = games.screen.width/2,
                                    y = games.screen.height/3,
                                    lifetime = 5 * games.screen.fps,
                                    after_death = games.screen.quit)
        games.screen.add(end_message)


class Ball(games.Sprite):
    """ Мячик """
    ball_image = games.load_image("ball.png")

    def __init__(self):
        # Инициализирует объект Ball

        super(Ball, self).__init__(image = Ball.ball_image,
                                x = games.screen.width/4,
                                y = random.randrange(30, games.screen.height-30),
                                dx = 2,
                                dy = 2)
        self.message()

    def message(self):
        ball_message = games.Message(value = "Подача",
                                    size = 50,
                                    color = color.green,
                                    right = games.screen.width/2 - 25,
                                    y = games.screen.height/6,
                                    lifetime = 3 * games.screen.fps)
        games.screen.add(ball_message)

    def update(self):
                if self.left < 0 or self.right > games.screen.width:
                    wav_ping.play()  # звук одиночный
                    self.dx = -self.dx
                if self.bottom > games.screen.height or self.top < 0:
                    wav_ping.play()  # звук одиночный
                    self.dy = -self.dy

    def goal(self):
        # менять направление мяча без смены скорости
        self.dx = -self.dx

    def recoil(self):
        # меняет направление и скорость
        wav_pingpong.play()  # звук от ракетки
        self.dx = -(self.dx + 1)

    def correct(self):
        # корректирует направление и скорость
        if self.dx < 0: # движется влево
            self.dy = -(self.dy)
        if self.dx < -2:
            self.dx = -2    # ограничение скорости


def main():
    wall_image = games.load_image("table.jpg", transparent = False)
    games.screen.background = wall_image

    the_rakets = Rakets()
    games.screen.add(the_rakets)

    the_prism = Prism()
    games.screen.add(the_prism)

    out_right = Out()
    games.screen.add(out_right)

    goal_left = Goal()
    games.screen.add(goal_left)

    the_ball = Ball()
    games.screen.add(the_ball)

    games.mouse.is_visible = False
    games.screen.event_grab = True

    games.screen.mainloop()

# Игра
main()
