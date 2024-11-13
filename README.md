# grav-giant-test



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