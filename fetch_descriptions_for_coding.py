"""
Script to fetch NFT descriptions for axial coding challenge.

Creates:
1. Student file: descriptions with alphanumeric codes only
2. Instructor key: mapping of codes to projects and metadata
3. Metadata log: documents what was fetched for reproducibility
"""

import json
import hashlib
import os
from huggingface_hub import hf_hub_download
from pathlib import Path
from datetime import datetime


# Two distinct categories for expected clustering
CATEGORY_A_ANIMAL_APE = [
    "BoredApeYachtClub",
    "Mutant Ape Yacht Club", 
    "0xApes",
    "Bored Ape Kennel Club",
    "Angry Ape Army",
    "Angry Apes Society",
    "Ape Invaders",
    "Desperate ApeWives",
    "apekidsclub",
    "CyberKongz",
    "Rumble Kong League",
    "Alpha Kongs Club",
    "Cool Cats",
    "Lazy Lions",
    "Pudgy Penguins",
    "LilPudgys",
    "Sappy Seals",
    "Tubby Cats",
    "Anonymice",
    "Boss Beauties",
]

CATEGORY_B_FANTASY_ART = [
    "Azuki",
    "CloneX",
    "Doodles",
    "Moonbirds",
    "CryptoPunks",
    "World of Women",
    "VeeFriends",
    "DigiDaigaku",
    "Murakami.Flowers",
    "Akutars",
    "Imaginary Ones",
    "The Humanoids",
    "Wizards & Dragons Game",
    "Lives of Asuna",
    "Galactic Apes",
    "MOAR by Joan Cornella",
    "AlphaBetty Doodles",
    "Chimpers",
    "a KID called BEAST",
]


def generate_code(project_name, index):
    """Generate alphanumeric code for anonymization."""
    # Create a unique hash-based code
    hash_input = f"{project_name}{index}".encode()
    hash_digest = hashlib.md5(hash_input).hexdigest()
    # Use first 8 characters, uppercase
    return f"NFT{hash_digest[:8].upper()}"


