from os import listdir

def listdir_exclude(path, exclude_list=[]):
    """
    This is the helper function to list
    all the files in the directory: path
    and exclude the exclude list
    - Input:
        path: path for the directory
        exclude_list: exclude the files start with
            entries in exclude_list
    - Return:
        file_list: a list of files that 
        are in the path but not in the exclude
        list. 
    """
    directory_list = []
    for f in listdir(path):
        for exclude in exclude_list:
            if f.startswith(exclude):
                break
        else:
            directory_list.append(f)

    return directory_list

            