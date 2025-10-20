import tools

commands = {}
config = tools.configManager.load_config()
VERSION = config.get("version", "0.0.0")

def command(name, desc=""):
    def decorator(func):
        commands[name] = {"func": func, "desc": desc}
        return func
    return decorator

@command("cls", "Clear the console screen")
def cmd_cls():
    tools.grader.cls()

@command("grade", "Run grading menu")
def cmd_grade():
    tools.grader.display_grading_menu()

@command("download", "Download submissions from Google Drive")
def cmd_download():
    tools.gdriveDownloader.download_folder_from_drive()

@command("deleteFiles", "Clear all files in the submissions folder")
def cmd_deleteFiles():
    tools.clearFolder.clear_submission_folder()

@command("config", "Show current configuration")
def cmd_config():
    print("\n=== Current Configuration ===")
    for key, val in config.items():
        print(f"{key:<20}: {val}")
    print()

@command("version", "Show program version")
def cmd_version():
    print(f"\nGrader CLI version {VERSION}\n")

@command("help", "Show this help menu")
def cmd_help():
    tools.grader.cls()
    print("\n=== Available Commands ===")
    for name, data in sorted(commands.items()):
        print(f"{name:<14} - {data['desc']}")
    print("exit       - Exit the program\n")

def main():
    print(f"Welcome to the Grader CLI v{VERSION}!")
    print("Type 'help' to see available commands.\n")

    while True:
        cmd = input("grader> ").strip().lower()

        if cmd in ("exit", "quit"):
            print("Exiting...")
            break
        elif cmd in commands:
            try:
                commands[cmd]["func"]()
            except Exception as e:
                print(f"⚠️ Error while running '{cmd}': {e}")
        elif cmd == "":
            continue
        else:
            print("Unknown command. Type 'help' to see all options.\n")

if __name__ == "__main__":
    main()
