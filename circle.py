from PIL import Image, ImageDraw, ImageSequence
import numpy as np

# Parameters
num_frames = 16  # Number of frames in the animation
sprite_sheet_path = "./sprite_sheet_20.png"  # Path to the existing sprite sheet
target_size = (300, 300)  # Target size for the output frames
radius = 1000  # Radius of the circle
canvas_size = 2400  # Canvas size

# Load the sprite sheet
sprite_sheet = Image.open(sprite_sheet_path)
frame_width = sprite_sheet.width // num_frames
frame_height = sprite_sheet.height

# Extract frames from the sprite sheet
frames = []
for i in range(num_frames):
    frame = sprite_sheet.crop((i * frame_width, 0, (i + 1) * frame_width, frame_height))
    frames.append(frame.resize(target_size, Image.ANTIALIAS))

# Create a blank canvas with a white background
canvas = Image.new("RGBA", (canvas_size, canvas_size), (255, 255, 255, 255))
draw = ImageDraw.Draw(canvas)

# Calculate the center of the canvas
center_x = canvas_size // 2
center_y = canvas_size // 2

# Draw the outer circle, center point, and inner circle
draw.ellipse((center_x - radius, center_y - radius, center_x + radius, center_y + radius), outline="black")
draw.ellipse((center_x - 3, center_y - 3, center_x + 3, center_y + 3), fill="black")
draw.ellipse((center_x - 200, center_y - 200, center_x + 200, center_y + 200), outline="black")

# Place frames on the circle and rotate
for i, frame in enumerate(frames):
    angle = 2 * np.pi * i / num_frames
    rotated_frame = frame.rotate(-angle * 180 / np.pi, expand=True)
    frame_width, frame_height = rotated_frame.size
    x = center_x + 0.8 * radius * np.cos(angle) - frame_width // 2
    y = center_y + 0.8 * radius * np.sin(angle) - frame_height // 2
    canvas.paste(rotated_frame, (int(x), int(y)), rotated_frame)

# Save the circle image
circle_image_path = "./circle_image_from_sprite.png"
canvas.save(circle_image_path)

# Save as GIF
gif_path = "./circle_animation_from_sprite.gif"
frames[0].save(gif_path, save_all=True, append_images=frames[1:], optimize=False, duration=100, loop=0)
