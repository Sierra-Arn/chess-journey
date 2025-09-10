# src/legacy/setup_legacy_images.py
"""
Legacy image symlinks setup utility.

This module provides functionality to create symbolic links for legacy code
that expects old image filenames. It maps new descriptive image names to
legacy short names through symbolic links, maintaining compatibility without
duplicating files.

The script can be run with 'setup' or 'clean' commands to manage the symlinks.
"""

from pathlib import Path
import os
import sys
import shutil

IMAGE_MAPPING = {
    "wp.png": "white-pawn.png", "bp.png": "black-pawn.png",
    "wR.png": "white-rook.png", "bR.png": "black-rook.png", 
    "wN.png": "white-knight.png", "bN.png": "black-knight.png",
    "wB.png": "white-bishop.png", "bB.png": "black-bishop.png",
    "wQ.png": "white-queen.png", "bQ.png": "black-queen.png",
    "wK.png": "white-king.png", "bK.png": "black-king.png",
}

def get_paths():
    """
    Get source and target paths for image symlinks.
    
    Returns:
        tuple[Path, Path]: A tuple containing:
            - legacy_images: Path to the legacy images directory
            - source_images: Path to the source images directory
    """
    # Current file: src/legacy/setup_legacy_images.py
    script_path = Path(__file__).parent  # src/legacy/
    
    # Path to legacy images directory
    legacy_images = script_path / "legacy_code" / "chess_images"
    
    # Path to new images in chess_game
    source_images = script_path.parent / "chess_game" / "assets" / "images"
    
    return legacy_images, source_images

def setup():
    """
    Create symbolic links for legacy image compatibility.
    
    This function creates symbolic links in the legacy images directory
    that point to the corresponding images in the new assets directory.
    Existing files or symlinks are removed before creating new ones.
    
    Returns:
        bool: True if all symlinks were created successfully, False otherwise
    """
    legacy_images, source_images = get_paths()
    
    # Verify source directory exists
    if not source_images.exists():
        print(f"Source images directory not found: {source_images}")
        return False
    
    # Create target directory
    legacy_images.mkdir(parents=True, exist_ok=True)
    print(f"Created directory: {legacy_images}")
    
    success_count = 0
    
    for old_name, new_name in IMAGE_MAPPING.items():
        source_file = source_images / new_name
        target_link = legacy_images / old_name
        
        if not source_file.exists():
            print(f"Image not found: {source_file}")
            continue
        
        # Remove existing link/file
        if target_link.exists() or target_link.is_symlink():
            target_link.unlink()
        
        try:
            # Create relative symbolic link
            relative_path = os.path.relpath(source_file, legacy_images)
            target_link.symlink_to(relative_path)
            print(f"{old_name} -> {new_name}")
            success_count += 1
        except OSError as e:
            print(f"Failed to create symlink {old_name}: {e}")
    
    print(f"Created {success_count}/{len(IMAGE_MAPPING)} symbolic links")
    return success_count == len(IMAGE_MAPPING)

def clean():
    """
    Remove the legacy images directory and all symlinks.
    
    This function completely removes the legacy images directory
    and all its contents, including symbolic links.
    """
    legacy_images, _ = get_paths()
    
    if legacy_images.exists():
        shutil.rmtree(legacy_images)
        print(f"Removed directory: {legacy_images}")
    else:
        print("Legacy images directory does not exist")

def main():
    """
    Main entry point - processes command line arguments.
    
    Supports two commands:
    - 'setup': Creates symbolic links (default behavior)
    - 'clean': Removes the legacy images directory
    
    Usage:
        python setup_legacy_images.py [setup|clean]
    """
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "clean":
            clean()
        elif command == "setup":
            setup()
        else:
            print(f"Unknown command: {command}")
            print("Usage: python setup_legacy_images.py [setup|clean]")
    else:
        # Default to setup command
        setup()

if __name__ == "__main__":
    main()