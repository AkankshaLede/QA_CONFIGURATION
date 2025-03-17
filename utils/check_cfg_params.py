import configparser
import argparse

def read_cfg_to_dict(file_path):
    """ Reads a .cfg file and returns a dictionary representation. """
    # print(f"  Reading file: {file_path}")  # Debugging
    config = configparser.ConfigParser()
    config.optionxform = str  # Preserve case sensitivity
    config.read(file_path)
    return {section: dict(config.items(section)) for section in config.sections()}

def compare_configs(actual_cfg, expected_cfg, file_name):
    """ Compares actual config with expected config and prints mismatches. """
    mismatches = []

    # Check missing sections
    for section in expected_cfg:
        if section not in actual_cfg:
            mismatches.append(f" Missing section: [{section}] in {file_name}")

    # Check for key mismatches and missing keys
    for section, expected_keys in expected_cfg.items():
        if section in actual_cfg:
            for key, expected_value in expected_keys.items():
                actual_value = actual_cfg[section].get(key)

                if actual_value is None:
                    mismatches.append(f" Missing key '{key}' in section [{section}] in {file_name}")
                elif actual_value != expected_value:
                    mismatches.append(f" '{key}' in section [{section}] is '{actual_value}', expected '{expected_value}' in {file_name}")

    # Check for extra keys in actual config
    # for section, actual_keys in actual_cfg.items():
    #     if section in expected_cfg:
    #         for key in actual_keys:
    #             if key not in expected_cfg[section]:
    #                 mismatches.append(f" Unexpected key '{key}' found in section [{section}] in {file_name}")

    return mismatches

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate configuration files")
    parser.add_argument("--input_files", required=True, help="Comma-separated list of input config files")
    parser.add_argument("--default_file", required=True, help="Path to expected configuration file")

    args = parser.parse_args()
    input_files = args.input_files.split(",")
    expected_cfg = read_cfg_to_dict(args.default_file)

    all_mismatches = []

    for file in input_files:
        actual_cfg = read_cfg_to_dict(file)
        mismatches = compare_configs(actual_cfg, expected_cfg, file)
        if mismatches:
            all_mismatches.extend(mismatches)

    # Print mismatches
    if all_mismatches:
        # print("\n CONFIGURATION MISMATCHES FOUND:\n")
        print("\n".join(all_mismatches))
        exit(1)  # Fail script
    else:
        print("\n  All configuration files match expected values!")