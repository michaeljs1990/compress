"""
This file is a general purpose utility file. If the set of
functions being stored here grows to a large enough size it
should likely be split up into multiple files that makes it
more clear what you actual want you are actually including.
"""
import yaml

def fetch_yaml_file(file_name):
    """
    Load yaml from disk given a file name and
    turn it into a python dict for manipulation

    Keyword arguments:
        file_name -- file name to fetch yaml from
    """
    file_stream = open(file_name, "r")
    return read_config(file_stream)

def read_config(content):
    """
    Load yaml file into memory

    Keyword arguments:
        content -- dict containing all CLI flags
    """
    return yaml.safe_load(content)

def write_yaml_file(file_name, yaml_struct):
    """
    write output of yaml_struct to a file on disk

    Keyword arguments:
        file_name -- name of file to write to
        yaml_struct -- yaml structure to be written
    """
    file_stream = open(file_name, "w")
    return write_config(yaml_struct, file_stream)

def write_config(yaml_struct, target):
    """
    Write out config to target

    Keyword arguments:
        yaml_struct -- yaml structure to be written
        target -- stream to file on disk
    """
    yaml.dump(
        yaml_struct,
        stream=target,
        indent=4,
        width=80,
        default_flow_style=False)
