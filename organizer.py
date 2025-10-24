# organize.py
# Automated File Organizer CLI Tool using Typer and JSON Configuration

import typer
import json
import shutil
import sys
from pathlib import Path
from typing import Dict, List, Optional

app = typer.Typer(help="Organizes files in a target directory by file type.")
def load_config(config_path: Path) -> Dict[str, List[str]]:

    """
    Loads the configuration from a JSON file.

    If the file does not exist or is invalid, it returns a hardcoded default configuration.

    :param config_path: The path to the JSON configuration file.
    :return: A dictionary mapping categories to lists of file extensions.
    :rtype: Dict[str, List[str]]
    """
    default_config = {
        "Documents": [".pdf", ".doc", ".docx", ".txt", ".csv", ".xls", ".xlsx"],
        "Images": [".jpg", ".jpeg", ".png", ".gif", ".svg"],
        "Videos": [".mp4", ".mov", ".mkv"],
        "Audio": [".mp3", ".wav"],
        "Archives": [".zip", ".rar", ".7z"],
        "Applications": [".exe", ".dmg", ".pkg"],
    }
    
    if not config_path.exists():
        typer.echo(typer.style(f"Warning: Config file not found at {config_path}. Using hardcoded defaults.", fg=typer.colors.YELLOW))
        return default_config

    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        typer.echo(typer.style(f"Error: Invalid JSON format in {config_path}. Using hardcoded defaults.", fg=typer.colors.RED), err=True)
        return default_config
    except Exception as e:
        typer.echo(typer.style(f"Error loading config: {e}. Using hardcoded defaults.", fg=typer.colors.RED), err=True)
        return default_config
def get_category_map(config_path: Path) -> Dict[str, str]:

    """
    Builds a dictionary mapping file extensions to their corresponding folder names.

    :param config_path: The path to the JSON configuration file.
    :return: A dictionary mapping file extensions to their corresponding folder names.
    :rtype: Dict[str, str]
    """
    folder_to_extensions = load_config(config_path)

    extension_to_folder = {}
    for folder_name, extensions in folder_to_extensions.items():
        
        clean_folder_name = folder_name.strip().capitalize()
        for ext in extensions:
            
            extension_to_folder[ext.lower().strip()] = clean_folder_name

    return extension_to_folder
def classify_file(file_path: Path, category_map: Dict[str, str]) -> str:

    """
    Determines the folder name to which a file should be moved based on its extension.

    :param file_path: The path to the file to be classified.
    :param category_map: A dictionary mapping file extensions to their corresponding folder names.
    :return: The folder name to which the file should be moved.
    :rtype: str
    """
    extension = file_path.suffix.lower()

    
    return category_map.get(extension, 'Other')
def move_file_safely(source_path: Path, destination_dir: Path, dry_run: bool) -> bool:

    """
    Safely moves a file from its source path to the destination directory.
    
    If the file already exists in the destination directory, it will be skipped.
    
    If the dry_run flag is set to True, it will simulate the move without actually performing it.
    
    Returns True if the move was successful, False otherwise.
    
    :param source_path: The path to the file to be moved.
    :param destination_dir: The directory where the file should be moved.
    :param dry_run: Whether to simulate the move without performing it.
    :return: Whether the move was successful.
    :rtype: bool
    """
    final_path = destination_dir / source_path.name
    action_color = typer.colors.CYAN if dry_run else typer.colors.GREEN

    if final_path.exists():
        typer.echo(typer.style(f"  --> SKIPPED (Conflict): '{source_path.name}' already exists in '{destination_dir.name}'", fg=typer.colors.YELLOW))
        return False

    if dry_run:
        typer.echo(typer.style(f"  --> SIMULATED MOVE: '{source_path.name}' would move to '{destination_dir.name}'", fg=action_color))
        return True

    
    try:
        shutil.move(str(source_path), str(final_path))
        typer.echo(typer.style(f"  --> MOVED: '{source_path.name}' to '{destination_dir.name}'", fg=action_color))
        return True

    except PermissionError:
        typer.echo(typer.style(f"  --> FAILED (Permission): Could not move '{source_path.name}'.", fg=typer.colors.RED))
        return False
    except Exception as e:
        typer.echo(typer.style(f"  --> FAILED (Error): Could not move '{source_path.name}'. Reason: {e}", fg=typer.colors.RED))
        return False
