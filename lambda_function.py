import parallel_wget
import tif_stats
import boto3
import os

client = boto3.client('s3')

def lambda_handler(event, context):
    config = event['config']
    # Return a list of files
    extracted_files = parallel_wget.parallel_wget(
       host=config['provider']['host'],
       path=config['collection']['provider_path'],
       files=event['input']
    )
    # Return csv file names
    stats_files = tif_stats.generate_stats()
    # Upload to S3
    dest_bucket = config['buckets']['protected']
    file_prefix = 'sezu-stats/'
    map(lambda f: client.put_object(
      Bucket = dest_bucket,
      Key = '{0}{1}'.format(file_prefix, f),
      Body = open(f, 'r').read())
    , stats_files)
    # Delete all files
    map(os.remove, extracted_files)
    return {'messsage': 'processing complete'}
