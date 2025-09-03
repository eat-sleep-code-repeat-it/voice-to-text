import re
from pathlib import Path
import sys

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
file1 = root / 'mmba-ai-programmers-01-01-the-big-three.txt'  # voice.py (Google)
file2 = root / 'mmba-ai-programmers-01-01-the-big-three_whisper_base.txt'

s1 = file1.read_text(encoding='utf-8')
s2 = file2.read_text(encoding='utf-8')

w1 = normalize(s1).split()
w2 = normalize(s2).split()

d = levenshtein(w1,w2)
print(f'Words in voice.py output: {len(w1)}')
print(f'Words in whisper base output: {len(w2)}')
print(f'Edits between them: {d}')
print(f'Relative diff (edits / voice words): {d/len(w1):.2%}')
