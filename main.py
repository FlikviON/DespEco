from main_menu import MainMenu


def main() -> None:
    """Starts the game"""
    main_menu = MainMenu()
    is_running = True
    while is_running:
        main_menu.open_main_menu()


if __name__ == "__main__":
    main()
