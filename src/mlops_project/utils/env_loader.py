
#.env loader .py

import os
from pathlib import Path
from dotenv import load_dotenv

def load_all_envs(env_dir:str | Path = ".env"):
    """
    Loads ALL .env files inside the given directory.

    Args:
        env_dir (str | Path): Directory containing .env files.

    Notes:
        - Loads files in alphabetical order.
        - Supports any file ending with .env
        - Later files override earlier ones.
    """

    env_dir = Path(env_dir)

    if not env_dir.exists():
        raise FileNotFoundError(f"[ENV LOADER] WARNING: directory not found: {env_dir}")
    
    #Find all .env files inside directory
    env_files = sorted(env_dir.glob("*.env"))

    for env_file in env_files:
        load_dotenv(env_file,override=True)
        print(f"[ENV LOADER] Loaded:{env_file}")


        
    
