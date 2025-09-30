import json
import os
from pathlib import Path

def convert_workflow(input_file, output_dir):
    """
    Convert n8n workflow from captured format to standard format.
    
    Args:
        input_file: Path to the captured workflow JSON file
        output_dir: Directory to save the converted workflow
    """
    try:
        # Read the captured workflow file
        with open(input_file, 'r', encoding='utf-8') as f:
            captured_data = json.load(f)
        
        # Check if this is already in the correct format (no 'data' wrapper)
        if 'data' not in captured_data:
            print(f"✓ {input_file} is already in correct format, copying as-is")
            workflow_data = captured_data
        else:
            # Extract the actual workflow from the 'data' wrapper
            workflow_data = captured_data['data']
            print(f"✓ Converting {input_file}")
        
        # Build the output workflow in correct format
        output_workflow = {
            "name": workflow_data.get("name", "Untitled Workflow"),
            "nodes": workflow_data.get("nodes", []),
            "pinData": workflow_data.get("pinData", {}),
            "connections": workflow_data.get("connections", {}),
            "active": workflow_data.get("active", False),
            "settings": workflow_data.get("settings", {"executionOrder": "v1"}),
            "versionId": workflow_data.get("versionId", ""),
            "meta": workflow_data.get("meta", {}),
            "id": workflow_data.get("id", ""),
            "tags": workflow_data.get("tags", [])
        }
        
        # Create output filename (remove 'Captured' suffix if present)
        input_filename = Path(input_file).stem
        if input_filename.endswith('Captured'):
            output_filename = input_filename[:-8] + '.json'
        else:
            output_filename = input_filename + '_converted.json'
        
        output_path = Path(output_dir) / output_filename
        
        # Write the converted workflow
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_workflow, f, indent=2, ensure_ascii=False)
        
        print(f"  → Saved to {output_path}")
        return True
        
    except json.JSONDecodeError as e:
        print(f"✗ Error parsing JSON in {input_file}: {e}")
        return False
    except Exception as e:
        print(f"✗ Error processing {input_file}: {e}")
        return False

def batch_convert(input_dir, output_dir):
    """
    Convert all workflow JSON files in a directory.
    
    Args:
        input_dir: Directory containing captured workflow files
        output_dir: Directory to save converted workflows
    """
    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Find all JSON files
    json_files = list(Path(input_dir).glob('*.json'))
    
    if not json_files:
        print(f"No JSON files found in {input_dir}")
        return
    
    print(f"Found {len(json_files)} JSON file(s) to process\n")
    
    success_count = 0
    for json_file in json_files:
        if convert_workflow(json_file, output_dir):
            success_count += 1
        print()  # Empty line between files
    
    print(f"\nConversion complete: {success_count}/{len(json_files)} files processed successfully")

if __name__ == "__main__":
    # Configuration
    INPUT_DIR = "."  # Current directory - change as needed
    OUTPUT_DIR = "./converted_workflows"  # Output directory
    
    print("N8N Workflow Format Converter")
    print("=" * 50)
    print(f"Input directory: {INPUT_DIR}")
    print(f"Output directory: {OUTPUT_DIR}")
    print("=" * 50 + "\n")
    
    batch_convert(INPUT_DIR, OUTPUT_DIR)