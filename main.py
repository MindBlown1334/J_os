#main.py
import os, sys, time
import subprocess
from datetime import datetime
from settings import *
from commands_info import INFO

ITEMS_PER_PAGE = HEIGHT - 5

#CHUNK_SIZE = 500
CHUNK_SIZE = (HEIGHT - 5) * WIDTH

max_lines = HEIGHT - 5

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

def help_message():
    commends = len(INFO)
    blank_spaces = HEIGHT - 7 - commends
    for i in INFO:
        print(i)
    print(WIDTH * CHAR)
    print('\n' * blank_spaces)

def run_exe(path):
    try:
        if os.name == 'nt':
            os.startfile(path)  # działa tylko na Windows
        else:
            subprocess.Popen([path])
    except Exception as e:
        typingPrint(0.01, f"ERROR: {e}")
    print(CHAR * WIDTH)
    input("PRESS ENTER TO CONTINUE")

def typingPrint(t, text):
    for character in text:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(t)
    print()

def typingInput(t, text):
    for character in text:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(t)
    value = input()
    return value

def draw_bars(bars, v_cur, v_max, full="█", empty="░"):
    if v_max == 0:
        return
    remaining_bars = round((v_cur / v_max) * bars)
    lost_bars = bars - remaining_bars
    print(f"[{full * remaining_bars}{empty * lost_bars}]")
    
def get_current_datetime():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def delate_folder(path):
    if not os.path.isdir(path):
        return

    for root, dirs, files in os.walk(path, topdown=False):
        for file in files:
            try:
                os.remove(os.path.join(root, file))
            except Exception as e:
                print(f"Nie można usunąć pliku: {file} ({e})")
        for dir in dirs:
            try:
                os.rmdir(os.path.join(root, dir))
            except Exception as e:
                print(f"Nie można usunąć folderu: {dir} ({e})")
    try:
        os.rmdir(path)
    except Exception as e:
        print(f"Nie można usunąć głównego folderu: {e}")

