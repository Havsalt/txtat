
__version__ = "0.1.0"

import argparse

import keyboard
import pyautogui
import pyperclip
import pytesseract
from actus import info, LogSection


echo = LogSection("", left_deco="", right_deco="", suppress_color=True)


class ParserArguments(argparse.Namespace): ...


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="txtat",
        description="Copy text from screen region to clipboard",
        add_help=False
    )
    parser.add_argument(
        "-h", "--help",
        action="help",
        help="Show this help message and exit",
        default=argparse.SUPPRESS
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"%(prog)s: v{__version__}",
        help="Show `%(prog)s` version number and exit"
    )

    args = ParserArguments()
    parser.parse_args(namespace=args)

    info("Waiting for $[CTRL] event... ($[1/2])")
    keyboard.wait("ctrl")
    start = pyautogui.position()
    info(f"Region start: $[{start.x, start.y}]")
    info("Waiting for $[CTRL] event... ($[2/2])")
    keyboard.wait("ctrl")
    end = pyautogui.position()
    info(f"Region end: $[{end.x, end.y}]")
    width = int(end.x - start.x)
    height = int(end.y - start.y)
    info(f"Region size: $[{width}]x$[{height}]")
    region = (int(start.x), int(start.y), width, height)
    screenshot = pyautogui.screenshot(region=region)
    info("$[Extracting] screenshot text...")
    text: str = (
        pytesseract.image_to_string(screenshot)
        .lstrip()
        .rstrip()
        .replace("\n\n", "\n")
        .replace("\n\n", "\n")
    )
    pyperclip.copy(text)
    info(f"$[Copied] to clipboard:")
    echo(text)

    return 0
