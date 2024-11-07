#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 27.09.2024 at 15:58

@author: piledge
@description: Utility Functions for adhering to the DRY-principle
"""

default_lang_dict = dict(
    # Default Dictionary for get_message()
    list_files_booleans=(
        "\033[31mWarning: '{var_name}' has to be {type_name}!\033[0m",
        "\033[31mWarnung: '{var_name}' muss {type_name} sein!\033[0m"
    ), list_files_paths=(
        "\033[31mWarning: dir_paths {invalid_paths} not valid!\033[0m",
        "\033[31mWarnung: dir_paths {invalid_paths} ung�ltig!\033[0m",
    ), list_files_regex=(
        "\033[31mInvalid regular expression: {pattern}\033[0m",
        "\033[31mUng�ltiger regul�rer Ausdruck: {pattern}\033[0m"
    ), list_files_empty=(
        "\033[31mNothing found!\033[0m",
        "\033[31mNichts gefunden!\033[0m"
    ))

default_style_dict = dict(
    # Default Color palette for ansi_style()
    reset="\033[0m",
    red="\033[31m",
    green="\033[92m",
    blue="\033[34m",
    yellow="\033[93m",
    cyan="\033[96m",
    magenta="\033[35m",
    black="\033[30m",
    white="\033[97m",
    bold="\033[1m",
    underline="\033[4m"
)


def get_description() -> None:
    """
    Prints package-description.
    :return: None
    """
    print('Utility Functions for adhering to the DRY-principle')


def ansi_style(style: str = 'reset', style_dict: dict = None) -> str:
    """
    Returns the ANSI-Code of a colour or text style to use it in a console-output
    :param style: Can be 'red', 'green', '',blue 'yellow', 'cyan', 'magenta', 'black', 'white', 'reset', 'bold' or 'underline'.
    :param style_dict: dictionary to provide messages in different languages
    :return: Style-string to be directly used in fstring.
    """
    if not isinstance(style_dict, dict): style_dict = default_style_dict

    return style_dict.get(style.lower(), "\033[0m")


def clear_screen() -> None:
    """
    Clears the screen of the terminal OS-independent.
    :return: None
    """
    from os import name, system
    if name == 'nt':
        system('cls')
    else:
        system('clear')


def format_file_size(size_in_bytes: int) -> str:
    """
    Formats the file size in bits to a string with unit.
    :param size_in_bytes: e.g. 123456.
    :return: Formatted string, e.g. "120.56 KiB".
    """
    if size_in_bytes >= 2 ** 30:
        size = size_in_bytes / (2 ** 30)
        return f"{size:.2f} GiB"
    elif size_in_bytes >= 2 ** 20:
        size = size_in_bytes / (2 ** 20)
        return f"{size:.2f} MiB"
    elif size_in_bytes >= 2 ** 10:
        size = size_in_bytes / (2 ** 10)
        return f"{size:.2f} KiB"
    else:
        return f"{size_in_bytes} Bytes"


def format_seconds(seconds: int | float, decimal_places: int = 1) -> str:
    """
    Formats the time in seconds to a string with units.
    :param seconds: e.g. 3665.
    :param decimal_places: Number of the seconds decimal places.
    :return: Formatted string, e.g. "1h 1m 5s".
    """
    if seconds >= 3600:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = round(seconds % 60, decimal_places)
        return f"{hours}h {minutes}m {seconds}s"
    elif seconds >= 60:
        minutes = seconds // 60
        seconds = round(seconds % 60, decimal_places)
        return f"{minutes}m {seconds}s"
    else:
        return f"{round(seconds, decimal_places)}s"


def list_files(dir_paths: str | list = '.', pattern: str = '*', full_names: bool = False, recursive: bool = False,
               files: bool = True, folders: bool = False, verbose: bool = True, lang: str = 'en') -> list[str] | None:
    """
    A Python-implementation of R's list.files()-function, supporting multiple directories and providing additional features. These functions produce a list of file/directory names.
    :param dir_paths: A list of directory paths or a single directory path (default: current working directory).
    :param pattern: A regular expression to filter file names.
    :param full_names: If True, full relative paths are returned; if False, only file names.
    :param recursive: If True, the listing recurses into subdirectories.
    :param files: Should files be returned.
    :param folders: Should folders be returned.
    :param verbose: If True, console hints will be printed.
    :param lang: Language of outputs. Either 'en' or 'de'.
    :return: A list of matching file/folder names or full paths.
    """
    from pathlib import Path
    from os.path import isdir

    if isinstance(dir_paths, str): dir_paths = [dir_paths]
    if not isinstance(lang, str): lang = 'en'

    error_occurred = False
    bools = {'full_names': full_names, 'recursive': recursive, 'files': files, 'folders': folders, 'verbose': verbose}
    for var_name, var_value in bools.items():
        if not isinstance(var_value, bool):
            error_occurred = True
            if verbose: print(get_message('list_files_booleans', lang=lang, var_name=var_name, type_name=bool))
    if error_occurred:
        return None

    invalid_paths = [i for i, path in enumerate(dir_paths) if not isdir(path)]
    if invalid_paths:
        if verbose: print(get_message('list_files_paths', lang=lang, invalid_paths=invalid_paths))
        return None

    all_files = []
    for dir_path in dir_paths:
        dir_path = Path(dir_path).resolve()
        elements = dir_path.rglob('*') if recursive else dir_path.glob('*')
        if not folders: elements = (f for f in elements if f.is_file())
        if not files: elements = (f for f in elements if f.is_dir())

        if pattern != '*':
            from re import compile, error
            try:
                if pattern == 'asm': print('komisch')
                regex = compile(pattern)
            except error:
                if verbose: print(get_message('list_files_regex', lang=lang, pattern=pattern))
                return None
            elements = [f for f in elements if regex.search(f.name)]

        if not full_names: elements = [f.name for f in elements]

        all_files.extend([str(f) for f in elements])
    if pattern == 'asm': print('komisch')
    if len(all_files) == 0 and verbose:
        print(get_message('list_files_empty', lang=lang))

    return all_files


def console_width() -> int:
    """
    Returns the length of the characters to be plottet on the current console.
    :return: e.g. 80.
    """
    from shutil import get_terminal_size
    terminal_size = get_terminal_size()

    return terminal_size.columns


def print_separator(sep_char: str = '-') -> None:
    """
    Prints a separating line on the console, based on the current console_width().
    :param sep_char: Character to be used for the separating line.
    :return: e.g. "--------------------------------"
    """
    print(sep_char * console_width())


def copyright_header(name: str = 'Cool program', dev: str = 'Cool Guy', version: str = '1.0', year: int | str = 2024,
                     sep_char: str = '-') -> None:
    """
    Returns a nice looking formatted header to be shown at the start of a script.
    :param sep_char: Character to draw the line.
    :param name: Name of the Program.
    :param dev: Developer's name.
    :param version: current revision of the program.
    :param year: Year of development.
    :return:
    """
    width = console_width()
    len_v = len(version)
    string_length = len(f'{name}{dev}{year}{width}') + (3 + len_v)
    clear_screen()
    print_separator(sep_char)
    print(f'{name} v{version}{' ' * (width - string_length)}\u00A9 {dev} {year}')
    print_separator(sep_char)


def run_dir() -> str:
    """
    Returns the directory from which the script was executed
    :return: Path of the script
    """
    from os.path import abspath, dirname, normpath
    script_path = abspath(__file__)
    script_normpath = normpath(script_path)

    return dirname(script_normpath)


def memoize(func):
    """
    A cache-function
    :param func:
    :return: wrapper-function
    """
    from functools import wraps
    cache = {}

    @wraps(func)
    def wrapper(*args, **kwargs):
        key = str(args) + str(kwargs)

        if key not in cache:
            cache[key] = func(*args, **kwargs)

        return cache[key]

    return wrapper


def get_message(key: str, lang: str = "en", lang_dict: dict = None, **kwargs) -> str:
    """
    A function to provide multilingual console outputs by using a defined dictionary
    :param key: key of translation-dictionary
    :param lang: 'en' for English, 'de' for German
    :param lang_dict: dictionary to provide messages in different languages
    :return: A formatted message in the required language
    """
    if not isinstance(lang_dict, dict): lang_dict = default_lang_dict

    text_template = lang_dict.get(key)[0] if lang == "en" else lang_dict.get(key)[1]
    try:
        return text_template.format(**kwargs)
    except KeyError as e:
        return f"\033[31mError: Missing value for placeholder {e.args[0]} in message '{key}'\033[0m"
