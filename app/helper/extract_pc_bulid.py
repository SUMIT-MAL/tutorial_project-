import json
import ast


def extract_pc_build(parsed_chunk):
    # Handle a Python representation stored as a string.
    if isinstance(parsed_chunk, str):
        try:
            parsed_chunk = json.loads(parsed_chunk)
        except json.JSONDecodeError:
            parsed_chunk = ast.literal_eval(parsed_chunk)

    # Search nested lists and dictionaries for MCP text.
    if isinstance(parsed_chunk, list):
        for item in parsed_chunk:
            result = extract_pc_build(item)
            if result is not None:
                return result

    elif isinstance(parsed_chunk, dict):
        if parsed_chunk.get("type") == "text":
            text = parsed_chunk.get("text", "")
            return extract_pc_build(text)

        if isinstance(parsed_chunk.get("parts"), list):
            return parsed_chunk

        for value in parsed_chunk.values():
            result = extract_pc_build(value)
            if result is not None:
                return result

    elif isinstance(parsed_chunk, str):
        try:
            data = json.loads(parsed_chunk)
            if isinstance(data, dict) and "parts" in data:
                return data
            return extract_pc_build(data)
        except json.JSONDecodeError:
            return None

    return None
