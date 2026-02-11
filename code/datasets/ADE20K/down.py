#down.py ADE20K VSY Twenkid
from datasets import load_dataset
from pathlib import Path
from PIL import Image
from tqdm import tqdm
from collections import defaultdict
import json

def download_places365_subset(
    save_dir='places365_subset',
    mode='sample_per_class',
    skip_n=100, 
    samples_per_class=50,
    class_indices=None,
    total_samples=None,
    split='train'
):
    """
    Download a subset of Places365 dataset from HuggingFace with streaming.
    
    Args:
        save_dir: Directory to save images and metadata
        mode: Download mode - 'sample_per_class', 'class_indices', or 'total_samples'
        samples_per_class: Number of samples per class (for 'sample_per_class' mode)
        class_indices: List of class indices to download (for 'class_indices' mode)
        total_samples: Total number of samples to download randomly (for 'total_samples' mode)
        split: Dataset split ('train' or 'val')
    
    Examples:
        # Download 50 images from each class
        download_places365_subset(mode='sample_per_class', samples_per_class=50)
        
        # Download specific classes (e.g., beach, forest, kitchen)
        download_places365_subset(mode='class_indices', class_indices=[26, 123, 156])
        
        # Download 1000 random images
        download_places365_subset(mode='total_samples', total_samples=1000)
    """
    
    # Create directories
    save_path = Path(save_dir)
    img_dir = save_path / 'images'
    img_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Loading Places365-{split} dataset with streaming...")
    
    # Load dataset with streaming (doesn't download everything at once)
    dataset = load_dataset(
        'Andron00e/Places365-custom',
        split=split,
        streaming=True
    )
    
    # Get class names for reference
    print("Getting class information...")
    # Sample one item to get feature info
    first_item = next(iter(dataset))
    
    # Print available keys to understand structure
    print(f"Available keys in dataset: {list(first_item.keys())}")
    print(f"Sample item structure: {first_item}")
    
    # Try to determine the correct field names
    image_key = None
    label_key = None
    
    for key in first_item.keys():
        if key.lower() in ['image', 'img', 'picture']:
            image_key = key
        if key.lower() in ['label', 'category', 'class', 'labels']:
            label_key = key
    
    print(f"Detected image key: {image_key}")
    print(f"Detected label key: {label_key}")
    
    if image_key is None or label_key is None:
        raise ValueError(f"Could not detect image and label keys. Available keys: {list(first_item.keys())}")
    
    # Handle different possible structures
    class_names = None
    if label_key in first_item:
        label_info = first_item[label_key]
        if hasattr(label_info, 'names'):
            class_names = label_info.names
    
    num_classes = len(class_names) if class_names else 365
    
    print(f"Dataset has {num_classes} classes")
    
    # Initialize tracking
    class_counts = defaultdict(int)
    downloaded_count = 0
    metadata = []
    
    # Determine which classes to download
    if mode == 'class_indices':
        if class_indices is None:
            raise ValueError("class_indices must be provided when mode='class_indices'")
        target_classes = set(class_indices)
        print(f"Downloading from {len(target_classes)} specific classes: {class_indices}")
        
    elif mode == 'sample_per_class':
        target_classes = set(range(num_classes))
        print(f"Downloading {samples_per_class} images from each of {num_classes} classes")
        max_per_class = samples_per_class
        
    elif mode == 'total_samples':
        if total_samples is None:
            raise ValueError("total_samples must be provided when mode='total_samples'")
        target_classes = None
        print(f"Downloading {total_samples} random images")
        
    else:
        raise ValueError(f"Invalid mode: {mode}")
    
    # Stream and download images
    print("\nDownloading images...")
    pbar = tqdm(desc="Images downloaded")
    
    for idx, item in enumerate(dataset):
        # Extract image and label using detected keys
        image = item.get(image_key)
        label = item.get(label_key)
        
        if image is None or label is None:
            if idx < 10:  # Only print first 10 warnings
                print(f"Warning: Skipping item {idx} - image={image is not None}, label={label is not None}")
            continue
        
        # Check if we should download this image
        should_download = False
        if mode == 'skip':
           if idx % skip_n == 0: should_download = True
           
        if mode == 'total_samples':should_download = True #slow comparisons       
            if downloaded_count < total_samples:
                should_download = True
            else:
                break
                
        elif mode == 'class_indices':
            if label in target_classes:
                should_download = True
                
        elif mode == 'sample_per_class':
            if label in target_classes and class_counts[label] < max_per_class:
                should_download = True
        
        if should_download:
            # Create class subdirectory
            class_dir = img_dir / f"class_{label:03d}"
            class_dir.mkdir(exist_ok=True)
            
            # Save image
            img_filename = f"{label:03d}_{class_counts[label]:05d}.jpg"
            img_path = class_dir / img_filename
            
            if isinstance(image, Image.Image):
                # Convert to RGB if necessary
                if image.mode != 'RGB':
                    image = image.convert('RGB')
                image.save(img_path, 'JPEG', quality=95)
            
            # Update tracking
            class_counts[label] += 1
            downloaded_count += 1
            
            # Store metadata
            metadata.append({
                'filename': str(img_path.relative_to(save_path)),
                'class_id': label,
                'class_name': class_names[label] if class_names else f"class_{label}"
            })
            
            pbar.update(1)
            pbar.set_postfix({
                'classes': len(class_counts),
                'total': downloaded_count
            })
        
        # Check if we're done
        if mode == 'sample_per_class':
            # Check if all target classes have enough samples
            if all(class_counts[c] >= max_per_class for c in target_classes):
                break
    
    pbar.close()
    
    # Save metadata
    metadata_file = save_path / 'metadata.json'
    with open(metadata_file, 'w') as f:
        json.dump({
            'mode': mode,
            'split': split,
            'total_images': downloaded_count,
            'num_classes': len(class_counts),
            'class_counts': dict(class_counts),
            'images': metadata
        }, f, indent=2)
    
    # Save class names if available
    if class_names:
        class_names_file = save_path / 'class_names.json'
        with open(class_names_file, 'w') as f:
            json.dump(class_names, f, indent=2)
    
    # Print summary
    print(f"\n✓ Downloaded {downloaded_count} images from {len(class_counts)} classes")
    print(f"✓ Images saved to: {img_dir}")
    print(f"✓ Metadata saved to: {metadata_file}")
    
    # Print class distribution
    if len(class_counts) <= 20:
        print("\nClass distribution:")
        for class_id, count in sorted(class_counts.items()):
            class_name = class_names[class_id] if class_names else f"class_{class_id}"
            print(f"  Class {class_id} ({class_name}): {count} images")
    else:
        print(f"\nSamples per class range: {min(class_counts.values())} - {max(class_counts.values())}")


