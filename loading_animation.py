import sys
import time

def loading_animation(duration):
    animation = "|/-\\"
    idx = 0
    end_time = time.time() + duration
    while time.time() < end_time:
        sys.stdout.write("\rInstalando requerimientos " + animation[idx % len(animation)])
        sys.stdout.flush()
        idx += 1
        time.sleep(0.1)

try:
    duration = 5  # Duración en segundos
    loading_animation(duration)
finally:
    sys.stdout.write("\n")