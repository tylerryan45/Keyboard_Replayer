from pynput import keyboard
from pynput.keyboard import Key, Controller
import time

start_time: float
end_time: float
recorded_key_presses: dict = {}


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


def wait_for_go(explanation):

    def on_press(key):
        pass

    def on_release(key):
        if key == keyboard.Key.enter:
            time.sleep(.1)
            return False

    print(explanation)
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
    listener.stop()


def replay(inputs):
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


def create_file(file_name):
    try:
        open(file_name + ".txt", "x")
        return True
    except FileExistsError:
        print(f"{file_name}.txt already exists. Would you like to overwrite it? Press enter to confirm input. "
              f"\n1 = yes\n2 = no")
        while True:
            try:
                response = input()
                if response == "1":
                    return True
                elif response == "2":
                    return False
                else:
                    raise TypeError
            except TypeError:
                print(f"enter only 1 or 2. \nWould you like to overwrite {file_name}.txt? \n1 = yes\n2 = no")


def user_wants_to_save_record():
    while True:
        try:
            print("Would you like to save the recorded inputs? Press enter to confirm input. \n1 = yes\n2 = no")
            result = input()
            if result == "1":
                return True
            elif result == "2":
                return False
            else:
                raise TypeError
        except TypeError:
            print(f"Enter only 1 or 2.")


def write_file(recorded_inputs, file_name):
    file = open(file_name + ".txt", "w")
    for action in recorded_inputs:
        file.write(str(action) + "\n")


def make_file(recorded_inputs):
    file_name = input("Enter the name of the file you would like to save the inputs to. Press enter when finished "
                      "writing file name. \n")
    if create_file(file_name):
        write_file(recorded_inputs, file_name)
        print("file created")


def get_file(file_name):
    try:
        file = open(str(file_name) + ".txt", "r")
        return file
    except FileNotFoundError:
        print(f"{file_name} not found")


def create_inputs_from_input_file():
    file = get_file(input("Enter the name of the file you would like to replay.\n"))
    file_inputs = []
    for line in file:
        line = line.split(",")
        time_amount = float(line[0][1:])
        instruction = line[1][2:-3]
        file_inputs.append((time_amount, instruction))
    return file_inputs


if __name__ == "__main__":
    wait_for_go("press enter to start recording keyboard inputs.")
    recorded_inputs = record_keyboard()
    wait_for_go("press enter to replay recorded keyboard inputs.")
    replay(recorded_inputs)
    print("finished replaying inputs")
    if user_wants_to_save_record():
        make_file(recorded_inputs)
    print("done")
    # recorded_inputs = create_inputs_from_input_file()
    # print(recorded_inputs)
    # wait_for_go()
    # replay(recorded_inputs)


