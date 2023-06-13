import Keyboard_Replayer


def create_file(file_name):
    try:
        open(file_name + ".txt", "x")
        return True
    except FileExistsError:
        while True:
            response = input(
                print(f"{file_name}.txt already exists. Would you like to overwrite it? Press enter to confirm "
                      f"input. \n1 = yes\n2 = no"))
            try:
                if response == "1":
                    return True
                elif response == "2":
                    return False
                else:
                    raise TypeError
            except TypeError:
                print(f"enter only 1 or 2.")


def write_file(recorded_inputs, file_name):
    file = open(file_name + ".txt", "w")
    for action in recorded_inputs:
        file.write(str(action) + "\n")


def get_file():
    while True:
        try:
            file_name = input("Enter the name of the file you would like to replay.\n"
                              "Press 1 if you'd like to quit the app\n")
            if file_name == "1":
                quit(1)
            file = open(str(file_name) + ".txt", "r")
            return file
        except FileNotFoundError:
            print(f"{file_name} not found")


def check_for_comma(line):
    if line[-7:-6] == ",":
        return True
    else:
        return False


def create_inputs_from_input_file():
    file = get_file()
    file_inputs = []
    for line in file:
        line = line.split(",")
        time_amount = float(line[0][1:])
        # if a line has a comma, the line after the split will contain 3 parts: the time between instructions,
        # followed by the instruction broken into two parts by the split.
        if len(line) != 3:  # key pressed is not a comma
            instruction = line[1][2:-3]
            file_inputs.append((time_amount, instruction))
        else:  # key pressed is a coma
            instruction = f"\',\' {line[2][-4:-3]}"
            file_inputs.append((time_amount, instruction))
    return file_inputs, file


def run():
    finished = False
    while not finished:
        recorded_inputs, file = create_inputs_from_input_file()
        Keyboard_Replayer.wait_for_go(f"press enter to replay keyboard inputs from {file.name}.")
        Keyboard_Replayer.replay(recorded_inputs)
        result = input("would you like to replay another file? \n1 = yes\n2 = no\n")
        if result == "2":
            finished = True
    print("done")


if __name__ == "__main__":
    run()
