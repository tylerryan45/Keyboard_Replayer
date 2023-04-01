from pynput import keyboard
import time


def run():
    start_time: float
    end_time: float
    recorded_key_presses: list = []

    def on_press(key):
        global start_time
        start_time = time.time()

    def on_release(key):
        global start_time
        global end_time
        end_time = time.time()
        if key == keyboard.Key.esc:
            return False
        recorded_key_presses.append((key, end_time - start_time))

    with keyboard.Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()
    return recorded_key_presses


if __name__ == "__main__":
    print(run())