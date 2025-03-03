# NA Archief Downloader

This Python project provides a command-line interface (CLI) to download files from an online archive service. The user can specify a set to fetch data from, as well as a directory to save the files. The project uses `click`, `requests`, and `lxml` libraries to interact with the archive service and save files locally.

## Features

- Fetches data from an online archive service using OAI.
- Extracts and downloads files associated with specific dossiers.
- Saves files in a specified directory.
- Provides verbose logging for debugging and tracking the download progress.
- Allows the user to limit the number of dossiers to download.

## Requirements

- Python 3.7 or higher
- Required Python packages:
  - `click`
  - `requests`
  - `lxml`

You can install the required packages using `pip`:

```bash
pip install -r requirements.txt
```

## Setup

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/archief-downloader.git
    cd archief-downloader
    ```

2. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. If you're using a virtual environment, make sure to activate it before running the application.

## Usage

The tool is a command-line application that allows you to download files from an archive based on a specific set identifier. You can specify the directory to save the files, limit the number of dossiers to download, and enable verbose output.

### Commands

To run the application, use the following command:

```bash
python archief_downloader.py --set <set_number> --directory <path_to_save_files> [--limit <number_of_dossiers>] [--verbose]
```

#### Options

- `--set`: (Required) The set number to fetch data from. This can be obtained from the Archive block page (e.g., `2.19.185`).
- `--directory`: (Required) The directory where files will be saved. This is relative to where the script is run.
- `--limit`: (Optional) Limit the number of dossiers to download. Default is 0 (no limit).
- `--verbose`: (Optional) Print verbose output. Default is `False`.

### Example

To download files for a specific set and save them to a directory:

```bash
python archief_downloader.py --set 2.19.185 --directory ./downloaded_files
```

To limit the number of dossiers to download to 10 and enable verbose logging:

```bash
python archief_downloader.py --set 2.19.185 --directory ./downloaded_files --limit 10 --verbose
```

## Contributing

We welcome contributions from the open-source community! If you have suggestions for improvements or bug fixes, feel free to submit a pull request.

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to your fork (`git push origin feature-branch`).
6. Create a new pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
