import random
from turtle import Turtle

COLOUR_SHIP = "#B8860B"
COLOUR_WALL = "#F0E68C"
COLOUR_BULLET = "#FFFF00"
X_MARGIN = 50
Y_MARGIN = 50
SIDE_STEP = 5
DOWN_STEP = 30
WALL_VERTICAL_STEP = 30
BULLET_STEP = 20
NUMBER_OF_SHIPS = 6
WALL_PER_SHIP = 6


class AlienShip(Turtle):
    def __init__(self):
        super().__init__()
        self.color(COLOUR_SHIP)
        self.shapesize(1, 1)
        self.shape("turtle")
        self.penup()
        self.setheading(270)
        self.has_been_hit = False


class AlienWall(Turtle):
    def __init__(self):
        super().__init__()
        self.color(COLOUR_WALL)
        self.shapesize(1, 0.2)
        self.has_been_hit = False
        self.shape("square")
        self.penup()
        self.setheading(270)


class AlienBullet(Turtle):
    def __init__(self):
        super().__init__()
        self.color(COLOUR_BULLET)
        self.shapesize(0.4, 1)
        self.penup()
        self.setheading(270)
        self.has_been_hit = False


class AlienArmy(Turtle):
    def __init__(self):
        super().__init__()
        self.hideturtle()
        self.ships = []
        self.walls = []
        self.bullets = []
        self.window_width = self.getscreen().window_width()
        self.window_height = self.getscreen().window_height()
        self.ship_interval = (self.window_width / 2) / NUMBER_OF_SHIPS
        self.starting_point = (X_MARGIN - (self.window_width / 2), (self.window_height / 2) - Y_MARGIN)
        self.direction = "RIGHT"
        self.ready_to_shoot = True
        self.ready_to_move_down = True

    def create_army(self):
        for i in range(NUMBER_OF_SHIPS):
            new_item = AlienShip()

            new_item.goto(self.starting_point[0] + i * self.ship_interval, self.starting_point[1])
            self.ships.append(new_item)

        for item in self.ships:

            for i in range(WALL_PER_SHIP):
                new_item = AlienWall()

                pos = item.position()
                new_item.goto(pos[0], pos[1] - ((i + 1) * WALL_VERTICAL_STEP))
                self.walls.append(new_item)

    def move_side(self):
        if len(self.ships) > 0:
            pos_first = self.ships[0].position()
            pos_last = self.ships[-1].position()

            point_to_return = (self.window_width / 2) - X_MARGIN

            if self.direction == "RIGHT" and pos_last[0] > point_to_return:
                self.direction = "LEFT"
            if self.direction == "LEFT" and pos_first[0] < (-point_to_return):
                self.direction = "RIGHT"

            heading = 0
            if self.direction == "LEFT":
                heading = 180

            for item in self.ships:
                item.setheading(heading)
                item.forward(SIDE_STEP)
                item.setheading(270)

            for item in self.walls:
                item.setheading(heading)
                item.forward(SIDE_STEP)
                item.setheading(270)

    def move_down(self):
        for item in self.ships:
            item.forward(DOWN_STEP)

        for item in self.walls:
            item.forward(DOWN_STEP)

        self.ready_to_move_down = False

    def shoot(self):
        if len(self.ships) > 0:
            ship = random.choice(self.ships)
            new_bullet = AlienBullet()

            new_bullet.goto(ship.position())
            self.bullets.append(new_bullet)
            new_bullet.forward(BULLET_STEP)

            self.ready_to_shoot = False

    def move_bullets(self):
        for bullet in self.bullets:
            bullet.forward(BULLET_STEP)

            self.remove_off_screen_bullets(bullet)

    def remove_off_screen_bullets(self, bullet):
        if bullet.ycor() <= -(self.window_height / 2):
            bullet.hideturtle()

            self.bullets.remove(bullet)

    def remove_has_been_hit(self):
        for item in self.ships:
            if item.has_been_hit:
                item.hideturtle()
                try:
                    self.ships.remove(item)
                except:
                    pass

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

    def make_ready_to_shoot(self):
        self.ready_to_shoot = True

    def make_ready_to_move_down(self):
        self.ready_to_move_down = True
