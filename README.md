# doordash-generator

Automatically creates DoorDash accounts with given details.

## Running
1. Clone the repository and navigate to the project directory.
2. Install poetry and project dependencies:
```bash
pip install poetry
poetry install
```
3. Create a `config.toml` file by copying the example file `example.config.toml` and editing it with your own info.
5. Run the script:
```
poetry run python src/main.py
```

## Example configuration
```toml
first_name = "John"
last_name = "Doe"
email_name = "example"
email_domain = "gmail.com"
password = "password" # Optional
address = "303 2nd St, Suite 800 San Francisco"
quantity = 5
headless = true # Optional
```
