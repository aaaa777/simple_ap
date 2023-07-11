import feedparser
import pandas
import django
django.setup()
from activitypub.models import Account, Note

pandas.set_option('display.max_columns', 500)

def get_feeds_from_url(url):
    feed = feedparser.parse(url)
    # print(feed)
    return pandas.DataFrame(feed.entries)

def get_new_feeds(account):
    feeds = get_feeds_from_url(account.feed_url)
    # print(feeds)
    note_ids = Note.objects.filter(account=account).values_list('url', flat=True)
    print(list(note_ids))
    print(feeds[~feeds['link'].isin(list(note_ids))])
    return feeds[~feeds['link'].isin(list(note_ids))]

def run():
    accounts = Account.objects.all()
    for account in accounts:
        new_feeds = get_new_feeds(account)
        if not new_feeds.empty:
            for key, row in new_feeds.iterrows():
                note = Note(account=account, content=row['title'], url=row['link'])
                note.save()
                print('new feed:'+row['title'])
                note.post()
