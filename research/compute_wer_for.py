import re
import sys
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

if len(sys.argv) < 2:
    print('Usage: compute_wer_for.py <transcription_txt_path>')
    sys.exit(2)

trans_path = Path(sys.argv[1])
if not trans_path.exists():
    print('Transcription file not found:', trans_path)
    sys.exit(1)

root = trans_path.parent
ref = (root / 'mmba-ai-programmers-01-01-the-big-three.txt').read_text(encoding='utf-8')
trans = trans_path.read_text(encoding='utf-8')

r = normalize(ref).split()
t = normalize(trans).split()

dist = levenshtein(r,t)
wer = dist / max(1,len(r))
print(f'Reference words: {len(r)}')
print(f'Edits: {dist}, WER: {wer:.2%}')
