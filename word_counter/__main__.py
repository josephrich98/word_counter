import sys
from .app import main as launch_gui
from .cli import run_cli


def main():
    args = sys.argv[1:]

    if not args:
        # No arguments → open GUI
        launch_gui()
        return

    # Otherwise → use CLI mode
    run_cli(args)


if __name__ == "__main__":
    main()
