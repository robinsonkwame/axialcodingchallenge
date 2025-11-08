"""
Script to fetch NFT descriptions for axial coding challenge using NFT-NET-Hub.

This follows the NFT-NET-Hub conventions and uses their query() method
to fetch metadata only (no full ZIP downloads).
"""

import json
import hashlib
import sys
import os
from datetime import datetime
from pathlib import Path

# Add NFT-NET-Hub to Python path
nft_hub_path = Path(__file__).parent / "NFT-NET-Hub" / "nft_net_hub"
sys.path.insert(0, str(nft_hub_path))

try:
    from utils.downloader import NFT1000
except ImportError:
    print("❌ Error: NFT-NET-Hub not found!")
    print("\nPlease run:")
    print("  git clone https://github.com/ShuxunoO/NFT-NET-Hub.git")
    print("  cd NFT-NET-Hub")
    print("  pip install -r requirements.txt")
    print("\nThen run this script again.")
    sys.exit(1)


# Two distinct categories for expected clustering
CATEGORY_A_ANIMAL_APE = [
    "BoredApeYachtClub",
    "MutantApeYachtClub", 
    "0xApes",
    "BoredApeKennelClub",
    "CyberKongz",
    "Cool Cats",
    "Lazy Lions", 
    "Pudgy Penguins",
    "Tubby Cats",
    "Anonymice",
    "Sappy Seals",
    "Rumble Kong League",
    "Alpha Kongs Club",
    "Desperate ApeWives",
    "Boss Beauties",
]

CATEGORY_B_FANTASY_ART = [
    "Azuki",
    "CloneX", 
    "Doodles",
    "Moonbirds",
    "CRYPTOPUNKS",
    "World of Women",
    "VeeFriends",
    "DigiDaigaku",
    "Akutars",
    "Imaginary Ones",
    "The Humanoids",
    "Lives of Asuna",
    "AlphaBetty Doodles",
    "Chimpers",
]


def generate_code(project_name, index):
    """Generate alphanumeric code for anonymization."""
    hash_input = f"{project_name}{index}".encode()
    hash_digest = hashlib.md5(hash_input).hexdigest()
    return f"NFT{hash_digest[:8].upper()}"


