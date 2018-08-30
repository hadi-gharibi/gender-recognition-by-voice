import os,gender_recognation, tarfile


if __name__ == '__main__':
    module_path = os.path.dirname(gender_recognation.__file__)
    tar_path = os.path.join(module_path, 'data', 'tar')
    raw_path = os.path.join(module_path, 'data', 'raw')
    if not os.path.exists(raw_path): os.mkdir(raw_path)
    files = os.listdir(tar_path)

    for file in files:
        tar = tarfile.open(tar_path+'/' + file)
        tar.extractall(raw_path+'/' + file)
        tar.close()
