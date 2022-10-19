from bs4 import BeautifulSoup
import codecs
import os
from distutils.dir_util import copy_tree
import re
import sys


def iterate_folders(folder_path, list_of_f, flag):
    """
    Iterates through folder and returns a list of:
    * (if flag == 'F') files in the current folder and files in all subfolders
    OR
    * (if flag == 'D') folders (directories) only on the current level, without going through subfolders
    """
    if flag == 'F':
        dir_files = os.listdir(folder_path)
        full_paths = map(lambda name: os.path.join(folder_path, name), dir_files)
        for f in full_paths:
            if os.path.isfile(f):
                list_of_f.append(f)
            else:
                iterate_folders(f, list_of_f, flag='F')
        return list_of_f
    elif flag == 'D':
        dir_files = os.listdir(folder_path)
        full_paths = map(lambda name: os.path.join(folder_path, name), dir_files)
        for f in full_paths:
            if os.path.isdir(f):
                list_of_f.append(f)
        return list_of_f


def copy_files(src_path, tgt_path):
    print('\nCopying files from Target folder to Processed...')
    copy_tree(src_path, tgt_path)


def clean_folder(processed_folder):
    file_list = []
    file_list = iterate_folders(processed_folder, file_list, flag='F')
    for f in file_list:
        os.remove(f)
    print('\nProcessed folder cleared')


def parse_to_list(htm):
    """
    Parses html file tags to list with BeautifulSoup package
    """
    with codecs.open(htm, 'r', 'utf-8') as fp:
        soup = BeautifulSoup(fp, 'xml')
    parsed_list = [tag.name for tag in soup.find_all()]
    return parsed_list


def replace_tags(target_file, dictionary):
    """
    Replaces tags in target translation using matching glossary
    Also, performs additional replacements with regular expressions
    """
    with codecs.open(target_file, 'r+', 'utf-8') as file:
        result = (file.read())
        for key, value in dictionary.items():
            result = result.replace(value, key)
            result = re.sub(r'<(\w+)></\1>', r'<\1 />', result, flags=re.IGNORECASE)
            result = re.sub(r'enctoken=', r'encToken=', result)
            #result = re.sub(r'<br>', r'<br />', result)
            result = re.sub(r'(<img[^>]*)(?<!/)>', r'\1 />', result)
            result = re.sub(r'(</?)standardMetadata', r'\1StandardMetadata', result)
        file.seek(0)
        file.write(result)
        file.truncate()
        print('Done')


if __name__ == "__main__":

    if len(sys.argv) < 4:
        sys.exit('Three arguments required: <PATH TO SOURCE FILES> <PATH TO TARGET FILES> <PATH TO PUT PROCESSED FILES>')

    source = sys.argv[1]
    target = sys.argv[2]
    processed = sys.argv[3]
    source_files = []
    processed_files = []

    clean_folder(processed)
    copy_files(target, processed)

    source_files = iterate_folders(source, source_files, flag='F')
    print('\nSource files found:\n', '\n'.join(source_files))

    processed_files = iterate_folders(processed, processed_files, flag='F')
    print('\nTranslations found:\n', '\n'.join(processed_files))

    for i in source_files:
        print('\nFor source file:', i)
        source_tags = parse_to_list(i)
        for j in processed_files:
            relative_name = os.path.basename(i[0:-5]) # removes full path and '.html' extension from filename
            if relative_name not in j:                # condition to skip unused files
                continue
            print('Start processing translation:', j)
            tag_pairs = {}
            target_tags = parse_to_list(j)
            for x, y in zip(source_tags, target_tags): # fills dictionary with 2 list of tags
                tag_pairs[x] = y
            replace_tags(j, tag_pairs)
