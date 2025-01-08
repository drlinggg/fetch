import json
import os
import sys
import subprocess
from pathlib import Path

arts = [[
    "                  ▄",
    "                 ▟█▙",
    "                ▟███▙",
    "               ▟█████▙",
    "              ▟███████▙",
    "             ▂▔▀▜██████▙",
    "            ▟██▅▂▝▜█████▙",
    "           ▟█████████████▙",
    "          ▟███████████████▙",
    "         ▟█████████████████▙",
    "        ▟███████████████████▙",
    "       ▟█████████▛▀▀▜████████▙",
    "      ▟████████▛      ▜███████▙",
    "     ▟█████████        ████████▙",
    "    ▟██████████        █████▆▅▄▃▂",
    "   ▟██████████▛        ▜█████████▙",
    "  ▟██████▀▀▀              ▀▀██████▙",
    " ▟███▀▘                       ▝▀███▙",
    "▟▛▀                               ▀▜▙"]
    ,
    [
    '       .',
    '      /#\\ ',
    '     /###\\ ',
    '    /p^###\\ ',
    '   /##P^q##\\ ',
    '  /##(   )##\\ ',
    ' /###P   q#,^\\ ',
    '/P^         ^q\\ '
   ]
]

i = 0

def change_ascii():
    global i
    i = 0
    print("Press 'a' or 'd' to switch ascii. Press enter to save")
    while True:
        os.system('clear')
        print(f"current: {i}")
        for line in arts[i]:
            print(line)
        arrow = input()
        if arrow == 'd':
             i = (i + 1) % len(arts)
        elif arrow == 'a':
            i = (i - 1) % len(arts)
        elif arrow == '':
           save_ascii_index(i)
           break


def save_ascii_index(index):
    script_dir = Path(__file__).resolve().parent
    data_file_path = script_dir / "data.json"
    try:
        with open(data_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}
    data['asciilogo'] = index
    with open(data_file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    print(f"Saved ascii logo index: {index}")

class RGB:
    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], list):
            arr = args[0]
            self.r = int(arr[0])
            self.g = int(arr[1])
            self.b = int(arr[2])

        elif len(args) == 3:
            self.r = int(args[0])
            self.g = int(args[1])
            self.b = int(args[2])

def colored_string(string, rgb):
    return f"\033[38;2;{rgb.r};{rgb.g};{rgb.b}m{string}\033[0m"

