
## QuickView

A few simple RAGs wrapped in streamlit 

## Overview

This project provides a collection of summarization and assistant tools that process text, video, and audio content using AI models. It includes:

- `news_summarizer.py`: Fetches and summarizes news articles.
- `yt_summarizer.py`: Processes YouTube transcripts or videos and generates summaries.
- `voice_assistant.py`: A voice-based assistant that interacts with users and delivers spoken summaries.
- `ui.py`: A simple user interface wrapper to interact with the summarization tools.
- `.env.sample`: Example environment configuration for API keys.
- `requirements.txt`: Python dependencies required to run the project.

## Features

- Modular design for summarizing news, YouTube videos, and spoken input.
- Simple UI for quick experimentation and interaction.
- Extensible structure for adding new summarization sources or models.
- Optional voice interface for interactive responses.

## Setup and Usage

1. Clone the repository:
   ```bash
   git clone https://github.com/daud1/glowing-octo-goggles.git
   cd glowing-octo-goggles
2. Copy the environment template and add your keys
   ```bash
   cp .env.sample .env
3. Install dependencies
   ```bash
   pip install -r requirements.txt
4. Run the UI application
   ```bash
   streammlit run ui.py
