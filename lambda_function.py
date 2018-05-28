import parallel_wget
import tif_stats

def lambda_handler(event, context):
    config = event['config']
    parallel_wget.parallel_wget(
       host=config['provider']['host'],
       path=config['collection']['provider_path'],
       files=event['input']
    )
    tif_stats.generate_stats()
    return {'messsage': 'processing complete'}
