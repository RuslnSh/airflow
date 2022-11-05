import pandas as pd
from include.utils.email_utils import send_email


def _calculate_stats(input_path, output_path):
    events = pd.read_json(input_path)
    stats = events.groupby(['date', 'user']).size().reset_index()
    stats.to_csv(output_path, index=False)


def _send_email(address_to, **context):
    stats = pd.read_csv(context["templates_dict"]["stats_path"])
    send_email(address_to, stats)
