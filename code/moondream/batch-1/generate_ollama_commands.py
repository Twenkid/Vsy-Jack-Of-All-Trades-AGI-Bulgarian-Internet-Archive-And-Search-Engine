#!/usr/bin/env python3
"""
Script to scan image class directories and generate Ollama moondream commands.
Supports selecting specific folders, limiting items per folder, and outputs to shell script.
"""

import os
import argparse
import random
from pathlib import Path
from typing import List, Dict


def scan_directories(base_path: str, selected_folders: List[str] = None) -> Dict[str, List[str]]:
    """
    Scan the base directory for class folders and their image files.
    
    Args:
        base_path: Path to the directory containing class folders
        selected_folders: Optional list of specific folders to scan
        
    Returns:
        Dictionary mapping folder names to lists of image file paths
    """
    base_path = Path(base_path)
    
    if not base_path.exists():
        raise ValueError(f"Directory does not exist: {base_path}")
    
    # Common image extensions
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff', '.tif'}
    
    class_files = {}
    
    # Get all subdirectories
    subdirs = [d for d in base_path.iterdir() if d.is_dir()]
    
    # Filter by selected folders if provided
    if selected_folders:
        subdirs = [d for d in subdirs if d.name in selected_folders]
    
    for subdir in sorted(subdirs):
        files = []
        for file in sorted(subdir.iterdir()):
            if file.is_file() and file.suffix.lower() in image_extensions:
                files.append(str(file.absolute()))
        
        if files:
            class_files[subdir.name] = files
    
    return class_files


def generate_commands(class_files: Dict[str, List[str]], 
                      items_per_folder: int = None,
                      random_sample: bool = False,
                      seed: int = None) -> List[str]:
    """
    Generate Ollama moondream commands for the image files.
    
    Args:
        class_files: Dictionary mapping folder names to file paths
        items_per_folder: Optional limit on number of items per folder (None = all)
        random_sample: If True, randomly sample files when items_per_folder is set
        seed: Random seed for reproducible sampling
        
    Returns:
        List of shell commands
    """
    commands = []
    
    # Set random seed if provided
    if seed is not None:
        random.seed(seed)
    
    for class_name in sorted(class_files.keys()):
        files = class_files[class_name]
        
        # Limit files if specified
        if items_per_folder is not None:
            if random_sample:
                # Random sampling
                files = random.sample(files, min(items_per_folder, len(files)))
            else:
                # Sequential selection (first N files)
                files = files[:items_per_folder]
        
        for file_path in files:
            command = f'ollama run moondream "{file_path}"'
            commands.append(command)
    
    return commands


def save_to_script(commands: List[str], output_file: str):
    """
    Save commands to a shell script file.
    
    Args:
        commands: List of shell commands
        output_file: Path to output script file
    """
    with open(output_file, 'w') as f:
        f.write("#!/bin/bash\n")
        f.write("# Generated Ollama moondream commands\n")
        f.write(f"# Total commands: {len(commands)}\n\n")
        
        for cmd in commands:
            f.write(cmd + '\n')
    
    # Make the script executable
    os.chmod(output_file, 0o755)
    print(f"Script saved to: {output_file}")
    print(f"Make it executable with: chmod +x {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate Ollama moondream commands for image class directories",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process all files in all folders
  python generate_ollama_commands.py /path/to/images
  
  # Process only 10 files per folder (first 10)
  python generate_ollama_commands.py /path/to/images --items-per-folder 10
  
  # Randomly sample 10 files per folder
  python generate_ollama_commands.py /path/to/images --items-per-folder 10 --random
  
  # Random sampling with seed (reproducible)
  python generate_ollama_commands.py /path/to/images --items-per-folder 10 --random --seed 42
  
  # Process specific folders only
  python generate_ollama_commands.py /path/to/images --folders class_1 class_2 class_5
  
  # Random sample 20 files per folder from specific folders
  python generate_ollama_commands.py /path/to/images --items-per-folder 20 --random --folders class_1 class_10
  
  # Specify custom output file
  python generate_ollama_commands.py /path/to/images --output my_script.sh
        """
    )
    
    parser.add_argument(
        'base_path',
        type=str,
        help='Path to directory containing class folders (class_1, class_2, etc.)'
    )
    
    parser.add_argument(
        '--items-per-folder',
        type=int,
        default=None,
        help='Number of items to process per folder (default: all)'
    )
    
    parser.add_argument(
        '--random',
        action='store_true',
        help='Randomly sample files when using --items-per-folder (default: sequential)'
    )
    
    parser.add_argument(
        '--seed',
        type=int,
        default=None,
        help='Random seed for reproducible sampling (only with --random)'
    )
    
    parser.add_argument(
        '--folders',
        nargs='+',
        default=None,
        help='Specific folders to process (default: all folders)'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        default='run_moondream.sh',
        help='Output shell script filename (default: run_moondream.sh)'
    )
    
    parser.add_argument(
        '--print-only',
        action='store_true',
        help='Only print commands without saving to file'
    )
    
    args = parser.parse_args()
    
    try:
        # Scan directories
        print(f"Scanning directory: {args.base_path}")
        class_files = scan_directories(args.base_path, args.folders)
        
        if not class_files:
            print("No image files found!")
            return
        
        # Print summary
        print(f"\nFound {len(class_files)} class folders:")
        for class_name, files in class_files.items():
            total = len(files)
            processing = min(total, args.items_per_folder) if args.items_per_folder else total
            sample_type = "random" if args.random and args.items_per_folder else "sequential"
            print(f"  {class_name}: {processing}/{total} files ({sample_type})")
        
        # Generate commands
        commands = generate_commands(class_files, args.items_per_folder, 
                                     args.random, args.seed)
        
        print(f"\nGenerated {len(commands)} commands")
        
        # Print commands if requested
        if args.print_only:
            print("\nCommands:")
            print("-" * 80)
            for cmd in commands:
                print(cmd)
        else:
            # Save to file
            save_to_script(commands, args.output)
            
            # Print first few commands as preview
            print("\nFirst 5 commands (preview):")
            print("-" * 80)
            for cmd in commands[:5]:
                print(cmd)
            if len(commands) > 5:
                print(f"... and {len(commands) - 5} more")
    
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
