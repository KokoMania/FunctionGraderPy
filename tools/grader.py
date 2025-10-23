import importlib.util
import os
import json
from time import perf_counter as timer

SUBMISSIONS_FOLDER = "submissions"
TEST_FILE = "tests.json"


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def load_tests():
    """Load test cases from tests.json file."""
    if not os.path.exists(TEST_FILE):
        raise FileNotFoundError(f"Test file not found: {TEST_FILE}")

    with open(TEST_FILE, "r") as f:
        data = json.load(f)

    tests = []
    for item in data:
        func = item.get("function")
        args = item.get("args", [])
        expected = item.get("expected")
        if func is not None:
            tests.append((func, tuple(args), expected))
    return tests


def load_module(path):
    """Load a Python module dynamically from a file path."""
    spec = importlib.util.spec_from_file_location("student_module", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def grade_module(module):
    """Run all test cases on the given module/function and return score + details."""
    try:
        TESTS = load_tests()
    except Exception as e:
        print(f"⚠️ Could not load test cases: {e}")
        return 0, []

    score = 0
    results = []

    for func_name, args, expected in TESTS:
        func = getattr(module, func_name, None)
        if func is None:
            results.append((func_name, "❌ Missing function"))
            continue

        try:
            start_case = timer()
            output = func(*args)
            duration = timer() - start_case

            if output == expected:
                score += 1
                results.append((func_name, f"✅ PASS ({duration:.6f}s)"))
            else:
                results.append((func_name, f"❌ FAIL ({duration:.6f}s, got {output}, expected {expected})"))
        except Exception as e:
            results.append((func_name, f"⚠️ ERROR: {e}"))

    return score, results


def list_submissions():
    """Return a list of .py files in the submissions folder."""
    if not os.path.exists(SUBMISSIONS_FOLDER):
        os.makedirs(SUBMISSIONS_FOLDER)
    return [f for f in os.listdir(SUBMISSIONS_FOLDER) if f.endswith(".py")]


def grade_selected(selected):
    """Grade one or more submissions."""
    for file in selected:
        path = os.path.join(SUBMISSIONS_FOLDER, file)
        try:
            module = load_module(path)
        except Exception as e:
            print(f"\n❌ Could not load {file}: {e}")
            continue

        start_time = timer()
        score, results = grade_module(module)
        elapsed = timer() - start_time

        print(f"\nResults for {file}: ")
        for func, result in results:
            print(f"  {func:<10}: {result}")
        print(f"  => Final Score: {score}/{len(load_tests())}")
        print(f"  🕒 Total Time: {elapsed:.6f} seconds")

    input("\nPress Enter to return to menu...")


def display_grading_menu():
    """Display a menu for grading submissions (used by main.py)."""
    while True:
        cls()
        submissions = list_submissions()
        print("📂 Available submissions:")
        for i, file in enumerate(submissions, start=1):
            print(f"{i}. {file}")
        print("\nY. Test ALL")
        print("N. Return to Main Menu")

        choice = input("\nSelect an option: ").strip().lower()

        # test-all and exit
        if choice == "n":
            break
        elif choice == "y":
            grade_selected(submissions)
            continue

        # test your choice
        if choice.isdigit():
            choice_num = int(choice)
            if 1 <= choice_num <= len(submissions):
                grade_selected([submissions[choice_num - 1]])
            else:
                input("Invalid choice. Press Enter to continue...")
        else:
            input("Invalid input. Press Enter to continue...")
