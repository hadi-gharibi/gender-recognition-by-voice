from lxml import html
import requests
import urllib3
from urllib3.util import Retry
import multiprocessing
from tqdm import tqdm
import os
from pympler import asizeof
import gender_recognation


module_path = os.path.dirname(gender_recognation.__file__)
tar_path = str(os.path.join(module_path, 'data', 'tar'))

def download_file(fname_url, data_path=tar_path):
    main_url, fname = fname_url
    url = main_url + fname
    file_path = data_path + '/' + fname
    if not os.path.exists(file_path):
        while 1:
            http = urllib3.PoolManager(retries=Retry(connect=3, read=2, redirect=3))
            response = http.request("GET", url)
            if asizeof.asizeof(response.data)/1024 > 1: break
        with open(file_path, 'wb') as out_file:
            out_file.write(response.data)


if __name__ == '__main__':
    main_url = 'http://www.repository.voxforge1.org/downloads/SpeechCorpus/Trunk/Audio/Main/16kHz_16bit/'
    data_path = tar_path
    if not os.path.exists(data_path): os.makedirs(data_path)

    page = requests.get(main_url)
    webpage = html.fromstring(page.content)
    dl_url_list = [(main_url,url) for url in webpage.xpath('//a/@href') if '.tgz' in url]

    pool = multiprocessing.Pool(processes=12)
    with tqdm(total=len(dl_url_list)) as progress_bar:
        for _ in pool.imap_unordered(download_file, dl_url_list):
            progress_bar.update(1)

'''
main_url = 'http://www.repository.voxforge1.org/downloads/SpeechCorpus/Trunk/Audio/Main/16kHz_16bit/'
page = requests.get(main_url)
webpage = html.fromstring(page.content)
dl_url_list = [(main_url,url) for url in webpage.xpath('//a/@href') if '.tgz' in url][0]
download_file(dl_url_list)
'''
