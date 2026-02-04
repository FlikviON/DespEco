import main_menu


def main() -> None:
    """Starts the game"""
    is_running = True
    while is_running:
        main_menu.open_main_menu()


if __name__ == "__main__":
    main()