def fetch_descriptions(projects, category_name):
    """Fetch descriptions from Hugging Face for given projects."""
    descriptions = []
    
    # Get token from environment if available
    hf_token = os.environ.get('HF_TOKEN') or os.environ.get('HUGGING_FACE_HUB_TOKEN') or os.environ.get('HUGGINGFACE_TOKEN')
    
    print(f"\n{'='*60}")
    print(f"Fetching {category_name} projects...")
    print(f"{'='*60}")
    
    for i, project in enumerate(projects, 1):
        try:
            file_path = hf_hub_download(
                repo_id="shuxunoo/NFT-Net",
                filename=f"NFT1000/{project}/metadata_dashboard.json",
                repo_type="dataset",
                token=hf_token
            )
            
            with open(file_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            
            description = metadata.get("description", "")
            
            if description:
                code = generate_code(project, i)
                
                descriptions.append({
                    "code": code,
                    "description": description,
                    "project_name": project,
                    "category": category_name,
                    "total_supply": metadata.get("total_supply", "Unknown"),
                    "contract_address": metadata.get("contract_address", ""),
                    "official_url": metadata.get("official_url", ""),
                })
                
                print(f"✓ {i:2d}. {project:40s} [{len(description):4d} chars]")
            else:
                print(f"✗ {i:2d}. {project:40s} [NO DESCRIPTION]")
                
        except Exception as e:
            print(f"✗ {i:2d}. {project:40s} [ERROR: {e}]")
    
    return descriptions


def create_student_file(all_descriptions, output_path):
    """Create anonymized file for students with codes only."""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("NFT PROJECT DESCRIPTIONS - AXIAL CODING CHALLENGE\n")
        f.write("=" * 80 + "\n\n")
        f.write("Instructions:\n")
        f.write("Read through these descriptions and perform axial coding.\n")
        f.write("Each description has a unique code (e.g., NFT12ABC345).\n")
        f.write("Use these codes when referring to specific items.\n")
        f.write("\n" + "=" * 80 + "\n\n")
        
        for item in all_descriptions:
            f.write(f"CODE: {item['code']}\n")
            f.write("-" * 80 + "\n")
            f.write(f"{item['description']}\n")
            f.write("\n" + "=" * 80 + "\n\n")
    
    print(f"\n✓ Created student file: {output_path}")
    return output_path


def create_instructor_key(all_descriptions, output_path):
    """Create instructor key mapping codes to projects."""
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(all_descriptions, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Created instructor key: {output_path}")
    return output_path


def create_metadata_log(all_descriptions, category_counts, output_path):
    """Create metadata log documenting the data collection."""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("DATA COLLECTION LOG\n")
        f.write("=" * 80 + "\n\n")
        
        f.write(f"Collection Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Dataset Source: Hugging Face - shuxunoo/NFT-Net (NFT1000)\n")
        f.write(f"Total Descriptions Collected: {len(all_descriptions)}\n\n")
        
        f.write("CATEGORY BREAKDOWN:\n")
        f.write("-" * 80 + "\n")
        for category, count in category_counts.items():
            f.write(f"{category}: {count} descriptions\n")
        
        f.write("\n\nDESCRIPTION STATISTICS:\n")
        f.write("-" * 80 + "\n")
        lengths = [len(d['description']) for d in all_descriptions]
        f.write(f"Total characters: {sum(lengths):,}\n")
        f.write(f"Average length: {sum(lengths) // len(lengths):,} characters\n")
        f.write(f"Shortest: {min(lengths):,} characters\n")
        f.write(f"Longest: {max(lengths):,} characters\n")
        
        # Estimate pages (assuming ~3000 chars per page)
        estimated_pages = sum(lengths) / 3000
        f.write(f"\nEstimated pages (3000 chars/page): {estimated_pages:.1f} pages\n")
        
        f.write("\n\nPROJECTS COLLECTED:\n")
        f.write("-" * 80 + "\n")
        
        for category in category_counts.keys():
            f.write(f"\n{category}:\n")
            category_items = [d for d in all_descriptions if d['category'] == category]
            for item in category_items:
                f.write(f"  - {item['code']}: {item['project_name']}\n")
    
    print(f"✓ Created metadata log: {output_path}")
    return output_path


def main():
    """Main execution function."""
    print("\n" + "=" * 80)
    print("NFT DESCRIPTION FETCHER FOR AXIAL CODING CHALLENGE")
    print("=" * 80)
    
    # Fetch descriptions from both categories
    category_a_descriptions = fetch_descriptions(CATEGORY_A_ANIMAL_APE, "CATEGORY_A_ANIMAL_APE")
    category_b_descriptions = fetch_descriptions(CATEGORY_B_FANTASY_ART, "CATEGORY_B_FANTASY_ART")
    
    # Combine all descriptions
    all_descriptions = category_a_descriptions + category_b_descriptions
    
    if not all_descriptions:
        print("\n✗ No descriptions were fetched. Check dataset access.")
        return
    
    # Category counts
    category_counts = {
        "CATEGORY_A_ANIMAL_APE": len(category_a_descriptions),
        "CATEGORY_B_FANTASY_ART": len(category_b_descriptions),
    }
    
    print(f"\n{'='*60}")
    print(f"SUMMARY")
    print(f"{'='*60}")
    print(f"Total descriptions: {len(all_descriptions)}")
    print(f"  Category A (Animal/Ape): {category_counts['CATEGORY_A_ANIMAL_APE']}")
    print(f"  Category B (Fantasy/Art): {category_counts['CATEGORY_B_FANTASY_ART']}")
    
    # Create output files
    print(f"\n{'='*60}")
    print("Creating output files...")
    print(f"{'='*60}")
    
    student_file = create_student_file(
        all_descriptions, 
        "student_descriptions.txt"
    )
    
    instructor_key = create_instructor_key(
        all_descriptions,
        "instructor_key.json"
    )
    
    metadata_log = create_metadata_log(
        all_descriptions,
        category_counts,
        "collection_metadata.txt"
    )
    
    print(f"\n{'='*60}")
    print("✓ COMPLETE!")
    print(f"{'='*60}")
    print("\nFiles created:")
    print(f"1. {student_file} - Give this to students")
    print(f"2. {instructor_key} - Keep for reference")
    print(f"3. {metadata_log} - Documents what was collected")
    print("\nExpected outcome: Students should identify 2 distinct clusters")
    print("through axial coding based on content themes.\n")


if __name__ == "__main__":
    main()
