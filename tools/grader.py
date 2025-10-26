import importlib.util
import os
import json
from time import perf_counter_ns as timer

SUBMISSIONS_FOLDER = "submissions"
TEST_FILE = "tests.json"


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def load_tests():
    if not os.path.exists(TEST_FILE):
        raise FileNotFoundError(f"Test file not found: {TEST_FILE}")
    with open(TEST_FILE, "r") as f:
        data = json.load(f)
    return [(i["function"], tuple(i.get("args", [])), i["expected"]) for i in data if "function" in i]


def load_module(path):
    spec = importlib.util.spec_from_file_location("student_module", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def grade_module(module, TESTS=None):
    if TESTS is None:
        TESTS = load_tests()
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
            duration = (timer() - start_case) / 1e9
            if output == expected:
                score += 1
                results.append((func_name, f"✅ PASS ({duration:.6f}s)"))
            else:
                results.append((func_name, f"❌ FAIL ({duration:.6f}s, got {output}, expected {expected})"))
        except Exception as e:
            results.append((func_name, f"⚠️ ERROR in {func_name}: {type(e).__name__}: {e}"))
    return score, results


def list_submissions():
    if not os.path.exists(SUBMISSIONS_FOLDER):
        os.makedirs(SUBMISSIONS_FOLDER)
    return [f for f in os.listdir(SUBMISSIONS_FOLDER) if f.endswith(".py")]


def format_results(filename, score, total, results, elapsed):
    lines = [f"\nResults for {filename}:"]
    lines += [f"  {func:<10}: {result}" for func, result in results]
    lines.append(f"  => Final Score: {score}/{total}")
    lines.append(f"  🕒 Total Time: {elapsed:.6f} seconds\n")
    return "\n".join(lines)


def grade_selected(selected):
    TESTS = load_tests()
    for file in selected:
        path = os.path.join(SUBMISSIONS_FOLDER, file)
        try:
            module = load_module(path)
        except Exception as e:
            print(f"\n❌ Could not load {file}: {e}")
            continue
        start_time = timer()
        score, results = grade_module(module, TESTS)
        elapsed = (timer() - start_time) / 1e9
        print(format_results(file, score, len(TESTS), results, elapsed))
    input("\nPress Enter to return to menu...")


def display_grading_menu():
    while True:
        cls()
        submissions = list_submissions()
        print("📂 Available submissions:")
        for i, file in enumerate(submissions, start=1):
            print(f"{i}. {file}")
        print("\nY. Test ALL")
        print("N. Return to Main Menu")

        choice = input("\nSelect an option: ").strip().lower()
        if choice == "n":
            break
        elif choice == "y":
            grade_selected(submissions)
            continue
        if choice.isdigit():
            idx = int(choice)
            if 1 <= idx <= len(submissions):
                grade_selected([submissions[idx - 1]])
            else:
                input("Invalid choice. Press Enter to continue...")
        else:
            input("Invalid input. Press Enter to continue...")
