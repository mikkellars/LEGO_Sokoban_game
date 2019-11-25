""" MAIN MODULE """

###############################################
##               LIBRARY IMPORT               ##
###############################################
from state_machine import (
    state_machine,
    forward,
    start,
    controller,
    back,
    backward,
    left,
    right,
    stop
)
from controller import line_follower, play_music
from collections import deque

def sequence2behaviors(sequence):
    """Converts the sequence to the build behaviors"""

    result = ""
    for i in range(len(sequence)):
        # get the characters
        current_char = sequence[i]
        # next_char = sequence[i+1]
        if (i != 0):
            prev_char = sequence[i-1]
        else:
            prev_char = ''

        if current_char.islower():
            if prev_char.isupper():
                result += 'T'
                result += current_char
            else:
                result += current_char
        elif current_char.isupper():
            if prev_char.islower():
                result += current_char.lower()
                result += current_char.lower()
            elif prev_char.isupper():
                result += current_char.lower()
            else:
                result += current_char.lower()
                result += current_char.lower()
    return result

def compass(sequence):
    """Keeps track of the robot position on the map"""

    temp_seq = list(sequence)
    result = ""
    circular_queue = deque(['u', 'r', 'd', 'l'], maxlen=4)
    char2idx = {'u':0, 'r':1, 'd':2, 'l':3}
    for i in range(len(temp_seq)):
        # get chars
        current_char = temp_seq[i]
        if i != 0:
            prev_char = temp_seq[i-1]
        else:
            prev_char = ''

        # insert char
        result += current_char

        # if chars are equal no rotation needed
        if prev_char == current_char:
            continue

        # update compass
        if current_char == 'r':
            circular_queue.rotate(1)
        elif current_char == 'l':
            circular_queue.rotate(-1)
        elif current_char == 'd':
            circular_queue.rotate(-2)
        elif current_char == 'T': 
            circular_queue.rotate(-2)
        
        # update temp_seq
        for j, char in enumerate(sequence):
            if char == 'T':
                continue
            idx = char2idx[char]
            new_char = circular_queue[idx]
            temp_seq[j] = new_char
        
    return result


###############################################
##              Main function                ##
###############################################
def main():
    # get sequence
    # task_seq = "uldruldruldruldruldr"
    txtFile = open("sequence.txt", 'r')
    task_seq = txtFile.read()
    txtFile.close()

    # translate sequence to behaviors
    task_seq = sequence2behaviors(task_seq)
    print(task_seq)
    task_seq = compass(task_seq)
    print(task_seq)

    # state machine
    m = state_machine()
    m.add_state("start", start)
    m.add_state("ctrl", controller)
    m.add_state("follow", line_follower.follow)
    m.add_state("forward", forward)
    m.add_state("left", left)
    m.add_state("right", right)
    m.add_state("follow backwards", line_follower.follow_backwards)
    m.add_state("backward", backward)
    m.add_state("back", back)
    m.add_state("end", stop, end_state=1)
    m.set_start("start")
    m.run(task_seq)

if __name__ == "__main__":
    main()
    # while True:
    #     line_follower.intersection()
