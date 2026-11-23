import os

def apply_configuration(config_file_path, desired_content):
    """
    Simulates a configuration management tool applying a desired state to a file.
    This function checks the current state and applies changes if necessary,
    demonstrating idempotency.
    """
    print(f"Checking configuration for: {config_file_path}")
    current_content = ""
    file_exists = os.path.exists(config_file_path)

    if file_exists:
        with open(config_file_path, 'r') as f:
            current_content = f.read()

    # Normalize content for comparison (remove leading/trailing whitespace/newlines)
    if current_content.strip() == desired_content.strip():
        print("Configuration is already in the desired state. No changes needed.")
        return False # No change made
    else:
        print("Configuration mismatch detected. Applying desired state...")
        with open(config_file_path, 'w') as f:
            f.write(desired_content.strip() + "\n") # Ensure a newline at the end
        print(f"Configuration applied to {config_file_path}.")
        return True # Change made

if __name__ == "__main__":
    # Define the desired state for a simple configuration file.
    # This represents the "Infrastructure as Code" principle, where desired
    # system states are defined in code, similar to Puppet manifests.
    config_filename = "myapp_config.conf"
    desired_config_content = """
[application]
debug_mode = false
log_level = INFO

[database]
host = localhost
port = 5432
user = appuser
"""

    print("--- Simulating Configuration Management ---")

    # First run: The script will likely create the file or update it
    # to match the desired state, just as Puppet would enforce a state.
    print("\n--- First Run ---")
    changed_first_run = apply_configuration(config_filename, desired_config_content)
    if changed_first_run:
        print(f"Initial configuration applied successfully to {config_filename}.")
    else:
        print(f"Initial configuration for {config_filename} was already correct.")

    # Second run: Demonstrates idempotency. No changes should be reported
    # if the desired state is already met, which is a key feature of CM tools.
    print("\n--- Second Run (should be idempotent) ---")
    changed_second_run = apply_configuration(config_filename, desired_config_content)
    if not changed_second_run:
        print(f"Configuration for {config_filename} remains in desired state (idempotent).")

    # Simulate a manual change or configuration drift, which a CM tool
    # like Puppet is designed to detect and correct.
    print("\n--- Simulating Configuration Drift ---")
    print(f"Manually modifying {config_filename} to simulate drift...")
    with open(config_filename, 'w') as f:
        f.write("[application]\ndebug_mode = true\nlog_level = DEBUG\n") # Malicious or accidental change

    # Re-apply configuration after drift: The script should detect the change
    # and revert the file to the desired state.
    print("\n--- Re-applying configuration after drift ---")
    changed_after_drift = apply_configuration(config_filename, desired_config_content)
    if changed_after_drift:
        print(f"Drift detected and corrected for {config_filename}.")
    else:
        print(f"Configuration for {config_filename} was unexpectedly correct after drift simulation.")

    print("\n--- Configuration Management Simulation Complete ---")
    print(f"Check the file '{config_filename}' in your current directory to see the final state.")
