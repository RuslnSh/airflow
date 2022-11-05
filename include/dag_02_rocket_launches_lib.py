import requests
import requests.exceptions as request_exceptions
import pathlib
import json
from include.utils.log_utils import print_log


def _get_pictures_by_json(p_jsn: str, p_dst: str):
    '''
    Function download images from url's from p_jsn file

    :param p_jsn: json file for parsing
    :param p_dst: destination to save images
    :return: None
    '''

    # TODO check if p_dst ends with "/"
    pathlib.Path(p_dst).mkdir(parents=True, exist_ok=True)

    # TODO this file is read during parsing DAGs, I thought that scheduler only parse files in dag folder
    try:
        with open(p_jsn) as f:
            launches = json.load(f)
            image_urls = [launch["image"] for launch in launches["results"]]

            for image_url in image_urls:
                try:
                    response = requests.get(image_url)
                    image_filename = image_url.split("/")[-1]
                    target_file = f"{p_dst}{image_filename}"
                    with open(target_file, "wb") as fw:
                        fw.write(response.content)

                    print_log(f"Downloaded image from {image_url} to {target_file}")
                except request_exceptions.MissingSchema:
                    print_log(f"Url {image_url} is invalid")
                except request_exceptions.ConnectionError:
                    print_log(f"Could not connect to {image_url}")
    except FileNotFoundError:
        print_log(f"File {p_jsn} not found")
