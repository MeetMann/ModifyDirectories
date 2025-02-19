import os
import json
import shutil
from subprocess import PIPE, run
import sys

GAME_DIR_PATTERN = "game"
mappings = {}

def save_mappings(mappings , filename = "mappings.json"):
    with open(filename, "w") as f: 
        json.dump(mappings, f)

def get_mappings(filename = "mappings.json"):
    if (os.path.exists(filename)):
        with open(filename, "r") as f:
            return json.load(f)
    return {}

def find_all_game_paths(source):
    game_paths = []

    for root, dirs, files in os.walk(source):
        for directory in dirs:
            if GAME_DIR_PATTERN in directory:
                path = os.path.join(source, directory)
                game_paths.append(path)
        break

    return game_paths


def remove_part_of_paths(paths, remove_this):
    new_names = []

    for path in paths:
        _, dir_name = os.path.split(path)
        new_dir_name = dir_name.replace(remove_this, "")
        if new_dir_name[-1] == "_":
            new_dir_name = new_dir_name[:-1]
        new_names.append(new_dir_name)
    
    return new_names

def move_games_to_new_dir(game_paths, game_dirs, target_path):
    for src, dest in zip(game_paths, game_dirs):
        new_path = os.path.join(target_path, dest)
        mappings[new_path] = src

        if (os.path.exists(new_path)):
            shutil.rmtree(new_path)
        
        shutil.move(src, new_path)
        save_mappings(mappings)

def move_games_back(mappings):
    for src, dest in mappings.items():
        if (os.path.exists(dest)):
            continue
        shutil.move(src, dest)
    os.remove("mappings.json")

def create_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)

def main(source, target):
    cwd = os.getcwd()
    source_path = os.path.join(cwd, source)
    target_path = os.path.join(cwd, target)

    game_paths = find_all_game_paths(source_path)
    new_game_dirs = remove_part_of_paths(game_paths, GAME_DIR_PATTERN)

    create_dir(target_path)

    if (os.path.exists("mappings.json")):
        mappings = get_mappings()
        move_games_back(mappings)
    else:
        move_games_to_new_dir(game_paths, new_game_dirs, target_path)
    

if __name__ == "__main__":
    args = sys.argv

    if len(args) != 3:
        raise Exception("You must pass a source and target directory - no more, no less")
    
    source, target = args[1:]
    main(source, target)


