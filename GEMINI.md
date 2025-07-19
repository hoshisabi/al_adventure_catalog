## Gemini Notes for Windows `jq` and Verification

- When running `jq` commands with filters or complex expressions on Windows, it's often necessary to write the `jq` command to a temporary batch file (e.g., `temp_jq_command.bat`) and then execute the batch file. This helps bypass quoting issues with `cmd.exe`.
- After running `maintaindb/aggregator.py`, it's crucial to verify the `all_adventures.json` file using `jq` to ensure the data is correctly aggregated and formatted. For example, to check the `hours` field for a specific adventure:
  ```
  jq ".[] | select(.full_title == \"Your Adventure Title\") | .hours" assets/data/all_adventures.json
  ```
  Remember to use a temporary batch file for this command on Windows.