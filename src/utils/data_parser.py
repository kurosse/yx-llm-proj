import json
import pandas as pd


def parse_csv(file_path: str) -> pd.DataFrame:
    """
    Parses a CSV file and returns a DataFrame.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pd.DataFrame: The parsed DataFrame.
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        print(f"Error parsing CSV file: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error


def parse_json(file_path: str) -> dict:
    """
    Parses a JSON file and returns its content as a dictionary.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        dict: The parsed JSON content.
    """
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
        return data
    except Exception as e:
        print(f"Error parsing JSON file: {e}")
        return {}  # Return an empty dictionary on error


def append_rating(model_output, path="ratings.json"):
    # model_output: a Pydantic model instance
    item = model_output.dict()  # or json.loads(model_output.json())
    with open(path, "r+", encoding="utf-8") as f:
        data = json.load(f)  # load existing list
        data.append(item)  # append new entry
        f.seek(0)  # rewind to file start
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.truncate()  # cut off any leftover
