from PIL import Image, ImageDraw

# Image size
width, height = 1200, 1200  

# Create a blank image with transparent background
image = Image.new("RGBA", (width, height), (255, 255, 255, 0))

# Create a draw object
draw = ImageDraw.Draw(image)

# Define dot properties
dot_radius = 500
dot_color = (255, 117, 20, 255)  # RGBA

# Center of the dot
center = (width // 2, height // 2)

# Draw the circle
draw.ellipse(
    (center[0] - dot_radius, center[1] - dot_radius,
     center[0] + dot_radius, center[1] + dot_radius),
    fill=dot_color
)

# Save as PNG
image.save("orange_dot.png", "PNG")