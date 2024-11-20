import tkinter as tk
import random

# Set up the main game window
root = tk.Tk()
root.title("Ping Pong Game")
root.resizable(False, False)

# Game settings
WIDTH, HEIGHT = 500, 400
BALL_SIZE = 20
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 10
BALL_SPEED_X, BALL_SPEED_Y = 4, 4  # Initial speed
SPEED_INCREMENT = 0.5  # Speed increase per paddle hit

# Canvas for drawing
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")  # Black background
canvas.pack()

# Paddle
paddle = canvas.create_rectangle(
    WIDTH // 2 - PADDLE_WIDTH // 2,
    HEIGHT - PADDLE_HEIGHT * 2,
    WIDTH // 2 + PADDLE_WIDTH // 2,
    HEIGHT - PADDLE_HEIGHT,
    fill="blue",  # Paddle color set to blue for contrast
)

# Ball (White color)
ball = canvas.create_oval(
    WIDTH // 2 - BALL_SIZE // 2,
    HEIGHT // 2 - BALL_SIZE // 2,
    WIDTH // 2 + BALL_SIZE // 2,
    HEIGHT // 2 + BALL_SIZE // 2,
    fill="white",  # Ball color set to white
)

# Ball movement variables
ball_dx, ball_dy = BALL_SPEED_X, BALL_SPEED_Y
game_over_text = None
play_again_button = None

# Move paddle left or right with keyboard
def move_paddle(event):
    x = 0
    if event.keysym == "Left":
        x = -20
    elif event.keysym == "Right":
        x = 20
    canvas.move(paddle, x, 0)

# Bind paddle movement (Keyboard)
root.bind("<Left>", move_paddle)
root.bind("<Right>", move_paddle)

# Smooth touch paddle movement
def move_paddle_touch(event):
    # Get paddle's current position
    paddle_pos = canvas.coords(paddle)
    # Calculate the new paddle x position centered on the touch event x
    new_paddle_x = event.x - PADDLE_WIDTH / 2

    # Keep paddle within the screen bounds
    if new_paddle_x < 0:
        new_paddle_x = 0
    elif new_paddle_x + PADDLE_WIDTH > WIDTH:
        new_paddle_x = WIDTH - PADDLE_WIDTH

    # Move paddle directly to new x position
    canvas.coords(paddle, new_paddle_x, paddle_pos[1], new_paddle_x + PADDLE_WIDTH, paddle_pos[3])

# Bind touch movement (Mouse or Touchscreen)
canvas.bind("<B1-Motion>", move_paddle_touch)

# Restart the game
def reset_game():
    global ball_dx, ball_dy, game_over_text, play_again_button
    # Reset ball position and speed
    canvas.coords(ball, WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, WIDTH // 2 + BALL_SIZE // 2, HEIGHT // 2 + BALL_SIZE // 2)
    ball_dx, ball_dy = BALL_SPEED_X, BALL_SPEED_Y
    
    # Remove game over text and play again button if they exist
    if game_over_text:
        canvas.delete(game_over_text)
        game_over_text = None
    if play_again_button:
        play_again_button.destroy()
        play_again_button = None

    # Start the game loop again
    game_loop()

# Game loop
def game_loop():
    global ball_dx, ball_dy, game_over_text, play_again_button

    # Move the ball
    canvas.move(ball, ball_dx, ball_dy)
    ball_pos = canvas.coords(ball)
    paddle_pos = canvas.coords(paddle)

    # Bounce off walls
    if ball_pos[0] <= 0 or ball_pos[2] >= WIDTH:
        ball_dx = -ball_dx
    if ball_pos[1] <= 0:
        ball_dy = -ball_dy

    # Bounce off paddle
    if (
        paddle_pos[0] < ball_pos[2] < paddle_pos[2]
        and paddle_pos[1] < ball_pos[3] < paddle_pos[3]
    ):
        ball_dy = -ball_dy

        # Increase ball speed after each paddle hit
        ball_dx += SPEED_INCREMENT if ball_dx > 0 else -SPEED_INCREMENT
        ball_dy += SPEED_INCREMENT if ball_dy > 0 else -SPEED_INCREMENT

    # Game over if ball hits bottom
    if ball_pos[3] >= HEIGHT:
        game_over_text = canvas.create_text(
            WIDTH // 2,
            HEIGHT // 2,
            text="Game Over",
            fill="white",
            font=("Arial", 24)
        )

        # Create a "Play Again" button
        play_again_button = tk.Button(root, text="Play Again", command=reset_game, bg="black", fg="white")
        play_again_button.pack()
        return

    # Slightly reduce the delay for faster ball movement
    root.after(25, game_loop)

# Start game loop
game_loop()
root.mainloop()
