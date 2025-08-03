import os
import click
import google.generativeai as genai
from moviepy.video.io.VideoFileClip import VideoFileClip
from tqdm import tqdm
from dotenv import load_dotenv
import time
import json
from pathlib import Path

# --- Configuration ---
VIDEO_EXTENSIONS = ('.mp4', '.mkv', '.avi', '.mov', '.webm')
AUDIO_DIR = "audio"
TEXT_DIR = "text"

# --- API Key Management ---

def get_config_dir():
    """Get the configuration directory for storing API keys."""
    home = Path.home()
    config_dir = home / ".kotha"
    config_dir.mkdir(exist_ok=True)
    return config_dir

def get_config_file():
    """Get the path to the configuration file."""
    return get_config_dir() / "config.json"

def save_api_key(api_key):
    """Save the API key to the configuration file."""
    config_file = get_config_file()
    config = {}

    if config_file.exists():
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            config = {}

    config['gemini_api_key'] = api_key

    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)

    click.echo(click.style("✅ API key saved successfully!", fg='green'))

def load_api_key():
    """Load the API key from the configuration file."""
    config_file = get_config_file()

    if not config_file.exists():
        return None

    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        return config.get('gemini_api_key')
    except (json.JSONDecodeError, FileNotFoundError):
        return None

# --- Helper Functions ---

def setup_directories():
    """Ensures that the audio and text output directories exist."""
    os.makedirs(AUDIO_DIR, exist_ok=True)
    os.makedirs(TEXT_DIR, exist_ok=True)

def find_video_files(directory, specific_file=None):
    """Finds video files in the given directory."""
    if specific_file:
        if os.path.exists(specific_file) and specific_file.lower().endswith(VIDEO_EXTENSIONS):
            return [specific_file]
        else:
            click.echo(click.style(f"Error: File '{specific_file}' not found or is not a supported video format.", fg='red'))
            return []

    video_files = [f for f in os.listdir(directory) if f.lower().endswith(VIDEO_EXTENSIONS)]
    return video_files

def convert_videos_to_mp3(video_files):
    """Converts a list of video files to MP3 format."""
    converted_audio_paths = []
    if not video_files:
        click.echo(click.style("No video files found to convert.", fg='yellow'))
        return converted_audio_paths

    click.echo(click.style("\nStep 1: Converting videos to MP3...", fg='cyan', bold=True))

    with tqdm(total=len(video_files), desc="Converting", unit="file") as pbar:
        for video_file in video_files:
            base_name = os.path.splitext(os.path.basename(video_file))[0]
            audio_path = os.path.join(AUDIO_DIR, f"{base_name}.mp3")

            pbar.set_description(f"Processing {video_file}")

            if os.path.exists(audio_path):
                pbar.update(1)
                converted_audio_paths.append(audio_path)
                continue # Skip if already converted

            try:
                with VideoFileClip(video_file) as video_clip:
                    video_clip.audio.write_audiofile(audio_path, logger=None)
                converted_audio_paths.append(audio_path)
            except Exception as e:
                click.echo(click.style(f"\nError converting {video_file}: {e}", fg='red'))

            pbar.update(1)

    click.echo(click.style("✅ Video to MP3 conversion complete.", fg='green'))
    return converted_audio_paths

def transcribe_audio_files(audio_paths, api_key):
    """Transcribes a list of audio files using the Gemini API."""
    if not audio_paths:
        click.echo(click.style("No audio files found to transcribe.", fg='yellow'))
        return

    click.echo(click.style("\nStep 2: Transcribing audio to text...", fg='cyan', bold=True))

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('models/gemini-2.0-flash')
    except Exception as e:
        click.echo(click.style(f"Error configuring Gemini API: {e}", fg='red'))
        click.echo(click.style("Please check your API key and try again.", fg='yellow'))
        return

    with tqdm(total=len(audio_paths), desc="Transcribing", unit="file") as pbar:
        for audio_path in audio_paths:
            base_name = os.path.splitext(os.path.basename(audio_path))[0]
            text_path = os.path.join(TEXT_DIR, f"{base_name}.txt")

            pbar.set_description(f"Transcribing {os.path.basename(audio_path)}")

            if os.path.exists(text_path):
                pbar.update(1)
                continue # Skip if already transcribed

            try:
                audio_file = genai.upload_file(path=audio_path)
                response = model.generate_content(["Please transcribe this audio", audio_file])

                # Free up resources
                genai.delete_file(audio_file.name)

                with open(text_path, 'w', encoding='utf-8') as f:
                    f.write(response.text)
            except Exception as e:
                 click.echo(click.style(f"\nError transcribing {audio_path}: {e}", fg='red'))

            pbar.update(1)
            time.sleep(1) # To respect API rate limits if any

    click.echo(click.style("✅ Audio transcription complete.", fg='green'))

# --- CLI Command ---

@click.group(invoke_without_command=True)
@click.pass_context
@click.argument('filename', required=False)
@click.option('--set-api', help='Set the Gemini API key for the current user')
@click.version_option("1.0.0", prog_name="kotha")
def cli(ctx, filename, set_api):
    """
    'kotha' converts video files in the current directory to MP3,
    then transcribes them to text using the Gemini API.

    You can optionally specify a single FILENAME to process.
    """
    if set_api:
        save_api_key(set_api)
        return

    if ctx.invoked_subcommand is None:
        # This is the main command functionality
        run_main(filename)

def run_main(filename):
    """Main functionality for processing videos."""
    click.echo(click.style("--- Starting Kotha CLI ---", fg='magenta', bold=True))

    # Load environment variables from .env file (for backward compatibility)
    load_dotenv()

    # Try to get API key from multiple sources
    api_key = os.getenv("GEMINI_API_KEY") or load_api_key()

    if not api_key:
        click.echo(click.style("Fatal Error: GEMINI_API_KEY not found.", fg='red', bold=True))
        click.echo("Please set your API key using: kotha --set-api='your_api_key_here'")
        click.echo("Or create a '.env' file and add: GEMINI_API_KEY='your_api_key_here'")
        return

    # 1. Setup
    setup_directories()

    # 2. Find videos
    current_directory = '.'
    videos_to_process = find_video_files(current_directory, filename)

    # 3. Convert videos
    converted_audios = convert_videos_to_mp3(videos_to_process)

    # 4. Transcribe audios
    transcribe_audio_files(converted_audios, api_key)

    click.echo(click.style("\n--- Kotha process finished! ---", fg='magenta', bold=True))

if __name__ == "__main__":
    cli()
