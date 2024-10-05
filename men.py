from turtle import Turtle

COLOUR_SHIP = "#2E8B57"
COLOUR_WALL = "#9ACD32"
COLOUR_BULLET = "#00FF7F"
X_MARGIN = 50
Y_MARGIN = 50
SIDE_STEP = 10
WALL_VERTICAL_STEP = 30
BULLET_STEP = 20
DEFENCE_WALL = (6, 3)


class MenShip(Turtle):
    def __init__(self):
        super().__init__()
        self.color(COLOUR_SHIP)
        self.shapesize(1, 1),
        self.shape("turtle")
        self.penup()
        self.setheading(90)
        self.has_been_hit = False


class MenWall(Turtle):
    def __init__(self):
        super().__init__()
        self.color(COLOUR_WALL)
        self.shapesize(1, 0.2)
        self.shape("square")
        self.penup()
        self.has_been_hit = False


class MenBullet(Turtle):
    def __init__(self):
        super().__init__()
        self.color(COLOUR_BULLET)
        self.shapesize(0.4, 1)
        self.has_been_hit = False


class MenArmy(Turtle):
    def __init__(self):
        super().__init__()
        self.hideturtle()
        self.ship = MenShip()
        self.walls = []
        self.bullets = []
        self.window_width = self.getscreen().window_width()
        self.window_height = self.getscreen().window_height()
        self.wall_interval = (self.window_width - (2 * X_MARGIN)) / DEFENCE_WALL[0]
        self.starting_point = ((2 * X_MARGIN) - (self.window_width / 2), (2 * Y_MARGIN) - (self.window_height / 2))

    def create_army(self):
        self.ship.goto(self.starting_point)

        for i in range(DEFENCE_WALL[0]):

            for j in range(DEFENCE_WALL[1]):
                new_wall = MenWall()
                new_wall.setheading(90)
                new_wall.goto(self.starting_point[0] + (i * self.wall_interval),
                              self.starting_point[1] + ((j + 1) * WALL_VERTICAL_STEP))
                self.walls.append(new_wall)

    def move_ship_left(self):
        if self.ship.xcor() > -(self.window_width / 2 - X_MARGIN):
            self.ship.setheading(180)
            self.ship.forward(SIDE_STEP)
            self.ship.setheading(90)

    def move_ship_right(self):
        if self.ship.xcor() < (self.window_width / 2 - X_MARGIN):
            self.ship.setheading(0)
            self.ship.forward(SIDE_STEP)
            self.ship.setheading(90)

    def shoot(self):
        new_bullet = MenBullet()
        new_bullet.penup()
        new_bullet.goto(self.ship.position())
        new_bullet.setheading(90)

        self.bullets.append(new_bullet)
        new_bullet.forward(BULLET_STEP)

    def move_bullets(self):
        for bullet in self.bullets:
            bullet.forward(BULLET_STEP)

            self.remove_off_screen_bullets(bullet)

    def remove_off_screen_bullets(self, bullet):
        if bullet.ycor() >= (self.getscreen().window_height() / 2):
            bullet.hideturtle()
            self.bullets.remove(bullet)

    def remove_has_been_hit(self):
        for item in self.walls:
            if item.has_been_hit:
                item.hideturtle()
                try:
                    self.walls.remove(item)
                except:
                    pass

        for item in self.bullets:
            if item.has_been_hit:
                item.hideturtle()
                try:
                    self.bullets.remove(item)
                except:
                    pass
