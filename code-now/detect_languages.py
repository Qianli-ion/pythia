"""Detect paper's language and create language labels for all papers in S2AG dataset
"""
from langdetect import detect
from glob import glob
import jsonlines
import pickle
from tqdm import tqdm
import os
from joblib import Parallel, delayed
#------------------ Load paper title ---------------------
# Directory definition
S2AG_FOLDER = '/home/qianli/Research/literature-discovery/data/S2AG-dataset/2022-12-27/'
PAPERS_FOLDER = f'{S2AG_FOLDER}papers/'
OUTPUT_PKL_DIR = S2AG_FOLDER+'language/'

# Load all jsonl files
papers_jsonl_list = sorted(glob(PAPERS_FOLDER+'*.jsonl'))

def detect_language(this_papers_jsonl):
    id_lan_dict = {}    # dictionary saving paper language, {corpusid: language}
    en_num = 0          # total number of English entries

    print(f'Loading {this_papers_jsonl} ...')
    jsonl_idx = os.path.basename(this_papers_jsonl)[:-6]
    # breakpoint()
    with jsonlines.open(this_papers_jsonl) as reader:
        for paper in tqdm(reader.iter()):
            corpusid = paper['corpusid']
            title = paper['title']
            try:                            # try language detection
                language = detect(title)
            except:                         # save failed status
                language = 'failed'
            id_lan_dict[corpusid] = language
            if language == 'en':
                en_num += 1
    print(f'Completed. # of English entries = {en_num}')
    print(f'Total {len(id_lan_dict)} entries in dataset. {en_num} English entries found.')

    # save the language dictionary as pickle file
    output_pkl_file_dir = f'{OUTPUT_PKL_DIR}{jsonl_idx}.pkl'
    os.makedirs(os.path.dirname(output_pkl_file_dir),exist_ok=True)
    with open(output_pkl_file_dir,'wb') as f:
        pickle.dump(id_lan_dict,f)
    print(f'Output saved at {output_pkl_file_dir}')

# Run language detection in parallel
Parallel(n_jobs=6)(delayed(detect_language)(this_papers_jsonl) for this_papers_jsonl in papers_jsonl_list[1:])



