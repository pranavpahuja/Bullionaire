import tweepy
import pandas as pd
from textblob import TextBlob
import time
import os
from dotenv import load_dotenv

# --- X API Authentication ---
load_dotenv()
bearer_token = os.getenv("BEARER_TOKEN")

client = tweepy.Client(bearer_token=bearer_token)

# --- Function to fetch tweets safely with rate limit handling ---
def fetch_tweets_safe(query, max_results_per_page=10, max_pages=1):
    all_tweets = []
    try:
        paginator = tweepy.Paginator(
            client.search_recent_tweets,
            query=query,
            tweet_fields=["created_at", "public_metrics", "text"],
            max_results=max_results_per_page
        )

        page_count = 0
        for tweet_page in paginator:
            if tweet_page.data:
                for tweet in tweet_page.data:
                    likes = tweet.public_metrics['like_count']
                    retweets = tweet.public_metrics['retweet_count']
                    all_tweets.append({
                        "text": tweet.text,
                        "likes": likes,
                        "retweets": retweets
                    })
            page_count += 1
            if page_count >= max_pages:
                break
            time.sleep(2)  # avoid hitting rate limits

    except tweepy.TooManyRequests as e:
        reset_time = int(e.response.headers.get("x-rate-limit-reset", time.time() + 60))
        sleep_time = max(reset_time - int(time.time()), 1)
        print(f"Rate limit reached. Sleeping for {sleep_time} seconds...")
        time.sleep(sleep_time)
    return pd.DataFrame(all_tweets)

# --- Sentiment Analysis and Buzz Score ---
def analyze_sentiment(df):
    df['polarity'] = df['text'].apply(lambda x: TextBlob(x).sentiment.polarity)
    df['sentiment'] = df['polarity'].apply(lambda x: 'positive' if x>0 else ('negative' if x<0 else 'neutral'))
    df['buzz_score'] = df['likes'] + df['retweets']
    return df

# --- Main Function ---
def finance_buzz_summary(company_keywords):
    print(f"Fetching tweets for: {company_keywords}")
    tweets_df = fetch_tweets_safe(company_keywords, max_results_per_page=100, max_pages=10)
    if tweets_df.empty:
        print("No tweets found for this query.")
        return None

    tweets_df = analyze_sentiment(tweets_df)

    # Summary: total buzz score and count per sentiment
    summary = tweets_df.groupby('sentiment').agg({
        'buzz_score': 'sum',
        'text': 'count'
    }).rename(columns={'text':'tweet_count'}).sort_values(by='buzz_score', ascending=False)

    return summary

# --- Example Usage ---
if __name__ == "__main__":
    # Use keywords instead of $CASHTAG
    company_keywords = "Apple earnings"
    summary_df = finance_buzz_summary(company_keywords)
    print(summary_df)
