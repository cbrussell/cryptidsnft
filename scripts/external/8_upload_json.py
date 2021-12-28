import os
from pathlib import Path 
import ipfshttpclient
import fnmatch
from pinatapy import PinataPy

# IPFS Daemon must be running

# Function will upload json directory to IPFS then pin file to Pinata

# Only do this with test - not ALL files, or final images.

json_path = Path(__file__).resolve().parents[2] / "assets/shifted_json/"
json_list = fnmatch.filter(os.listdir(json_path), '*.json')
json_count = len(json_list)

client = ipfshttpclient.connect()

response = client.add(json_path, wrap_with_directory=False, pattern='*.json')
ipfs_hash_directory = response[json_count]['Hash']

base_url = 'https://ipfs.io/ipfs/'
final_url = base_url + ipfs_hash_directory
print(f" \nIPFS json directory CID is: {ipfs_hash_directory}\n")
print(f" \nGo to folder: {final_url}\n")

api_key = os.environ.get("PINATA_API_KEY")
secret_key = os.environ.get("PINATA_SECRET_API_KEY")
if api_key and secret_key:
    pinata = PinataPy(api_key, secret_key)
else:
    raise ValueError("No API keys in environment variables")

response = pinata.pin_hash_to_ipfs(ipfs_hash_directory, "Json")

print(response)









