""" MAIN MODULE """

###############################################
##               LIBARY IMPORT               ##
###############################################
# from state_machine import (
#     state_machine, start, controller, forward,
#     back, left, right, turn
# )
# from controller import line_follower, play_music

def sequence2behaviours(sequence):
    """ converts the sequence to the build behaviours """

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

###############################################
##              Main function                ##
###############################################
def main():
    # get sequence
    txtFile = open("sequence.txt", 'r')
    task_seq = txtFile.read()
    txtFile.close()

    # translate sequence to behaviours
    task_seq = sequence2behaviours(task_seq)
    print(task_seq)

    # state machine
    # m = state_machine()
    # m.add_state("start", start)
    # m.add_state("controller", controller)
    # m.add_state("follow", line_follower.follow)
    # m.add_state("forward", forward)
    # m.add_state("left", left)
    # m.add_state("right", right)
    # m.add_state("turn", turn)
    # m.add_state("back", back)
    # m.add_state("End", None, end_state=1)
    # m.set_start("start")
    # m.run(task_sequence)

if __name__ == "__main__":
    main()
