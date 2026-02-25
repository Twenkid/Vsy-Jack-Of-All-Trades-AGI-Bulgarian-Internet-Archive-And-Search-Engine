## Claude 4.5

# Ollama Moondream Command Generator

Two Python scripts to scan image class directories and generate Ollama moondream commands.

## Scripts

### 1. `generate_ollama_commands.py` - Command-line version
Full-featured script with command-line arguments for automation.

### 2. `generate_ollama_interactive.py` - Interactive version
User-friendly menu-driven interface for interactive use.

## Requirements

- Python 3.6+
- Image files organized in class directories (class_1, class_2, etc.)

## Usage

### Command-line Version

**Basic usage - process all files:**
```bash
python generate_ollama_commands.py /path/to/images
```

**Limit items per folder:**
```bash
# Process only 10 files per folder (first 10)
python generate_ollama_commands.py /path/to/images --items-per-folder 10

# Randomly sample 10 files per folder
python generate_ollama_commands.py /path/to/images --items-per-folder 10 --random

# Random sampling with seed for reproducibility
python generate_ollama_commands.py /path/to/images --items-per-folder 10 --random --seed 42

# Process 20 files per folder
python generate_ollama_commands.py /path/to/images --items-per-folder 20
```

**Select specific folders:**
```bash
# Process only class_1, class_2, and class_5
python generate_ollama_commands.py /path/to/images --folders class_1 class_2 class_5
```

**Combine options:**
```bash
# Process 10 files from class_1 and class_10 only
python generate_ollama_commands.py /path/to/images \
    --items-per-folder 10 \
    --folders class_1 class_10 \
    --output my_script.sh

# Randomly sample 15 files from specific folders
python generate_ollama_commands.py /path/to/images \
    --items-per-folder 15 \
    --random \
    --folders class_1 class_5 class_10 \
    --output random_sample.sh
```

**Print commands without saving:**
```bash
python generate_ollama_commands.py /path/to/images --print-only
```

**Get help:**
```bash
python generate_ollama_commands.py --help
```

### Interactive Version

Simply run the script and follow the prompts:

```bash
python generate_ollama_interactive.py
```

The script will guide you through:
1. Entering the directory path
2. Selecting folders (all or specific ones)
3. Setting items per folder limit
4. Choosing sampling method (sequential or random)
5. Previewing and saving commands

## Directory Structure

Expected directory structure:
```
images/
├── class_1/
│   ├── image1.jpg
│   ├── image2.png
│   └── ...
├── class_2/
│   ├── image1.jpg
│   └── ...
├── class_3/
│   └── ...
└── class_364/
    └── ...
```

## Supported Image Formats

- JPG/JPEG
- PNG
- GIF
- BMP
- WebP
- TIFF/TIF

## Output

The scripts generate a shell script (default: `run_moondream.sh`) containing commands like:

```bash
#!/bin/bash
# Generated Ollama moondream commands
# Total commands: 150

ollama run moondream "/absolute/path/to/images/class_1/image1.jpg"
ollama run moondream "/absolute/path/to/images/class_1/image2.png"
ollama run moondream "/absolute/path/to/images/class_2/image1.jpg"
...
```

Make the script executable and run it:
```bash
chmod +x run_moondream.sh
./run_moondream.sh
```

## Examples

### Example 1: Test with 5 random images per class
```bash
python generate_ollama_commands.py ~/datasets/images --items-per-folder 5 --random
```

### Example 2: Reproducible random sample with seed
```bash
python generate_ollama_commands.py ~/datasets/images \
    --items-per-folder 20 \
    --random \
    --seed 123 \
    --output sample_seed123.sh
```

### Example 3: Process specific classes completely
```bash
python generate_ollama_commands.py ~/datasets/images \
    --folders class_1 class_50 class_100 class_200 \
    --output selected_classes.sh
```

### Example 4: Generate commands for first 20 items in all folders
```bash
python generate_ollama_commands.py ~/datasets/images \
    --items-per-folder 20 \
    --output batch_20.sh
```

### Example 5: Random sample from specific classes
```bash
python generate_ollama_commands.py ~/datasets/images \
    --folders class_1 class_2 class_3 \
    --items-per-folder 30 \
    --random \
    --seed 42 \
    --output random_3classes.sh
```

### Example 6: Interactive exploration
```bash
python generate_ollama_interactive.py
# Then follow prompts to explore and select
```

## Tips

1. **Test first**: Use `--items-per-folder 1` or `--items-per-folder 5` to test with a small subset
2. **Random sampling**: Use `--random` to get a diverse sample across your dataset instead of just the first N files
3. **Reproducibility**: Use `--seed` with a number to get the same random sample every time
4. **Preview**: Use `--print-only` to see what will be generated without creating a file
5. **Organize output**: Use `--output` to create different script files for different batches
6. **Check disk space**: Processing 364 classes with many images per class will generate large output
7. **Parallel processing**: You can split the work by generating separate scripts for different class ranges
8. **Data distribution**: Random sampling is useful when you want to ensure your sample represents the entire dataset, not just alphabetically-first files

## Troubleshooting

**"Directory does not exist"**
- Check that the path is correct
- Use absolute paths or ensure you're in the right directory

**"No image files found"**
- Verify the directory structure matches expectations
- Check file extensions are supported
- Ensure files are in subdirectories, not the root

**Permission errors**
- Run `chmod +x generate_ollama_commands.py` to make the script executable
- Ensure you have read permissions on the image directories

## License

Free to use and modify.
