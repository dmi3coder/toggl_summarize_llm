# Toggl summary report with LLM

This loader fetches time entries from Toggl workspace and project into `Document`s. It then merges and summarizes time
entries

Before working with Toggl's API, you need to get API token:

1. Log in to Toggl
2. [Open profile](https://track.toggl.com/profile)
3. Scroll down and click `-- Click to reveal --` for API token
4. Copy the API token

Before working with OpenAI's API, you need to get API key:

1. Log in to OpenAI
2. [Open API key page](https://platform.openai.com/account/api-keys)
3. Click `Create API Key`
4. Copy the API key

## Setup

1. Install the packages
```bash
pip install -r requirements.txt
```
2. Populate `.env` from `.env.example`

## Usage

```shell
python cli.py report today
'''
20 Jun

- *Development of Toggl reader app*: 2h46m
    - Three separate sessions worked on this ticket.

Total: 2h46m
'''
python cli.py report yesterday
'''
19 Jun

- *Development of Toggl reader app*: 1h30m
    - Two separate sessions worked on this ticket.

Total: 2h46m
'''
python cli.py report today --format "*{{ticket_name}}* ->> {{duration_hours_minutes}}"
'''
21 Jun

*Development of Toggl reader app* ->> 1h30m

Total: 1h30m

'''
```