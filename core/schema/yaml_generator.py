import yaml
from core.schema.schema_reader import read_schema

def generate_schema_yaml(output_path="schemas/generated/schema.yaml"):
    schema = read_schema()
    with open(output_path, "w") as f:
        yaml.dump(schema, f, default_flow_style=False)
    return output_path