def get_folder_size(path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            try:
                if os.path.exists(fp):
                    total_size += os.path.getsize(fp)
            except:
                pass
    return total_size

def list_dir(path):
    entries = sorted(os.listdir(path), key=lambda x: (not os.path.isdir(os.path.join(path, x)), x.lower()))

    if not entries:
        print(CHAR * WIDTH)
        left_text = f"J_OS VER: {VER}"
        right_text = get_current_datetime()
        space_padding = WIDTH - len(left_text) - len(right_text)
        print(f"{left_text}{' ' * max(space_padding, 1)}{right_text}")
        print(CHAR * WIDTH)
        print("(NO FILES IN THIS FOLDER)")
        print(CHAR * WIDTH)
        return entries

    max_name_len = max(len(entry) for entry in entries)
    column_width = max(max_name_len + 5, 20)

    total_pages = (len(entries) + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE

    for page in range(total_pages):
        cls()
        print(CHAR * WIDTH)
        left_text = f"J_OS VER: {VER}"
        right_text = get_current_datetime()
        space_padding = WIDTH - len(left_text) - len(right_text)
        print(f"{left_text}{' ' * max(space_padding, 1)}{right_text}")
        print(CHAR * WIDTH)

        page_entries = entries[page * ITEMS_PER_PAGE:(page + 1) * ITEMS_PER_PAGE]

        for entry in page_entries:
            full_path = os.path.join(path, entry)
            try:
                modified_time = time.strftime('%Y-%m-%d %H:%M', time.localtime(os.path.getmtime(full_path)))
            except:
                modified_time = "N/A"

            if os.path.isdir(full_path):
                size_display = "-" * 8
                print(f"| {entry:<{column_width}}| >FOLDER< | {modified_time} | {size_display:>12} |")
            else:
                try:
                    size = os.path.getsize(full_path)
                    if size < 1024:
                        size_display = f"{size:.2f}  B"
                    elif size < 1024**2:
                        size_display = f"{size / 1024:.2f} KB"
                    elif size < 1024**3:
                        size_display = f"{size / 1024**2:.2f} MB"
                    else:
                        size_display = f"{size / 1024**3:.2f} GB"
                except:
                    size_display = "N/A"
                print(f"| {entry:<{column_width}}| --FILE-> | {modified_time} | {size_display:>12} |")

        if len(page_entries) < max_lines:
            print(WIDTH * CHAR)
            print("\n" * (max_lines - len(page_entries) - 2))

        print(CHAR * WIDTH)
        if page + 1 < total_pages:
            input("Press ENTER to view next page...")
    return entries

def file_browser():
    current_path = os.getcwd()

    while True:
        cls()
        entries = list_dir(current_path)
        if current_path == "C:\\":
            choice = typingInput(0.005, f"{current_path}").strip()
        else:
            choice = typingInput(0.005, f"{current_path}\\").strip()

        if choice.lower() == '\\help' or choice.lower() == '\\?':
            cls()
            print(WIDTH * CHAR)
            print(" HELP WINDOW")
            print(WIDTH * CHAR)
            help_message()
            print(WIDTH * CHAR)
            input("PRESS ENTER TO CONTINUE")

        elif choice.lower() == '\\quit':
            break

        elif choice.lower().startswith('\\color '):
            try:
                color_change = choice[8:].strip()
                os.system(f'color {color_change}')
            except Exception as e:
                pass

        elif choice.lower().startswith('\\delete '):  # poprawiona komenda
            name = choice[8:].strip()
            if not name:
                cls()
                print(WIDTH * CHAR)
                typingPrint(0.01, "NO NAME PROVIDED")
                print(WIDTH * CHAR)
                input("PRESS ENTER TO CONTINUE")
                continue

            target_path = os.path.join(current_path, name)

            if os.path.exists(target_path):
                cls()
                print(WIDTH * CHAR)
                answer = typingInput(0.01, f"DELETE '{name}'? (Y/N) >> ").lower()
                if answer == 'y':
                    try:
                        if os.path.isfile(target_path):
                            os.remove(target_path)
                        elif os.path.isdir(target_path):
                            delate_folder(target_path)

                        print(CHAR * WIDTH)
                    except Exception as e:
                        typingPrint(0.01, f"ERROR: {e}")
                    input("PRESS ENTER TO CONTINUE")
                    continue
                else:
                    print(CHAR * WIDTH)
                    input("PRESS ENTER TO CONTINUE")
                    continue

        elif choice.lower().startswith('\\create '):
            name = choice[8:].strip()
            if not name:
                cls()
                print(WIDTH * CHAR)
                typingPrint(0.01, "NO NAME PROVIDED")
                print(WIDTH * CHAR)
                input("PRESS ENTER TO CONTINUE")
                continue

            target_path = os.path.join(current_path, name)

            if os.path.exists(target_path):
                cls()
                print(WIDTH * CHAR)
                typingPrint(0.01, "FILE OR FOLDER ALREADY EXISTS")
                print(WIDTH * CHAR)
                input("PRESS ENTER TO CONTINUE")
                continue

            if '.' in name:  # zakładamy, że to plik
                cls()
                print(WIDTH * CHAR)
                try:
                    with open(target_path, "w", encoding="utf-8") as f:
                        f.write("")
                    typingPrint(0.01, f"FILE {name} CREATED")
                except Exception as e:
                    typingPrint(0.01, f"FAILED TO CREATE FILE: {e}")
            else:  # zakładamy, że to folder
                cls()
                print(WIDTH * CHAR)
                try:
                    os.makedirs(target_path)
                    typingPrint(0.01, f"FOLDER {name} CREATED")
                except Exception as e:
                    typingPrint(0.01, f"FAILED TO CREATE FOLDER: {e}")
            
            print(WIDTH * CHAR)
            input("PRESS ENTER TO CONTINUE")

        #edytowanie pliku
        elif choice.lower().startswith('\\edit '):
            edit_target = choice[6:].strip()
            matching = [e for e in entries if e.lower() == edit_target.lower()]
            if not matching:
                typingPrint(0.01, "FILE NOT FOUND")
                input("PRESS ENTER TO CONTINUE")
                continue

            matched = matching[0]
            selected = os.path.join(current_path, matched)
            if os.path.isdir(selected):
                typingPrint(0.01, "CANNOT EDIT A FOLDER")
                input("PRESS ENTER TO CONTINUE")
                continue

            cls()
            typingPrint(0.005, f"EDITING FILE: {matched}")
            try:
                with open(selected, 'r', encoding='utf-8') as f:
                    old_content = f.read()
            except Exception as e:
                typingPrint(0.01, f"FAILED TO OPEN FILE: {e}")
                input("PRESS ENTER TO CONTINUE")
                continue

            print(CHAR * WIDTH)
            print(old_content)
            print(CHAR * WIDTH)
            print("ENTER NEW CONTENT (FINISH WITH \\quit):")
            print(CHAR * WIDTH)

            new_lines = []
            while True:
                line = input()
                if line == "\\quit":
                    break
                new_lines.append(line)

            new_content = '\n'.join(new_lines)
            try:
                with open(selected, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                typingPrint(0.01, "FILE SAVED SUCCESSFULLY")
                print(CHAR * WIDTH)
            except Exception as e:
                typingPrint(0.01, f"FAILED TO SAVE FILE: {e}")
            input("PRESS ENTER TO CONTINUE")

        elif choice == '..':
            current_path = os.path.dirname(current_path)

        elif choice.lower() in [e.lower() for e in entries]:
            matched = [e for e in entries if e.lower() == choice.lower()][0]
            selected = os.path.join(current_path, matched)

            #otwieranie nowej ścieszki lub pliku
            if os.path.isdir(selected):
                current_path = selected
            else:
                # Jeśli plik - pytamy o uruchomienie
                file_ext = matched.lower().rsplit('.', 1)[-1]  # pobiera końcówkę pliku bez kropki
                if file_ext in EXTENSIONS:
                #if matched.lower().endswith(tuple(EXTENSIONS)):
                    cls()
                    print(CHAR * WIDTH)
                    answer = typingInput(0.01, f"EXECUTE {matched} ? (Y/N) >> ").lower()
                    if answer == 'y':
                        run_exe(selected)
                        print(CHAR * WIDTH)
                        continue
                    else:
                        print(CHAR * WIDTH)
                        input("PRESS ENTER TO CONTINUE")
                        continue

                cls()
                size = input("ENTER CHUNK SIZE: ")
                try:
                    size = int(size)
                except:
                    size = CHUNK_SIZE
                cls()
                typingPrint(0.005, f"FILE: {matched}")
                try:
                    with open(selected, 'r', encoding='utf-8') as f:
                        content = f.read()
                        lines = content.splitlines()
                        total = len(lines)

                        for i in range(0, total, max_lines):
                            cls()
                            typingPrint(0.005, f"FILE: {matched}")
                            draw_bars(WIDTH - 2, i, total)
                            print(CHAR * WIDTH)
                            chunk = lines[i:i + max_lines]
                            print('\n'.join(chunk))
                            if i + max_lines < len(content):
                                print(CHAR * WIDTH)
                                input("PRESS ENTER TO CONTINUE")
                except Exception as e:
                    print(CHAR * WIDTH)
                    typingPrint(0.01, f"CANT OPEN FILE: {e}")
                print("END OF FILE")
                print(CHAR * WIDTH)
                input("PRESS ENTER TO CONTINUE")
        else:
            pass

if __name__ == "__main__":
    cls()
    os.system(f'color {COLOR}')
    file_browser()
