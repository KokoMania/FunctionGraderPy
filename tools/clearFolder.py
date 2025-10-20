import os
import shutil
SUBMISSIONS_FOLDER = "submissions"
def clear_submission_folder():
    """Delete all files and subfolders inside the submissions folder."""
    if not os.path.exists(SUBMISSIONS_FOLDER):
        print("No submissions folder found.")
        input("\nPress Enter to continue...")
        return

    # Confirm delete
    confirm = input("⚠️ This deletes all files in 'submissions'. Continue? (y/N): ").strip().lower()
    if confirm != "y":
        print("\nCancelled.")
        input("\nPress Enter to continue...")
        return

    try:
        for item in os.listdir(SUBMISSIONS_FOLDER):
            path = os.path.join(SUBMISSIONS_FOLDER, item)
            if os.path.isfile(path) or os.path.islink(path):
                os.remove(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)
        print("\n✅ Submissions folder cleared.")
    except Exception as e:
        print(f"\n❌ Error clearing folder: {e}")

    input("\nPress Enter to return to menu...")
