import tkinter as tk
import random

def generate_random_color():
    """Generates a random color in hexadecimal format."""
    return "#{:02x}{:02x}{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def draw_bars(canvas, num_bars, width, height, time_markers, beat_pattern, current_time, bar_width_factor=0.8):
    """
    Draws the bars representing the polyrhythm.

    Args:
        canvas: The Tkinter canvas to draw on.
        num_bars: The number of bars.
        width: The width of the canvas.
        height: The height of the canvas.
        time_markers: List of time markers (in beats) for each bar.
        beat_pattern: List of lists.  Each sublist represents the on/off pattern for a bar.
        current_time: The current time (in beats).
        bar_width_factor:  The fraction of the available space each bar should occupy.
    """
    canvas.delete("all")  # Clear the canvas

    bar_spacing = width / (num_bars + 1)
    bar_width = bar_spacing * bar_width_factor # Make bars slightly narrower
    max_beat_time = max(time_markers) #get the max time
    beat_height = height / max_beat_time

    for i in range(num_bars):
        x = (i + 1) * bar_spacing
        color = generate_random_color()
        marker = time_markers[i]
        # Ensure beat_pattern[i] exists and has enough elements.
        pattern = beat_pattern[i] if i < len(beat_pattern) else []
        #Make sure that the pattern does not cause an error.
        safe_current_time = int(current_time) % len(pattern) if pattern else 0

        # Draw the main bar
        canvas.create_rectangle(x - bar_width / 2, height, x + bar_width / 2, 0, fill=color)

        # Draw the time markers
        for j in range(1, marker + 1):
            y = height - j * beat_height
            canvas.create_line(x - bar_width / 2, y, x + bar_width / 2, y, fill="white")

        # Draw the beat pattern
        if pattern:
            for index, beat_state in enumerate(pattern):
                beat_y = height - (index + 1) * beat_height
                if beat_state == 1:
                    canvas.create_rectangle(x - bar_width / 2, beat_y, x + bar_width / 2, beat_y + beat_height, fill="white")
        #Draw the current beat indicator
        if pattern:
            current_beat_y = height - (safe_current_time + 1) * beat_height
            canvas.create_rectangle(x - bar_width / 2, current_beat_y, x + bar_width / 2, current_beat_y + beat_height, fill="yellow")

def update_time(canvas, time, time_step, num_bars, time_markers, beat_pattern):
    """
    Updates the time and redraws the bars.

    Args:
        canvas: The Tkinter canvas.
        time: The current time.
        time_step: The amount to increment time by.
        num_bars: The number of bars.
        time_markers: The time markers for each bar.
        beat_pattern:  The beat pattern for each bar.
    """
    time[0] += time_step
    draw_bars(canvas, num_bars, int(canvas.cget("width")), int(canvas.cget("height")), time_markers, beat_pattern, time[0])
    canvas.after(100, update_time, canvas, time, time_step, num_bars, time_markers, beat_pattern)  # Update every 100 ms

def create_random_beat_pattern(length):
    """Creates a random beat pattern of 0s and 1s."""
    return [random.choice([0, 1]) for _ in range(length)]

def main():
    """Main function to create the Tkinter window and start the animation."""
    root = tk.Tk()
    root.title("Polyrhythm Visualizer")
    width = 800
    height = 600
    canvas = tk.Canvas(root, width=width, height=height, bg="black")
    canvas.pack()

    num_bars = 4
    time_markers = [4, 6, 8, 3]  # Example time signatures (beats per bar)
    # Create a list of beat patterns, one for each bar.
    beat_pattern = [create_random_beat_pattern(time_markers[i]) for i in range(num_bars)]
    time = [0.0]  # Use a list to make it mutable

    draw_bars(canvas, num_bars, width, height, time_markers, beat_pattern, time[0])  # Initial draw
    canvas.after(100, update_time, canvas, time, 0.1, num_bars, time_markers, beat_pattern)  # Start the update loop
    root.mainloop()

if __name__ == "__main__":
    main()
