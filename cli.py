import os
from datetime import datetime, timedelta

import click
import dotenv
from llama_index.core.indices import ListIndex
from llama_index.core.settings import Settings
from llama_index.readers.toggl import TogglReader
from llama_index.readers.toggl.dto import TogglOutFormat
from reportlm.llms import openai

dotenv.load_dotenv()

toggl_reader = TogglReader(api_token=os.getenv("TOGGL_TOKEN"))
Settings.llm = openai(os.getenv("OPENAI_TOKEN"))

workspace_id = os.getenv("WORKSPACE_ID")
project_id = os.getenv("PROJECT_ID")

DEFAULT_PROMPT = """
- *{{ticket_name}}*: {{duration_hours_minutes}}
        - {{description}}
"""

@click.group()
def cli():
    pass


@click.group()
def report():
    pass


@report.command()
@click.option("--format", "-f", help="Output format", default=DEFAULT_PROMPT)
def today(format):
    now = datetime.now()
    data = load_report(now)
    print(summarize(data, now, format=format))


@report.command()
@click.option("--format", "-f", help="Output format", default=DEFAULT_PROMPT)
def yesterday(format):
    _yesterday = datetime.now() - timedelta(days=1)
    data = load_report(_yesterday)
    print(summarize(data, _yesterday, format=format))


def load_report(date):
    data = toggl_reader.load_data(workspace_id=workspace_id, project_id=project_id,
                                  start_date=date.replace(hour=0, minute=0, second=0, microsecond=0),
                                  end_date=date.replace(hour=23, minute=59, second=59, microsecond=999999),
                                  out_format=TogglOutFormat.markdown)
    # Removing unused metadata
    for doc in data:
        doc.metadata = []
    return data


def summarize(data, date, format: str = DEFAULT_PROMPT):
    index = ListIndex.from_documents(data)
    return index.as_query_engine().query(f"""
Tell me how much I worked on each item in next format:
```
{date:%d %b}

{format}

Total: {{total time of all items}}
```
Group items with same name and sum their durations.
    """)


cli.add_command(report)
report.add_command(today)
report.add_command(yesterday)

if __name__ == '__main__':
    cli()
