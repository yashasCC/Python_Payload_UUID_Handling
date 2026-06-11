import re
import sys

def convert_ids(input_path, output_path, start_index=1):
    with open(input_path, "r", encoding="utf-8") as f:
        content = f.read()

    counter = start_index

    # Match only hardcoded UUID under "id" key
    pattern = r'("id"\s*:\s*")([0-9a-fA-F\-]{36})(")'

    def replace_id(match):
        nonlocal counter

        uuid_value = match.group(2)

        # Strict UUID validation (extra safety)
        strict_uuid = re.fullmatch(
            r'[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}',
            uuid_value
        )

        if strict_uuid:
            replacement = f'"id": "${{P_RandomID{counter}}}"'
            counter += 1
            return replacement
        else:
            return match.group(0)

    new_content = re.sub(pattern, replace_id, content)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"✅ Done! Replaced {counter - start_index} id fields.")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python convert_ids.py input.json output.json")
    else:
        convert_ids(sys.argv[1], sys.argv[2])
