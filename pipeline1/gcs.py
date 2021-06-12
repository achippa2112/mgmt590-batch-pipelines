from google.cloud import storage
import os
import python_pachyderm

# creating a GCS client
client = storage.Client()

bucket = client.get_bucket('gcsrestapi')

for filecsv in client.list_blobs('gcsrestapi'):
    blob = bucket.blob(filecsv.name)
    blob.download_to_filename(os.path.join("/pfs/images",filecsv.name))
    
