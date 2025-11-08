# Dependency Management

## Approach

This project uses code from the NFT-NET-Hub repository as a library. Here's how dependencies are managed:

### Two Repositories, One Virtual Environment

1. **Main Project** (axialcodingchallenge)
   - Contains the fetch scripts and logic
   - Has its own requirements in `requirements.txt`

2. **NFT-NET-Hub** (Git submodule)
   - Provides NFT metadata fetching utilities
   - Has its own requirements in `NFT-NET-Hub/requirements.txt`

### Unified Requirements

Since NFT-NET-Hub doesn't have a `setup.py` (not installable as a package), we:

1. Keep NFT-NET-Hub as a Git submodule for code access
2. Merge both requirement files into `requirements-all.txt`
3. Exclude platform-specific packages (pywin32 for Windows-only)
4. Install everything in one step into the same venv
5. Use `sys.path.insert()` to make NFT-NET-Hub importable

### Files

- `requirements.txt` - Main project dependencies (huggingface_hub, etc.)
- `requirements-all.txt` - **USE THIS** - All dependencies merged, excludes pywin32
- `NFT-NET-Hub/requirements.txt` - Original NFT-NET-Hub deps (UTF-16 encoded)

### Why This Works

- Both repos' dependencies coexist in the same venv
- No conflicts in dependency versions (both use compatible versions)
- NFT-NET-Hub code accessed via submodule + sys.path
- Single `pip install -r requirements-all.txt` installs everything

### Maintenance

If NFT-NET-Hub updates its requirements:
1. Pull submodule changes: `git submodule update --remote`
2. Regenerate `requirements-all.txt` from both requirement files
3. Exclude any Windows-specific packages


## Important: No Hugging Face Access Required

This project uses the `query()` method from NFT-NET-Hub, which reads from a **local JSON file** (`NFT-NET-Hub/nft_net_hub/info/NFT1000.json`) that's included in the submodule.

- ✅ **query()** - Reads local metadata (848KB JSON file) - No authentication needed
- ❌ **download()** - Downloads full datasets from Hugging Face - Requires authentication

Since we only need project descriptions (metadata), no Hugging Face account or authentication is required.

