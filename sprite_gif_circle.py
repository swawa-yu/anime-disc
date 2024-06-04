from PIL import Image, ImageDraw, ImageSequence
import numpy as np


# Function to generate a frame with the snake in a specific wave position
def generate_frame(img, amplitude, phase, num_frames, frame_number, target_size):
    print(f"generating frame {frame_number}")
    img = img.convert("RGBA")
    width, height = img.size
    pixels = img.load()

    new_img = Image.new("RGBA", img.size)
    new_pixels = new_img.load()

    for x in range(width):
        for y in range(height):
            if pixels[x, y][3] > 0:  # Check if not transparent
                new_y = int(y + amplitude * np.sin(2 * np.pi * (x / width) + (frame_number / num_frames) * 2 * np.pi + phase))
                if new_y >= 0 and new_y < height:
                    new_pixels[x, new_y] = pixels[x, y]

    # Crop the image to the target size
    crop_x = (width - target_size[0]) // 2
    crop_y = (height - target_size[1]) // 2
    new_img = new_img.crop((crop_x, crop_y, crop_x + target_size[0], crop_y + target_size[1]))

    return new_img


# Parameters for the wave animation
amplitude = 40  # Amplitude of the wave
num_frames = 12  # Number of frames in the animation
img_path = "./img.jpeg"
original_size = (800, 500)  # Original size for the output frames
target_size = (480, 300)  # Target size after resizing
radius = 1000  # Radius of the circle
canvas_size = 2400  # Canvas size

# Generate frames
frames = [generate_frame(Image.open(img_path), amplitude, 0, num_frames, i, original_size) for i in range(num_frames)]

# Create a sprite sheet
sprite_sheet_width = target_size[0] * num_frames
sprite_sheet_height = target_size[1]
sprite_sheet = Image.new("RGBA", (sprite_sheet_width, sprite_sheet_height))

for i, frame in enumerate(frames):
    sprite_sheet.paste(frame, (i * target_size[0], 0))

# Save the sprite sheet
sprite_sheet_path = f"./sprite_sheet_{amplitude}.png"
sprite_sheet.save(sprite_sheet_path)

# Save as GIF
gif_path = f"./animation_{amplitude}.gif"
frames[0].save(gif_path, save_all=True, append_images=frames[1:], optimize=False, duration=100, loop=0)

# Resize frames to target size
frames = [frame.resize(target_size, Image.ANTIALIAS) for frame in frames]

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
    x = center_x + 0.75 * radius * np.cos(angle) - frame_width // 2
    y = center_y + 0.75 * radius * np.sin(angle) - frame_height // 2
    canvas.paste(rotated_frame, (int(x), int(y)), rotated_frame)

# Save the sprite sheet
sprite_sheet_path = f"./circle_sprite_{amplitude}.png"
canvas.save(sprite_sheet_path)
