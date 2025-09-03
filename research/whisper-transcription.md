```bash
Invoke-WebRequest -Uri https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip -OutFile ffmpeg.zip

Expand-Archive ffmpeg.zip -DestinationPath "C:\\ffmpeg"

Move-Item "C:\\ffmpeg\\ffmpeg-*"\bin "C:\\ffmpeg\\bin"

$env:Path += ";C:\ffmpeg\bin"
[Environment]::SetEnvironmentVariable("Path", $env:Path, [EnvironmentVariableTarget]::Machine)

ffmpeg -version


python voice_whisper.py 'C:\\workspace\\ai-programmers-mmba\\audio.mp3' --model small


