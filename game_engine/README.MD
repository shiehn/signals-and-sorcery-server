
# RUN THE TESTS FROM THE MODULE ROOT DIRECTORY (game_engine)

```bash
python3 -m unittest discover -s game_engine/tests -p 'test_*'
```


# RUN THE E2E GAME ENGINE API TESTS

First, start the docker-compose services. then run the following command:

```bash
pytest e2e_game_tests/
```