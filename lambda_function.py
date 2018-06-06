import parallel_wget
import tif_stats
import boto3
import json
import os

client = boto3.client('s3')

def lambda_handler(event, context):
    print(json.dumps(event, indent=2))
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
        print('storing files')
        print('dest_bucket: {0}'.format(dest_bucket))
        for file in  stats_files:
          res = client.put_object(
            Bucket = dest_bucket,
            Key = '{0}{1}'.format(file_prefix, file),
            Body = open(file, 'r').read())
          print(json.dumps(res, indent=2))
    except Exception as err:
        print('caught error:')
        print(err)
    print('processing complete')
    return {'messsage': 'processing complete'}
