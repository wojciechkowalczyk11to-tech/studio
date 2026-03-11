import argparse
import sys
import tomllib
from pathlib import Path

def validate_command_file(filepath):
    print(f"Validating {filepath}...")
    try:
        with open(filepath, "rb") as f:
            data = tomllib.load(f)
    except Exception as e:
        print(f"ERROR: Failed to parse TOML: {e}")
        return False

    allowed_keys = {"description", "prompt"}
    required_keys = {"prompt"}

    keys = set(data.keys())

    # Check for unknown keys
    unknown_keys = keys - allowed_keys
    if unknown_keys:
        print(f"ERROR: Unknown keys found: {unknown_keys}. Allowed: {allowed_keys}")
        return False

    # Check for required keys
    missing_keys = required_keys - keys
    if missing_keys:
        print(f"ERROR: Missing required keys: {missing_keys}")
        return False

    # Validate prompt content
    prompt = data["prompt"]
    if not isinstance(prompt, str) or not prompt.strip():
        print("ERROR: 'prompt' must be a non-empty string.")
        return False

    return True

def main():
    parser = argparse.ArgumentParser(description="Validate Gemini command TOML files.")
    parser.add_argument("directory", type=Path, help="Directory containing .toml command files")
    args = parser.parse_args()

    if not args.directory.exists() or not args.directory.is_dir():
        print(f"ERROR: Directory not found: {args.directory}")
        sys.exit(1)

    failed = False
    files = list(args.directory.glob("*.toml"))
    if not files:
        print(f"WARNING: No .toml files found in {args.directory}")

    for command_file in files:
        if not validate_command_file(command_file):
            failed = True

    if failed:
        print("\nValidation FAILED.")
        sys.exit(1)
    else:
        print("\nValidation PASSED.")
        sys.exit(0)

if __name__ == "__main__":
    main()
