import os
import json
import requests
import tweepy
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP, Context
from mcp.types import PromptMessage, TextContent
from typing import List, Optional
import logging
import time


mcp = FastMCP("Twitter Marketing MCP", dependencies=["tweepy", "google-genai"])

load_dotenv()


RATE_LIMITS = {}
RATE_LIMIT_WINDOW = 15 * 60 
@mcp.tool()
def tweet(text: str) -> str:
    """ Text should be less than 280 characters and takes image filename as input """
    try:
        # Load credentials
        api_key = os.getenv('X_api_key')
        api_secret = os.getenv('X_api_key_sec')
        access_token = os.getenv('X_access_token')
        access_token_secret = os.getenv('X_access_token_sec')
        bearer_token = os.getenv('X_bearer_token')

        auth_v1 = tweepy.OAuth1UserHandler(api_key, api_secret)
        auth_v1.set_access_token(access_token, access_token_secret)
        client_v1 = tweepy.API(auth_v1, wait_on_rate_limit=True)

        client_v2 = tweepy.Client(
            bearer_token=bearer_token,
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_token_secret,
            wait_on_rate_limit=True
        )

        media_ids = None
        # Check if the image path is provided and exists
        response = client_v2.create_tweet(text=text, media_ids=media_ids)
        return f"✅ Tweet posted: {response.data['id']}"


    except tweepy.TweepyException as e:
        return f"❌ Twitter error: {e}"

    except Exception as e:
        return f"❌ Unexpected error: {e}"
    
@mcp.tool()
def web_scrape(query: str) -> str:
    """
    Web scrape using the Serper API to perform Google-like search.

    Args:
        query (str): Search query.

    Returns:
        str: Raw JSON response with search results.
    """
    try:
        url = "https://google.serper.dev/search"
        payload = json.dumps({"q": query})
        headers = {
            'X-API-KEY': os.getenv('serper_api'),
            'Content-Type': 'application/json'
        }

        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()  # Raises error for bad status codes
        return response.text

    except requests.exceptions.RequestException as e:
        return f"❌ Web scraping error: {e}"

    except Exception as e:
        return f"❌ Unexpected error: {e}"

@mcp.prompt()
def username_change_prompt(screen_name: str) -> List[PromptMessage]:
    """Prompt template for querying Twitter username changes."""
    return [
        PromptMessage(
            role="user",
            content=TextContent(
                type="text",
                text=f"Please show the username change history for Twitter user @{screen_name}"
            )
        ),
        PromptMessage(
            role="assistant",
            content=TextContent(
                type="text",
                text=f"I'll fetch the username change history for @{screen_name}."
            )
        )
    ]

@mcp.tool()
def query_username_changes(screen_name: str, ctx: Context) -> str:
    """
    Query the username change history for a Twitter user using the memory.lol API.

    Parameters:
        screen_name (str): The current Twitter screen name (handle) of the user, without the '@' symbol.
                          For example, use 'OSINT_Ukraine' for '@OSINT_Ukraine'.
                          Case-insensitive and must be a valid Twitter handle.

    Returns:
        A formatted string containing the username change history, including user ID and timestamps.
        If no history is found or an error occurs, returns an error message.
    """
    ctx.info(f"Querying username changes for screen name: {screen_name}")
    
    # Fetch data from memory.lol API
    try:
        response = requests.get(f"https://api.memory.lol/v1/tw/{screen_name}")
        response.raise_for_status()
        data = response.json()
    except requests.HTTPError as e:
        return f"Error: Failed to fetch data for {screen_name} (status {e.response.status_code})"
    except requests.RequestException:
        return f"Error: Network issue while fetching data for {screen_name}"

    if not data.get("accounts"):
        return f"No username change history found for {screen_name}"

    # Format username change history
    formatted_history = []
    for account in data["accounts"]:
        user_id = account["id_str"]
        screen_names = account["screen_names"]
        history = "\n".join(
            f"- {name} ({' to '.join(dates) if isinstance(dates, list) else dates})"
            for name, dates in screen_names.items()
        )
        formatted_history.append(f"User ID {user_id}:\n{history}")
    
    return f"Username change history for {screen_name}:\n\n" + "\n\n".join(formatted_history)

async def get_twitter_client() -> tweepy.Client:
    api_key = os.getenv('X_api_key')
    api_secret = os.getenv('X_api_key_sec')
    access_token = os.getenv('X_access_token')
    access_token_secret = os.getenv('X_access_token_sec')
    bearer_token = os.getenv('X_bearer_token')

    return tweepy.Client(
        bearer_token=bearer_token,
        consumer_key=api_key,
        consumer_secret=api_secret,
        access_token=access_token,
        access_token_secret=access_token_secret,
        wait_on_rate_limit=True
    )


def convert_tweets_to_markdown(tweets: Optional[tweepy.Response]) -> str:
    if not tweets or not tweets.data:
        return "No tweets found."

    output = []
    for tweet in tweets.data:
        output.append(f"- 🕒 {tweet.created_at}:\n  {tweet.text}\n")
    return "\n".join(output)

# Main MCP tool
@mcp.tool()
async def get_user_tweets(username: str, count: int = 10, ctx: Context = None) -> str:
    """Fetch recent tweets from a user's timeline."""
    try:
        client = await get_twitter_client()
        username = username.lstrip('@')

        # ❌ Removed `await` - these are synchronous calls
        user_response = client.get_user(username=username)
        if not user_response or not user_response.data:
            return f"❌ Could not find user: @{username}"

        user_id = user_response.data.id
        tweets = client.get_users_tweets(
            id=user_id,
            max_results=count,
            tweet_fields=["created_at", "text"]
        )

        return convert_tweets_to_markdown(tweets)
    except Exception as e:
        return f"⚠️ Failed to get tweets for @{username}: {str(e)}"
    
def check_rate_limit(endpoint: str) -> bool:
    """Check if we're within rate limits for a given endpoint."""
    now = time.time()
    if endpoint not in RATE_LIMITS:
        RATE_LIMITS[endpoint] = []

    # Remove old timestamps
    RATE_LIMITS[endpoint] = [t for t in RATE_LIMITS[endpoint] if now - t < RATE_LIMIT_WINDOW]

    # Check limits based on endpoint
    if endpoint == 'tweet':
        return len(RATE_LIMITS[endpoint]) < 300  # 300 tweets per 15 minutes
    elif endpoint == 'dm':
        return len(RATE_LIMITS[endpoint]) < 1000  # 1000 DMs per 15 minutes
    return True
    
@mcp.tool()
async def send_dm(user_id: str, message: str) -> str:
    """Send a direct message to a user."""
    try:
        if not check_rate_limit('dm'):
            return "Rate limit exceeded for DMs. Please wait before sending again."

        client = await get_twitter_client()

        await client.send_dm(
            user_id=user_id,
            text=message
        )
        RATE_LIMITS.setdefault('dm', []).append(time.time())
        return f"Successfully sent DM to user {user_id}"
    except Exception as e:
        return f"Failed to send DM: {e}"