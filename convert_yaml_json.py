import yaml
import json

def convert_yaml_file_to_json(yaml_file_path):
    with open(yaml_file_path, 'r') as file:
        yaml_data = yaml.safe_load(file)
        json_data = json.dumps(yaml_data, indent=4)
        return json_data

# Example usage
yaml_file_path = 'config.yaml'

json_data = convert_yaml_file_to_json(yaml_file_path)
print(json_data)





