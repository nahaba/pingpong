"""
One player is playing, control with the mouse by one racket on the right
and at the same time an element of Prism-type racquet for flight adjustment
ball near the left wall.

Ball, bounces off everything.
Racket, beats the ball, increasing its speed.

Prism is transparent for the ball going to the left and adjusts the trajectory of the ball,
going to the right.

Moving gates to the left, moving chaotically changing the direction of motion.

If you hit a moving gate, the point is counted as a Player.
If you hit the ball past the Racket in the right wall, the point is counted against the computer.

The task is to score the enemy and not miss it yourself.
After the goal immediately follows the flow from the random point near the left side to the right.

The game goes to 11 eyes. Accompanied by the sounds of playing table tennis."""

from livewires import games, color
import pygame
import random

# color definition
YELLOW = (255, 255, 0)

pygame.init()

games.init(screen_width=720, screen_height=480, fps=70)


class Recapture(games.Sprite):
    """ Movable object. Changes the trajectory of the ball """
    """ Перемещаемый объект. Меняет траекторию движения мяча """

    def update(self):
        """ Moves the object to the position of the mouse pointer along a single line. """
        """ Перемещает объект в позицию указателя мыши по одной линии. """
        self.y = games.mouse.y
        self.touch()    # Checks the touch to the ball | проверка касания к мячу

    def touch(self):
        """ Checks the touch to the ball """
        """ Проверяет касание к мячу """
        # if applicable, changes the direction and speed of the ball
        # если касается, изменяет направление и скорость мяча
        for ball in self.overlapping_sprites:
            ball.recoil()


class Rakets(Recapture):
    """ Movable racket. The Descendant of Recaptur """
    """ Перемещаемая мышью ракетка. Потомок Recapture """

    rakets_image = games.load_image("rakets.jpg", transparent=False)

    def __init__(self):
        # Инициализирует объект Rakets

        super(Rakets, self).__init__(image=Rakets.rakets_image,
                                     y=games.mouse.y,
                                     right=games.screen.width - 20)


class Prism(Recapture):
    """ Movable object Prism. Changes the trajectory of the ball. The Descendant of Recaptur """
    """ Перемещаемый объект Призма. Меняет траекторию движения мяча. Потомок Recapture """
    prism_image = games.load_image("prisma.jpg", transparent=False)

    def __init__(self):
        super(Prism, self).__init__(image=Prism.prism_image,
                                    y=games.mouse.y,
                                    left=150)

    def touch(self):
        """ Checks the touch to the ball """
        """ Проверяет касание к мячу """
        # if applicable, refracts the direction and speed of the ball
        # если касается, преломляет направление и скорость мяча
        for ball in self.overlapping_sprites:
            ball.correct()


class Out(games.Sprite):
    # the edge of the table, invisible, fixes the touch and counts the glasses
    # край стола, невидимый, фиксирует касание и считает очки
    out_image = games.load_image("line_bok.jpg", transparent=True)
    wav_goal = games.load_sound("pingpong_goal.wav")
    wav_loss = games.load_sound("pingpong_loss.wav")

    def __init__(self):

        # Initializes the Out object
        # Инициализирует объект Out
        super(Out, self).__init__(image=Out.out_image,
                                  y=games.screen.height / 2,
                                  right=games.screen.width - 1)
        self.score = games.Text(value=0, size=42, color=YELLOW,
                                top=10, right=games.screen.width / 2 - 30)
        games.screen.add(self.score)

    def update(self):
        self.touch()    # Checks the touch to the ball | проверка касания к мячу

    def touch(self):
        # Checks the touch to the ball
        # if applicable, destroys the ball and creates a new one
        # Проверяет касание к мячу
        # если касается, уничтожает мяч и создает новый
        for ball in self.overlapping_sprites:
            Out.wav_goal.play()
            self.add_score()
            ball.goal()
            ball.message()
            # ball.destroy()
            new_ball = Ball()
            games.screen.add(new_ball)

    def add_score(self):
        # Adds points if 11 eyes are scored - the end of the game
        # Добавляет очки, если набрано 11 очей - конец игры
        self.score.value += 1
        self.score.right = games.screen.width / 2 - 30
        if self.score.value == 11:
            self.end_game()

    def end_game(self):
        """ Finishes the game. """
        """ Завершает игру. """
        Out.wav_loss.play()
        end_message = games.Message(value="The game is over. You have lost",
                                    size=60,
                                    color=color.red,
                                    x=games.screen.width / 2,
                                    y=games.screen.height / 3,
                                    lifetime=5 * games.screen.fps,
                                    after_death=games.screen.quit)
        games.screen.add(end_message)


