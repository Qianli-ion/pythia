"""
testing semantic scholar's API for the dataset downloading purpose
For training purpose, 2022-12-27 release of the S2AG dataset will be used
"""
import os
import requests
import urllib.request
from utils import show_progress
import progressbar

# get semantic scholar API key
s2_api_key = os.getenv("S2_API_KEY")
# target dataset info
target_release = '2022-12-27'
target_dataset_names_list = ['papers','citations','abstracts']



pbar = None
def show_progress(block_num, block_size, total_size):
    global pbar
    if pbar is None:
        pbar = progressbar.ProgressBar(maxval=total_size)
        pbar.start()

    downloaded = block_num * block_size
    if downloaded < total_size:
        pbar.update(downloaded)
    else:
        pbar.finish()
        pbar = None

# get list of dataset releases
response = requests.get("https://api.semanticscholar.org/datasets/v1/release/")
if response.ok:
    print(f'Dataset Release retrivel successful.')
    print(response.json())
    
    # sanity check: if the target release is still avaliable in the dataset. if yes, use it. 
    if target_release in response.json():
        release_id = target_release
    else:
        print(f'target release: {target_release} is no longer avaliable in S2AG dataset')
        assert(False)


# get datasets for the release
response = requests.get(f"https://api.semanticscholar.org/datasets/v1/release/{release_id}")
if response.ok:
    print(f'Dataset information retrivel successful.')
    print(response.json())
    
    # print list of datasets names
    print(f'Avaliable dataset names are:')
    dataset_names_list = [s['name'] for s in response.json()['datasets']]
    print(dataset_names_list)
    
    # sanity check: if the target dataset name is still avaliable in the release.
    for target_dataset_name in target_dataset_names_list:
        if target_dataset_name not in dataset_names_list:
            print(f'target dataset name: {target_dataset_name} is no longer avaliable inrelease {release_id}')
            assert(False)


# get dataset downloading link - this step needs API key
headers = {"x-api-key" : s2_api_key}
for dataset_name in target_dataset_names_list:
    response = requests.get(f"https://api.semanticscholar.org/datasets/v1/release/{release_id}/dataset/{dataset_name}", headers=headers)    
    save_dir = f'../../data/S2AG-dataset/{release_id}/{dataset_name}/'   
    os.makedirs(save_dir,exist_ok=True) 
    
    if response.ok:
        print('Request successful.')
        print(f"dataset: {response.json()['name']}")
        
        # download all the files for the dataset
        files = response.json()['files']
        print(f'Number of files to download: {len(files)}')
        for idx, file in enumerate(files):
            urllib.request.urlretrieve(file, f"{save_dir}/{idx}.jsonl.gz", reporthook=show_progress)