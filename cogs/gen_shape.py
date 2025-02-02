import random
from PIL import Image, ImageDraw

# Function to generate random shape
def generate_random_shape():
    # Create a blank image with white background
    img = Image.new("RGB", (400, 400), "white")
    draw = ImageDraw.Draw(img)

    # Randomize the shape to draw (circle, square, triangle, etc.)
    shape_type = random.choice([
        'circle', 'square', 'triangle', 'rectangle', 'waterbottle', 'apple', 'semicircle', 'trapezium', 'hexagon', 'rhombus', 'cat', 'laptop', 'scales', 'dip', 'bird', 'hourglass', 'skyline', 'river', 'butterfly', 'slinky'
    ])

    # Set the coordinates and size
    size = 200
    x, y = 100, 100  # Starting position of the shape

    if shape_type == 'circle':
        # Draw a circle
        draw.ellipse([x, y, x + size, y + size], outline="black", width=5)

    elif shape_type == 'square':
        # Draw a square
        draw.rectangle([x, y, x + size, y + size], outline="black", width=5)

    elif shape_type == 'triangle':
        # Draw a triangle
        draw.polygon([x, y + size + 50, x + size, y + size + 50, x + size / 2, y - size / 2 + 50], outline="black", width=5)

    elif shape_type == 'rectangle':
        # Draw a rectangle
        draw.rectangle([x - 50, y, x + size * 1.5 - 50, y + size], outline="black", width=5)

    elif shape_type == 'waterbottle':
        # Waterbottle shape (simplified representation)
        draw.rectangle([x + 40, y + 40, x + size - 40, y + size], outline="black", width=5)  # Bottle body
        draw.ellipse([x, y, x + size, y + 40], outline="black", width=5)  # Bottle cap

    elif shape_type == 'apple':
        # Apple shape (simplified)
        draw.ellipse([x, y, x + size, y + size], outline="black", width=5)  # Apple body
        draw.rectangle([x + size / 2 - 10, y - 20, x + size / 2 + 10, y], outline="black", width=5)  # Stem

    elif shape_type == 'semicircle':
        # Semi-Circle
        draw.arc([x, y, x + size, y + size], start=0, end=180, fill="black", width=5) 

    elif shape_type == 'trapezium':
        # Trapezium shape
        draw.polygon([x, y, x + size, y, x + size * 0.8, y + size, x + size * 0.2, y + size], outline="black", width=5)

    elif shape_type == 'hexagon':
        # Hexagon shape
        size = 100  # Decreased size for a smaller hexagon
        y -= 50  # Shift it upwards
        draw.polygon([x, y, 
                    x + size, y, 
                    x + size * 1.5, y + size * 0.866, 
                    x + size, y + size * 1.732, 
                    x, y + size * 1.732, 
                    x - size * 0.5, y + size * 0.866], 
                    outline="black", width=5)

    elif shape_type == 'rhombus':
        # Rhombus shape
        y += 50
        draw.polygon([x, y, x + size / 2, y - size / 2, x + size, y, x + size / 2, y + size / 2, x, y], outline="black", width=5)

    elif shape_type == 'cat':
        # Cat shape (simplified)
        draw.ellipse([x, y, x + size, y + size], outline="black", width=5)  # Cat face
        draw.rectangle([x + size / 3, y + size / 2, x + size * 2 / 3, y + size], outline="black", width=5)  # Cat body

    elif shape_type == 'laptop':
        # Laptop shape (simplified)
        draw.rectangle([x, y + 40, x + size, y + size], outline="black", width=5)  # Laptop screen
        draw.rectangle([x + 50, y + size, x + size - 50, y + size + 30], outline="black", width=5)  # Laptop body

    elif shape_type == 'scales':
        # River shape (simplified with four arcs facing left in a vertical line)
        arc_height = 30  # Height of each arc
        arc_width = 50   # Width of each arc
        # Draw the four arcs facing left, one below the other
        for i in range(4):
            draw.arc([x, y + i * arc_height, x + arc_width, y + (i + 1) * arc_height], 
                    start=270, end=90, fill="black", width=5)
            
    elif shape_type == 'dip':
        # Arc with two horizontal lines at the top end
        arc_width = 70  # Width of the arc
        arc_height = 70  # Height of the arc
        line_length = 70  # Length of the horizontal lines
        line_offset = 35
        # Draw the arc
        draw.arc([x, y, x + arc_width, y + arc_height], start=0, end=180, fill="black", width=5)
        # Draw the left horizontal line
        draw.line([x, y + line_offset, x - line_length, y + line_offset], fill="black", width=5)
        # Draw the right horizontal line
        draw.line([x + arc_width, y + line_offset, x + arc_width + line_length, y + line_offset], fill="black", width=5)

    elif shape_type == 'bird':
        # Open V-shape using lines
        draw.line([x, y, x + size / 2, y + size], fill="black", width=5)  # Left line
        draw.line([x + size, y, x + size / 2, y + size], fill="black", width=5)  # Right line

    elif shape_type == 'hourglass':
        # Hourglass shape using two triangles
        lower_offset = 150
        # Upper triangle (pointing downwards)
        draw.polygon([x, y, x + size * 0.5, y, x + size * 0.5 / 2, y + size * 0.5], outline="black", width=5)
        # Lower triangle (pointing upwards)
        draw.polygon([x, y + size * 0.5 + lower_offset, x + size * 0.5, y + size * 0.5 + lower_offset, x + size * 0.5 / 2, y - size * 0.5 / 2 + lower_offset], outline="black", width=5)

    elif shape_type == 'skyline':
        # Increase the y offset to move the shape down
        y_offset = 20  # Adjust this value to move the lines further down
        # Line 1 (left vertical line)
        draw.line([x, y + y_offset, x, y + y_offset + size], fill="black", width=5)
        # Line 2 (middle vertical line)
        draw.line([x + 50, y + y_offset, x + 50, y + y_offset + size], fill="black", width=5)
        # Line 3 (right vertical line)
        draw.line([x + 100, y + y_offset, x + 100, y + y_offset + size], fill="black", width=5)
    
    elif shape_type == 'butterfly': 
        # Set the size and position for the semicircles
        x, y = 50, 50  # Top left corner for positioning
        size = 150
        # Draw the first semicircle
        draw.arc([x, y, x + size, y + size], start=270, end=90, fill="black", width=5)
        # Draw the second semicircle (mirrored)
        draw.arc([x + 200, y, x + size + 200, y + size], start=90, end=270, fill="black", width=5)
        
    elif shape_type == 'river': 
        # Set the size and position for the semicircles
        x, y = 100, 50  # Top left corner for positioning
        size = 150
        # Draw the first semicircle 
        draw.arc([x, y, x + size, y + size], start=90, end=270, fill="black", width=5)
        # Draw the second semicircle
        draw.arc([x, y + size, x + size, y + size * 2], start=270, end=90, fill="black", width=5)

    elif shape_type == 'slinky': 
        # Define initial positions and size for the ellipses
        x, y = 100, 150
        width, height = 50, 100
        num_ellipses = 4  # Number of overlapping ellipses

        # Draw overlapping ellipses to create a slinky effect
        for i in range(num_ellipses):
            # Adjust the y-position for each ellipse to create overlap
            draw.ellipse([x + i * 30, y, x + i * 30 + width, y + height], outline="black", width=5)
        
    # Save the image
    img.save("random_shape.png")

    # Show the generated shape
    # img.show()  # Display the image
    # print(f"A random {shape_type} has been generated and saved as 'random_shape.png'.")

# # Generate and save the random shape
# generate_random_shape()