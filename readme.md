## **Terminal Researcher**

---

### **Table of Contents**

1. [Introduction](#introduction)
2. [Setup and Installation](#setup-and-installation)
3. [Configuration](#configuration)
4. [How to Use](#how-to-use)
   - [Using `python chat.py`](#using-python-chatpy)
   - [Using `tr` Command](#using-tr-command)
5. [Color-Coded Terminal Output](#color-coded-terminal-output)
6. [Error Handling](#error-handling)
7. [Logging](#logging)
8. [FAQ](#faq)

---

### **Introduction**

The Terminal Researcher is a terminal-based chat application that interacts with the **Perplexica REST API** to provide answers to user queries. It also logs chat history and any external sources referenced in the responses. You need to get [Perplexica](https://github.com/ItzCrazyKns/Perplexica) up and running as a prequisite. This guide walks you through the setup, usage, and detailed functionality of the application.

---

### **Setup and Installation**

#### **Prerequisites**

- Python 3.8 or higher
- An internet connection to communicate with the API
- [Anaconda](https://www.anaconda.com/) installed on your system (if using a Conda environment)

#### **Install Dependencies**

If using Conda, ensure the `terminal-researcher` environment is active, and install dependencies:

```bash
conda create --name terminal-researcher python=3.11 pip
conda activate terminal-researcher
pip install requests termcolor rich
```
Install the required dependencies:

```bash
pip install -r requirements.txt
```

#### **Clone the Repository**

To set up the project locally, clone the repository:

```bash
git clone <this repo>
cd terminal-researcher
```

---

### **Configuration**

The application requires a **`config.json`** file to be present in the root directory. Below is an example configuration:

```json
{
    "base_url": "http://localhost:3001",
    "timeout": 60,
    "history_limit": 3,
    "chat_model": {
        "provider": "ollama",
        "model": "marco-o1:latest"
    },
    "embedding_model": {
        "provider": "ollama",
        "model": "nomic-embed-text:latest"
    },
    "optimization_mode": "balanced",
    "focus_mode": "webSearch"
}
```

- **base_url**: The URL of the Perplexica API.
- **timeout**: The timeout in seconds for each API request.
- **chat_model**: Configuration for the chat model.
- **embedding_model**: Configuration for the embedding model.
- **optimization_mode**: Controls the speed vs. quality trade-off.
- **focus_mode**: The context mode for the API query.

---

### **How to Use**

#### **Using `python chat.py`**

1. **Run the Application**

   Activate the `terminal-researcher` Conda environment, navigate to the project directory, and run:

   ```bash
   python chat.py
   ```

2. **Interact with the Assistant**

   The assistant will greet you and wait for your query:

   ```plaintext
   Assistant: Hi there! How can I assist you today?
   ```

3. **Type Queries**

   Type your query and hit **Enter**:

   ```plaintext
   You: What happened to DJT yesterday?
   ```

4. **View Results**

   The assistant responds with the query result and referenced sources (if any):

   ```plaintext
   Assistant: Thinking... [Response took 3 seconds]
   Assistant: 5 sources referenced.
    - DJT stock skyrockets following Donald Trump's ...: https://finance.yahoo.com/news/...
    - Trump Media shares halted repeatedly as DJT whipsaws ...: https://www.nbcnews.com/business/...
   ```

5. **Exit the Chat**

   Type **`exit`** or **`quit`** to end the session:

   ```plaintext
   You: exit
   Ending chat. Goodbye!
   ```

---

#### **Using `tr` Command**

1. **Set Up the `tr` Command**

   Create a script named `tr` in the project directory (it already exists if you have cloned the repo, ensure that the path is correct):

   ```bash
   nano ~/dev-ai/terminal-researcher/tr
   ```

   Add the following content:

   ```bash
   #!/bin/bash
   # Activate the Conda environment
   source ~/anaconda3/etc/profile.d/conda.sh
   conda activate terminal-researcher

   # Navigate to the project directory
   cd ~/dev-ai/terminal-researcher

   # Run the Python script with passed arguments
   python chat.py "$@"
   ```

   Replace `~/anaconda3` with your Anaconda installation path.

2. **Make the Script Executable**

   ```bash
   chmod +x ~/dev-ai/terminal-researcher/tr
   ```

3. **Add the Script to Your PATH (Optional)**

   To use the `tr` command from anywhere, add the project directory to your PATH:

   ```bash
   echo 'export PATH="$HOME/dev-ai/terminal-researcher:$PATH"' >> ~/.bashrc
   source ~/.bashrc
   ```

4. **Usage Examples**

   - **Run a Query Directly**:
     ```bash
     tr "Who is DJT?"
     ```

   - **Enter Interactive Chat**:
     ```bash
     tr
     ```

---

### **Color-Coded Terminal Output**

- **User Input**: Displayed in **green**.
- **Assistant Messages**: Displayed in **blue**.
- **Referenced Sources**: Displayed in **yellow** with **cyan URLs**.
- **Errors**: Displayed in **red**.

---

### **Error Handling**

- **Timeouts**: If the server does not respond within the configured timeout, the following message is displayed:
  
  ```plaintext
  Assistant: [No response received within the timeout period]
  ```

- **HTTP Errors**: If the server returns an error, the following message is displayed:

  ```plaintext
  Assistant: [HTTP error: 404 Client Error: Not Found]
  ```

- **Connection Errors**: If the API is unreachable, the following message is displayed:

  ```plaintext
  Assistant: [An error occurred. Please try again later.]
  ```

---

### **Logging**

The application generates two log files:

1. **activity.log**: Stores information about API requests, responses, and errors.

   **Example**:
   ```
   2024-10-30 14:25:05 - INFO - Query sent: What happened to DJT yesterday?
   2024-10-30 14:25:08 - INFO - Sources referenced: 5
   ```

2. **chat_history.log**: Stores the chat history between the user and the assistant.

   **Example**:
   ```
   [2024-10-30 14:25:05] Human: Hello!
   [2024-10-30 14:25:08] Assistant: Hi there! How can I assist you today?
   ```

---

### **FAQ**

#### **1. How do I change the timeout setting?**

Modify the `timeout` value in the `config.json` file:

```json
"timeout": 120
```

#### **2. What happens if the API is unreachable?**

The application will display an error message and log the error in `activity.log`.
