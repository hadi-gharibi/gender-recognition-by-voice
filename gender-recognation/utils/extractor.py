import os, sys, tarfile

if __name__ == '__main__':
    tar_path = os.getcwd()+'/../data/tar'
    raw_path = os.getcwd()+'/../data/raw'
    if not os.path.exists(raw_path) : os.mkdir(raw_path)
    files = os.listdir(os.getcwd()+'/../data/tar')

    for file in files:
        tar = tarfile.open(tar_path+'/' + file)
        tar.extractall(raw_path+'/' + file)
        tar.close()




