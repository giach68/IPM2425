import tkinter as tk
from time import time
import random
import math

# Initialize variables
num_targets = 5  # Number of target positions
canvas_size = 300
target_radius = 20
click_times = []
errors = 0
start_time = None
current_position_index = 0

# Function to generate positions with constant distance, starting randomly
def generate_positions(num_positions, canvas_size, radius):
    positions = []
    constant_distance = canvas_size / 2  # Set the desired distance between points

    # Generate the first position randomly
    x = random.randint(radius, canvas_size - radius)
    y = random.randint(radius, canvas_size - radius)
    positions.append((x, y))

    # Generate subsequent positions
    for _ in range(1, num_positions):
        while True:
            angle = random.uniform(0, 2 * math.pi)  # Random direction
            new_x = int(positions[-1][0] + constant_distance * math.cos(angle))
            new_y = int(positions[-1][1] + constant_distance * math.sin(angle))

            # Ensure the new position is within canvas boundaries
            if radius <= new_x <= canvas_size - radius and radius <= new_y <= canvas_size - radius:
                positions.append((new_x, new_y))
                break

    return positions

# Function to handle canvas clicks
def on_canvas_click(event):
    global current_position_index, errors, start_time

    # Get current target position
    target_x, target_y = target_positions[current_position_index]

    # Check if the click is within the target
    distance = ((event.x - target_x)**2 + (event.y - target_y)**2)**0.5
    if distance <= target_radius:
        if current_position_index == 0:
            start_time = time()  # Start timing on the first correct click
        click_times.append(time() - start_time)  # Store time taken for this click
        start_time = time()  # Reset the timer for the next target
        current_position_index += 1  # Move to the next target

        if current_position_index < len(target_positions):
            move_target()  # Move the target to the next position
        else:
            end_experiment()  # Finish the experiment
    else:
        errors += 1  # Count errors for clicks outside the target

# Function to move the target to the next position
def move_target():
    global current_position_index
    target_x, target_y = target_positions[current_position_index]
    canvas.coords(target_circle, target_x - target_radius, target_y - target_radius,
                  target_x + target_radius, target_y + target_radius)

# Function to end the experiment and save results
def end_experiment():
    # Calculate the average click time
    average_time = sum(click_times) / len(click_times) if click_times else 0

    # Append the average time to averaged_times.txt
    with open("averaged_times.txt", "a") as time_file:
        time_file.write(f"{average_time:.2f}\n")

    # Append the number of errors to errors.txt
    with open("errors.txt", "a") as error_file:
        error_file.write(f"{errors}\n")

    # Display a message and close the program
    print("Experiment Complete!")
    print(f"Average time appended to averaged_times.txt")
    print(f"Number of errors appended to errors.txt")
    root.destroy()

# Generate dynamic positions with a random starting point and constant distances
target_positions = generate_positions(num_targets, canvas_size, target_radius)

# Setup the tkinter window
root = tk.Tk()
root.title("Click the Target Experiment")

# Create a canvas
canvas = tk.Canvas(root, width=canvas_size, height=canvas_size, bg="white")
canvas.pack()

# Create the initial target
target_x, target_y = target_positions[0]
target_circle = canvas.create_oval(target_x - target_radius, target_y - target_radius,
                                   target_x + target_radius, target_y + target_radius,
                                   fill="red")

# Bind the click event
canvas.bind("<Button-1>", on_canvas_click)

# Run the application
root.mainloop()