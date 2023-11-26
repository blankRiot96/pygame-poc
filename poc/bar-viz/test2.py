import sys

import numpy as np
import pygame
from pydub import AudioSegment

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Music Visualizer")

# Set up audio
pygame.mixer.init()

# Convert MP3 to WAV (Pygame does not support MP3 directly)
mp3_file = "hiding-in-the-dark.mp3"
wav_file = "hiding-in-the-dark.wav"
AudioSegment.from_mp3(mp3_file).export(wav_file, format="wav")
sound = pygame.mixer.Sound(wav_file)

# Set up FFT parameters
chunk_size = 2048
sample_rate = 44100

# Initialize Pygame clock
clock = pygame.time.Clock()


def draw_bars(spectrum):
    bar_width = width // (chunk_size // 2)
    print(bar_width)
    for i in range(chunk_size // 2):
        bar_height = max(2, spectrum[i] / 2)
        pygame.draw.rect(
            screen,
            (255, 255, 255),
            (i * bar_width, height - bar_height, bar_width, bar_height),
        )


# Main loop
running = True
sound.play(-1)  # Play sound in a loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sound.stop()
            pygame.quit()
            sys.exit()

    # Get audio data
    sound_array = pygame.sndarray.array(sound)
    audio_data = np.frombuffer(sound_array, dtype=np.int16)

    # Apply FFT
    spectrum = np.fft.fft(audio_data[-chunk_size:])
    spectrum = np.abs(spectrum)[: chunk_size // 2]

    # Normalize the spectrum values
    spectrum = (spectrum / max(spectrum)) * height

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw the bars
    draw_bars(spectrum)

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(30)

# Quit Pygame
pygame.quit()
