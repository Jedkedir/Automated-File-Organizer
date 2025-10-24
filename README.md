#  Automated File Organizer CLI

A simple, fast, and customizable Command Line Interface (CLI) tool designed to automatically sort and organize files within a specified directory (like your Downloads folder) based on their file type.

##  Features

* **Customizable Mappings (JSON):** Easily define which file extensions go into which folders by editing the `config.json` file.
* **Dry-Run Mode:** Preview the organization changes before moving any files, ensuring safety and confidence in the operation.
* **Typer CLI Interface:** Uses the powerful Typer library for a clean, user-friendly command-line experience with automatic help generation.
* **Standard Library Focus:** Relies heavily on Python's built-in libraries (`pathlib`, `shutil`) for robust and portable file operations.
* **'Other' Folder Handling:** Automatically moves files with unknown extensions into an `Other` folder, preventing clutter.

##  Setup and Installation

### Prerequisites

You need **Python 3.6+** installed on your system.

### Steps

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/Jedkedir/Automated-File-Organizer.git](https://github.com/Jedkedir/Automated-File-Organizer.git)
    cd automated-file-organizer
    ```

2.  **Create and Activate Virtual Environment (Recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Linux/macOS
    # .\venv\Scripts\activate  # On Windows
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

##  Configuration (`config.json`)

The default organization rules are stored in the `config.json` file. You can easily modify this file to customize your organization structure.

The structure is **`"FolderName": [".ext1", ".ext2", ...]`**.

**Example Snippet:**
```json
{
    "Documents": [".pdf", ".docx", ".txt", ".csv"],
    "Images": [".jpg", ".png", ".gif"],
    "Other": []
}
```

**Note:** Files with extensions not listed in the map will be moved to a folder named `Other`.

##  Usage

The main script is `organize.py`. Use the command `python organize.py [OPTIONS] [TARGET_PATH]`

### Basic Execution

If no path is specified, the script defaults to organizing your system's Downloads folder.

```bash
python organize.py
```

### Organizing a Specific Directory

Provide the path to the folder you wish to clean up.

```bash
python organize.py /Users/Desktop/MessyFolder
```

### Dry-Run Mode (Safe Preview)

Use the `--dry-run` or short `-d` flag to see exactly what actions the script would take without actually moving any files.

```bash
python organize.py --dry-run /path/to/folder
```

### Using a Custom Configuration File

If you want to use a rule set different from the default `config.json`, specify its path using the `--config` flag.

```bash
python organize.py --config ./my_custom_rules.json /path/to/folder
```

### Help

To view all available commands and options:

```bash
python organize.py --help
```

##  Project Structure

```
automated-file-organizer/
├── .gitignore
├── README.md
├── requirements.txt
├── config.json         # User-customizable mapping rules
└── organize.py         # The main CLI application logic
