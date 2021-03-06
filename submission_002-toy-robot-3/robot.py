#Global list of valid commands
list_of_commands = ["off", "help", "forward", "back", "left", "right", "sprint","history", "replay"]

#Global silent boolean
bool_silent = False
#Global history list
history = []

def robot_name():
    """Asks the user to input a name for their robot

    Returns:
        name [str]: Returns the name of the robot
    """
    name = input("What do you want to name your robot? ")
    print(f"{name}: Hello kiddo!")
    return name

def get_commands(name):
    """Get's commands from the user, checks if it is a valid command,
       and if not will print out error message

    Args:
        name [str]: name of the robot

    Returns:
        user_input [str]: returns string of user's input

    """
    user_input = input(f"{name}: What must I do next? ")
    while len(user_input)==0 or not valid_input(user_input):
        print(f"{name}: Sorry, I did not understand '{user_input}'.")
        user_input = input(f"{name}: What must I do next? ")
    user_input = user_input.lower()
    command_history(user_input)
    return user_input

def command_history(command):
    """Adds valid user input into the global history list

    Args:
        command [str]: string of valid user input
    """
    history.append(command)

def clean_list(history):
    """Filters out "" and "" from the list that stores all valid inputs

    Args:
        history [list]: list of all valid commands

    Returns:
        [list]: returns a new list after filtering out unwanted strings
    """
    return list(filter(lambda a: a != "history" and a!="help", history))

def do_history(history):
    """Returns the a local variable of history after removin the "history" and "help" commands

    Args:
        history [list]: list of all the commands that have been input

    Returns:
        history [list]: returns the new list of history that has been filtered
    """
    history = clean_list(history)
    return history

def replay_com(command):
    """Checks for valid replay commands. Returns True/False if valid commands

    Args:
        command [list]: list of user input

    Returns:
        [Boolean]: returns True or False
    """
    replay_list = ['silent', 'reversed']
    command[1] = command[1].lower()
    arg = command[1].split()
    if is_dash(command) or arg[0].isdigit() or command[1] in replay_list or ("silent" in arg and "reversed" in arg):
        return True
    else:
        return False

def valid_input(user_input):
    """Splits the string of the user input and checks if it is a valid command
       and if it is and digit

    Args:
        user_input [str]: string of the user input

    Returns:
        [boolean]: returns True or False if valid command and True or False 
        if there is a second element or if second element is a digit
    """
    one_list = ["left", "right", "help", "history", "off"]
    command = user_input.split(" ", 1)
    if len(command)==1 and command[0].lower() in one_list:
        return command[0].lower() in list_of_commands
    elif command[0].lower() not in one_list:
        return command[0].lower() in list_of_commands and (len(command)==1 or is_int(command) or replay_com(command))
    else:
        return False


def clean_input(user_input):
    """Splits up user input, seperates commands from flags, numbers or one-word commands,
       and makes sure single commands have no extra value => will return NONE

    Args:
        user_input [str]: string from the user

    Returns:
        command[0] [str]: returns the command in lowercase letters so that we can
                          match it easily to the conditionals
        command[1] [str]: returns all the following flags for replay, steps 
                          or NONE if command is of length 1
    """
    command = user_input.split(" ", 1)
    command[0] = command[0].lower()
    if len(command)>1:
        command[1] = command[1].lower()
        return command[0], command[1]
    else:
        return command[0], None


def is_dash(command):
    """Checks if the second element has a "-" character. Checks if the integer
       n is greater than m. Checks if the characters before and after the "-" are 
       integers.

    Args:
        command (list): list of the user input

    Returns:
        [Boolean]: Returns True or False if there is a "-" and that n is greater than m
    """
    n, m = 0,0
    arg = command[1].split()
    dash = False
    for a in arg:
        if "-" in a:
            n, m = a.split("-", 1)
            try:
                int(n)
                int(m)
                dash = True 
            except:
                return False
    if dash and n>m:
        return True
    else:
        return False

