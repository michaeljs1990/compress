"""
This class manages parsing an already compressed file
and extending the parts that have been specified inside
the config file. You can't run this command on it's own
currently but it is instead called from inside the generate
command. Keeping this in it's own class makes it easy to
maintain as new features are added.
"""

class ExtendYaml(object):
    """
    Extend class impliments the functionality that
    can be found when using the extend property in
    the .compress.yml file.
    """

    def __init__(self, yaml_struct, config_yaml):
        """
        Don't fail if extend is not set. This is an
        implimentation detail of generate since the
        use of extend may not always be needed.

        Keyword arguments:
            yaml_struct -- struct of yaml file
            config_yaml -- .compress.yml config file
        """
        self.yaml_struct = yaml_struct
        self.extend_yaml = None
        if 'extend' in config_yaml:
            self.extend_yaml = config_yaml['extend']

    def parse(self):
        """
        Look through self.yaml_struct and replace or
        add values that are defined in self.extend_yaml
        """
        parsed_yaml = self.yaml_struct.copy()

        if self.extend_yaml != None:
            for key, value in self.extend_yaml.items():
                parsed_yaml[key] = self.alter_yaml(key, value)

        return parsed_yaml

    def alter_yaml(self, yaml_key, yaml_value):
        """
        given the yaml key and value this method
        updates the python dict with the value
        found inside the .compress.yml file.

        Keyword arguments:
            yaml_key -- key in dict generated from yaml file
            yaml_value -- value in dict generated from yaml file
        """
        altered_yaml = self.yaml_struct[yaml_key].copy()
        # Special care must be taken for merging links so as
        # to not drop other links. If this grows in popularity we
        # will have to see if this is what users expect or if
        # we need something a little more fancy.
        if('links' in altered_yaml and
           'links' in yaml_value and
           yaml_value['links'].__class__ is list and
           altered_yaml['links'].__class__ is list):
            yaml_value['links'] = altered_yaml['links'] + yaml_value['links']

        altered_yaml.update(yaml_value)

        return altered_yaml
