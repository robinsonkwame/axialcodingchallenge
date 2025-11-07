"""
Script to extract only project descriptions from NFT1000 dataset
This requires access to the gated Hugging Face dataset: shuxunoo/NFT-Net
"""

import json
import os
from pathlib import Path

def extract_project_descriptions(dataset_path, output_file, max_projects=50):
    """
    Extract project descriptions from NFT1000 metadata dashboard files.
    
    Args:
        dataset_path: Path to the NFT1000 directory
        output_file: Path to save the extracted descriptions
        max_projects: Number of projects to extract (default 50)
    """
    
    project_data = []
    nft1000_path = Path(dataset_path) / "NFT1000"
    
    if not nft1000_path.exists():
        print(f"Error: Path {nft1000_path} does not exist")
        return
    
    # Get all project directories
    project_dirs = sorted([d for d in nft1000_path.iterdir() if d.is_dir()])
    
    print(f"Found {len(project_dirs)} projects in NFT1000")
    print(f"Extracting descriptions for first {max_projects} projects...\n")
    
    for i, project_dir in enumerate(project_dirs[:max_projects], 1):
        project_name = project_dir.name
        metadata_file = project_dir / "metadata_dashboard.json"
        
        if metadata_file.exists():
            try:
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
                
                # Extract relevant information
                project_info = {
                    "rank": i,
                    "project_name": project_name,
                    "description": metadata.get("description", "No description available"),
                    "contract_address": metadata.get("contract_address", ""),
                    "total_supply": metadata.get("total_supply", ""),
                    "official_url": metadata.get("official_url", ""),
                    "opensea_url": metadata.get("opensea_url", "")
                }
                
                project_data.append(project_info)
                print(f"{i}. {project_name}")
                
            except Exception as e:
                print(f"Error reading metadata for {project_name}: {e}")
        else:
            print(f"Warning: No metadata_dashboard.json found for {project_name}")
    
    # Save to JSON file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(project_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Extracted descriptions for {len(project_data)} projects")
    print(f"✓ Saved to: {output_file}")
    
    return project_data


def create_readable_report(project_data, output_file):
    """Create a human-readable text report of the projects."""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("NFT1000 DATASET - FIRST 50 PROJECTS\n")
        f.write("=" * 80 + "\n\n")
        
        for project in project_data:
            f.write(f"{project['rank']}. {project['project_name']}\n")
            f.write("-" * 80 + "\n")
            f.write(f"Description: {project['description']}\n")
            if project.get('total_supply'):
                f.write(f"Total Supply: {project['total_supply']}\n")
            if project.get('official_url'):
                f.write(f"Official URL: {project['official_url']}\n")
            if project.get('opensea_url'):
                f.write(f"OpenSea: {project['opensea_url']}\n")
            if project.get('contract_address'):
                f.write(f"Contract: {project['contract_address']}\n")
            f.write("\n\n")
    
    print(f"✓ Created readable report: {output_file}")


if __name__ == "__main__":
    # Example usage - modify these paths as needed
    
    # Option 1: If you've downloaded/cloned the entire dataset
    dataset_path = "/path/to/your/NFT-Net"
    
    # Or Option 2: If you've downloaded individual projects
    # dataset_path = "/path/to/your/download/location"
    
    output_json = "nft1000_first50_descriptions.json"
    output_txt = "nft1000_first50_descriptions.txt"
    
    # Extract descriptions
    project_data = extract_project_descriptions(
        dataset_path=dataset_path,
        output_file=output_json,
        max_projects=50
    )
    
    # Create readable report
    if project_data:
        create_readable_report(project_data, output_txt)
        
        print(f"\nSummary:")
        print(f"- JSON data: {output_json}")
        print(f"- Text report: {output_txt}")