def is_int(command):
    """Checks if second element of user input is a digit
       and returns true or false

    Args:
        command [list]: list of user input 

    Returns:
        [boolean]: returns True or False if second element is a digit()
    """
    if command[1].isdigit():
        return True
    else:
        return False

def go_forward(name, steps, coord, turn):
    """Moves the robot forward and checks if it's new position is within
       the limited area. If not, will reset position to last saved

    Args:
        name [str]: name of the robot
        steps [int]: units of movement the robot should take
        coord [list]: position of the robot
        turn [int]: direction the robot is facing

    Returns:
        coord [list]: returns the new position of the robot
    """
    copy = coord.copy()
    if calc_position(steps, coord, turn)[0]:
        output = " > "+name+" moved forward by "+str(steps)+" steps."

    else:
        coord = copy
        output = name+": Sorry, I cannot go outside my safe zone."

    return coord, output

def go_back(name, steps, coord, turn):
    """Moves the robot backward and checks if it's new position is within
       the limited area. If not, will reset position to last saved. Changes
       steps to a negative

    Args:
        name [str]: name of the robot
        steps [int]: units of movement the robot should take
        coord [list]: position of the robot
        turn [int]: direction the robot is facing

    Returns:
        coord [list]: returns the new position of the robot
    """
    steps *= -1
    copy = coord.copy()
    if calc_position(steps, coord, turn)[0]:
        steps *= -1
        output = " > "+name+" moved back by "+str(steps)+" steps."
    else:
        coord = copy
        output = name+": Sorry, I cannot go outside my safe zone."
    return coord, output

def go_right(name, turn):
    """Moves the robot right

    Args:
        name [str]: name of the robot
        turn [int]: direction the robot

    Returns:
        turn [int]: returns the new direction that the robot is facing
    """
    turn += 1
    output = " > "+name+" turned right."
    return turn, output

def go_left(name, turn):
    """Moves the robot left

    Args:
        name [str]: name of the robot
        turn [int]: direction the robot

    Returns:
        turn [int]: returns the new direction that the robot is facing
    """
    turn -= 1
    output = " > "+name+" turned left."
    return turn, output


def go_help():
    """Generates a list of help options and returns them as a string

    Returns:
        command_string [str]: Returns a string of all help options
    """
    commands = {"OFF " : "Shut down robot",
                "HELP" : "provide information about commands",
                "FORWARD" : "Moves the robot forward by a number of steps",
                "BACK" : "Moves the robot backwards by a number of steps",
                "RIGHT" : "Turns the robot to face the right",
                "LEFT" : "Turns the robot to face the left",
                "SPRINT" : "makes the robot sprint forward",
                "HISTORY": "gives a list of all the previous commands that were input",
                "REPLAY": "makes the robot replay previous moves"}
    command_list = ["I can understand these commands:\n"]
    for i, j in commands.items():
        command_list.append(i+ " - " +j+"\n")
    
    command_string = ""
    for i in command_list:
        command_string = "".join(command_list)
    return command_string

def go_sprint(name, steps, coord, turn):
    """Moves the robot forward recursively by adding steps-1 to the position
       and checks if it's new position is within the limited area. 
       If not, will reset position to last saved. Changes steps to a negative

    Args:
        name [str]: name of the robot
        steps [int]: units of movement the robot should take
        coord [list]: position of the robot
        turn [int]: direction the robot is facing

    Returns:
        coord [list]: returns the new position of the robot
    """
    copy = coord.copy()
    valid_limit, coord, turn = calc_sprint(steps, coord, turn)
    if valid_limit and ("replay silent" not in history and "replay reversed silent" not in history):
        while steps > 0:
            print(f" > {name} moved forward by {steps} steps.")
            steps -= 1
    elif valid_limit == False:
        coord = copy
        print(f"{name}: Sorry, I cannot go outside my safe zone.")
    return coord


