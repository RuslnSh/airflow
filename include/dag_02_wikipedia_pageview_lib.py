import pathlib
import requests
import requests.exceptions as request_exceptions
from include.utils.log_utils import print_log


def _download_pages_python(output_path, output_file, **context):
    '''
    Download .gz file from wikipedia dump and save it at specified location

    :param output_path: result file location
    :param output_file: result file name
    :param context: task context
    :return: return None, but save file at specified location
    '''
    pathlib.Path(output_path).mkdir(parents=True, exist_ok=True)

    year, month, day, hour, *_ = context["execution_date"].timetuple()
    hour = hour - 1  # Не всегда выкладывается архив за текущее время, берем предыдущий

    url = (
        "https://dumps.wikimedia.org/other/pageviews/"
        f"{year}/{year}-{month:0>2}/pageviews-{year}{month:0>2}{day:0>2}-{hour:0>2}0000.gz"
    )

    try:
        response = requests.get(url)

        with open(output_path + "/" + output_file, 'wb') as fw:
            fw.write(response.content)

    except request_exceptions.MissingSchema:
        print_log(f"Url {url} is invalid")
    except request_exceptions.ConnectionError:
        print_log(f"Could not connect to {url}")



def _fetch_pageviews(pagenames, execution_date, **_):
    '''
    Fetches pageview from wikipageviews file and create sql file based on it's information

    :param pagenames: list of pages to look for in wikipageviews file
    :param execution_date:
    :return: None, but create a sql file
    '''
    result = dict.fromkeys(pagenames, 0)

    filename = f"{cwd}/tmp/wikipageviews"
    try:
        with open(filename, "r") as fr:
            for line in fr:
                domain_code, page_title, view_counts, _ = line.split(" ")
                if domain_code == "en" and page_title in pagenames:
                    result[page_title] = view_counts

        with open(f"{cwd}/tmp/postgres_insert_stat.sql", "w") as fw:
            for pagename, pageviewcount in result.items():
                fw.write(
                    "INSERT INTO airflow.pageview_counts VALUES ("
                    f"'{pagename}', {pageviewcount}, '{execution_date}'"
                    ");\n"
                )

    except FileNotFoundError:
        print_log(f"File {file_name} not found")