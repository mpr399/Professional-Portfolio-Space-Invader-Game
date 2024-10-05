from turtle import Turtle

SCORE_MARGIN = 30
FONT = ("Arial", 16, "normal")


class ScoreBoard(Turtle):
    def __init__(self):
        super().__init__()
        self.hideturtle()
        self.color("white")
        self.speed("fastest")
        self.level = 1
        self.score = 0
        self.goto(0, (self.getscreen().window_height() / 2 - SCORE_MARGIN))
        self.refresh()

    def refresh(self):
        self.clear()
        self.write(f"Level:{self.level}  Score:{self.score}", font=FONT, align='center')

    def update_score(self):
        self.score += self.level * self.level
        self.refresh()


