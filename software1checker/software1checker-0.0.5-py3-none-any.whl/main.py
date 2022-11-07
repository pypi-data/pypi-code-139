from urllib.request import urlopen
import json


def get_all_tests():
    with urlopen(
        "https://gist.githubusercontent.com/noamzaks/38e9723f7f131ce2e2363957afa8324e/raw/tests.json"
    ) as u:
        return json.load(u)


def main():
    import os
    import argparse
    import subprocess

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "folder",
        help="Some directory called hwX-username. Defaults to cwd.",
        default=os.getcwd(),
        nargs="?",
    )
    args = parser.parse_args()

    folder: str = os.path.basename(args.folder)
    if not folder.startswith("hw"):
        print(
            "You should either be in a folder called hwX-username, or pass the folder argument to it"
        )
        exit(-1)
    hw_number = int(folder[2:].split("-")[0])
    os.chdir(os.path.join(args.folder, "src"))

    all_tests = get_all_tests()
    total_passing = 0
    total_failing = 0
    to_fix = set()
    for assignment in all_tests[hw_number - 1]:
        print("Checking " + assignment["filename"])
        for test in assignment["tests"]:
            try:
                p = subprocess.run(
                    ["java", assignment["filename"], *test["arguments"]],
                    input=test["input"],
                    capture_output=True,
                    timeout=20,
                    text=True,
                )
            except subprocess.TimeoutExpired:
                print("Test failed!")
                print("-" * 80)
                print(
                    f"{assignment['filename']} with arguments `{' '.join(test['arguments'])}`"
                )
                print(f"Process took more than 20 seconds")
                print("-" * 80)
                total_failing += 1
                to_fix.add(assignment["filename"])
                continue
            if p.returncode != 0:
                print("Test failed!")
                print("-" * 80)
                print(
                    f"{assignment['filename']} with arguments `{' '.join(test['arguments'])}`"
                )
                print(f"Process exited with status code {p.returncode}.")
                print("-" * 80)
                total_failing += 1
                to_fix.add(assignment["filename"])
            elif p.stdout == test["output"]:
                print("Test passed!")
                total_passing += 1
            else:
                print("Test failed!")
                print("-" * 80)
                print(
                    f"{assignment['filename']} with arguments `{' '.join(test['arguments'])}`"
                )
                print("Expected:\n" + test["output"] + "\nReceived:\n" + p.stdout)
                print("-" * 80)
                total_failing += 1
                to_fix.add(assignment["filename"])

    if total_failing == 0:
        print(f"All {total_passing} tests passed!")
    else:
        print(f"\nResults: {total_failing} failed, {total_passing} succeeded")
        print("You need to fix the following assignments:")
        print("\n".join(map(lambda a: "- " + a, sorted(to_fix))))
