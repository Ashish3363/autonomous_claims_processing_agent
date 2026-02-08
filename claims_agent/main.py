import argparse
import json
import os
import sys

# Add current directory to sys.path to ensure local imports work
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.ingest import read_file
from src.extract import extract_fields
from src.logic import find_missing_fields, decide_route, build_reasoning
from src.models import RoutingOutput

def process_fnol(file_path: str):
    """
    End-to-end processing of a single FNOL file.
    """
    print(f"Processing: {file_path}")
    
    # 1. Ingestion
    try:
        raw_text = read_file(file_path)
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    # 2. Extraction
    extracted_fields = extract_fields(raw_text)

    # 3. Validation
    missing_fields = find_missing_fields(extracted_fields)

    # 4. Routing
    route = decide_route(extracted_fields, missing_fields)

    # 5. Reasoning
    reasoning = build_reasoning(route, extracted_fields, missing_fields)

    # 6. Output
    output = RoutingOutput(
        extractedFields=extracted_fields,
        missingFields=missing_fields,
        recommendedRoute=route,
        reasoning=reasoning
    )

    # Print nicely formatted JSON
    print(json.dumps(output.model_dump(), indent=2, default=str))

    # Optional: Save to file
    output_filename = os.path.splitext(os.path.basename(file_path))[0] + "_output.json"
    
    # Always save to logic-defined output directory (project_root/output)
    project_root = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(project_root, "output")
    os.makedirs(output_dir, exist_ok=True)
    
    output_path = os.path.join(output_dir, output_filename)
    with open(output_path, "w") as f:
        json.dump(output.model_dump(), f, indent=2, default=str)
    print(f"Output saved to: {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Insurance Claims Processing Agent")
    parser.add_argument("--file", type=str, help="Path to the FNOL document (PDF or TXT)")
    parser.add_argument("--all", action="store_true", help="Process all dummy files in data/ folder")
    
    args = parser.parse_args()

    if args.all:
        data_dir = os.path.join(os.path.dirname(__file__), "data")
        for filename in os.listdir(data_dir):
            if filename.endswith(".txt") or filename.endswith(".pdf"):
                filepath = os.path.join(data_dir, filename)
                print("-" * 40)
                process_fnol(filepath)
    elif args.file:
        process_fnol(args.file)
    else:
        print("Please provide a file using --file or use --all to process all dummy data.")

if __name__ == "__main__":
    main()
