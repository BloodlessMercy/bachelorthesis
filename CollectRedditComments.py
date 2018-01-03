import praw
import pprint
import csv
import nltk

nltk.data.path.append('/srv/sentiment/nltk_data/')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
sid = SentimentIntensityAnalyzer()

fieldnames = [
    'type',
    'id',
    'author',
    'author_flair_css_class',
    'score',
    'ups',
    'downs',
    'positivity',
    'neutrality',
    'negativity',
    'compound_emotion',
    'controversiality',
    'created',
    'gilded',
    'edited',
    'is_submitter',
    'stickied',
    'depth',
    'body'
]


csvWriter = csv.DictWriter(
    open("C:\\Users\\m.vanwinsum\\PycharmProjects\\BachelorThesis\\comments_from_2013_till_20171.csv", 'wb'),
    fieldnames=fieldnames,
    delimiter=";"
)

csvWriter.writeheader()

pprinter = pprint.PrettyPrinter(indent=4)
reddit = praw.Reddit(client_id='MgakeFs_B-JFEQ',
                     client_secret='4dmbLF498Qiq6M0GNoMCxckIX9M',
                     password='Stefano12',
                     user_agent='script:bachelorthesis 0.1 by /u/NameIzSecret',
                     username='NameIzSecret')


def encode_dictionary(comment_to_be_encoded, type):
    ss = sid.polarity_scores(comment_to_be_encoded.body.replace('\n', '').encode('utf-8', 'ignore'))
    encodedCommentInformation = {
        'type': type,
        'author': comment_to_be_encoded.author.name.encode('utf-8') or "[deleted]",
        'author_flair_css_class': comment_to_be_encoded.author_flair_css_class or "[deleted]",
        'body': comment_to_be_encoded.body.replace('\n', '').encode('utf-8') or "[deleted]",
        'id':comment_to_be_encoded.id.encode('utf-8'),
        'gilded': comment_to_be_encoded.gilded,
        'ups': comment_to_be_encoded.ups,
        'score': comment_to_be_encoded.score,
        'downs': comment_to_be_encoded.downs,
        'positivity': ss['pos'],
        'neutrality': ss['neu'],
        'negativity': ss['neg'],
        'compound_emotion': ss['compound'],
        'edited': comment_to_be_encoded.edited,
        'is_submitter': comment_to_be_encoded.is_submitter,
        'stickied': comment_to_be_encoded.stickied,
        'created': comment_to_be_encoded.created,
        'controversiality': comment_to_be_encoded.controversiality,
        'depth': comment_to_be_encoded.depth
    }
    return encodedCommentInformation


lolsubreddit = reddit.subreddit('leagueoflegends')


for submission in lolsubreddit.submissions(1356998400, 1513636317):
    if submission.score > 300:
        submission.comments.replace_more(limit=0)
        for comment in submission.comments.list():
            if hasattr(comment, 'author_flair_css_class'):
                if comment.author_flair_css_class == 'riot':
                    print(submission.title)
                    parentComment = comment.parent()
                    while True:
                        if parentComment.id == submission.id:
                            break
                        else:
                            pprinter.pprint(parentComment)
                            if not parentComment.author:
                                break
                            csvWriter.writerow(
                                encode_dictionary(parentComment, 'parent')
                            )
                            parentComment = parentComment.parent()
                    for reply in comment.replies:
                        if not reply.author:
                            continue
                        pprinter.pprint(reply)
                        csvWriter.writerow(
                            encode_dictionary(reply, 'child')
                        )
                    if not comment.author:
                        continue
                    pprinter.pprint(comment)
                    csvWriter.writerow(
                        encode_dictionary(comment, 'riot')
                    )

# Now: 1512067788
# Last Month: 1506723479
# One week ago: 1508716799
# Three days ago: 1511740800
# Yesterday: 1511913600
