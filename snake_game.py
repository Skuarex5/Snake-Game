import tkinter as tk
import random

WIDTH = 400
HEIGHT = 400
SEG_SIZE = 20
IN_GAME = True

DIRECTIONS = {'Left': (-SEG_SIZE, 0), 'Right': (SEG_SIZE, 0), 'Up': (0, -SEG_SIZE), 'Down': (0, SEG_SIZE)}

class SnakeGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Snake Game")
        self.canvas = tk.Canvas(master, width=WIDTH, height=HEIGHT, bg="black")
        self.canvas.pack()

        self.snake = [(WIDTH//2, HEIGHT//2)]
        self.snake_dir = 'Right'
        self.food = None
        
        self.start()


    def draw_snake(self):
        self.canvas.delete("snake")
        for x, y in self.snake:
            self.canvas.create_oval(x, y, x + SEG_SIZE, y + SEG_SIZE, fill="green", tag="snake")

    def create_food(self):
        x = random.randrange(0, WIDTH, SEG_SIZE)
        y = random.randrange(0, HEIGHT, SEG_SIZE)
        self.food = (x, y)
        self.canvas.create_oval(x, y, x + SEG_SIZE, y + SEG_SIZE, fill="red", tag="food")

    def move_snake(self):
        if not IN_GAME:
            self.game_over()
            return

        x, y = self.snake[0]
        dx, dy = DIRECTIONS[self.snake_dir]
        new_head = (x + dx, y + dy)

        if (new_head in self.snake or
            new_head[0] < 0 or new_head[0] >= WIDTH or
            new_head[1] < 0 or new_head[1] >= HEIGHT):
            self.game_over()
            return

        self.snake = [new_head] + self.snake[:-1]

        if new_head == self.food:
            self.snake.append(self.snake[-1])
            self.canvas.delete("food")
            self.create_food()

        self.draw_snake()
        self.master.after(150, self.move_snake)

    def change_direction(self, event):
        if event.keysym in DIRECTIONS:
            if (self.snake_dir == 'Left' and event.keysym != 'Right') or \
               (self.snake_dir == 'Right' and event.keysym != 'Left') or \
               (self.snake_dir == 'Up' and event.keysym != 'Down') or \
               (self.snake_dir == 'Down' and event.keysym != 'Up'):
                self.snake_dir = event.keysym

    def game_over(self):
        global IN_GAME
        IN_GAME = False
        self.canvas.create_text(WIDTH//2, HEIGHT//2, text="GAME OVER", fill="red", font="Arial 20 bold")

    def start(self):
        def show_countdown(number):
            if number > 0:
                self.canvas.delete("countdown")
                self.canvas.create_text(WIDTH // 2, HEIGHT // 2,
                                    text=str(number), fill="red",
                                    font="Arial 40 bold", tag="countdown")
                self.master.after(1000, show_countdown, number - 1)
            else:
                self.canvas.delete("countdown")
                self.draw_snake()
                self.create_food()
                self.master.bind("<KeyPress>", self.change_direction)
                self.move_snake()

        show_countdown(3)

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
