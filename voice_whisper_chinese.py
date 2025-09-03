import whisper

model = whisper.load_model("base") # or tiny, small, medium, large

result = model.transcribe("chinese_audio.mp3", language="zh")

print("Chinese transcription:")
print(result["text"])


import opencc
# Convert Traditional Chinese to Simplified Chinese
cc = opencc.OpenCC('t2s')  # t2s = Traditional to Simplified
simplified_text = cc.convert(result["text"])

print(simplified_text)