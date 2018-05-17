import parallel_wget

def lambda_handler(event, context):
    config = event['config']
    parallel_wget.parallel_wget(
       host=config['provider']['host'],
       path=config['collection']['provider_path'],
       files=event['input']
    )
    return {'messsage': 'files downloaded'}
