import random
import cv2
import numpy as np
import pygame

# Initialize Pygame and font
pygame.init()
font = pygame.font.Font(None, 50)

# List of emojis
emojis = ['😀', '😃', '😄', '😁', '😆', '😅', '😂', '🤣', '😊', '😇']

def replace_with_emoji(frame, contour_detectors):
    for detected_detector in contour_detectors:
        x, y, w, h = detected_detector
        random_emoji = random.choice(emojis)
        emoji_surface = font.render(random_emoji, True, (255, 255, 255))  # Render text surface with white color
        emoji_surface = pygame.transform.rotate(emoji_surface, 90)  # Rotate emoji surface by 90 degrees
        emoji_rect = emoji_surface.get_rect(center=(x + w // 2, y + h // 2))

        # Convert emoji surface to numpy array
        emoji_array = pygame.surfarray.array3d(emoji_surface)
        emoji_array = cv2.cvtColor(emoji_array, cv2.COLOR_RGB2BGR)

        # Resize emoji array to fit within detected contour region
        emoji_height, emoji_width, _ = emoji_array.shape
        scaling_factor = min(h / emoji_height, w / emoji_width)
        emoji_array_resized = cv2.resize(emoji_array, (int(emoji_width * scaling_factor), int(emoji_height * scaling_factor)))

        # Blend emoji with the frame
        x_offset = x + (w - emoji_array_resized.shape[1]) // 2
        y_offset = y + (h - emoji_array_resized.shape[0]) // 2
        frame[y_offset:y_offset + emoji_array_resized.shape[0], x_offset:x_offset + emoji_array_resized.shape[1]] = emoji_array_resized

    return frame
