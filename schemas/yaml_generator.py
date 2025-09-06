import yaml
from config.logger import logger

def generate_schema_yaml(schema_data: dict) -> str:
    """
    Converts a structured schema dictionary into a YAML string.
    
    Args:
        schema_data: A dictionary representing the database schema. 
                     Example: {'tables': [{'name': 'employees', 'columns': [...]}]}
    
    Returns:
        A YAML formatted string representing the schema.
    """
    try:
        # Dumps the dictionary to a YAML string. indent=2 makes it readable.
        return yaml.dump(schema_data, indent=2, sort_keys=False)
    except Exception as e:
        logger.error(f"Failed to generate schema YAML: {e}")
        return ""