import sys
import yaml


def convert_yaml_to_string(yaml_file, format="key-value"):
    """
    Converts a YAML file to a string in the desired format.

    Args:
        yaml_file (str): Path to the YAML file.
        format (str, optional): Desired output format ('key-value-pair' or 'key-value'). Defaults to 'key-value'.

    Returns:
        str: The converted string.
    """

    with open(yaml_file, "r") as f:
        data = yaml.safe_load(f)

    if format == "key-value-pair":
        output_str = " ".join(
            f"ParameterKey={key},ParameterValue={value}" for key, value in data.items()
        )
    elif format == "key-value":
        output_str = " ".join(f"{key}={value}" for key, value in data.items())
    else:
        raise ValueError(
            "Invalid format specified. Please choose 'key-value-pair' or 'key-value'."
        )

    return output_str


output_string = convert_yaml_to_string(sys.argv[1], "key-value-pair")
print(output_string)
