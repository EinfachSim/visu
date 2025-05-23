import pygame
from view import Screen
from audio import AudioInput
import threading
import numpy as np

pygame.init()

screen_manager = Screen.from_yaml("screen_configs.yaml")

screen = screen_manager.get_pygame_screen()
clock = pygame.time.Clock()
dt = clock.tick(screen_manager.fps)

trail_surface = pygame.Surface((400, 400), pygame.SRCALPHA)  # Alpha-enabled surface

running = True

audioinp = AudioInput(monitor=False)

audio_thread = threading.Thread(target=audioinp.stream_audio)
audio_thread.start()

num_bars = 40

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    trail_surface.fill((0, 0, 0, 255))  # last number = alpha (0–255), lower = longer trails
    screen.blit(trail_surface, (0, 0))
    if isinstance(audioinp.data, np.ndarray):
        #x_offset = audioinp.data[:, 0].mean()
        audio = audioinp.data.sum(axis=1)
        
        windowed = audio * np.hanning(len(audio))

        amplitude = np.sqrt(np.mean(windowed**2))
        freqs = np.fft.rfftfreq(len(audio), d=1/44100)
        magnitudes = np.abs(np.fft.rfft(windowed))

        valid = freqs <= 20000
        freqs = freqs[valid]
        magnitudes = magnitudes[valid]

        valid = freqs >= 20
        freqs = freqs[valid]
        magnitudes = magnitudes[valid]

        in_bin = (freqs >= 20) & (freqs < 100)
        low_amplitude = 0
        if np.any(in_bin):
            low_amplitude = magnitudes[in_bin].mean()

        x_pos = screen_manager.width/2 #+ low_amplitude * 10
        y_pos = screen_manager.height/2 #- amplitude * 10000
        pygame.draw.circle(screen, (255, 255, 255), (int(x_pos), int(y_pos)), low_amplitude * 10)



    pygame.display.flip()

    dt = clock.tick(screen_manager.fps)

pygame.quit()
