#!/usr/bin/env python3
"""
Interactive script to scan image directories and generate Ollama moondream commands.
"""

import os
import random
from pathlib import Path
from typing import List, Dict


def get_image_files(base_path: str) -> Dict[str, List[str]]:
    """Scan directory and return dict of class folders and their image files."""
    base_path = Path(base_path)
    
    if not base_path.exists():
        print(f"Error: Directory '{base_path}' does not exist!")
        return {}
    
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff', '.tif'}
    class_files = {}
    
    for subdir in sorted(base_path.iterdir()):
        if subdir.is_dir():
            files = []
            for file in sorted(subdir.iterdir()):
                if file.is_file() and file.suffix.lower() in image_extensions:
                    files.append(str(file.absolute()))
            
            if files:
                class_files[subdir.name] = files
    
    return class_files


def display_folders(class_files: Dict[str, List[str]]):
    """Display available folders with file counts."""
    print("\nAvailable class folders:")
    print("-" * 60)
    for i, (class_name, files) in enumerate(sorted(class_files.items()), 1):
        print(f"{i:3d}. {class_name:20s} ({len(files)} images)")


def get_folder_selection(class_files: Dict[str, List[str]]) -> List[str]:
    """Get user's folder selection."""
    while True:
        print("\nFolder selection:")
        print("1. All folders")
        print("2. Select specific folders")
        
        choice = input("\nEnter choice (1-2): ").strip()
        
        if choice == '1':
            return list(class_files.keys())
        elif choice == '2':
            display_folders(class_files)
            print("\nEnter folder numbers (space-separated) or names (comma-separated):")
            selection = input("Selection: ").strip()
            
            selected = []
            # Try parsing as numbers first
            try:
                numbers = [int(x.strip()) for x in selection.split()]
                folder_list = sorted(class_files.keys())
                selected = [folder_list[n-1] for n in numbers if 0 < n <= len(folder_list)]
            except ValueError:
                # Try parsing as names
                names = [x.strip() for x in selection.replace(',', ' ').split()]
                selected = [name for name in names if name in class_files]
            
            if selected:
                return selected
            else:
                print("Invalid selection. Please try again.")
        else:
            print("Invalid choice. Please try again.")


def get_items_per_folder() -> int:
    """Get number of items to process per folder."""
    while True:
        print("\nItems per folder:")
        print("1. All items")
        print("2. Specify a limit")
        
        choice = input("\nEnter choice (1-2): ").strip()
        
        if choice == '1':
            return None
        elif choice == '2':
            try:
                limit = int(input("Enter number of items per folder: ").strip())
                if limit > 0:
                    return limit
                else:
                    print("Please enter a positive number.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        else:
            print("Invalid choice. Please try again.")


def get_sampling_method() -> tuple:
    """Get sampling method (sequential or random) and seed."""
    while True:
        print("\nSampling method:")
        print("1. Sequential (first N items)")
        print("2. Random sampling")
        
        choice = input("\nEnter choice (1-2): ").strip()
        
        if choice == '1':
            return False, None
        elif choice == '2':
            seed_choice = input("Enter random seed for reproducibility (or press Enter for random): ").strip()
            seed = int(seed_choice) if seed_choice else None
            return True, seed
        else:
            print("Invalid choice. Please try again.")


def generate_commands(class_files: Dict[str, List[str]], 
                     selected_folders: List[str],
                     items_per_folder: int,
                     random_sample: bool = False,
                     seed: int = None) -> List[str]:
    """Generate Ollama commands for selected folders and items."""
    commands = []
    
    # Set random seed if provided
    if seed is not None:
        random.seed(seed)
    
    for folder in selected_folders:
        if folder in class_files:
            files = class_files[folder]
            if items_per_folder:
                if random_sample:
                    # Random sampling
                    files = random.sample(files, min(items_per_folder, len(files)))
                else:
                    # Sequential selection
                    files = files[:items_per_folder]
            
            for file_path in files:
                commands.append(f'ollama run moondream "{file_path}"')
    
    return commands


def save_script(commands: List[str], filename: str):
    """Save commands to shell script."""
    with open(filename, 'w') as f:
        f.write("#!/bin/bash\n")
        f.write("# Generated Ollama moondream commands\n")
        f.write(f"# Total commands: {len(commands)}\n")
        f.write(f"# Generated: {os.popen('date').read().strip()}\n\n")
        
        for cmd in commands:
            f.write(cmd + '\n')
    
    os.chmod(filename, 0o755)
    print(f"\n✓ Script saved to: {filename}")
    print(f"  Run with: ./{filename}")


def main():
    print("=" * 60)
    print("Ollama Moondream Command Generator")
    print("=" * 60)
    
    # Get base directory
    base_path = input("\nEnter path to image directory: ").strip()
    
    # Scan directories
    print("\nScanning directories...")
    class_files = get_image_files(base_path)
    
    if not class_files:
        print("No image files found!")
        return
    
    print(f"\nFound {len(class_files)} class folders with images")
    
    # Get folder selection
    selected_folders = get_folder_selection(class_files)
    print(f"\nSelected {len(selected_folders)} folders")
    
    # Get items per folder
    items_per_folder = get_items_per_folder()
    
    # Get sampling method if limiting items
    random_sample = False
    seed = None
    if items_per_folder is not None:
        random_sample, seed = get_sampling_method()
        if seed is not None:
            print(f"Using random seed: {seed}")
    
    # Generate commands
    print("\nGenerating commands...")
    commands = generate_commands(class_files, selected_folders, items_per_folder,
                                random_sample, seed)
    
    # Display summary
    print("\n" + "=" * 60)
    print(f"Generated {len(commands)} commands")
    print("=" * 60)
    
    # Preview
    print("\nFirst 10 commands (preview):")
    for cmd in commands[:10]:
        print(f"  {cmd}")
    if len(commands) > 10:
        print(f"  ... and {len(commands) - 10} more")
    
    # Save options
    print("\n" + "=" * 60)
    print("1. Save to file")
    print("2. Print all commands")
    print("3. Exit without saving")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == '1':
        filename = input("Enter filename (default: run_moondream.sh): ").strip()
        if not filename:
            filename = "run_moondream.sh"
        save_script(commands, filename)
    elif choice == '2':
        print("\nAll commands:")
        print("-" * 60)
        for cmd in commands:
            print(cmd)
    
    print("\nDone!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nCancelled by user.")
    except Exception as e:
        print(f"\nError: {e}")
