# FuelCostCalculator

## Running

Assuming you have Python 3.3 or later installed you should create a virtual environment using the `venv` command.
    ```
    python3 -m venv .venv
    ```

Then, dependencies must be installed and this can be done using pip and the requirements.txt file
    ```
    pip install -r flask/requirements.txt
    ```

You can run the project by running the main.py file
    ```
    python3 main.py
    ```

### Running with Docker

To run this server with docker start by ensuring you have docker and the compose plugin installed

First clone the repository
    ```
    git clone https://github.com/robertmonopoly/FuelCostCalculator
    ```
Next you can start the docker service
    ```
    docker compose up -d
    ```
The SQLite database will be stored in the /data dirctory and the service will be accessible on `localhost:3000`

If you make changes to the codebase or pull changes from upstream 
you must rebuild the docker image by either running compose with the rebuild flag:
    ```
    docker compose up -d --build
    ```

Or by manually rebuilding the image (Note that you must be in the same folder as the Dockerfile)
    ```
    docker build .
    ```
And then recreating the containers with
    ```
    docker compose up -d
    ```

To stop the service you can either stop the running container
    ```
    docker compose stop
    ```
Or completely destroy the containers (This doesn't destroy the database though)
    ```
    docker compose down
    ```

## Running Tests
TODO
