import subprocess
import re
from dateutil.parser import parse


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


def download_file_from_link(link, format_code=22):
    """
    Download the file to ~/Downloads
    :param link: string
    :param format_code: format_code (defaults to 22)
    :return: str (Path to file)
    """
    path = check_for_existing_file(link)
    if path is None:
        filename = filename_from_link(link)
        subprocess.check_output(['youtube-dl', '-f', format_code,
                                 '-o', "/home/ubuntu/Youtube-dl-AWS/static/" + filename, link])
        path = "/home/ubuntu/Youtube-dl-AWS/static/" + filename + ".mp4"

    return path


def filename_from_link(link):
    """
    Parse and generate filename from the video link
    :param link: string
    """
    file_name = subprocess.check_output(['youtube-dl', '--get-filename', link]).decode("utf-8")
    try:
        datetime_result = parse(re.search("\d+\w* \w* \d+", file_name).group()).strftime("%d_%m_%Y")
    except ValueError:
        raise ValueError(f"DataTime Format failed to parse from filename: {file_name}")
    file = re.search("((\w*\s)?Jabardasth)", file_name)
    if file is not None:
        file = file.groups()[0]
    else:
        if "Devi" in file_name:
            file = "Sri Devi Drama Company"
        elif "Cash" in file_name:
            file = "Cash"
        else:
            file = "Unknown File"

    return file + " " + datetime_result + ".mp4"


def check_for_existing_file(link):
    """
    Check the Filename from the link and verify it against the files in Downloads directory
    :param link: str
    :return: str if file is found else None
    """
    file_name = filename_from_link(link)
    list_of_files = get_files_from_static()
    for name in list_of_files:
        if file_name == name:
            return f"/home/ubuntu/Youtube-dl-AWS/static/{name}"

    return None


def get_files_from_static():
    """
    Return List of file names in static directory
    :return: List(str) [filenames]
    """

    files = subprocess.check_output(['ls', '-a', '/home/ubuntu/Youtube-dl-AWS/static/']).decode("utf-8")
    return files.split("\n")
