# FuelCostCalculator

## Setting up Dev Environment

1. Assuming you have Python 3.3 or later installed you should create a virtual environment using the `venv` command.
    ```
    python3 -m venv .venv
    ```

2. Then, dependencies must be installed and this can be done using pip and the requirements.txt file
    ```
    pip install -r flask/requirements.txt
    ```

3. You can run the project by running the main.py file
    ```
    python3 main.py
    ```
The server will be available at http://localhost:3000 and any changes you make to the code will be automatically applied once saved

## Docker

### Running
To run this server with docker start by ensuring you have docker and the compose plugin installed

1. Clone the repository
    ```
    git clone https://github.com/robertmonopoly/FuelCostCalculator
    ```
2. Bring the docker service up
    ```
    docker compose up -d
    ```
* The SQLite database will be stored in the /data dirctory and the service will be accessible on `localhost:3000`

### Updating
* If you make changes to the codebase or pull changes from upstream 
you must rebuild the docker image by running compose with the rebuild flag:
    ```
    docker compose up -d --build
    ```

* Alternatively, you can manually rebuild the image (Note that you must be in the same folder as the Dockerfile)
    ```
    docker build .
    ```
* After manually rebuilding the image you still have to recreate the container
    ```
    docker compose up -d
    ```
### Stopping
* To stop the service you can either stop the running container 
    ```
    docker compose stop
    ```
* Or completely destroy the containers (This doesn't destroy the database though)
    ```
    docker compose down
    ```

## Running Tests
TODO
