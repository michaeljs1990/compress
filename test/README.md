# Tests

This file right now consists solely of manual config tests. In order to verify that a change you have made has not broken anything assess that the following is true when running the following commands.

#### Test Cases (Manual)

###### Test Case First


    ./env/bin/docker-compress generate --file-in test/manual/first/micro_service_one/.compress.yml

The generated `docker-compose.gen.yml` file should look as follows.

    host:
        extends:
            file: ../micro_service_two/docker/base.yml
            service: host
        volumes_from:
        - storage
    host2:
        extends:
            file: docker/base.yml
            service: host
        volumes_from:
        - storage
