import colorama


def print_error(text: str) -> None:
    print(f'{colorama.Fore.RED}{text}{colorama.Style.RESET_ALL}')


def print_success(text: str) -> None:
    print(f'{colorama.Fore.GREEN}{text}{colorama.Style.RESET_ALL}')
