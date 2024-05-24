import logging
import os
import praw
import numpy as np
from datetime import datetime, timedelta

reddit = praw.Reddit(
    client_id="ghj5rFGtFyJbzXYjZNOr8g",
    client_secret="0OsY35NbQ8iW6ZHrrC8IYnY9dDiBDg",
    password="m!Z3X_BUJV2AVJJ",
    user_agent="ios:com.example.myredditapp:v1.2.3 (by u/SouthernFishing8475)",
    username="SouthernFishing8475",
)

def is_stock_name(text):
    if text[0] == '$':
        text = text[1:]
    not_stock_names = ['LOL', 'YOLO', 'WSB', 'BTC', 'CEO', 'HATES', 'TIL', 'NOT', 'THIS','EST', 'BLOW', 'EOM', 'BUY', 'SELL', 'BIG', 'ETH', 'PEACE', 'NICE', 'SORRY', 'BUDDY', 'STOCK', 'SPLIT','ASAP', 'PUTS', 'I', 'FUCK', 'YES', 'GG', 'GOD', 'BLESS', 'RIP', 'STOCK', 'AI', 'LMAO', 'LMFAO']
    is_stock = (text.isupper() and text.isalpha() and 2 < len(text) <= 5 and text not in not_stock_names)
    if is_stock:
        if text not in hyped_stocks.keys():
            hyped_stocks[text] = 0
        hyped_stocks[text] += 1

def contains_stock_name(text):
    return any(is_stock_name(word) for word in text.split())


if __name__ == '__main__':
    hyped_stocks = {}

    # Get the current time
    current_time = datetime.now()

    # Add 2 hours
    new_time = current_time + timedelta(hours=2)

    # Format the new time as DD-MM_HH-MM
    formatted_time = new_time.strftime('%d-%m_%H-%M')


    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO,
                        format='%(message)s',
                        handlers=[
                            logging.FileHandler(f'logs/{formatted_time}.log'),
                            logging.StreamHandler()
                        ])

    logger.info(f"Starting script at {formatted_time}")
    # Stores all posts and comments that mention a stock
    mentioning_posts = []

    subreddits = ['stocks', 'shortsqueeze', 'pennystocks', 'Aktien', 'ValueInvesting', 'Daytrading', 'wallstreetbets',
                  'Superstonks']

    for sr in subreddits:
        logger.info(20*'-' + '\n' + f"Checking subreddit: {sr}")
        # Go through posts and comments in the subreddit
        for submission in reddit.subreddit(sr).top('day'):
            if contains_stock_name(submission.title):
                mentioning_posts.append(submission.title)
            submission.comments.replace_more(limit=0)
            for comment in submission.comments.list():
                if contains_stock_name(comment.body) and "I am a bot" not in comment.body:
                    mentioning_posts.append(comment.body)
        logger.info(f"Saving data for {sr} \n" + 20*"-")
        np.save(f"data/{sr}_{formatted_time}_data.npy", hyped_stocks)

        hyped_stocks = {}

    logger.info(f"Finished script!")



