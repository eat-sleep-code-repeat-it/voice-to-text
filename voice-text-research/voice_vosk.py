#!/usr/bin/env python3
from vosk import Model, KaldiRecognizer
import sys, os, wave, json, tempfile, argparse
from pydub import AudioSegment


def ensure_wav_mono_16bit(src_path):
    """Convert audio to mono 16kHz 16-bit WAV and return path to temp file."""
    audio = AudioSegment.from_file(src_path)
    audio = audio.set_channels(1).set_sample_width(2).set_frame_rate(16000)
    tmp = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
    audio.export(tmp.name, format='wav')
    return tmp.name


def _ffmpeg_available():
    # pydub looks for ffmpeg/avconv on PATH; check venv Scripts too
    paths = os.environ.get('PATH', '').split(os.pathsep)
    # also check common venv script location
    venv_scripts = os.path.join(os.path.dirname(os.path.realpath(__file__)), '.venv', 'Scripts')
    if venv_scripts not in paths:
        paths.insert(0, venv_scripts)
    for p in paths:
        if not p:
            continue
        ff = os.path.join(p, 'ffmpeg.exe')
        if os.path.exists(ff):
            return True
    return False


def transcribe(model_path, wav_path, out_path=None, json_out=None, show_progress=True):
    if not os.path.exists(model_path):
        print(f"Model not found at {model_path}.\nDownload a small model from https://alphacephei.com/vosk/models and unpack it into this path.")
        sys.exit(1)

    if show_progress:
        print(f"Using model: {model_path}")
        print(f"Input file: {wav_path}")

    wf_path = wav_path
    try:
        with wave.open(wav_path, "rb") as wf:
            needs_convert = (wf.getnchannels() != 1) or (wf.getsampwidth() != 2) or (wf.getframerate() != 16000)
    except wave.Error:
        needs_convert = True

    if needs_convert:
        if show_progress:
            print("Converting input to mono 16kHz WAV...")
        wf_path = ensure_wav_mono_16bit(wav_path)

    # check ffmpeg availability and warn once
    if not _ffmpeg_available():
        print("Warning: ffmpeg not found on PATH. Conversions may fail or be slow. Consider installing ffmpeg and adding it to PATH.")

    wf = wave.open(wf_path, "rb")
    model = Model(model_path)
    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)

    segments = []
    total_frames = wf.getnframes()
    frames_read = 0
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        frames_read += 4000
        if rec.AcceptWaveform(data):
            res = json.loads(rec.Result())
            # Vosk returns {'text': '...', 'result': [{word, start, end}, ...]}
            if 'result' in res:
                segments.append(res)
        if show_progress:
            pct = min(100, int(frames_read / total_frames * 100)) if total_frames else 0
            print(f"Progress: {pct}%", end='\r')

    final = json.loads(rec.FinalResult())
    if 'result' in final:
        segments.append(final)

    # flatten text for plain TXT output
    all_text = " ".join([seg.get('text', '') for seg in segments if seg.get('text')])
    if out_path is None:
        out_path = os.path.splitext(os.path.basename(wav_path))[0] + "_vosk_transcription.txt"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(all_text)

    if json_out is None:
        json_out = os.path.splitext(os.path.basename(wav_path))[0] + "_vosk_transcription.json"
    # build structured JSON with segments and words
    structured = {
        'file': os.path.basename(wav_path),
        'model': os.path.basename(model_path),
        'segments': []
    }
    for seg in segments:
        structured['segments'].append({
            'text': seg.get('text', ''),
            'words': seg.get('result', [])
        })

    with open(json_out, 'w', encoding='utf-8') as jf:
        json.dump(structured, jf, ensure_ascii=False, indent=2)

    if show_progress:
        print('\nTranscription saved to', out_path)
        print('JSON saved to', json_out)

    if wf_path != wav_path:
        try:
            wf.close()
        except:
            pass
        try:
            os.remove(wf_path)
        except:
            pass


def main():
    p = argparse.ArgumentParser(description='Simple Vosk offline transcription')
    p.add_argument('wav', nargs='?', help='Path to WAV/MP3 file (defaults to bundled file)',
                   default=os.path.join(os.path.dirname(os.path.realpath(__file__)), "mmba-ai-programmers-01-01-the-big-three.wav"))
    p.add_argument('--model', '-m', help='Path to Vosk model directory', default=os.path.join(os.path.dirname(os.path.realpath(__file__)), "vosk-model-small-en-us-0.15"))
    p.add_argument('--out', '-o', help='Output text file path')
    p.add_argument('--quiet', '-q', action='store_true', help='Suppress progress output')
    args = p.parse_args()

    transcribe(args.model, args.wav, out_path=args.out, show_progress=not args.quiet)


if __name__ == '__main__':
    main()
