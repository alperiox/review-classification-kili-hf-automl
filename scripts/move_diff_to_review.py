'''
Sets the distinct elements of two datasets to be reviewed
'''

from kili.client import Kili
from dotenv import load_dotenv
import os
import argparse

import pandas as pd

load_dotenv()

parser = argparse.ArgumentParser()
parser.add_argument('--first',
                    required=True,
                    type=str,
                    help='Path to first dataframe')
parser.add_argument('--second',
                    required=True,
                    type=str,
                    help='Path to second dataframe')

args = vars(parser.parse_args())

# set the kili connection up
API_KEY = os.getenv('KILI_API_KEY')
kili = Kili(API_KEY)

# read dataframes
df1 = pd.read_csv(args['first'])
df2 = pd.read_csv(args['second'])

# concating two of them should let us have duplicates of common elements
# then we can drop the duplicated elements without keeping any duplicates to get the different elements across the two dataframes
diff_df = pd.concat((df1, df2)).drop_duplicates(keep=False)
diff_ids = diff_df['id'].to_list()

kili.update_properties_in_assets(diff_ids,
                                 status_array=['TO_REVIEW'] * len(diff_ids))

print('SET %d ENTRIES TO BE REVIEWED!' % len(diff_df))
