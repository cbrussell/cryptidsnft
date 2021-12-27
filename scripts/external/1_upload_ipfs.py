import os
from pathlib import Path 
import ipfshttpclient
import fnmatch

image_path = Path(__file__).resolve().parents[2] / "assets/images/"
image_list = fnmatch.filter(os.listdir(image_path), '*.png')
image_count = len(image_list)

client = ipfshttpclient.connect()

response = client.add(image_path, wrap_with_directory=False, pattern='*.png')
ipfs_hash_directory = response[image_count]['Hash']

base_url = 'https://ipfs.io/ipfs/'
final_url = base_url + ipfs_hash_directory
print(f" \nIPFS image directory CID is: {ipfs_hash_directory}\n")
print(f" \nGo to folder: {final_url}\n")




