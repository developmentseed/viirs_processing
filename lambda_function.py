import parallel_wget
import tif_stats
import boto3
import json
import os

client = boto3.client('s3')

def remove_files(files=[], suffix=None):
  if suffix is not None:
    files.extend([os.path.join(os.getcwd(), f) for f in os.listdir('.') if os.path.isfile(f) and f.endswith(suffix)])
  map(os.remove, files)

def lambda_handler(event, context):
    config = event['config']
    # Return a list of files
    try:
        parallel_wget.parallel_wget(
           host=config['provider']['host'],
           path=config['collection']['provider_path'],
           files=event['input']
        )
        # Return csv file names
        stats_files = tif_stats.generate_stats()
        # Upload to S3
        dest_bucket = config['buckets']['protected']
        file_prefix = 'sezu-stats/'
        for file in  stats_files:
          res = client.put_object(
            Bucket = dest_bucket,
            Key = '{0}{1}'.format(file_prefix, file),
            Body = open(file, 'r').read())
        # Remove any extra files, to save space
        remove_files([], '.tif')
        remove_files(stats_files, None)
    except Exception as err:
        print('caught error:')
        print(err)
    print('processing complete')
    return {'messsage': 'processing complete'}
