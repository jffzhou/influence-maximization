"""
Scraping subreddits with PRAW Python package
"""
import praw
import pandas as pd

NUM_POSTS = 100
SUBREDDITS = ["Cornell"] #Cooking, personalfinance, cscareerquestions, Cryptocurrency

def parse_submission(data, submission):
    data["content"].append(submission.selftext)
    data["id"].append(submission.id)
    data["user"].append(submission.author.id)
    data["replying-to"].append(None)
    data["url"].append(submission.url)

def parse_comment(data, comment):
    data["content"].append(comment.body)
    data["id"].append(comment.id)
    data["user"].append(comment.author.id)
    data["replying-to"].append(comment.parent().author.id)
    data["url"].append(comment.permalink)

def scrape_subreddit(reddit, subreddit_name):
    print("Scraping " + subreddit_name)
    subreddit = reddit.subreddit(subreddit_name)

    data = {"content": [], "id": [], "user": [], "replying-to": [], "url": []}

    for submission in subreddit.top(time_filter="day"):
        parse_submission(data, submission)
        submission.comments.replace_more()
        for comment in submission.comments.list():
            parse_comment(data, comment)

    return pd.DataFrame(data).to_csv(subreddit_name+".csv")


if __name__ == "__main__":
    print("Reddit Scraping Script")
    reddit = praw.Reddit(
        "bot",
        user_agent="desktop:CS6850-Network-Project-IM:v0.1.0 (by /u/pognet)"
    )
    print("Successfully acquired Reddit instance")

    for subreddit in SUBREDDITS:
        scrape_subreddit(reddit, subreddit)
    
    print("Scraping finished")
