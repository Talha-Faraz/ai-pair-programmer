# AI Pair Programmer — Floating AI Coding Assistant

An AI-powered macOS desktop assistant that analyzes a selected IDE or application window and provides coding assistance using Google Gemini.

## Overview

AI Pair Programmer is a lightweight desktop application designed to provide contextual coding assistance directly from the developer's screen.

The application can detect active macOS windows, capture a selected window, send the screenshot together with the user's question to Google Gemini, and display the AI-generated analysis through a floating interface.

## Features

* Detect active macOS windows
* Select a specific IDE/application window for analysis
* Capture the selected screen/window
* Send screenshots and coding questions to Google Gemini
* Identify potential syntax errors and logical issues
* Detect missing imports and other coding problems
* Provide interactive coding assistance
* Floating always-on-top interface
* Background processing using PyQt6 QThread
* macOS-focused desktop workflow

## Tech Stack

* Python
* PyQt6
* Google Gemini API
* MSS
* Pillow
* Quartz
* Multithreading

## Project Structure

```text
ai-pair-programmer/
│
├── main.py
├── modules/
│   ├── ai_analyzer.py
│   ├── capture_engine.py
│   └── Demo.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

## How It Works

```text
Select Application
       ↓
Capture Window
       ↓
Send Screenshot + Query
       ↓
Google Gemini Analysis
       ↓
Display Coding Feedback
```

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/ai-pair-programmer.git
cd ai-pair-programmer
```

Create a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## API Key

Set your Google Gemini API key as an environment variable.

Do not commit API keys directly to the repository.

Example:

```bash
export GEMINI_API_KEY="YOUR_API_KEY"
```

## Run

```bash
python main.py
```

## Screenshots

Add screenshots of the application here.

## Future Improvements

* Better code extraction from screenshots
* Support for additional AI models
* Improved code-context handling
* Code suggestions and automated fixes
* Cross-platform support
* Improved UI/UX
* Project/file-level context analysis

## Author

Talha Faraz

Computer Science & Engineering (Artificial Intelligence)

GitHub: https://github.com/YOUR_USERNAME
LinkedIn: https://www.linkedin.com/in/talhafaraz