def go_off(name):
    """Prints Shutdown and returns boolean of false to break out of while loop

    Args:
        name [str]: name of the robot

    Returns:
        [Boolean]: Returns False
    """
    print(f"{name}: Shutting down..")
    return False

def calc_position(steps, coord, turn):
    """Finds the position the robot is facing and adds/subtracts the number
       of steps the robot will move along either the x or y axis.
       If turns is 4 or -4, it will reset turns to 0

    Args:
        coord [list]: list of integers that stores the x and y positions
        steps [int]: number of steps the robot must move
        turn [int]: used to represent the direction the robot is facing

    Returns:
        [Boolean]: Returns True or False if the new position is with range
        coord [list]: returns the updated x and y positions
        turn [int]: returns a integer that represents the direction the robot is currently facing
    """
    if turn == 0 or turn == 4 or turn == -4:
        coord[1] += steps
        turn = 0
    elif turn == 1 or turn == -3:
        coord[0] += steps
    elif turn == 3 or turn == -1:
        coord[0] -= steps
    elif turn == 2 or turn == -2:
        coord[1] -= steps

    if limit(coord):
        return True, coord, turn
    else:
        return False, coord, turn

def calc_sprint(steps, coord, turn):
    """Recursive function to calculate the number of steps by adding steps to itself
       while steps decreases by -1.

    Args:
        coord [list]: list of integers that stores the x and y positions
        steps [int]: The number of spaces the robot will move
        turn [int]: direction the robot is facing

    Returns:
        [Boolean]: Returns True or False if the new position is with range
        coord [list]: returns the updated x and y positions
        turn [int]: returns a integer that represents the direction the robot is currently facing
    """
    if steps > 0:
        if turn == 0 or turn == 4 or turn == -4:
            coord[1] += steps
            turn = 0
            return calc_sprint(steps-1, coord, turn)
        elif turn == 1 or turn == -3:
            coord[0] += steps
            return calc_sprint(steps-1, coord, turn)
        elif turn == -1 or turn == 3:
            coord[0] -= steps
            return calc_sprint(steps-1, coord, turn)
        elif turn == 2 or turn == -2:
            coord[1] -= steps
            return calc_sprint(steps-1, coord, turn)
    elif limit(coord):
        return True, coord, turn
    else:
        return False, coord, turn

def limit(coord):
    """Checks if new position is within the range

    Args:
        coord [list]: new position of the robot

    Returns:
        [Boolean]: returns True or False if the coordinates are within the range
    """
    if coord[0] in range(-100, 100) and coord[1] in range(-200, 200):
        return True
    else:
        return False

def n_and_m_check(arg_list, n, m):
    """Finds the "-" and changes the characters before and after to integers.
       Also checks that if n(number of commands to be executed by user) 
       is greater than the number of commands in history, then n is reset to last element

    Args:
        arg_list [list]: list of all arguements

    Returns:
        n [int]: returns the starting element for the range of the history list
        m [int]: returns the ending element for the range of the history list
    """
    if arg_list != None:
        for i in arg_list:
            if "-" in i:
                m, n = i.split("-")
                m, n = int(m), int(n)
                m = (len(history)-1)-m
                n = (len(history)-1)-n
            elif i.isdigit():
                m = (len(history)-1)-int(i)
    # print(f"m:{m} and n:{n}")
    if n==None or len(history)<=m:
        return None, m
    else:
        return n, m


