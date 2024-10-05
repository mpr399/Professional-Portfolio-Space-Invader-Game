import time
import turtle
from turtle import Screen
from aliens import AlienArmy
from men import MenArmy
from score import ScoreBoard

WIDTH = 1000
HEIGHT = 800
SCREEN_COLOR = "black"
SCREEN_TITLE = "SPACE INVADER GAME"
COLLISION_MARGIN = 20
SCREEN_REFRESH = 0.05
BULLET_FIRING_INTERVAL_START = 1000
BULLET_FIRING_INTERVAL_LIMIT = 100
MOVE_DOWN_INTERVAL = 5000
GAME_LEVEL = 1
GAME_SCORE = 0

play_again = True
while play_again:

    screen = Screen()
    screen.bgcolor(SCREEN_COLOR)
    screen.title(SCREEN_TITLE)
    screen.setup(width=WIDTH, height=HEIGHT)
    screen.tracer(0)

    men_army = MenArmy()
    alien_army = AlienArmy()

    my_score = ScoreBoard()
    my_score.score = GAME_SCORE
    my_score.level = GAME_LEVEL
    my_score.refresh()

    alien_army.create_army()
    men_army.create_army()

    screen.listen()
    screen.onkey(men_army.move_ship_left, "Left")
    screen.onkey(men_army.move_ship_right, "Right")
    screen.onkey(men_army.shoot, "space")

    bullet_firing_interval = BULLET_FIRING_INTERVAL_START - ((GAME_LEVEL - 1) * BULLET_FIRING_INTERVAL_LIMIT)

    game_on = True
    while game_on:
        time.sleep(SCREEN_REFRESH)

        # aliens shooting
        if alien_army.ready_to_shoot:
            alien_army.shoot()
            turtle.ontimer(alien_army.make_ready_to_shoot, t=bullet_firing_interval)

        # aliens moving towards men after interval
        if alien_army.ready_to_move_down:
            alien_army.move_down()
            turtle.ontimer(alien_army.make_ready_to_move_down, t=MOVE_DOWN_INTERVAL)

        # aliens move ship left to right and right to left
        alien_army.move_side()

        # aliens bullets moving towards men
        alien_army.move_bullets()

        # men move bullets towards aliens
        men_army.move_bullets()

        # NOTE: men movement and shooting depends on key presses

        screen.update()

        # check for items that have been hit and must be removed -- MEN
        for item in men_army.walls:
            for bullet in alien_army.bullets:
                if item.distance(bullet) <= COLLISION_MARGIN:
                    item.has_been_hit = True
                    bullet.has_been_hit = True

        men_army.remove_has_been_hit()

        # check for items that have been hit and must be removed -- ALIENS
        for item in alien_army.ships + alien_army.walls:
            for bullet in men_army.bullets:
                if item.distance(bullet) <= COLLISION_MARGIN:
                    item.has_been_hit = True
                    bullet.has_been_hit = True

                    my_score.update_score()

        alien_army.remove_has_been_hit()

        screen.update()

        # if all aliens are shot down, increase game level
        if len(alien_army.ships) <= 0:
            GAME_LEVEL += 1
            GAME_SCORE = my_score.score
            screen.clear()
            break

        # check if alien ship has reached men ship
        if game_on:
            for item in alien_army.ships + alien_army.walls:
                if item.ycor() <= men_army.ship.ycor():
                    game_on = False

        # check for death of player
        for bullet in alien_army.bullets:
            if men_army.ship.distance(bullet) <= COLLISION_MARGIN:
                game_on = False
                # break current For Loop
                break

    if not game_on:
        GAME_LEVEL = 1
        GAME_SCORE = 0
        repeat = screen.textinput("Game Over!", "Press Y to play again. N to quit")
        if repeat.upper() == "Y":
            del alien_army, men_army, my_score
            screen.clear()
        else:
            play_again = False

screen.mainloop()


