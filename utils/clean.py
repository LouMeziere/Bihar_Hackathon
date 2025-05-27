import json

# Function to clean points GeoJSON by keeping only 'name' and 'geometry'
def clean_points(input_path, output_path):
    # Load original points data
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    cleaned_features = []
    for feature in data["features"]:
        cleaned_features.append({
            "type": "Feature",
            "properties": {
                "name": feature["properties"].get("name", "")  # Keep only the name
            },
            "geometry": feature["geometry"]  # Retain geometry (latitude/longitude)
        })

    # Construct cleaned GeoJSON structure
    cleaned_data = {
        "type": "FeatureCollection",
        "features": cleaned_features
    }

    # Save to new file
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(cleaned_data, f, indent=2)


# Function to clean lines GeoJSON by keeping only 'name' and 'geometry'
def clean_lines(input_path, output_path):
    # Load original lines data
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    cleaned_features = []
    for feature in data["features"]:
        cleaned_features.append({
            "type": "Feature",
            "properties": {
                "name": feature["properties"].get("name", "")  # Keep only the name
            },
            "geometry": feature["geometry"]  # Retain geometry (lines)
        })

    # Construct cleaned GeoJSON structure
    cleaned_data = {
        "type": "FeatureCollection",
        "features": cleaned_features
    }

    # Save to new file
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(cleaned_data, f, indent=2)


# === Run the cleaning functions for both datasets ===

# Clean points file
clean_points(
    "images/railway/railways_points.geojson",          # Input file path
    "images/railway/railways_points_cleaned.geojson"   # Output file path
)

# Clean lines file
clean_lines(
    "images/railway/railways_lines.geojson",           # Input file path
    "images/railway/railways_lines_cleaned.geojson"    # Output file path
)

