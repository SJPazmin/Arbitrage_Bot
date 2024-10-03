# Installation Guide

This document provides step-by-step instructions on how to install the project and its dependencies.

## Prerequisites

Before you begin, ensure you have the following installed on your machine:

- Python 3.6 or higher
- MetaTrader 5

## Installation Steps

1. **Clone the repository:**

    Open your terminal and run the following command to clone the repository:

    ```bash
    git clone https://github.com/SJPazmin/Arbitrage_Bot.git
    cd Arbitrage_Bot
    ```

2. **Create a virtual environment:**

    It is recommended to create a virtual environment to manage dependencies. Run the following commands:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages:**

    Run the following command to install the required packages listed in `requirements.txt`:

    ```bash
    pip install -r requirements.txt
    ```

4. **Configure MetaTrader 5:**

    Ensure that MetaTrader 5 is installed and configured on your machine. You need to have an active account and be logged in.

5. **Run the bot:**

    You can now run the bot by executing the `main.py` script:

    ```bash
    python main.py
    ```

## Additional Information

- For detailed usage instructions, refer to the `README.md` file.
- If you encounter any issues, please check the logs in the `app.log` file for more information.

