#!/bin/bash

# Initialize pyenv and Python environment
export PYENV_ROOT="/var/lib/jenkins/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv virtualenv-init -)"

# Set Python version
pyenv global 3.9.0

# Verify Python version
python --version

# Install dependencies
pip install -r /home/stevehiehn/dawnet/dawnet-server/e2e_tests/requirements.txt

# List of file paths to test
declare -a file_paths=(
    "/home/stevehiehn/dawnet/dawnet-server/e2e_tests/assets/old_mcdonald.wav"
    "/home/stevehiehn/dawnet/dawnet-server/e2e_tests/assets/guns_n_roses.mid"
    # Add more file paths as needed
)

# Function to run tests
run_test() {
    file_path="$1"
    echo "Starting test for $file_path"
    if python /home/stevehiehn/dawnet/dawnet-server/e2e_tests/test_file_transfer.py "$file_path"; then
        echo "Test passed for $file_path"
    else
        echo "Test failed for $file_path"
        exit 1
    fi
}

# Execute tests in parallel
for file_path in "${file_paths[@]}"; do
    run_test "$file_path" &
done

# Wait for all background processes to complete
wait
echo "All tests completed."
