import os
import gdown
import json

CONFIG_FILE = "config.json"

# Default fallback config
DEFAULT_CONFIG = {
    "submissions_folder": "submissions",
    "default_drive_folder": ""
}


def load_config():
    """Load config.json or create one with default values."""
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "w") as f:
            json.dump(DEFAULT_CONFIG, f, indent=4)
        print(f"⚙️ Created default {CONFIG_FILE}")
        return DEFAULT_CONFIG

    with open(CONFIG_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            print("⚠️ Invalid config.json, using defaults.")
            return DEFAULT_CONFIG


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def download_folder_from_drive():
    """Prompt user for a Google Drive folder URL and download all contents."""
    cls()
    print("=== Google Drive Downloader ===")

    config = load_config()
    SUBMISSIONS_FOLDER = config.get("submissions_folder", DEFAULT_CONFIG["submissions_folder"])
    default_url = config.get("default_drive_folder", "")

    print(f"Default destination folder: {SUBMISSIONS_FOLDER}")
    if default_url:
        print(f"Default Drive link: {default_url}")

    folder_url = input("\nEnter the shared Google Drive folder URL (leave blank to use default):\n> ").strip()

    # If user presses enter, use the default URL
    if not folder_url:
        if not default_url:
            print("\n⚠️ No URL provided and no default set. Returning to menu...")
            input("\nPress Enter to continue...")
            return
        folder_url = default_url

    print(f"\n🔽 Downloading submissions from:\n{folder_url}")
    print(f"📁 Destination: {SUBMISSIONS_FOLDER}")

    os.makedirs(SUBMISSIONS_FOLDER, exist_ok=True)

    try:
        gdown.download_folder(
            url=folder_url,
            output=SUBMISSIONS_FOLDER,
            quiet=False,
            use_cookies=False
        )
        print("\n✅ Download complete! Files saved to:", SUBMISSIONS_FOLDER)
    except Exception as e:
        print(f"\n❌ Download failed: {e}")

    input("\nPress Enter to return to the main menu...")
