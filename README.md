# medium2md

`medium2md` is a command-line tool written in Python that downloads articles from [Medium](https://medium.com) and converts them into markdown files. The tool not only converts the text, but also downloads the images in the articles, saving them locally and linking them appropriately in the markdown file.

## Features
- Downloads Medium articles as HTML
- Converts downloaded HTML articles into Markdown files
- Downloads images within the article and saves them locally
- Replaces image URLs in the markdown files with local paths
- Cleans up unnecessary data post processing
- Offers a user-friendly CLI interface with progress bars and prompts

## Installation

Before using `medium2md`, ensure you have Python 3.8 or later installed.

1. Clone the repository:
    ```bash
    git clone https://github.com/siddharthksah/medium2md
    ```
2. Navigate into the project folder:
    ```bash
    cd medium2md
    ```
3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the tool using the command:

```bash
python main.py -u <URL>
```

Replace <URL> with the URL of the Medium article you want to download.

If no URL is provided, the script will prompt you to enter one.

At the end of the process, the script will ask if you want to open the downloaded Markdown file in your default editor.

Output
The downloaded and converted articles are stored in the output directory, which is created in the root directory of the project.

Project Structure
.
├── LICENSE.txt
├── README.md
├── docs
├── output
├── requirements.txt
└── src
    ├── __init__.py
    ├── clean_md.py
    ├── clean_unnecessary_data.py
    ├── download_with_media.py
    ├── html_to_md.py
    ├── main.py
    └── url_to_local.py

Contributing
If you'd like to contribute to this project, feel free to submit a pull request. For major changes, please open an issue first to discuss the proposed change.

License
This project is licensed under the MIT License. See the LICENSE file for details.


