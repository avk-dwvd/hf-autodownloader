# hf-autodownloader

An interactive command-line tool for choosing files from a Hugging Face Hub model repository and downloading them into a local repository folder.

Use the guides to [install and run the CLI](getting-started.md), understand its [module layout](architecture.md), or [contribute changes](contributing.md).

## How it works

1. Enter a Hugging Face model repository ID, or pass it as a command-line argument.
2. Choose a parent directory for downloaded files.
3. Browse the paginated file list and select the files to download.
4. Review the selection summary and confirm before downloading.

Files are stored beneath `<parent>/<owner>_<repository>` with their repository paths preserved. For example, `meta-llama/Llama-3-8B` is stored in a `meta-llama_Llama-3-8B` folder. Press Ctrl+C to stop; files already completed remain in place.

Private or gated repositories require an available Hugging Face token. No files are downloaded before confirmation.
