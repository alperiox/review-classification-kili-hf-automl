from google_play_scraper import Sort, reviews, reviews_all
import pandas as pd
from datetime import datetime
import argparse

ap = argparse.ArgumentParser()
ap.add_argument('-l',
                '--lang',
                type=str,
                default='en',
                required=False,
                help='the language reviews are written in')
ap.add_argument('-c',
                '--country',
                type=str,
                default='us',
                required=False,
                help='specific country to get the reviews')
ap.add_argument('-n',
                '--name',
                type=str,
                required=True,
                help='package name of the app, ex: com.medium.reader')
ap.add_argument(
    '-co',
    '--count',
    type=str,
    required=False,
    help='number of reviews to gather, `all` for every review. default: 10',
    default='10')

ap.add_argument(
    '-f',
    '--filter',
    type=int,
    required=False,
    help=
    'integer to filter the reviews by rating. None for all ratings, default: None',
    default=None)

args = vars(ap.parse_args())

fetcher_args = dict(lang=args['lang'],
                    country=args['country'],
                    filter_score_with=args['filter'])
fetcher_args[
    'filter_score_with'] = args['filter'] if args['filter'] != None else None

if args['count'] == 'all':
    result = reviews_all(args['name'], **fetcher_args)
else:
    fetcher_args['count'] = int(args['count'])
    result, token = reviews(args['name'], **fetcher_args)

df = pd.DataFrame(result)
date = datetime.now()
df_name = args['name'].replace('.', '-') + '_' + str(
    date.strftime('%Y%m%d-%H-%M')) + '.csv'
df.to_csv(df_name, index=None)
print('Saved the data as %s' % df_name)
