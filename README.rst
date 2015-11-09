# Docker Compress
Using micro services? Have to maintain repos full of docker-compose.yml files to glue everything together? This project allows you to create a simple file that then generates your docker-compose.yml file for you based off of your config file making it so that you don't have to keep track of 10 different files anymore.

#### Install

This package can be installed through pythons trusted pip package manager. Be advised although this is currently in beta and the error warning may not be be the most user friendly. If you run into any issues please create an issue with the full stack trace as well as the command that you ran.

    pip install docker-compress

#### Important Notes

Since the feature set is still in it's early stages this does not work with all docker-compose syntax. The `extend` feature should be avoided although it does work in practice if you have volumes, dockerfile, or build nested inside the file that you are extending the paths will not be updated properly. `env_file` is not supported currently but will be soon I just haven't had time to add it yet and I don't use it often so it's at the back of the list.

#### Example

This is your firsts repo using docker and it contains a docker-compose.yml file that looks like this.

    web:
      container_name: micro-service-one
      build: .
      volumes:
        - .:/src
      ports:
        - 80:80

Repo two also has a docker-compose.yml file. However repo two can't run or even be tested much without the container in repo one

    internal_web:
      container_name: micro-service-two
      build: .
      volumes:
        - .:/src
      ports:
        - 81:81

Both of these files live in the base of each repo.

    .
    ├── micro-one
    │   └── docker-compose.yml
    └── micro-two
        └── docker-compose.yml

In the past you may have a third docker compose file that combines the info that is found in the repositories creating lots of duplicate information. Now you can create a `.compress` file in whatever directory you choose and tell it how the docker-compose.yml file should look. This .compress file would be places at the same level as micro-one and micro-two however you can put it whatever you would like.

    # .compress
    include:
      - micro-one/docker-compose.yml
      - micro-two/docker-compose.yml
    extend:
      web:
        link:
          - internal_web

This would generate a file that looks like so. Docker compress does allow you to make invalid configurations. Use docker-compose to verify what you are doing is correct. This is the only way to reliably test your config.

    web:
      container_name: micro-service-one
      build: .
      volumes:
        - .:/src
      ports:
        - 80:80
      link:
        - internal_web

    internal_web:
      container_name: micro-service-two
      build: .
      volumes:
        - .:/src
      ports:
        - 81:81

Wow! Look at all the information you didn't have to duplicate. Amazing!

#### Development

The following are requirement to develop. Although you can do it in different ways doing so will likely result in issues. All commands are assumed to be run from the root of this project. [PEP0008](https://www.python.org/dev/peps/pep-0008) compliant code is required.

- `pip install virtualenv` for more info see [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/)
- `virtualenv env`
- `env/bin/pip install -r requirements.txt`
- `env/bin/python setup.py develop` for more info see [setuptools](https://pythonhosted.org/setuptools/setuptools.html)
- `./env/bin/docker-compress` from the project root should allow you to now see quick feedback on changes you make.
- If anything is changed in the setup.py file while developing you will need to rerun `env/bin/python setup.py develop`.
- Right now only have manual tests since huge breaking changes will likely come until a 1.0 is released please read over the `tests/README.md` file.

#### Publishing Build

- `env/bin/python setup.py register`
- `env/bin/python setup.py sdist bdist_wheel upload`
