"""
Include and merge docker-compose configurations into a single file.
Given a docker-compose.yml file, fetch each configuration in the include
section and merge it into a base docker-compose.yml. If any of the included
files have include sections continue to fetch and merge each of them until
there are no more files to include.
"""
import os

from compress.logger import Logger
from compress.utils import fetch_yaml_file, write_yaml_file
from compress.extend import ExtendYaml

class GenerateCommand(object):
    """
    Read in the .compress.yml config file and generate a combined
    file based on the input files.
    """

    def __init__(self, args):
        """
        Keyword arguments:
            args -- dict containing all CLI flags
        """
        self.compress_file = args.get('FILE_IN')
        self.base_dir = ""
        if self.compress_file == None:
            self.compress_file = ".compress.yml"
        else:
            self.base_dir = os.path.dirname(self.compress_file) + "/"
            # Make check for case where the file is relative
            if self.base_dir == "/":
                self.base_dir = ""

    def run(self):
        """
        Method to facilitate the generate command and tie in
        classes such as extend which allow further manipulation
        of the object.
        """
        compress_config = fetch_yaml_file(self.compress_file)
        include_files = self.load_imports(compress_config)
        extended_file = ExtendYaml(include_files, compress_config).parse()
        write_yaml_file(self.base_dir + "docker-compose.gen.yml", extended_file)
        Logger.info("docker-compose.gen.yml file generated")


    def load_imports(self, config_yaml):
        """
        Load yaml files that are listed in the import
        section of the provided compress file.

        Keyword arguments:
            config_yaml -- yaml structure of .compress.yml file
        """
        include_files = dict()
        for include in config_yaml['include']:
            Logger.info("Including %s", include)
            yaml_file = fetch_yaml_file(self.base_dir + include)
            altered_yaml = self.alter_pathing(yaml_file, include)
            # TODO: Will need to be smarter about merging in the
            # future so we don't lose properties when merging
            # parent yaml blocks with child yaml blocks.
            for key, value in altered_yaml.items():
                include_files[key] = value
        return include_files

    def alter_pathing(self, include_yaml, include_file):
        """
        Alter the pathing of specific docker compose file
        properties. Currently the following are manipulated
        when a file not located at the same directory level
        as the .compress.yml file is passed into this function.

            - [x] build
            - [o] env_file
            - [x] extends.file
            - [x] volumes

        Keyword arguments:
            include_yaml -- yaml structure of included file
                            listed in the .compress.yml file
            include_file -- file name or path of included file
        """
        include_path = os.path.dirname(include_file)
        return_yaml = include_yaml.copy()
        if include_path != "":
            return_yaml = self.recurse_yaml(include_yaml, include_path)
        return return_yaml

    def recurse_yaml(self, yaml_struct, include_path):
        """
        Traverse all yaml that is passed in via yaml_struct
        recursively and manipulate the properties listed in
        the method def for alter_pathing. If anyone knows a
        better way to do this please let me know. I am also
        close to certain this will fail on some edge case.

        Keyword arguments:
            yaml_struct -- yaml that has been converted to
                            a python dict or list
            include_path -- path of the file this yaml structure
                            was retrieved from.
        """
        transformed_yaml = yaml_struct.copy()

        for key, value in transformed_yaml.items():
            nested_yaml = transformed_yaml[key]
            transformed_yaml[key] = self.alter_property(key, value, include_path)
            if nested_yaml.__class__ is dict:
                transformed_yaml[key] = self.recurse_yaml(nested_yaml, include_path)
            elif nested_yaml.__class__ is list:
                for index in nested_yaml:
                    if index.__class__ is dict:
                        transformed_yaml[key][index] = self.recurse_yaml(index, include_path)

        return transformed_yaml

    def alter_property(self, key, value, include_path):
        """
        Check if the given key needs to be changed. If
        it does change the value according to the
        include_path and return the new value.

        Keyword arguments:
            key -- yaml property key
            value -- yaml property value
            include_path -- path of the file that is currently
                            being included
        """
        altered_value = value

        if(key == "file" or
           key == "build"):
            altered_value = include_path + "/" + value
        elif key == "volumes":
            altered_value = self.alter_volumes(value, include_path)

        return altered_value

    @staticmethod
    def alter_volumes(yaml_list, include_path):
        """
        Change the volumes if they are not absolute paths

        Keyword arguments:
            yaml_list -- yaml list of volumes
            include_path -- path of the file that is currently
                            being included
        """
        altered_list = list(yaml_list)

        for key, value in enumerate(yaml_list):
            if value[0] != "/":
                altered_list[key] = include_path + "/" + value

        return altered_list
