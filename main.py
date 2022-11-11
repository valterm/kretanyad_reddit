import praw
import json
from random import randint
import logging


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def get_config() -> dict:
    f = open('./config.json','r')
    creds = json.loads(f.read())
    f.close()
    return(creds)

def get_random_insult() -> str:
    f = open('./dirty.json', 'r')
    json_data = json.loads(f.read())
    max_n = len(json_data['DirtyWords'])
    n = randint(0, max_n-1)
    f.close()

    return(json_data['DirtyWords'][n].lower())

def is_processed(comment: praw.models.reddit.comment.Comment) -> bool:
    f = open('./replied_to.json','r')
    l = json.loads(f.read())
    f.close()
    for c in l:
        if c == comment.id:
            return True
    
    return False

def append_comment(comment: praw.models.reddit.comment.Comment):
    f = open('./replied_to.json','r')
    l = json.loads(f.read())
    f.close()

    l.append(comment.id)
    f = open('./replied_to.json','w')
    f.write(json.dumps(l))
    return 0


def main():
    config = get_config()
    reddit = praw.Reddit(
        client_id=config['client_id'],
        client_secret=config['client_secret'],
        username=config['username'],
        password=config['password'],
        user_agent=config['user_agent']
    )

    subreddit = reddit.subreddit(config['sub'])
    
    for comment in subreddit.stream.comments():
        if not is_processed(comment):
            print(comment)
            if "/u/szolj_be_kreta_bot" in comment.body:
                author = comment.author.name
                if author != 'szolj_be_kretaa_bot':
                    insult = get_random_insult()
                    message = f"/u/{author}, te kis {insult}."
                    comment.reply(
                        body=message
                    )
                    print(message)
                    append_comment(comment)


if __name__ == "__main__":
    main()