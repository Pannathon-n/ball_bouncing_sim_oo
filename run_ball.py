import ball
import my_event
import turtle
import random
import heapq
import paddle
import math
import time

class GameOverScreen:
    def __init__(self):
        self.text_turtle = turtle.Turtle()
        self.text_turtle.hideturtle()
        self.text_turtle.penup()
        self.screen = turtle.Screen()

    def display_message(self, message, color=(255, 0, 0), font=("Arial", 24, "bold")):
        self.text_turtle.clear()
        self.text_turtle.color(color)
        self.text_turtle.goto(0, 50)  # Center the text slightly higher
        self.text_turtle.write(message, align="center", font=font)
        self.text_turtle.goto(0, -20)
        self.text_turtle.write("Press 'R' to Restart", align="center", font=("Arial", 18, "italic"))

    def clear_message(self):
        self.text_turtle.clear()

    def listen_for_restart(self, restart_callback):
        self.screen.listen()
        self.screen.onkey(restart_callback, "r")  # Press 'R' to restart

class GameTimer:
    def __init__(self, duration, screen):
        self.duration = duration  # Total duration in seconds
        self.start_time = time.time()  # Record the start time
        self.timer_turtle = turtle.Turtle()
        self.timer_turtle.hideturtle()
        self.timer_turtle.penup()
        self.screen = screen

        # Position the timer at the top-left corner
        self.timer_turtle.goto(-self.screen.window_width() // 2 + 20, self.screen.window_height() // 2 - 50)

    def update(self):
        """
        Update the timer display based on real elapsed time.

        Returns:
            bool: True if the timer has reached or exceeded the duration, False otherwise.
        """
        elapsed_time = time.time() - self.start_time
        remaining_time = max(0, self.duration - elapsed_time)

        # Clear the previous display and draw the updated time
        self.timer_turtle.clear()
        self.timer_turtle.write(
            f"Time: {int(remaining_time)}s",
            font=("Arial", 16, "bold"),
            align="left"
        )

        # Return whether the timer is finished
        return remaining_time == 0

    def clear(self):
        """Clear the timer display."""
        self.timer_turtle.clear()

class BouncingSimulator:
    def __init__(self, num_balls, time_limit=15):
        self.num_balls = num_balls
        self.time_limit = time_limit
        self.ball_list = []
        self.t = 0.0
        self.pq = []
        self.HZ = 4
        self.screen = turtle.Screen()
        turtle.speed(0)
        turtle.tracer(0)
        turtle.hideturtle()
        turtle.colormode(255)
        self.canvas_width = turtle.screensize()[0]
        self.canvas_height = turtle.screensize()[1]
        print(self.canvas_width, self.canvas_height)

        ball_radius = 0.05 * self.canvas_width
        for i in range(self.num_balls):
            x = -self.canvas_width + (i+1)*(2*self.canvas_width/(self.num_balls+1))
            y = 0.0
            speed = 15  # Set a fixed speed for all balls
            angle = random.uniform(0, 2 * math.pi)  # Random direction
            vx = speed * math.cos(angle)
            vy = speed * math.sin(angle)
            ball_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            self.ball_list.append(ball.Ball(ball_radius, x, y, vx, vy, ball_color, i))

        tom = turtle.Turtle()
        self.my_paddle = paddle.Paddle(200, 10, (255, 0, 0), tom)
        self.my_paddle.set_location([0, -260])

        Khaw = turtle.Turtle()
        self.my_second_paddle = paddle.Paddle(200, 10, (0, 0, 255), Khaw)
        self.my_second_paddle.set_location([0, 260])

        self.timer = GameTimer(self.time_limit, self.screen)

        self.screen = turtle.Screen()

    # updates priority queue with all new events for a_ball
    def __predict(self, a_ball):
        if a_ball is None:
            return

        # particle-particle collisions
        for i in range(len(self.ball_list)):
            dt = a_ball.time_to_hit(self.ball_list[i])
            # insert this event into pq
            heapq.heappush(self.pq, my_event.Event(self.t + dt, a_ball, self.ball_list[i], None))
        
        # particle-wall collisions
        dtX = a_ball.time_to_hit_vertical_wall()
        dtY = a_ball.time_to_hit_horizontal_wall()
        heapq.heappush(self.pq, my_event.Event(self.t + dtX, a_ball, None, None))
        heapq.heappush(self.pq, my_event.Event(self.t + dtY, None, a_ball, None))
    
    def __draw_border(self):
        turtle.penup()
        turtle.goto(-self.canvas_width, -self.canvas_height)
        turtle.pensize(10)
        turtle.pendown()
        turtle.color((0, 0, 0))   
        for i in range(2):
            turtle.forward(2*self.canvas_width)
            turtle.left(90)
            turtle.forward(2*self.canvas_height)
            turtle.left(90)

    def __redraw(self):
        turtle.clear()
        self.my_paddle.clear()
        self.my_second_paddle.clear()
        self.__draw_border()
        self.my_paddle.draw()
        self.my_second_paddle.draw()
        for i in range(len(self.ball_list)):
            self.ball_list[i].draw()
        turtle.update()
        heapq.heappush(self.pq, my_event.Event(self.t + 1.0 / self.HZ, None, None, None))

    def __paddle_predict(self):
        for i in range(len(self.ball_list)):
            a_ball = self.ball_list[i]
            dtP = a_ball.time_to_hit_paddle(self.my_paddle)
            heapq.heappush(self.pq, my_event.Event(self.t + dtP, a_ball, None, self.my_paddle))

            dtP2 = a_ball.time_to_hit_paddle(self.my_second_paddle)
            heapq.heappush(self.pq, my_event.Event(self.t + dtP2, a_ball, None, self.my_second_paddle))

    # move_left and move_right handlers update paddle positions
    def move_left(self):
        if (self.my_paddle.location[0] - self.my_paddle.width/2 - 40) >= -self.canvas_width:
            self.my_paddle.set_location([self.my_paddle.location[0] - 40, self.my_paddle.location[1]])

    # move_left and move_right handlers update paddle positions
    def move_right(self):
        if (self.my_paddle.location[0] + self.my_paddle.width/2 + 40) <= self.canvas_width:
            self.my_paddle.set_location([self.my_paddle.location[0] + 40, self.my_paddle.location[1]])

    def move_second_paddle_left(self):
        if (self.my_second_paddle.location[0] - self.my_second_paddle.width / 2 - 40) >= -self.canvas_width:
            self.my_second_paddle.set_location(
                [self.my_second_paddle.location[0] - 40, self.my_second_paddle.location[1]])

    def move_second_paddle_right(self):
        if (self.my_second_paddle.location[0] + self.my_second_paddle.width / 2 + 40) <= self.canvas_width:
            self.my_second_paddle.set_location(
                [self.my_second_paddle.location[0] + 40, self.my_second_paddle.location[1]])

    def run(self):
        def restart():
            print("Restarting game...")

            self.timer.timer_turtle.clear()

            game_over_screen.clear_message()

            self.my_paddle.clear()
            self.my_second_paddle.clear()
            
            self.__init__(self.num_balls,)  # Reinitialize the simulator
            self.run()  # Restart the game loop

        self.timer = GameTimer(self.time_limit, self.screen)

        # initialize pq with collision events and redraw event
        for i in range(len(self.ball_list)):
            self.__predict(self.ball_list[i])
        heapq.heappush(self.pq, my_event.Event(0, None, None, None))

        # listen to keyboard events and activate move_left and move_right handlers accordingly
        self.screen.listen()
        self.screen.onkey(self.move_left, "Left")
        self.screen.onkey(self.move_right, "Right")

        self.screen.onkey(self.move_second_paddle_left, "a")
        self.screen.onkey(self.move_second_paddle_right, "d")

        game_over_screen = GameOverScreen()

        while (True):
            e = heapq.heappop(self.pq)
            if not e.is_valid():
                continue

            ball_a = e.a
            ball_b = e.b
            paddle_a = e.paddle

            # update positions, and then simulation clock
            for i in range(len(self.ball_list)):
                self.ball_list[i].move(e.time - self.t)
            self.t = e.time

            if (ball_a is not None) and (ball_b is not None) and (paddle_a is None):
                ball_a.bounce_off(ball_b)
            elif (ball_a is not None) and (ball_b is None) and (paddle_a is None):
                ball_a.bounce_off_vertical_wall()
            elif (ball_a is None) and (ball_b is None) and (paddle_a is None):
                self.__redraw()
            elif (ball_a is not None) and (ball_b is None) and (paddle_a is not None):
                ball_a.bounce_off_paddle()
            elif (ball_a is not None) and (ball_b is None) and (paddle_a == self.my_second_paddle):
                ball_a.bounce_off_paddle()
            elif (ball_a is None) and (ball_b is not None) and (paddle_a is None):
                game_over = ball_b.bounce_off_horizontal_wall()
                if game_over:
                    game_over_screen.display_message("Game Over!")  # Show game over screen
                    game_over_screen.listen_for_restart(restart)  # Listen for restart
                    break  # Exit the while loop to allow restart

            self.__predict(ball_a)
            self.__predict(ball_b)

            # regularly update the prediction for the paddle as its position may always be changing due to keyboard events
            self.__paddle_predict()

            if self.timer.update():
                game_over_screen.display_message("Time's Up! It's a Draw!")
                game_over_screen.listen_for_restart(restart)
                break


        # hold the window; close it by clicking the window close 'x' mark
        turtle.done()

# num_balls = int(input("Number of balls to simulate: "))
num_balls = 1
my_simulator = BouncingSimulator(num_balls)
my_simulator.run()
