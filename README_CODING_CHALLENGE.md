# NFT Description Axial Coding Challenge - Data Collection

## Purpose

This script fetches NFT project descriptions from the NFT1000 dataset for a **2-hour axial coding exercise** where students identify themes and patterns in text data.

## Design Strategy

### Two Distinct Categories

The script selects projects from two intentionally distinct categories to create natural clustering:

**Category A: Animal/Ape Collections** (~20 projects)
- Bored Ape Yacht Club, Mutant Ape variants
- Kong-themed projects (CyberKongz, Rumble Kong League)
- Cat projects (Cool Cats, Tubby Cats)
- Penguin/seal projects (Pudgy Penguins, Sappy Seals)
- Other animal-focused collections

**Category B: Fantasy/Art Collections** (~19 projects)
- Art-focused (Murakami.Flowers, MOAR by Joan Cornella)
- Fantasy/anime style (Azuki, Lives of Asuna, DigiDaigaku)
- Iconic collections (CryptoPunks, Doodles, Moonbirds)
- Character/avatar projects (CloneX, VeeFriends, Imaginary Ones)

### Expected Outcome

Students performing axial coding should discover **two major thematic clusters** based on:
- Content themes (animals vs. artistic/fantasy)
- Language patterns (community-focused vs. artistic vision)
- Value propositions (membership/club vs. art/collectible)

### Data Volume

- **Target**: ~40 pages of content
- **Projects**: ~39 total (20 Category A + 19 Category B)
- **Estimated**: ~120,000 characters ≈ 40 pages at 3,000 chars/page
- **Time**: Should support 2 hours of coding work

## Prerequisites

1. **Hugging Face Account with Dataset Access**
   ```bash
   # Visit: https://huggingface.co/datasets/shuxunoo/NFT-Net
   # Request access to the gated dataset
   # Wait for approval
   ```

2. **Install Dependencies**
   ```bash
   pip install huggingface_hub
   ```

3. **Authenticate with Hugging Face**
   ```bash
   huggingface-cli login
   # Follow prompts to enter your token
   ```

## Running the Script

```bash
python fetch_descriptions_for_coding.py
```

## Output Files

### 1. `student_descriptions.txt` 
**Give this to students**

Contains:
- Anonymized descriptions with alphanumeric codes (e.g., `NFT12ABC345`)
- No project names or metadata
- Clean text for coding analysis

Example format:
```
CODE: NFT4A7B3C2D
--------------------------------------------------------------------------------
This project features a collection of 10,000 unique digital apes living on the
Ethereum blockchain. Each ape has distinct traits and provides access to...
================================================================================
```

### 2. `instructor_key.json`
**Keep for your reference**

Maps codes back to projects:
```json
[
  {
    "code": "NFT4A7B3C2D",
    "description": "...",
    "project_name": "BoredApeYachtClub",
    "category": "CATEGORY_A_ANIMAL_APE",
    "total_supply": 10000,
    "contract_address": "0x...",
    "official_url": "https://..."
  }
]
```

### 3. `collection_metadata.txt`
**Documentation log**

Records:
- Collection date and source
- Number of descriptions per category
- Statistics (character counts, estimated pages)
- Complete list of what was fetched

## Challenge Instructions for Students

Give students `student_descriptions.txt` with these instructions:

> **Axial Coding Exercise** (2 hours)
> 
> Read through the NFT project descriptions and perform axial coding:
> 
> 1. **Open Coding** (30 min): Identify themes, patterns, and concepts
> 2. **Axial Coding** (60 min): Organize codes into categories and relationships
> 3. **Analysis** (30 min): Document your findings and cluster structure
> 
> Use the provided codes (e.g., NFT12ABC345) to reference specific descriptions.

## Modifying the Script

### Change Project Selection

Edit the lists at the top of `fetch_descriptions_for_coding.py`:

```python
CATEGORY_A_ANIMAL_APE = [
    "BoredApeYachtClub",
    "Cool Cats",
    # Add or remove projects here
]

CATEGORY_B_FANTASY_ART = [
    "Azuki",
    "CloneX",
    # Add or remove projects here
]
```

### Adjust Data Volume

- **More content**: Add more projects to lists
- **Less content**: Remove projects from lists
- **Different categories**: Replace entire lists with different themes

### Find Available Projects

Check the NFT1000 dataset for all 1,001 available projects:
- Visit: https://huggingface.co/datasets/shuxunoo/NFT-Net
- Browse the `NFT1000/` directory
- Use project folder names exactly as they appear

## Time Period Coverage

The selected projects span different NFT eras:
- **Early NFTs** (2021): CryptoPunks, Bored Ape Yacht Club, Cool Cats
- **Mid period** (2022): Azuki, Moonbirds, Akutars
- **Later projects** (2023+): DigiDaigaku, a KID called BEAST

This temporal spread adds richness to the data without explicitly labeling time periods.

## Troubleshooting

**Error: Repository not found or access denied**
- Ensure you've requested and been granted access to the dataset
- Verify you're logged in: `huggingface-cli whoami`

**Error: Project not found**
- Check project name spelling (case-sensitive)
- Verify project exists in NFT1000 dataset

**Too many/few descriptions**
- Adjust project lists
- Some projects may not have descriptions in metadata

## Notes

- The categories are **not** given to students - they should discover them through coding
- The alphanumeric codes are generated consistently from project names
- Metadata is kept separate to ensure blind analysis
- The instructor key allows backtracking from codes to original projects
