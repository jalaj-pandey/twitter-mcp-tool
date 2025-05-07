# Twitter Marketing MCP

This repository contains the **Twitter Marketing MCP**, a tool designed to streamline social media marketing tasks using Python. It includes features for tweeting, image generation, and web scraping.

## Video Demonstration

Watch the video demonstration of the **Twitter Marketing MCP** in action:  
# Linkedin Post

[Watch the video demonstration on LinkedIn](https://www.linkedin.com/posts/rugvedp_ai-twitterbot-automation-activity-7324008443239903232-lVWa?utm_source=social_share_send&utm_medium=member_desktop_web&rcm=ACoAADawhcMB8OoVwx5oE_0k00nkpuwmA62Uzws)

## Features

### 1. **Tweet Posting**
Post tweets with or without images directly to Twitter.  

### 2. **Image Generation**
Generate images based on text prompts using Google's Gemini API.  

### 3. **Web Scraping**
Perform localized Google-like searches using the Serper API.  

## Installation

1. Clone the repository:
     ```bash
     git clone https://github.com/rugvedp/Twitter-Marketing-MCP.git
     cd Twitter-Marketing-MCP
     ```

2. Install dependencies:
     ```bash
     pip install requirements.txt
     mcp install script.py
     ```

3. Create a `.env` file with the following keys:
     ```env
     X_api_key=<your_twitter_api_key>
     X_api_key_sec=<your_twitter_api_secret>
     X_access_token=<your_twitter_access_token>
     X_access_token_sec=<your_twitter_access_token_secret>
     X_bearer_token=<your_twitter_bearer_token>
     GEMINI_API_KEY=<your_gemini_api_key>
     serper_api=<your_serper_api_key>
     ```

## Usage 

Open your claude desktop you will see the Twitter Marketing MCP` is ready to use.

If not then Copy paste the `config.json` into your claude_desktop_config.json

## Folder Structure
```
.
├── generated_images/   # Folder for storing generated images
├── script.py           # MCP core logic
├── .env                # Environment variables
├── requirements.txt    # Python dependencies
└── readme.md           # Project documentation
```

## License
This project is licensed under the MIT License.  
