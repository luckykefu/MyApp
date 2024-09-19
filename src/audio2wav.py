import os
from pydub import AudioSegment
from .log import get_logger

logger = get_logger(__name__)

def convert_audio(input_file, output_format, output_dir="output"):
    """
    Convert any audio format to the specified format.
    
    :param input_file: Path to the input audio file
    :param output_format: Desired output format (e.g., 'wav', 'mp3', 'ogg')
    :param output_dir: Directory to save the output file (optional)
    :return: Path to the output file
    """
    try:
        # Get the file name and extension
        file_name, file_extension = os.path.splitext(os.path.basename(input_file))
        
        # If output_dir is not specified, use the same directory as the input file
        if output_dir is None:
            output_dir = os.path.dirname(input_file)
        
        # Ensure the output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Set the output file path
        output_file = os.path.join(output_dir, f"{file_name}.{output_format}")
        
        # Load the audio file
        audio = AudioSegment.from_file(input_file, format=file_extension[1:])
        
        # Export as the specified format
        audio.export(output_file, format=output_format)
        
        logger.info(f"Successfully converted {input_file} to {output_file}")
        return output_file
    
    except Exception as e:
        logger.error(f"Error converting {input_file} to {output_format}: {str(e)}")
        return None

if __name__ == "__main__":
    # Example usage
    input_file = r"d:\Music\男孩 (Live)\男孩 (Live).flac"  # Replace with your input file path
    output_format = "wav"  # Replace with desired output format
    output_audio = convert_audio(input_file, output_format)
    if output_audio:
        print(f"Converted file saved at: {output_audio}")
    else:
        print("Conversion failed.")


