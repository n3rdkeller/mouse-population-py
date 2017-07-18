"""A little simulation of a population

This program shows you how classes work.
There were some Classes given: World, Thing, Plant, Corn, Creature, Mouse

Mouse and Corn can multiply and Mouse can also eat corn, but a Mouse can also
die of starvation, if it does not eat the Corn in the right amount of cycles.

Let´s Try
"""

import sys
import classes

def getCommand() -> int:
    '''Prints the menu and returns the command as a tuple.
    (0, *) should perform the life cycle * times.
    (1, {'mouse': 20}) should spawn 20 mice.
    (255, 255) is the error message.'''
    cmd = input("Enter command ('h' for help, <return> for next cycle): ")
    if cmd == "":
        return (0, 1)
    elif cmd == "h":
        return (255, 255)
    elif cmd == "q":
        print("Bye!")
        exit(0)
    elif cmd.startswith("spawn"):
        s = cmd.split(" ")
        return (1, {"number": s[1], "type": s[2]})
    elif cmd.isdigit():
        return (0, cmd)
    else:
        return (255, 255)

def printHelp():
    print("'h'                     shows this help")
    print("'q'                     quits")
    print("'spawn <number> <type>' spawns <number> random objects of type <type>")
    print("<return>                does one cycle")
    print("'<number>'              does <number> cycles")

def main():
    # get world size from command line arguments
    if len(sys.argv) > 1:
        w = classes.World(int(sys.argv[1]), int(sys.argv[2]))
    else:
        # if not given, initialize with defaults
        w = classes.World()
    w.clearScreen()
    while True:
        try:
            w.printMap()
            c = getCommand()
            if c[0] == 0:
                w.computeLifeCycle(int(c[1]))
            elif c[0] == 1:
                w.spawn(int(c[1]["number"]), c[1]["type"])
            elif c[0] == 255:
                printHelp()
        except SystemExit:
            exit(0)
        except KeyboardInterrupt:
            print("Bye!")
            exit(1)
        except:
            print("There was something wrong!")
            printHelp()

if __name__ == '__main__':
    main()
