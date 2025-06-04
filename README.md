#Configuration File Validator

This repository contains logic to validate .ini configuration files based on custom rules. These validations are intended to be used in CI/CD workflows (e.g., GitHub Actions or Jenkins pipelines) to ensure correctness and prevent potential deployment or runtime issues due to misconfigured parameters.


## Why Use This Validator?

1. **Prevent Errors:** Catch common configuration mistakes early in the development cycle.
2. **Improve Reliability:** Ensure consistent and correct configuration across different environments.
3. **Automate Checks:** Seamlessly integrate validation into your automated build and deployment processes.
4. **Customizable Rules:** Define specific validation logic tailored to your application's needs.


## Configuration File Structure

The configuration file is divided into logical sections. Below is a sample structure:

```ini
[System]
Read_delay= 10
Write_delay=100

[settings]
image_format = png
image_compression = SHOULD_NOT_BE_PRESENT

[dataset]
calibration_count = RANGE[1,5]
validation_count = 2

[regression]
network_detail = MUST_EXIST
```

MUST_EXIST
This rule dictates that a specific key must be present within its designated section in the configuration file
1. This means that the key must exist in the configuration file.
2. It should not be empty or missing.
3. If the key is not found, the check will fail.


SHOULD_NOT_BE_PRESENT
This rule specifies that a particular key must not be present in the configuration file at all.
1. If the key exists, even with an empty value, the check will fail.

RANGE[min,max]
This rule is designed for numeric values and ensures that a parameter's value falls within a specified inclusive range.
1. It checks whether the value lies within the specified range.
2. If the value is below or above the range, the check will fail.




