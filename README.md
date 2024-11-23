# TekConverter: Converter for .tek, JSON, and YAML Files

TekConverter is a Python class designed to facilitate bidirectional conversion between .tek, .json, and .yaml file formats. This utility is particularly useful for integrating configuration files across systems and simplifying interoperability.

## Key Features
File Reading and Writing:

- .tek: Supports a custom file format with headers, indices, descriptions, and associated parameters.
- JSON: A widely used structured data format.
- YAML: A human-readable data serialization format.

## File Conversion:

Converts between supported formats while preserving data structures and information integrity.

## Error and Warning Handling:

Returns specific codes to indicate errors and warnings during execution (e.g., file not found, unsupported format, load/write failure).

## Code Structure

- Status Codes
Status codes define the outcome of an operation:
  - ERROR_FAILED_TO_LOAD_FILE (-4): Failed to load the input file.
  - ERROR_FAILED_TO_WRITE_FILE (-3): Failed to write the output file.
  - WARNING_FILE_NOT_FOUND (-2): Input file not found.
  - WARNING_UNSUPPORTED_FORMAT (-1): Unsupported file format.
  - SUCCESS (0): Operation completed successfully.

## Class TekConverter

### Public Method:

convert(input: str, output: str) -> int:
- Accepts the paths for input and output files.
- Determines the format based on file extensions.
- Handles reading and writing through format-specific private methods.
- Returns a status code indicating the result.

### Private Methods:

#### File Reading:

- __load_yaml(settings: dict, input: str) -> bool:
Reads data from a YAML file and updates the settings dictionary.
- __load_json(settings: dict, input: str) -> bool:
Reads data from a JSON file and updates the settings dictionary.
- __load_tek(settings: dict, input: str) -> bool:
Parses .tek files, identifying headers, indices, descriptions, and associated parameters.

#### File Writing:

- __write_yaml(settings: dict, output: str) -> bool:
Writes the settings dictionary to a YAML file.
- __write_json(settings: dict, output: str) -> bool:
Writes the settings dictionary to a JSON file.
- __write_tek(settings: dict, output: str) -> bool:
Writes the settings dictionary to the .tek format.

## Execution Flow

### Verify Input File Existence:

If the input file does not exist, returns WARNING_FILE_NOT_FOUND.

### Determine Input and Output Formats:

Based on file extensions .tek, .json, or .yaml, calls the appropriate reading and writing methods.
Returns WARNING_UNSUPPORTED_FORMAT for invalid extensions.
Read Input File:

Loads the file's contents into a settings dictionary.
Write Output File:

Converts and saves the data to the desired format.
Return Result:

Returns the status of the operation using predefined status codes.
Usage Examples

```
converter = TekConverter()

# Convert from .tek to .json
status = converter.convert(input="config.tek", output="config.json")
print("Status:", status)  # Displays the status code

# Convert from .json to .yaml
status = converter.convert(input="config.json", output="config.yaml")
print("Status:", status)
```
## Requirements
### Dependencies:

- PyYAML: For handling YAML files.
- os, json: Standard Python libraries for system operations and JSON manipulation.