if __name__ == '__main__':

    # Example 3: Download 1000 random images
    download_places365_subset(
         mode='skip',
         skip_n=100,
         split='train'
    )
    
    
    
    # Example 3: Download 1000 random images
    download_places365_subset(
         mode='total_samples',
         total_samples=1000,
         split='train'
    )
    
    
    # Example 1: Download 50 images from each class (all 365 classes)
    # This will download 50 * 365 = 18,250 images
    download_places365_subset(
        mode='sample_per_class',
        #samples_per_class=50,
        samples_per_class=20,
        split='train'
    )
    
    # Example 2: Download from specific classes (beach=26, forest=123, kitchen=156, etc.)
    """
    download_places365_subset(
        mode='class_indices',
        class_indices=[26, 50, 100, 123, 156, 200],
        split='train',
        save_dir='places365_subset'
    )
    """
    
    # Example 3: Download 1000 random images
    # download_places365_subset(
    #     mode='total_samples',
    #     total_samples=1000,
    #     split='train'
    # )
    
    # Example 4: Download 20 images from 10 specific classes
    # download_places365_subset(
    #     mode='sample_per_class',
    #     samples_per_class=20,
    #     class_indices=[0, 10, 20, 30, 40, 50, 60, 70, 80, 90],
    #     split='train'
    # )
