from pynput import keyboard
from pynput.keyboard import Key, Controller
import file_handler
import time

start_time: float
end_time: float
recorded_key_presses: dict = {}


def user_boolean(explanation):
    while True:
        try:
            result = input(f"{explanation} \n1 = yes\n2 = no\n")
            if result == "1":
                return True
            elif result == "2":
                return False
            else:
                raise TypeError
        except TypeError:
            print(f"Enter only 1 or 2.")


def record_keyboard():
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

    print("press esc to stop recording keyboard inputs.")
    start_time = time.perf_counter()
    recorded_key_presses = []
    keys_pressed = set()
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
    listener.stop()
    return recorded_key_presses


def replay(inputs):
    try:
        controller = Controller()
        for action in inputs:
            time.sleep(float(action[0]))
            if action[1][-1] == "p":
                if action[1][0] == "'":
                    controller.press(str(action[1][1:-3]))
                elif action[1][0] == "K":
                    press_special_key(action[1][:-2], controller)
            elif action[1][-1] == "r":
                if action[1][0] == "'":
                    controller.release(str(action[1][1:-3]))
                elif action[1][0] == "K":
                    release_special_key(action[1][:-2], controller)
    except Exception:
        print("error occurred while trying to replay the inputs." + inputs)


def wait_for_go(explanation):
    def on_press(key):
        pass

    def on_release(key):
        if key == keyboard.Key.tab:
            return False

    print(explanation)
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
    listener.stop()


def press_special_key(key, controller):
    if key == "Key.space":
        controller.press(Key.space)
    elif key == "Key.shift_l":
        controller.press(Key.shift_l)
    elif key == "Key.shift_r":
        controller.press(Key.shift_r)
    elif key == "Key.enter":
        controller.press(Key.enter)
    elif key == "Key.left":
        controller.press(Key.left)
    elif key == "Key.right":
        controller.press(Key.right)
    elif key == "key.down":
        controller.press(Key.down)
    elif key == "key.up":
        controller.press(Key.up)
    elif key == "Key.backspace":
        controller.press(Key.backspace)


def release_special_key(key, controller):
    if key == "Key.space":
        controller.release(Key.space)
    elif key == "Key.shift_l":
        controller.release(Key.shift_l)
    elif key == "Key.shift_r":
        controller.release(Key.shift_r)
    elif key == "Key.enter":
        controller.release(Key.enter)
    elif key == "Key.left":
        controller.release(Key.left)
    elif key == "Key.right":
        controller.release(Key.right)
    elif key == "key.down":
        controller.release(Key.down)
    elif key == "key.up":
        controller.release(Key.up)
    elif key == "Key.backspace":
        controller.release(Key.backspace)


def run():
    finished = False
    while not finished:
        wait_for_go("press tab to start recording keyboard inputs.")
        recorded_inputs = record_keyboard()
        if user_boolean("would you like to replay the inputs you just recorded?"):
            wait_for_go("press tab to replay recorded keyboard inputs.")
            replay(recorded_inputs)
            print("finished replaying inputs")
        if user_boolean("would you like to save your inputs to a file?"):
            file_handler.make_file(recorded_inputs)
        if not user_boolean("would you like to record your keyboard again?"):
            finished = True
    print("done")


if __name__ == "__main__":
    run()
