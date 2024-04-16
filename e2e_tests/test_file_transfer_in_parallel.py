import concurrent.futures
import subprocess
import sys

# List of file paths to test
file_paths = [
    "/home/stevehiehn/dawnet/dawnet-server/e2e_tests/assets/old_mcdonald.wav",
    "/home/stevehiehn/dawnet/dawnet-server/e2e_tests/assets/guns_n_roses.mid",
    # Add more file paths as needed
]


def run_test(file_path):
    """Run the test_file_transfer.py script for a given file path."""
    try:
        # Execute the test script for the given file path
        result = subprocess.run(
            ["python", "/home/stevehiehn/dawnet/dawnet-server/e2e_tests/test_file_transfer.py", file_path], check=True)
        return result.returncode  # Should be 0 for success
    except subprocess.CalledProcessError as e:
        print(f"Test failed for {file_path}: {e}")
        return e.returncode  # Non-zero return code for failure


def main():
    # Use ThreadPoolExecutor to run tests in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        # Map each file path to the run_test function and execute them in parallel
        futures = [executor.submit(run_test, file_path) for file_path in file_paths]

        # Initialize a flag to track if any tests failed
        any_failures = False

        # Wait for all futures to complete
        for future in concurrent.futures.as_completed(futures):
            if future.result() != 0:
                any_failures = True  # Mark that we had at least one failure

        # If any tests failed, exit with a non-zero exit code
        if any_failures:
            print("One or more tests failed.")
            sys.exit(1)  # Exit with a failure code

        print("All tests passed successfully.")


if __name__ == "__main__":
    main()
