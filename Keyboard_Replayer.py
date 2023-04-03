from pynput import keyboard
from pynput.keyboard import Key, Controller
import time

start_time: float
end_time: float
recorded_key_presses: dict = {}


def keyboard_record():
    global start_time
    global end_time
    global keys_pressed
    global recorded_key_presses

    def on_press(key):
        global start_time
        global end_time
        end_time = time.perf_counter()
        if key == keyboard.Key.esc:
            return False
        incoming_key_stroke = (end_time - start_time, str(key) + " p")
        if recorded_key_presses == []:
            recorded_key_presses.append(incoming_key_stroke)
            keys_pressed.add(key)
            start_time = time.perf_counter()
        elif key not in keys_pressed:
            recorded_key_presses.append(incoming_key_stroke)
            keys_pressed.add(key)
            start_time = time.perf_counter()

    def on_release(key):
        global start_time
        global end_time
        end_time = time.perf_counter()
        outgoing_key_stroke = (end_time - start_time, str(key) + " r")
        recorded_key_presses.append(outgoing_key_stroke)
        keys_pressed.remove(key)
        start_time = time.perf_counter()

    start_time = time.perf_counter()
    recorded_key_presses = []
    keys_pressed = set()
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
    return recorded_key_presses


def press_special_key(key, keyboard):
    if key == "Key.space":
        keyboard.press(Key.space)
    elif key == "Key.shift_l":
        keyboard.press(Key.shift_l)
    elif key == "Key.shift_r":
        keyboard.press(Key.shift_r)
    elif key == "Key.enter":
        keyboard.press(Key.enter)
    elif key == "Key.left":
        keyboard.press(Key.left)
    elif key == "Key.right":
        keyboard.press(Key.right)
    elif key == "key.down":
        keyboard.press(Key.down)
    elif key == "key.up":
        keyboard.press(Key.up)
    elif key == "Key.backspace":
        keyboard.press(Key.backspace)


def release_special_key(key, keyboard):
    if key == "Key.space":
        keyboard.release(Key.space)
    elif key == "Key.shift_l":
        keyboard.release(Key.shift_l)
    elif key == "Key.shift_r":
        keyboard.release(Key.shift_r)
    elif key == "Key.enter":
        keyboard.release(Key.enter)
    elif key == "Key.left":
        keyboard.release(Key.left)
    elif key == "Key.right":
        keyboard.release(Key.right)
    elif key == "key.down":
        keyboard.release(Key.down)
    elif key == "key.up":
        keyboard.release(Key.up)
    elif key == "Key.backspace":
        keyboard.release(Key.backspace)


def replay(inputs):
    keyboard = Controller()
    for i in range(len(inputs)):
        action = inputs[i]
        time.sleep(float(action[0]))
        if action[1][-1] == "p":
            if action[1][0] == "'":
                keyboard.press(str(action[1][1:-3]))
            elif action[1][0] == "K":
                press_special_key(action[1][:-2], keyboard)
        elif action[1][-1] == "r":
            if action[1][0] == "'":
                keyboard.release(str(action[1][1:-3]))
            elif action[1][0] == "K":
                release_special_key(action[1][:-2], keyboard)


if __name__ == "__main__":
    recorded_inputs = keyboard_record()
    print(recorded_inputs)
    # wait_for_go()
    replay(recorded_inputs)
    print("replay done")
    time.sleep(5)