def get_gradient(rgb, count, step = 13):
    r, g, b = rgb.r, rgb.g, rgb.b
    gradient = []

    for i in range(-count//2, count//2):
        new_r = max(0, min(255, r - i * step))
        new_g = max(0, min(255, g + i * step/2))
        new_b = max(0, min(255, b + i * step))
        gradient.append(RGB(new_r, new_g, new_b))

    return gradient


def set_color():
    print(colored_string("COLOR_SET", RGB(170, 170, 170)))

    home_dir = os.path.expanduser("~")
    color_source = input("Would you like to get the color from the config file or enter an RGB value? (type 'file' or 'rgb', default is 'file'): ").strip().lower() or 'file'
    
    script_dir = Path(__file__).resolve().parent

    data_file_path = script_dir / "data.json"
    if color_source == 'file':
        kdeColorSchemePath = input("kde colorscheme path? (default: ~/.local/share/konsole/finale.colorscheme): ") or os.path.join(home_dir, ".local/share/konsole/finale.colorscheme")

        if not os.path.exists(kdeColorSchemePath):
            print(f"Error: File not found: {kdeColorSchemePath}")
            return

        color2_value = None
        in_color2_section = False

        try:
            with open(kdeColorSchemePath, 'r', encoding='utf-8') as file:
                text = file.read()
                lines = text.strip().splitlines()

                for line in lines:
                    line = line.strip()
                    if line == "[Color2]":
                        in_color2_section = True
                        continue
                    elif line.startswith("["):
                        in_color2_section = False
                        continue

                    if in_color2_section and line.startswith("Color="):
                        color2_value = line.split('=', 1)[1]
                        break

            if color2_value is not None:
                try:
                    with open(data_file_path, 'r', encoding='utf-8') as file:
                        data = json.load(file)
                except FileNotFoundError:
                    data = {}

                data['color'] = color2_value
                with open(data_file_path, 'w', encoding='utf-8') as json_file:
                    json.dump(data, json_file, ensure_ascii=False, indent=4)
                print(f"Color found: {color2_value}, written to {data_file_path}")
            else:
                print("Error: Color not found in [Color2] section.")

        except FileNotFoundError:
            print(f"Error: File not found: {kdeColorSchemePath}")
        except Exception as e:
            print(f"An error occurred: {e}")

    elif color_source == 'rgb':
        rgb_value = input("Please enter the RGB value (format: R,G,B, default is '255,255,255'): ") or '255,255,255'
        try:
            r, g, b = map(int, rgb_value.split(','))
            if all(0 <= x <= 255 for x in (r, g, b)):
                data = {'color': f'{r},{g},{b}'}
            else:
                print("Error: RGB values must be between 0 and 255.")
        except ValueError:
            print("Error: Invalid RGB format. Please enter three integers separated by commas.")

    else:
        print("Error: Invalid option. Please type 'file' or 'rgb'.")

    gradient = input("Would you like to use gradient? (y/n), default n): ") or 'n'
    data['gradient'] = gradient
    with open(data_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
        print(f"RGB value written to {data_file_path} as: {data['color']}, {data['gradient']}")

    print(colored_string("FINISHED, Now you can execute xfetch", RGB(170, 170, 170)))

def get_memory_usage():
    mem_command = "free -m"
    mem_result = subprocess.run(mem_command, shell=True, capture_output=True, text=True)
    lines = mem_result.stdout.strip().split('\n')
    memory_line = lines[1]
    mem_usage = memory_line.split()[2]
    return mem_usage

def get_uptime_hours_minutes():
    uptime_command = "uptime -p"
    uptime_result = subprocess.run(uptime_command, shell=True, capture_output=True, text=True)
    return uptime_result.stdout.strip()[3:]

def fetch(rgb_instance, gradient, asciilogo):

    art = arts[asciilogo]

    os_command = "grep PRETTY_NAME /etc/os-release | awk -F = '{ print $2 }' | sed -e 's/\"//g'"
    os_result = subprocess.run(os_command, shell=True, capture_output=True, text=True)

    whothisis_command = "echo $USER@$(hostname)"
    whothisis_result = subprocess.run(whothisis_command, shell=True, capture_output=True, text=True)

    memory_usage = get_memory_usage()
    uptime = get_uptime_hours_minutes()

    packages_command = "pacman -Q | wc -l"
    packages_result = subprocess.run(packages_command, shell=True, capture_output=True, text=True)

    info = []
    info.append(colored_string("OS: ", rgb_instance) + os_result.stdout.strip())
    info.append(colored_string("RAM (MB): ", rgb_instance) + memory_usage)
    info.append(colored_string("Uptime: ", rgb_instance) + uptime)
    info.append(colored_string("Packages: ", rgb_instance) + packages_result.stdout.strip())

    rgbs_logo = get_gradient(rgb_instance, len(art))
    if (gradient == 'n'):
        rgbs_logo = [rgb_instance for i in art]

    for i in range(len(art)):
        if i < len(info):
            print(colored_string(art[i], rgbs_logo[i]) + (' ' * (len(art[-1]) - len(art[i]))) + info[i])
        else:
            print(colored_string(art[i], rgbs_logo[i]))
    print()

def main():

    if (len(sys.argv) > 1):
        args = sys.argv[1:]

        if (args[0] == 'set-color'):
            set_color()
        elif (args[0] == 'change-ascii'):
            change_ascii()

    script_dir = Path(__file__).resolve().parent
    data_file_path = script_dir / "data.json"

    if not data_file_path.is_file():
        change_ascii()
        set_color()

    with open(data_file_path, 'r') as data:
        json_data = json.load(data)

        color_string = json_data['color']
        values = color_string.split(',')
        color = RGB(values)
        gradient = json_data['gradient']
        asciilogo = int(json_data['asciilogo'])

    fetch(color, gradient, asciilogo)


if __name__ == "__main__":
    main()
