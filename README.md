# Gravie Challenge

this implements the Gravie [challenge](https://github.com/gravieinc/gravie-developer-test)


- follow steps below to build/run docker image (assumes docker is running)
- then open browser to confirm search and checkout works





# help
look at [Makefile](Makefile) for quick examples.
```bash 
# get help
make help
```


# test with docker
look at [Makefile](Makefile) for quick examples.
```bash 
# make image
make docker.build
# run container
make docker.run
```

# test app in browser

## search for games
    http://localhost:8000/search/
    - example: http://localhost:8000/search/mario

## checkout game
    http://localhost:8000/checkout/<id>
    - example: http://localhost:8000/checkout/91349

## show checked out games
    http://localhost:8000/checked_out