def organize_directory(target_path: Path, category_map: Dict[str, str], dry_run: bool) -> Dict[str, int]:

    """
    Organizes all files in a target directory according to their extensions and moves them to corresponding folders.

    Skips files and directories that start with a dot (.) or do not have an extension.

    If the dry_run flag is set to True, it will simulate the organization process without moving any files.

    Returns a dictionary containing statistics about the organization process, including the number of moved, skipped, failed, and total items.

    :param target_path: The path to the target directory to be organized.
    :param category_map: A dictionary mapping file extensions to their corresponding folder names.
    :param dry_run: Whether to simulate the organization process without moving any files.
    :return: A dictionary containing statistics about the organization process.
    :rtype: Dict[str, int]
    """
    stats = {'moved': 0, 'skipped': 0, 'failed': 0, 'total_items': 0}

    
    for item in target_path.iterdir():
        stats['total_items'] += 1

        
        if item.is_dir() or item.name.startswith('.'):
            typer.echo(f"  - Skipped: {item.name}")
            stats['skipped'] += 1
            continue
        
        
        if not item.suffix:
            typer.echo(f"  - Skipped (No Extension): {item.name}")
            stats['skipped'] += 1
            continue

        
        folder_name = classify_file(item, category_map)
        destination_dir = target_path / folder_name

        
        if not dry_run:
            try:
                
                destination_dir.mkdir(exist_ok=True)
            except Exception as e:
                typer.echo(typer.style(f"Error: Could not create directory '{destination_dir.name}'. Skipping file. Reason: {e}", fg=typer.colors.RED), err=True)
                stats['failed'] += 1
                continue

        
        if move_file_safely(item, destination_dir, dry_run):
            stats['moved'] += 1
        else:
            
            stats['skipped'] += 1 

    return stats
@app.command()
def run(
    target_path: Optional[Path] = typer.Argument(
        
        None,
        exists=True,
        file_okay=False,
        dir_okay=True,
        writable=True,
        resolve_path=True,
        help="The directory to organize. Defaults to the system's Downloads folder.",
    ),
    config_file: Path = typer.Option(
        Path(__file__).parent / 'config.json',
        '--config',
        '-c',
        help="Path to the JSON configuration file for mappings."
    ),
    dry_run: bool = typer.Option(
        False,
        '--dry-run',
        '-d',
        help="Simulate the organization process without moving any files."
    ),
):
    """
    The main command to execute the file organization process.
    """
    
    if target_path is None:
        target_path = Path.home() / 'Downloads'
    
    if not target_path.is_dir():
        typer.echo(typer.style(f"Error: Target path '{target_path}' is not a valid directory.", fg=typer.colors.RED), err=True)
        raise typer.Exit(code=1)

    
    category_map = get_category_map(config_file)
    
    if dry_run:
        typer.echo(typer.style("\n*** DRY-RUN MODE ACTIVE: NO FILES WILL BE MOVED ***\n", fg=typer.colors.CYAN, bold=True))

    
    typer.echo("-" * 40)
    typer.echo(f"Processing directory: {target_path}")
    
    stats = organize_directory(target_path, category_map, dry_run)
    
    typer.echo("-" * 40)

    
    mode_text = "DRY-RUN COMPLETE" if dry_run else "Organization Complete"
    typer.echo(typer.style(f"✅ {mode_text}!", fg=typer.colors.BRIGHT_GREEN, bold=True))
    typer.echo(f"Total items scanned: {stats['total_items']}")
    typer.echo(f"Files successfully moved/simulated: {stats['moved']}")
    typer.echo(f"Items skipped (directories, hidden, conflicts, failures): {stats['total_items'] - stats['moved']}")

if __name__ == "__main__":
    try:
        app()
    except Exception as e:
        typer.echo(typer.style(f"\nFATAL ERROR: An unexpected error occurred: {e}", fg=typer.colors.RED), err=True)
        sys.exit(1)