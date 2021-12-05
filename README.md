# ReadMe
## Tools/Libraries Used:
- Alpine Linux (Base system for Docker image)
- Flask (Main framework)
- Pandas (Data processing)
- Redis (Count the request(task_run) number)

## Usage:
1. `docker-compose up` to build the environment and install necessary libraries and tools. 
2. Flask will listen `5000` port. When new `POST` request coming in, it will check the `Content-Type` to call the corresponding Pandas read function: `read_csv` for CSV/TEXT and `read_json` for JSON.
3. Read the database(current is `result.csv`)
4. Iterate all coins' `id` in request data and run `coinInquiry` function to each `id`. Within the function, it will call CoinGeicko's API. If the the coin is found, it will return a list of exchanges name or it will return an empty list.
5. If coin `id` is already in the database, it will only update `exchanges` field in the database. If the coin is new one, will add a new line to the database, task_run will be current `count` coming from Redis.
6. Lastly, write the result back to database.

## Improvement needed:
- Use database instead of CSV file to store the data. It will be faster, more sustainable. No need to download and upload everything on each run, just update where it is needed inside the database.