def fetch_descriptions(nft1000, projects, category_name):
    """Fetch descriptions using NFT-NET-Hub query method."""
    descriptions = []
    
    print(f"\n{'='*60}")
    print(f"Fetching {category_name} projects...")
    print(f"{'='*60}")
    
    for i, project in enumerate(projects, 1):
        try:
            # Use query method - this is the key method from NFT-NET-Hub
            metadata = nft1000.query(project)
            
            if metadata and isinstance(metadata, dict):
                description = metadata.get("description", "")
                
                if description and description.strip():
                    code = generate_code(project, i)
                    
                    descriptions.append({
                        "code": code,
                        "description": description,
                        "project_name": project,
                        "category": category_name,
                        "total_supply": metadata.get("total_supply", "Unknown"),
                        "contract_address": metadata.get("contract_address", ""),
                        "official_url": metadata.get("official_url", ""),
                        "opensea_url": metadata.get("opensea_url", ""),
                    })
                    
                    print(f"✓ {i:2d}. {project:40s} [{len(description):4d} chars]")
                else:
                    print(f"✗ {i:2d}. {project:40s} [NO DESCRIPTION]")
            else:
                print(f"✗ {i:2d}. {project:40s} [NO METADATA RETURNED]")
                
        except Exception as e:
            error_msg = str(e)
            if "do you mean" in error_msg.lower():
                # Extract suggestions from NFT-NET-Hub error message
                print(f"? {i:2d}. {project:40s} [SUGGESTIONS: {error_msg.split('do you mean')[1].strip()}]")
            else:
                print(f"✗ {i:2d}. {project:40s} [ERROR: {error_msg}]")
    
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
        f.write("Look for patterns, themes, and relationships between descriptions.\n")
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
        f.write(f"Method: NFT-NET-Hub query() method - metadata only\n")
        f.write(f"Tool: https://github.com/ShuxunoO/NFT-NET-Hub\n")
        f.write(f"Total Descriptions Collected: {len(all_descriptions)}\n\n")
        
        f.write("CATEGORY BREAKDOWN:\n")
        f.write("-" * 80 + "\n")
        for category, count in category_counts.items():
            f.write(f"{category}: {count} descriptions\n")
        
        f.write("\n\nDESCRIPTION STATISTICS:\n")
        f.write("-" * 80 + "\n")
        lengths = [len(d['description']) for d in all_descriptions]
        if lengths:
            f.write(f"Total characters: {sum(lengths):,}\n")
            f.write(f"Average length: {sum(lengths) // len(lengths):,} characters\n")
            f.write(f"Shortest: {min(lengths):,} characters\n")
            f.write(f"Longest: {max(lengths):,} characters\n")
            
            estimated_pages = sum(lengths) / 3000
            f.write(f"\nEstimated pages (3000 chars/page): {estimated_pages:.1f} pages\n")
        else:
            f.write("No descriptions collected.\n")
        
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
    """Main execution function following NFT-NET-Hub conventions."""
    print("\n" + "=" * 80)
    print("NFT DESCRIPTION FETCHER FOR AXIAL CODING CHALLENGE")
    print("Using NFT-NET-Hub query method (metadata only, no downloads)")
    print("=" * 80)
    
    # Check if NFT-NET-Hub directory exists
    if not nft_hub_path.exists():
        print(f"\n❌ ERROR: NFT-NET-Hub not found at {nft_hub_path}")
        print("\nPlease run:")
        print("  git clone https://github.com/ShuxunoO/NFT-NET-Hub.git")
        print("  cd NFT-NET-Hub")
        print("  pip install -r requirements.txt")
        print("\nThen run this script again.")
        return
    
    # Initialize NFT1000 following their pattern
    print("\n🔧 Initializing NFT1000...")
    # For query-only operations, the local_repo_path can be current directory
    local_repo_path = str(Path.cwd().absolute())
    
    try:
        nft1000 = NFT1000("NFT1000", local_repo_path)
        print("✓ NFT1000 initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize NFT1000: {e}")
        print("Make sure you have access to the NFT-Net dataset on Hugging Face")
        return
    
    # Show available NFT names for debugging
    try:
        print("\n🔍 Checking available NFT projects...")
        available_nfts = nft1000.get_NFT_name_list()
        print(f"✓ Found {len(available_nfts)} available NFT projects")
    except Exception as e:
        print(f"⚠️  Could not get NFT list: {e}")
        print("Proceeding anyway...")
    
    # Fetch descriptions from both categories
    category_a_descriptions = fetch_descriptions(nft1000, CATEGORY_A_ANIMAL_APE, "CATEGORY_A_ANIMAL_APE")
    category_b_descriptions = fetch_descriptions(nft1000, CATEGORY_B_FANTASY_ART, "CATEGORY_B_FANTASY_ART")
    
    # Combine all descriptions
    all_descriptions = category_a_descriptions + category_b_descriptions
    
    if not all_descriptions:
        print("\n❌ No descriptions were fetched!")
        print("\nPossible issues:")
        print("- Check your Hugging Face authentication")
        print("- Verify dataset access permissions")
        print("- Some project names might have changed")
        return
    
    # Category counts
    category_counts = {
        "CATEGORY_A_ANIMAL_APE": len(category_a_descriptions),
        "CATEGORY_B_FANTASY_ART": len(category_b_descriptions),
    }
    
    print(f"\n{'='*60}")
    print(f"COLLECTION SUMMARY")
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
    print("✅ COMPLETE!")
    print(f"{'='*60}")
    print("\nFiles created:")
    print(f"1. {student_file} - Give this to students")
    print(f"2. {instructor_key} - Keep for reference (maps codes to projects)")
    print(f"3. {metadata_log} - Documents what was collected")
    print("\nExpected outcome: Students should identify 2 distinct clusters")
    print("through axial coding based on content themes.")
    print("\nCluster A: Animal/Community theme (membership, clubs, avatars)")
    print("Cluster B: Art/Fantasy theme (collectibles, artistic vision)")
    print()


if __name__ == "__main__":
    main()