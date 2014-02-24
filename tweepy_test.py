import tweepy
import time
from getpass import getpass
from textwrap import TextWrapper

consumer_key = '5N6WnewfTr4TXiMNe7qqA'
consumer_secret = 'sF7duztDHCwtH3eeCsuAqQEp8GzqpnJp7S9UyndpKgA'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

access_token = '2321411072-yifWz3g7X3pleFo5WAz7F2oBie6a4U6CDojDtZJ'
access_secret = 'VlE0NzNaob6qCYbcLJNg6D93LSi4seX9eD7GSyEdmeYWb'

auth.set_access_token(access_token, access_secret)


api = tweepy.API(auth)

user = api.me()

#print api.friends_timeline()

class StreamWatcherListener(tweepy.StreamListener):

    status_wrapper = TextWrapper(width=60, initial_indent='    ', subsequent_indent='    ')

    def on_status(self, status):
        try:
            print self.status_wrapper.fill(status.text)
            print '\n %s  %s  via %s\n' % (status.author.screen_name, status.created_at, status.source)
            with open("sample_from_tweepy.txt", "a") as file:
                file.write(status.text + '\n')
        except:
            # Catch any unicode errors while printing to console
            # and just ignore them to avoid breaking application.
            pass

    def on_error(self, status_code):
        print 'An error has occured! Status code = %s' % status_code
        return True  # keep stream alive

    def on_timeout(self):
        print 'Snoozing Zzzzzz'



def main():
    # Prompt for login credentials and setup stream object
    stream = tweepy.Stream(auth, StreamWatcherListener(), timeout=10)

    # Prompt for mode of streaming
    valid_modes = ['sample', 'filter']
    while True:
        mode = raw_input('Mode? [sample/filter] ')
        if mode in valid_modes:
            break
        print 'Invalid mode! Try again.'

    if mode == 'sample':
        stream.sample()

    elif mode == 'filter':
        follow_list = raw_input('Users to follow (comma separated): ').strip()
        track_list = raw_input('Keywords to track (comma seperated): ').strip()
        if follow_list:
            follow_list = [u for u in follow_list.split(',')]
        else:
            follow_list = None
        if track_list:
            track_list = [k for k in track_list.split(',')]
        else:
            track_list = None

        stream.filter(follow_list, track_list)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print '\nGoodbye!'