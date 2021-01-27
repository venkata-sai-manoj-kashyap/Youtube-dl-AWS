import subprocess


def fetch_formats(link):
    """
    Obtains the available formats to download for the given Link
    :param link: str
    :return: str (result from the command 'youtube-dl -F <link>')
    """
    result = []
    output = fetch_formats_from_command(link)
    import re
    for line in output.split("\n")[3:]:
        if line.strip() and "video only" not in line or "audio only" not in line:
            format_code, resolution, notes = re.search("(\d+)\s+(\w+)\s+(.*)", line).groups()
            result.append("   ".join([format_code, resolution, notes]))

    return result


def fetch_formats_from_command(link):
    """
    Run youtube-dl command to fetch available formats
    :param link: str
    :return: str (Output from command lin)
    """
    return subprocess.check_output(["youtube-dl", "-F", link]).decode("utf-8")
