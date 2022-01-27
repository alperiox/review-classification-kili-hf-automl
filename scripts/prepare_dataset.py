import argparse
import os

import pandas as pd
from dotenv import load_dotenv
from kili.client import Kili

load_dotenv()

parser = argparse.ArgumentParser()
parser.add_argument('--output_name',
                    required=True,
                    type=str,
                    default='dataset.csv')
parser.add_argument('--remove', required=False, type=str)
args = vars(parser.parse_args())

API_KEY = os.getenv('KILI_API_KEY')
dataset_path = '..\data\processed\lowercase_cleaned_dataset.csv'
output_path = os.path.join('..\data\processed', args['output_name'])


def extract_labels(labels_dict):
    response = labels_dict[-1]  # pick the latest version of the sample
    label_job_dict = response['jsonResponse']['JOB_0']
    categories = label_job_dict['categories']
    # all samples have a label, we can just pick it by its index
    label = categories[0]['name']
    return label


kili = Kili(API_KEY)
print('Authenticated!')
# query will return a list that contains matched elements (projects in this case)
# since we have only one project with this name, we can just pick the first index
project = kili.projects(
    search_query='User review dataset for topic classification')[0]
project_id = project['id']

# we can customize the returned fields
# the fields below are pretty much enough,
# labels.jsonResponse carries the labeling data
returned_fields = [
    'id', 'externalId', 'labels.jsonResponse', 'skipped', 'status'
]
# I read the raw dataset too in order to match the samples with externalId
dataset = pd.read_csv(dataset_path)

# we can fetch the data as a dataframe
df = kili.assets(project_id=project_id,
                 status_in=['LABELED', 'REVIEWED'],
                 fields=returned_fields,
                 format='pandas')

print('Got the samples!')

# we will pass the skipped samples
df_ns = df[~df['skipped']].copy()

# extract the labeled samples
df_ns.loc[:, 'label'] = df_ns['labels'].apply(extract_labels)
# The externalId column is returned as string, let’s convert it to integer
# to use as indices
df_ns.loc[:, 'content'] = dataset.loc[df_ns.externalId.astype(int), 'content']

# we can drop the `labels` column now
df_ns = df_ns.drop(columns=['labels'])

# we'll remove the multi-labeled samples
df_ns = df_ns[df_ns['label'] != 'MULTI_LABEL'].copy()

# also remove the samples with label specified in remove argument if it's given
if args['remove']:
    df_ns = df_ns.drop(index=df_ns[df_ns['label'] == args['remove']].index)

print('DATA FETCHING DONE')
print('DATASET HAS %d SAMPLES' % (len(df_ns)))
print('SAVING THE PROCESSED DATASET TO: %s' % os.path.abspath(output_path))

df_ns.to_csv(output_path, index=False)

print('DONE!')
