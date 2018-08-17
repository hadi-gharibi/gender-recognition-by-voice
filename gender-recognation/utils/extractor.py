import os, sys, tarfile

if __name__ == '__main__':
    files = os.listdir(os.getcwd()+'/../data/tar')
    for file in files:
        tar = tarfile.open(file)
        tar.extractall()
        tar.close()