class Goal(games.Sprite):
    # left gate, fixes the touch and count points
    # левые ворота, фиксирует касание и считает очки
    goal_image = games.load_image("goal1.jpg", transparent=False)
    wav_goal = games.load_sound("pingpong_goal.wav")
    wav_loss = games.load_sound("pingpong_loss.wav")

    def __init__(self, y=games.screen.height / 2, speed=2, odds_change=200):
        # Initializes the Out object
        # Инициализирует объект Out

        super(Goal, self).__init__(image=Goal.goal_image,
                                   y=y,
                                   left=0,
                                   dy=speed)
        self.score = games.Text(value=0, size=42, color=YELLOW,
                                top=10, left=games.screen.width / 2 + 30)
        self.odds_change = odds_change
        games.screen.add(self.score)

    def update(self):
        # changes direction on the edges and chaotic
        # меняет направление на краях и хаотично
        if self.top <= 0 or self.bottom >= games.screen.height:
            self.dy = -self.dy
        elif random.randrange(self.odds_change) == 100:
            self.dy = -self.dy
        self.touch()    # проверка касания к мячу | Checks the touch to the ball

    def touch(self):
        # Checks the touch to the ball
        # if applicable, destroys the ball and creates a new one
        # Проверяет касание к мячу
        # если касается, уничтожает мяч и создает новый
        for ball in self.overlapping_sprites:
            Goal.wav_goal.play()
            self.add_score()
            ball.goal()
            ball.message()
            # ball.destroy()
            new_ball = Ball()
            games.screen.add(new_ball)

    def add_score(self):
        # Adds points if 11 eyes are scored - the end of the game
        # Добавляет очки, если набрано 11 очей - конец игры
        self.score.value += 1
        self.score.left = games.screen.width / 2 + 30
        if self.score.value == 11:
            self.end_game()

    def end_game(self):
        """ Finishes the game. """
        """ Завершает игру. """
        Goal.wav_loss.play()
        end_message = games.Message(value="The game is over. You won!",
                                    size=60,
                                    color=color.red,
                                    x=games.screen.width / 2,
                                    y=games.screen.height / 3,
                                    lifetime=5 * games.screen.fps,
                                    after_death=games.screen.quit)
        games.screen.add(end_message)


class Ball(games.Sprite):
    """ Ball """
    """ Мячик """
    ball_image = games.load_image("ball.png")
    wav_ping = games.load_sound("pingpong1.wav")
    wav_pingpong = games.load_sound("pingpong3.wav")

    def __init__(self):
        # Initializes a Ball object
        # Инициализирует объект Ball

        super(Ball, self).__init__(image=Ball.ball_image,
                                   x=games.screen.width / 4,
                                   y=random.randrange(30, games.screen.height - 30),
                                   dx=2,
                                   dy=2)
        self.message()

    def message(self):
        ball_message = games.Message(value="Innings",
                                     size=50,
                                     color=color.green,
                                     right=games.screen.width / 2 - 25,
                                     y=games.screen.height / 6,
                                     lifetime=3 * games.screen.fps)
        games.screen.add(ball_message)

    def update(self):
        if self.left < 0 or self.right > games.screen.width:
            Ball.wav_ping.play()  # single sound | звук одиночный
            self.dx = -self.dx
        if self.bottom > games.screen.height or self.top < 0:
            Ball.wav_ping.play()  # single sound | звук одиночный
            self.dy = -self.dy

    def goal(self):
        # change the direction of the ball without changing the speed
        # менять направление мяча без смены скорости
        self.destroy()

    def recoil(self):
        # changes direction and speed
        # меняет направление и скорость
        Ball.wav_pingpong.play()  # звук от ракетки
        self.dx = -(self.dx + 1)

    def correct(self):
        # corrects the direction and speed
        # корректирует направление и скорость
        if self.dx < 0:     # if it moves to the left | если движется влево
            self.dy = -(self.dy)
        if self.dx < -2:
            self.dx = -2    # speed limit | ограничение скорости


def main():
    wall_image = games.load_image("table.jpg", transparent=False)
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


# Game
main()
