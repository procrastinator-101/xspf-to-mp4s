from shutil import rmtree
from os import path, makedirs
from tempfile import gettempdir
from urllib.parse import urlparse

import xml.etree.ElementTree as ET
from argparse import ArgumentParser

from download import download_file
from convert_video import convert_to_mp4


def parse_cli_args():
    """
    Parses command line arguments
    """
    parser = ArgumentParser(
        description="Get playlist videos from an XSPF file and convert them to mp4 format.")
    parser.add_argument('filename', type=str, help='Path to the XSPF file')
    return parser.parse_args()


def extract_locations(file_path) -> list[str]:
    """
    Extracts all <location> tags from the XSPF file and returns them as a list of strings
    """
    # Parse the XML
    tree = ET.parse(file_path)
    root = tree.getroot()

    # XSPF uses a default namespace, we need to handle that
    ns = {'xspf': 'http://xspf.org/ns/0/'}

    # Extract all <location> tags
    locations = [track.find('xspf:location', ns).text for track in root.findall(
        'xspf:trackList/xspf:track', ns)]
    return locations


def is_remote_url(url: str) -> bool:
    """
    Returns True if the location is a remote URL, False if it's a local path
    """
    parsed = urlparse(url)
    return bool(parsed.scheme) and bool(parsed.netloc)


def normalize_locations(locations: list[str], temp_dir: str) -> list[str]:
    """
    Normalizes the list of locations by downloading remote URLs to the temp directory
    and returning local file paths as is.
    """
    normalized = []
    for loc in locations:
        if is_remote_url(loc):
            try:
                local_path = download_file(loc, temp_dir)
                normalized.append(local_path)
            except Exception as e:
                print(f"❌ Failed to download {loc} : {e}")
        else:
            loc = path.abspath(loc.replace("file:", ""))
            normalized.append(loc)
    return normalized


def main():
    args = parse_cli_args()
    locations = extract_locations(args.filename)
    
    # create a dedicated temp subfolder
    system_temp = gettempdir()
    temp_dir = path.join(system_temp, "my_script_temp")
    makedirs(temp_dir, exist_ok=True)
    
    # normalize locations and convert videos
    normalized_locations = normalize_locations(locations, temp_dir)
    script_dir = path.dirname(path.abspath(__file__))
    relative_output_path = "../output"
    output_folder = path.abspath(path.join(script_dir, relative_output_path))
    for loc in normalized_locations:
        convert_to_mp4(loc, output_folder)
        
    # safely remove the temp subfolder
    if path.exists(temp_dir):
        rmtree(temp_dir)


if __name__ == "__main__":
    main()
