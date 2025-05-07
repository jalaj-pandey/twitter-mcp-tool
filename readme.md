# Twitter MCP Tool

This repository contains the **Twitter MCP Tool**, a tool designed to streamline social media tasks using Python. It includes features for tweeting, username change history, Fetch recent tweets, and Send a direct message to a user.

## Features

### 1. **Tweet Posting**
Post tweets with or without images directly to Twitter.  

### 2. **Query Username Changes**
Track the username change history of any Twitter account.

### 3. **Fetch Recent Tweets**
Retrieve the latest tweets from any public Twitter user's timeline.  

### 4. **Send a Direct Message (DM)**
Send a private message directly to a Twitter user.

## Installing Dependencies and Running

1. Clone the repo using
     ```bash
     git clone https://github.com/jalaj-pandey/twitter-mcp-tool.git
     ```

2. Install dependencies:
     ```bash
     uv venv
     .venv\Scripts\activate
     pip install -r requirements.txt
     mcp dev script.py
     ```
     And if you want to install it in the claude desktop then use 
     ```bash
     pip install script.py
     ```

3. Create a `.env` file with the following keys:
     ```env
     X_api_key=<your_twitter_api_key>
     X_api_key_sec=<your_twitter_api_secret>
     X_access_token=<your_twitter_access_token>
     X_access_token_sec=<your_twitter_access_token_secret>
     X_bearer_token=<your_twitter_bearer_token>
     GEMINI_API_KEY=<your_gemini_api_key>
     ```

## Usage 

Open your claude desktop you will see the Twitter MCP Tool` is ready to use.

If not then Copy paste the `config.json` into your claude_desktop_config.json

## Folder Structure
```
.
├── script.py           # MCP core logic
├── .env                # Environment variables
├── requirements.txt    # Python dependencies
├── config.json         # config file for claude desktop
└── readme.md           # Project documentation
```
