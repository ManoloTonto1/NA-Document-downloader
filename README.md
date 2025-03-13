# 🌟 NA Archief Downloader 🌟

Welcome to the **NA Archief Downloader**! 🚀 This Python-powered tool allows you to effortlessly download files from an online archive service 📂. It provides a sleek command-line interface (CLI) that lets you specify which set to fetch and where to save the files. Built with the power of `click`, `requests`, and `lxml`, this project makes downloading from archives a breeze. 😎

## 🔥 Features

- 🚀 Fetches data from an online archive service using OAI (Open Archives Initiative).
- 🗂️ Extracts and downloads files tied to specific dossiers.
- 💾 Saves files in a directory of your choosing.
- 📊 Logs everything with detailed output to keep you in the loop.
- 🛠️ Optionally limits the number of dossiers to download — you're in control!

## ⚙️ Requirements

Make sure you've got the following:

- Python 3.7 or higher 🐍
- These Python packages:
  - `click`
  - `requests`
  - `lxml`

Install all the dependencies like this:

```bash
pip install -r requirements.txt
```

## 🏁 Setup

Let's get this up and running! 🚀

1. Clone the repo:

    ```bash
    git clone https://github.com/your-username/archief-downloader.git
    cd archief-downloader
    ```

2. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. If you're using a virtual environment (which we recommend 💡), don't forget to activate it before running the app.

## 🖥️ Usage

This tool runs in the command line, letting you download archive files with ease. You can pick the set to download from, choose where to save your files, limit the download, and even enable verbose logging to see everything happening under the hood. 🔥

### 🧑‍💻 Commands

Run the app using:

```bash
python archief_downloader.py --set <set_number> --directory <path_to_save_files> [--limit <number_of_dossiers>] [--verbose]
```

#### 🔧 Options

- `--set`: (Required) The archive set number (e.g., `2.19.185`). You can grab this from the archive block page.
- `--directory`: (Required) Path where the files will be saved 🔽.
- `--limit`: (Optional) Limit the number of dossiers to download. Default is `0` (no limit).
- `--verbose`: (Optional) Enable detailed logging. Default is `False`.

### 🚀 Example

Download files for a specific set and save them like this:

```bash
python archief_downloader.py --set 2.19.185 --directory ./downloaded_files
```

To limit the downloads to 10 dossiers and get verbose logging:

```bash
python archief_downloader.py --set 2.19.185 --directory ./downloaded_files --limit 10 --verbose
```

## 🤝 Contributing

We 💖 contributions from everyone! Have ideas for improvements or bug fixes? Awesome! Here's how you can get involved:

1. Fork the repo.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit those changes (`git commit -am 'Add new feature'`).
5. Push to your fork (`git push origin feature-branch`).
6. Create a pull request (PR) and let's review it! ✨

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 👌
