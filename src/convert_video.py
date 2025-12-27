from os import path, makedirs

from subprocess import run

def convert_to_mp4(input_file: str, output_folder: str) -> str:
    """
    Converts a video file to MP4 format (H.264 + AAC) using ffmpeg.

    Args:
        input_file (str): Path to the input video file.
        output_folder (str, optional): Folder to save the MP4. Defaults to same folder as input.

    Returns:
        str: Path to the converted MP4 file.
    """
    if not path.exists(input_file):
        raise FileNotFoundError(f"Input file not found: {input_file}")

    if not path.exists(output_folder):
        makedirs(output_folder, exist_ok=True)

    base_name = path.splitext(path.basename(input_file))[0]
    output_file = path.join(output_folder, base_name + ".mp4")

    # Run ffmpeg conversion
    ret = run([
        "ffmpeg",
        "-y",  # overwrite if exists
        "-i", input_file,
        "-c:v", "libx264",
        "-c:a", "aac",
        "-loglevel", "quiet",
        "-strict", "experimental",
        output_file
    ], check=True)

    if ret.returncode != 0:
        print(f"❌ Failed to convert {input_file} to MP4")
        return None

    print(f"✅ Converted {input_file} to {output_file}")
    return output_file


if __name__ == "__main__":
    convert_to_mp4("videos/file_example_AVI_480_750kB.avi", "output")
