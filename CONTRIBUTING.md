# Contributing to the Internet Performance Dashboard

Thank you for your interest in contributing! All contributions are welcome.

## How to Contribute

There are several ways you can contribute to this project:

### 1. Reporting Bugs

If you find a bug, please open an issue on the GitHub repository. When reporting a bug, please include:
- A clear and descriptive title.
- A description of the steps to reproduce the bug.
- The expected behavior and what happened instead.
- Any error messages or tracebacks.

### 2. Suggesting Enhancements

If you have an idea for a new feature or an improvement to an existing one, feel free to open an issue to discuss it. This is a great way to get feedback before you start working on an implementation.

### 3. Submitting Pull Requests

If you have code to contribute, please submit it as a pull request.

**Pull Request Process:**
1. Fork the repository and create a new branch from `main`.
2. Make your changes in the new branch. Please ensure your code follows the existing style.
3. Add or update tests if applicable.
4. Ensure your code lints and runs without errors.
5. Submit the pull request with a clear description of the changes you have made.

## Development Setup

1. Ensure you have Python 3 installed.
2. Clone the repository.
3. It is highly recommended to use a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```
4. The necessary Python packages (`dash`, `pandas`) will be installed automatically when you run `dashboard.py` for the first time.
5. Download the official Ookla Speedtest CLI for your operating system from [speedtest.net/apps/cli](https://www.speedtest.net/apps/cli) and place the executable in the project directory.

Thank you for contributing!
