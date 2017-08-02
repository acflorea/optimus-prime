import sys


def main(args):
    # calculate stuff
    sys.stdout.write(args[1])
    sys.stdout.flush()
    sys.exit(0)


if __name__ == "__main__":
    # execute only if run as a script
    main(sys.argv)
