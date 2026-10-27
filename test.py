import json
import js


def save(key: str, data_list: list):
  """Saves a Python list to browser localStorage as a JSON string."""
  json_string = json.dumps(data_list)
  js.localStorage.setItem(key, json_string)


def load(key: str) -> list:
  """Retrieves a JSON string from localStorage and parses it back into a Python list."""
  item = js.localStorage.getItem(key)
  if item is not None:
    return json.loads(item)
  return []