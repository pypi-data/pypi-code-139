import snscrape.modules.twitter as sntwitter
from datetime import datetime
import pandas as pd


class TwitterAPI:
    def __init__(self) -> None:
        pass

    def fetch_by_content(
        phrase: str,
        num: int,
        from_t: datetime,
        to_t=datetime.today().strftime("%Y-%m-%d"),
    ) -> pd.DataFrame:
        """fetching tweets based on specific phrase and time period and the number of tweets

        Args:
            phrase (str): phrase to be searched amongst tweets
            num (int): number of tweets to be scraped
            from_t (datetime): from this date
            to_t (_type_, optional): to this date. Defaults to datetime.today().strftime('%Y-%m-%d').

        Returns:
            pd.DataFrame: containing the content of tweets
        """
        tweets = []
        for i, tweet in enumerate(
            sntwitter.TwitterSearchScraper(
                "{} since:{} until:{}".format(phrase, from_t, to_t)
            ).get_items()
        ):
            if i > num:
                break
            tweets.append([tweet.date, tweet.id, tweet.content])

        df = pd.DataFrame(tweets, columns=["Datetime", "Tweet Id", "Text"])

        return df
