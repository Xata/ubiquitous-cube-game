from app.game import *


def main():
    """
    Main entry point for the game.

    Creates the game engine object and then starts the game loop.
    """
    main_app = Game()
    main_app.run()


if __name__ == '__main__':
    main()
