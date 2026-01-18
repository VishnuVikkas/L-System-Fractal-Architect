# This program creates an interactive L-System fractal generator using Tkinter for the GUI and Turtle for drawing.
# L-Systems are formal grammars used to model the growth processes of plant development and generate fractals.

import tkinter as tk
import turtle

# ---------------- L-SYSTEM ENGINE ----------------
# This function expands an L-System string based on given rules and number of iterations.
def expand_lsystem(axiom, rules, iterations):
    current = axiom  # Start with the initial axiom string
    for _ in range(iterations):  # Apply rules for the specified number of iterations
        next_string = []
        for ch in current:  # Process each character in the current string
            if ch in rules:  # If the character has a replacement rule
                next_string.append(rules[ch])  # Replace with the rule's output
            else:
                next_string.append(ch)  # Keep the character as is
        current = ''.join(next_string)  # Update current string for next iteration
    return current  # Return the final expanded string

# ---------------- DRAWING ENGINE ----------------
# This function interprets the L-System string and draws the fractal using Turtle graphics.
def draw_lsystem(t, instructions, angle):
    stack = []  # Stack to save and restore turtle positions and headings for branching
    length = len(instructions)  # Total length of instructions for gradient calculation

    turtle.tracer(0, 0)  # Disable animation for faster drawing

    for i, cmd in enumerate(instructions):  # Iterate through each command in the instructions
        # Set pen color with a gradient effect based on progress through the string
        t.pencolor(i / length, 0.6, 1 - i / length)

        if cmd == 'F':  # Move forward and draw a line
            t.forward(5)
        elif cmd == '+':  # Turn right by the specified angle
            t.right(angle)
        elif cmd == '-':  # Turn left by the specified angle
            t.left(angle)
        elif cmd == '[':  # Push current position and heading onto the stack (start branch)
            stack.append((t.position(), t.heading()))
        elif cmd == ']':  # Pop position and heading from stack and restore (end branch)
            pos, head = stack.pop()
            t.penup()  # Lift pen to move without drawing
            t.goto(pos)  # Go to saved position
            t.setheading(head)  # Set saved heading
            t.pendown()  # Lower pen to resume drawing

    turtle.update()  # Update the screen to show the drawing

# ---------------- GUI CALLBACK ----------------
# This function is called when the "Generate" button is pressed. It reads inputs, generates the L-System, and draws it.
def generate():
    t.reset()  # Clear the turtle's drawing
    t.speed(0)  # Set turtle speed to fastest
    t.left(90)  # Orient turtle upward
    t.penup()  # Lift pen
    t.goto(0, -250)  # Move to bottom center of canvas
    t.pendown()  # Lower pen to start drawing

    axiom = axiom_entry.get()  # Get axiom from input field
    angle = float(angle_entry.get())  # Get angle from input field
    iterations = int(iter_entry.get())  # Get iterations from input field

    # Parse the rules from the input string into a dictionary
    rules = {}
    raw_rules = rules_entry.get().split(',')  # Split rules by comma
    for r in raw_rules:
        if ':' in r:  # Ensure rule has key:value format
            k, v = r.split(':')  # Split into key and value
            rules[k.strip()] = v.strip()  # Add to rules dict, stripping whitespace

    final_string = expand_lsystem(axiom, rules, iterations)  # Expand the L-System
    draw_lsystem(t, final_string, angle)  # Draw the fractal

# ---------------- TKINTER + TURTLE SETUP ----------------
# Set up the main Tkinter window and integrate Turtle graphics for drawing.
root = tk.Tk()
root.title("L-System Fractal Architect")  # Set window title

# Create frames for layout: controls on the left, canvas on the right
control_frame = tk.Frame(root, padx=10, pady=10)
control_frame.pack(side=tk.LEFT, fill=tk.Y)  # Pack on left, fill vertically

canvas_frame = tk.Frame(root)
canvas_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)  # Pack on right, fill and expand

# Create a Tkinter canvas for Turtle to draw on
canvas = tk.Canvas(canvas_frame, width=800, height=600)
canvas.pack()  # Pack the canvas into the frame

# Create Turtle screen on the canvas
screen = turtle.TurtleScreen(canvas)
screen.colormode(1.0)  # Set color mode to 0-1 for RGB values

# Create the turtle object
t = turtle.RawTurtle(screen)
t.hideturtle()  # Hide the turtle icon
t.speed(0)  # Set speed to fastest

# ---------------- CONTROLS ----------------
# Create input fields and labels for user to enter L-System parameters.
tk.Label(control_frame, text="Axiom").pack(anchor='w')  # Label for axiom input
axiom_entry = tk.Entry(control_frame)  # Entry field for axiom
axiom_entry.insert(0, "F")  # Default value
axiom_entry.pack(fill='x')  # Pack and fill horizontally

tk.Label(control_frame, text="Rules (F:FF+[+F-F-F]-[-F+F+F])").pack(anchor='w')  # Label for rules input
rules_entry = tk.Entry(control_frame)  # Entry field for rules
rules_entry.insert(0, "F:F[+F]F[-F]F")  # Default value
rules_entry.pack(fill='x')  # Pack and fill horizontally

tk.Label(control_frame, text="Angle").pack(anchor='w')  # Label for angle input
angle_entry = tk.Entry(control_frame)  # Entry field for angle
angle_entry.insert(0, "25")  # Default value
angle_entry.pack(fill='x')  # Pack and fill horizontally

tk.Label(control_frame, text="Iterations").pack(anchor='w')  # Label for iterations input
iter_entry = tk.Entry(control_frame)  # Entry field for iterations
iter_entry.insert(0, "4")  # Default value
iter_entry.pack(fill='x')  # Pack and fill horizontally

tk.Button(control_frame, text="Generate", command=generate).pack(pady=10)  # Button to trigger generation

root.mainloop()  # Start the Tkinter event loop
