import pandas as pd
import yaml
import os

# Load CSV
df = pd.read_csv("dataset\heart.csv")

# Function to map pandas dtype to simplified schema type
def map_dtype(dtype):
    if "int" in str(dtype):
        return "int64"
    elif "float" in str(dtype):
        return "float64"
    elif "bool" in str(dtype):
        return "bool"
    else:
        return "string"

schema = {"columns": [], "numerical_columns": [], "categorical_columns": []}

# Loop through columns
for col in df.columns:
    dtype = map_dtype(df[col].dtype)

    # Add to columns
    schema["columns"].append({col: dtype})

    # Categorize
    if dtype in ["int64", "float64"]:
        schema["numerical_columns"].append(col)
    else:
        schema["categorical_columns"].append(col)

folder_name = "data_schema"
# Save to schema.yaml
output_path = os.path.join(os.getcwd(),folder_name, "schema.yaml")
with open(output_path, "w") as f:
    yaml.dump(schema, f, sort_keys=False)

print(f"Schema saved to: {output_path}")