def do_replay(name, arg, coord, turn):
    """Checks the string of replay commands and breaks it up. so that
       the commands can go to their respective functions

    Args:
        name [str]: name of the robot
        arg [str]: string of all replay commands
        coord [list]: position of the robot
        turn [int]: direction the robot is facing

    Returns:
        output [str]: returns a string with the name and number of commands executed
    """
    global history, bool_silent
    history = clean_list(history)
    replay, reverse, silent = True, False, False
    n, m = None, 0
    if arg != None:
        arg_list = arg.split()
        n, m = n_and_m_check(arg_list, n, m)
        silent =  "silent" in arg.split()
        reverse = "reversed" in arg.split()
    if silent: bool_silent = True
    argue = ""
    counter = 0
    if reverse or (reverse and silent):
        argue += " in reverse silently" if silent and reverse else " in reverse"
        counter, reverse, silent = do_reverse(name, counter, coord, turn, n, m)
    elif silent or replay:
        argue += " silently" if silent else argue
        counter = do_silent(name, counter, coord, turn, n, m)
    output = ' > '+name+' replayed '+str(counter)+" commands"+argue+"."
    bool_silent = False
    return output


def do_reverse(name, counter, coord, turn, n, m):
    """Does the reverse and reverse silent command.

    Args:
        name [str]: name of the robot
        counter [int]: number of commands that were executed
        coord [list]: position of the robot
        turn [int]: direction the robot is facing
        n [int]: number of commands that must be excuted/last element of list to execute
        m [int]: sets the starting element of the list

    Returns:
        counter [int]: returns the number of commands that were executed
    """
    global history
    history = history[::-1]
    # print(f"m:{m} and n:{n}")
    for i in history[m+1:n]:
        # re=i.split()
        if i != "replay reversed" and i!= "replay reversed silent":
            check_command(name, i, coord, turn)
            counter += 1
    history.pop(0)
    history = history[::-1]
    return counter, False, False

def do_silent(name, counter, coord, turn, n, m):
    """Does the replay and replay silent command.

    Args:
        name [str]: name of the robot
        counter [int]: number of commands that were executed
        coord [list]: position of the robot
        turn [int]: direction the robot is facing
        n [int]: number of commands that must be excuted/last element of list to execute
        m [int]: sets the starting element of the list

    Returns:
        counter [int]: returns the number of commands that were executed
    """
    # print(f"m:{m} and n:{n}")
    for i in history[m:n]:
        re = i.split()
        if i!= "replay silent" and  re[0] != "replay":
            check_command(name, i, coord, turn)
            counter += 1
    history.pop(-1)
    return counter

def check_command(name, commands, coord, turn):
    """Excutes the command that the user has input. Splits the command into 2 variables

    Args:
        name [str]: name of the robot
        commands [str]: string of the user input that has been validated
        coord [list]: position of the robot
        turn [int]: direction the robot is facing
    Returns:
        [Boolean]: returns True or False for next commmand or end of program
        coord [list]: returns the updated x and y positions
        turn [int]: returns a integer that represents the direction the robot is currently facing
    """
    output = ""
    commands, arg = clean_input(commands)
    if commands == "forward":
        coord, output = go_forward(name, int(arg), coord, turn)
    elif commands == "back":
        coord, output = go_back(name, int(arg), coord, turn)
    elif commands == "right":
        turn, output = go_right(name, turn)
    elif commands == "left":
        turn, output = go_left(name, turn)
    elif commands == "help":
        output = go_help()
    elif commands == "sprint":
        coord = go_sprint(name, int(arg), coord, turn)
    elif commands == "off":
        return go_off(name), coord, turn
    elif commands == 'history':
        output = do_history(history)
    elif commands == 'replay':
        output = do_replay(name, arg, coord, turn)

    if not bool_silent:                                             #global boolean that is set to False, only True when silent is in arg string
        if "sprint" != commands: print(output)
        print(f" > {name} now at position ({coord[0]},{coord[1]}).")
    return True, coord, turn
        

def robot_start():
    """Asks for robot name, gets user input, and exits program when requested
    """
    global history, bool_silent
    bool_silent = False
    history = []
    coord = [0, 0]
    turn = 0
    name = robot_name()
    while True:
        commands = get_commands(name)
        next, coord, turn = check_command(name, commands, coord, turn)
        if next == False: 
            history = [] 
            break


if __name__ == "__main__":
    robot_start()
