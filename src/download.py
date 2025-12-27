from seleniumbase import Driver
from time import sleep
from os import path, getcwd, remove
from urllib.parse import urlparse, urlsplit
from requests import get as requests_get
from shutil import copy2


def download_file_using_requests(url: str, dst_folder: str) -> None:
    """
    Downloads a file from the given URL to the destination path using requests.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/116.0.0.0 Safari/537.36",
        "Referer": url  # optional, some sites require it
    }

    response = requests_get(url, headers=headers, stream=True)
    response.raise_for_status()

    parsed_url = urlparse(url)
    filename = path.basename(parsed_url.path)
    dest = path.join(dst_folder, filename)
    with open(dest, "wb") as f:
        for chunk in response.iter_content(8192):
            f.write(chunk)



def download_file_using_seleniumBase(url: str, dst_folder: str) -> str:
    """
    Downloads a file from the given URL to the destination path using SeleniumBase
    to handle dynamic content or redirects.
    """
    # Initialize driver (undetected Chrome, GUI mode)
    driver = Driver(uc=True, headless=True)

    # Open the video page
    driver.get(url)
    sleep(10)

    # Find the <video> element and get its src attribute
    video_src = driver.execute_script("return document.querySelector('video').src;")
    print("🎬 Video source found:", video_src)

    # Create a temporary <a> element and click it to trigger download
    driver.execute_script("""
        const a = document.createElement('a');
        a.href = arguments[0];
        a.download = arguments[0].split('/').pop();
        document.body.appendChild(a);
        a.click();
        a.remove();
    """, video_src)

    # Wait for download to complete
    sleep(5)
    driver.quit()

    # Define source and destination paths
    filename = path.basename(urlsplit(url).path)
    download_folder = path.join(getcwd(), "downloaded_files")
    src_path = path.join(download_folder, filename)
    dest_path = path.join(dst_folder, filename)
    
    # Move the file from download_folder to dst_folder
    if path.exists(src_path):
        try:
            copy2(src_path, dest_path)
            remove(src_path)
        except Exception as e:
            print("❌ Failed to move downloaded file:", e)
        else:
            return dest_path
    return None


def download_file(url: str, dst_folder: str) -> str:
    """
    Downloads a file from the given URL to the destination path.
    """
    try:
        ret = download_file_using_requests(url, dst_folder)
    except Exception:
        ret = download_file_using_seleniumBase(url, dst_folder)
    return ret


def main():
    print("This is a module for downloading files.")


if __name__ == "__main__":
    main()
