import os
from pydub import AudioSegment

def convert_wav_to_mp3(source_folder, output_folder):
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(source_folder):
        if filename.lower().endswith(".wav"):
            wav_path = os.path.join(source_folder, filename)
            mp3_filename = os.path.splitext(filename)[0] + ".mp3"
            mp3_path = os.path.join(output_folder, mp3_filename)

            try:
                print(f"Converting: {filename} → {mp3_filename}")
                sound = AudioSegment.from_wav(wav_path)
                sound.export(mp3_path, format="mp3")
                print("✔️ Done")
            except Exception as e:
                print(f"❌ Failed to convert {filename}: {e}")

if __name__ == "__main__":
    src_folder = "C:\\Users\\eatsl\\Documents\\Audacity\\mmba-ai-lecture" #input("Enter the path to the folder with .wav files: ").strip()
    out_folder = "C:\\Users\\eatsl\\Documents\\Audacity\\mmba-ai-lecture\mp3" #input("Enter the output folder for .mp3 files: ").strip()
    convert_wav_to_mp3(src_folder, out_folder)
