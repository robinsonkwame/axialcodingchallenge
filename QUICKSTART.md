# Quick Start Guide

## To Fetch Descriptions for the Coding Challenge

### Step 1: Get Dataset Access
1. Go to https://huggingface.co/datasets/shuxunoo/NFT-Net
2. Log in or create account
3. Click "Access repository" and accept terms
4. Wait for approval

### Step 2: Set Up Hugging Face CLI
```bash
pip install huggingface_hub
huggingface-cli login
# Enter your token when prompted
```

### Step 3: Run the Fetch Script
```bash
python fetch_descriptions_for_coding.py
```

### Step 4: Use the Output

**Give to students:**
- `student_descriptions.txt` - Clean descriptions with codes only

**Keep for yourself:**
- `instructor_key.json` - Decode map (code → project name)
- `collection_metadata.txt` - Documentation of what was collected

---

## What Gets Created

### student_descriptions.txt
```
CODE: NFT4A7B3C2D
--------------------------------------------------------------------------------
Description text here with no identifying information...
================================================================================

CODE: NFT8F3E9A1B
--------------------------------------------------------------------------------
Another description...
================================================================================
```

### instructor_key.json
```json
[
  {
    "code": "NFT4A7B3C2D",
    "description": "...",
    "project_name": "BoredApeYachtClub",
    "category": "CATEGORY_A_ANIMAL_APE"
  }
]
```

### collection_metadata.txt
```
DATA COLLECTION LOG
Collection Date: 2025-11-06
Total Descriptions: 39
Estimated pages: 40.2 pages

CATEGORY A (Animal/Ape): 20 descriptions
CATEGORY B (Fantasy/Art): 19 descriptions
```

---

## Expected Results

Students should discover **2 major clusters** through axial coding:
1. **Animal/Community Theme** - membership, club culture, animal avatars
2. **Art/Fantasy Theme** - artistic vision, collectible art, fantasy worlds

---

## Customization

Edit `fetch_descriptions_for_coding.py` lists to change projects:

```python
CATEGORY_A_ANIMAL_APE = [
    "BoredApeYachtClub",  # Add/remove projects
    "Cool Cats",
]

CATEGORY_B_FANTASY_ART = [
    "Azuki",  # Add/remove projects
    "Doodles",
]
```

Target: ~40 pages ≈ 120,000 characters ≈ 39 projects

---

## Troubleshooting

**Can't access dataset?**
→ Check approval status at https://huggingface.co/datasets/shuxunoo/NFT-Net

**Login issues?**
→ Run `huggingface-cli whoami` to verify

**Project not found?**
→ Check spelling (case-sensitive), verify it exists in NFT1000/
