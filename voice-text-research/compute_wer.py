import re
from pathlib import Path

def normalize(s):
    s = s.lower()
    s = re.sub(r"[^a-z0-9\s]", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

def levenshtein(a,b):
    n,m=len(a),len(b)
    if n==0: return m
    if m==0: return n
    dp=[[0]*(m+1) for _ in range(n+1)]
    for i in range(n+1): dp[i][0]=i
    for j in range(m+1): dp[0][j]=j
    for i in range(1,n+1):
        for j in range(1,m+1):
            cost = 0 if a[i-1]==b[j-1] else 1
            dp[i][j]=min(dp[i-1][j]+1, dp[i][j-1]+1, dp[i-1][j-1]+cost)
    return dp[n][m]

root = Path(__file__).parent
ref = (root / 'mmba-ai-programmers-01-01-the-big-three.txt').read_text(encoding='utf-8')
vosk = (root / 'mmba-ai-programmers-01-01-the-big-three_vosk_transcription.txt').read_text(encoding='utf-8')
whisper = (root / 'mmba-ai-programmers-01-01-the-big-three_whisper_small.txt').read_text(encoding='utf-8')

r = normalize(ref).split()
v = normalize(vosk).split()
w = normalize(whisper).split()

dist_v = levenshtein(r,v)
dist_w = levenshtein(r,w)

wer_v = dist_v / max(1,len(r))
wer_w = dist_w / max(1,len(r))

print(f"Reference words: {len(r)}")
print(f"Vosk edits: {dist_v}, WER: {wer_v:.2%}")
print(f"Whisper edits: {dist_w}, WER: {wer_w:.2%}")
