from PIL import Image, ImageDraw, ImageSequence
import numpy as np


# Function to generate a frame with the snake in a specific wave position
def generate_frame(img, amplitude, phase, num_frames, frame_number, target_size):
    print(f"generating frame{frame_number}")
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
amplitude = 20  # Amplitude of the wave
num_frames = 16  # Number of frames in the animation
img_path = "./img.jpeg"
target_size = (800, 800)  # Target size for the output frames

# Generate frames
frames = [generate_frame(Image.open(img_path), amplitude, 0, num_frames, i, target_size) for i in range(num_frames)]

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
