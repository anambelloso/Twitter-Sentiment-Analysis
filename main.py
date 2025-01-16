import tweepy
import csv

# Authentication keys and tokens (replace with your actual keys)
bearer_token = 'AAAAAAAAAAAAAAAAAAAAAMvSyAEAAAAA%2FTYlL7DovdvscaZ8kbtqMi8LeW4%3D0yVZuPW9sza7qygszZETExw8ID3pwPK3hmJArZJ3OU0MY2JU7a'

# Create a client for Twitter API v2
client = tweepy.Client(bearer_token=bearer_token)

# Define the username and max tweets
username = 'MariaCorinaYA'
max_tweets = 100

try:
    # Fetch user ID for the username
    user = client.get_user(username=username)
    user_id = user.data.id

    # Fetch the most recent tweets
    response = client.get_users_tweets(
        id=user_id,
        max_results=min(max_tweets, 100),  # Twitter API allows up to 100 tweets per request
        tweet_fields=['created_at', 'public_metrics', 'text', 'id']
    )

    # Save tweets to a CSV file
    with open('maria_corina_last_100_tweets.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Date', 'Tweet', 'Likes', 'Retweets', 'URL'])  # CSV Header

        if response.data:
            for tweet in response.data:
                # Extract tweet details
                tweet_date = tweet.created_at
                tweet_text = tweet.text
                tweet_url = f"https://twitter.com/{username}/status/{tweet.id}"

                # Extract likes and retweets
                public_metrics = tweet.public_metrics or {}
                tweet_likes = public_metrics.get('like_count', 0)
                tweet_retweets = public_metrics.get('retweet_count', 0)

                # If likes or retweets are 0, fetch the tweet again to confirm
                if tweet_likes == 0 or tweet_retweets == 0:
                    detailed_tweet = client.get_tweet(tweet.id, tweet_fields=['public_metrics'])
                    if detailed_tweet.data:
                        tweet_likes = detailed_tweet.data.public_metrics.get('like_count', tweet_likes)
                        tweet_retweets = detailed_tweet.data.public_metrics.get('retweet_count', tweet_retweets)

                # Write row to CSV
                writer.writerow([tweet_date, tweet_text, tweet_likes, tweet_retweets, tweet_url])

        else:
            print("No tweets found for the specified user.")

    print("Tweets have been saved to 'maria_corina_last_100_tweets.csv'")

except tweepy.TweepyException as e:
    print(f"An error occurred: {e}")