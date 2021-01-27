import subprocess
from os.path import expanduser
import re


def fetch_formats(link):
    """
    Obtains the available formats to download for the given Link
    :param link: str
    :return: str (result from the command 'youtube-dl -F <link>')
    """
    result = []
    output = fetch_formats_from_command(link)
    for line in output.split("\n")[3:]:
        if line.strip() and "video only" not in line and "audio only" not in line:
            format_code, resolution, notes = re.search("(\d+)\s+(\w+)\s+(.*)", line).groups()
            result.append([format_code, resolution, notes])

    return result


def fetch_formats_from_command(link):
    """
    Run youtube-dl command to fetch available formats
    :param link: str
    :return: str (Output from command lin)
    """
    return subprocess.check_output(["youtube-dl", "-F", link]).decode("utf-8")


def download_file_from_link(link, format_code):
    """
    Download the file to ~/Downloads
    :param link:
    :param format_code
    :return: str (Path to file)
    """
    path = check_for_existing_file(link)
    if path is None:
        subprocess.check_output(['youtube-dl', '-f', format_code, '-o', expanduser("~/Downloads/") + "%(title)s.%(ext)s"])
        path = check_for_existing_file(link)

    if path is None:
        raise ValueError("Something went wrong when Trying to fetch Download")
    return path


def check_for_existing_file(link):
    """
    Check the Filename from the link and verify it against the files in Downloads directory
    :param link: str
    :return: str if file is found else None
    """
    file_name = subprocess.check_output(['youtube-dl', '--get-filename', link]).decode("utf-8")
    list_of_files = get_files_from_downloads()
    file_name_without_format = re.search("(.*)\.(webm|mp4)", file_name)
    if file_name_without_format is None:
        raise ValueError(f"Unknown file format encountered. Name:{file_name}")

    file_name = file_name_without_format.group(1)
    for name in list_of_files:
        if file_name in name:
            return expanduser(f"~/Downloads/{name}")

    return None


def get_files_from_downloads():
    """
    Return List of file names in Downloads directory
    :return: List(str) [filenames]
    """

    files = subprocess.check_output(['ls', '-a', expanduser('~/Downloads')]).decode("utf-8")
    return files.split("\n")
