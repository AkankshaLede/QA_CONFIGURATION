import configparser
import argparse
import os

def read_cfg_to_dict(file_path):
    config = configparser.ConfigParser()
    config.read(file_path)
    return {section: dict(config.items(section)) for section in config.sections()}

def validate_config(actual_cfg, expected_cfg, file1_cfg_path):
    mismatches = []
    flag = 0

    for section, expected_params in expected_cfg.items():
        for key, expected_value in expected_params.items():
            if expected_value == "SHOULD_NOT_BE_PRESENT":
                if section in actual_cfg and key in actual_cfg[section]:
                    mismatches.append(f"Error: '{key}' should not be present in section [{section}] in {file1_cfg_path}")
                    flag = 1

    for section, expected_params in expected_cfg.items():
        if section in actual_cfg:
            for key, expected_value in expected_params.items():
                if expected_value == "SHOULD_NOT_BE_PRESENT":
                    continue

                actual_value = actual_cfg[section].get(key)
                if actual_value is None:
                    mismatches.append(f"{key} is missing in section [{section}] {file1_cfg_path}")
                    flag = 1
                elif actual_value != expected_value:
                    mismatches.append(f"{key} in section [{section}] is {actual_value}, expected {expected_value}")
                    flag = 1
        else:
            if all(value == "SHOULD_NOT_BE_PRESENT" for value in expected_params.values()):
                continue
            mismatches.append(f"Section [{section}] is missing in {file1_cfg_path}")
            flag = 1
    
    return mismatches, flag

# Set path to parent directory of the script, where `cfgfiles` is located
script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cfg_path = os.path.join(script_dir, 'cfgfiles')

# Check if directory exists
if not os.path.exists(cfg_path):
    raise FileNotFoundError(f"Config directory '{cfg_path}' not found")

# Update file paths to use absolute paths
parser = argparse.ArgumentParser(description="Compare multiple .cfg files with a single expected .cfg file")
parser.add_argument('actual_files', nargs='+', type=str, help="Path to the actual .cfg files")
parser.add_argument('expected_file', type=str, help="Path to the expected .cfg file")

args = parser.parse_args()

# Use absolute paths to locate files
actual_files = [os.path.join(cfg_path, file) for file in args.actual_files]
expected_file = os.path.join(cfg_path, args.expected_file)

expected_config = read_cfg_to_dict(expected_file)

overall_flag = 0
for file in actual_files:
    actual_config = read_cfg_to_dict(file)
    mismatch_list, flag = validate_config(actual_config, expected_config, file)

    if mismatch_list:
        print("\n".join(mismatch_list))
    else:
        print(f"All parameters in '{file}' match the expected configuration.")

    overall_flag = max(overall_flag, flag)

print("\nOverall Execution flag:", overall_flag)
