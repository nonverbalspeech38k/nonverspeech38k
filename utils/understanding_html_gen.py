import html
from pathlib import Path
import json
import sys

models = {
    "nonverbaltts": "GT (NonVerbalTTS)", "whisper_large_v3": "Whisper-Large-V3", "qwen2audio": "Qwen2-Audio", 
    "capspeech": "Qwen2-Audio + <br> CapSpeech", "nonverbalspeech38k": "Qwen2-Audio + <br> NonVerbalSpeech38K (Ours)", "refined_aligned": "Qwen2-Audio + <br> NonVerbalSpeech-38K (Ours) + <br> Refined + Aligned"
}

file_dir = "./texts"

# Escape < and > in the text content
def escape(text):
    return html.escape(text.strip())

# Read the transcript
transcript = {}
for model in models:
    transcript_path = Path(file_dir) / f"{model}.json"
    with open(transcript_path, "r") as f:
        obj = json.load(f)
    transcript[model] = [escape(text) for text in obj]

# print(transcript)
# sys.exit(0)

# audio_path_pattern = f'texts/audios/{}.wav'
audio_path_root = 'texts/audios/'

# Generate HTML table content
rows = []

# First row: single audio spanning two columns
header_row = '  <thead><tr>\n'
# header_row += '    <th style="width: 100px; vertical-align: middle; text-align: center; position: sticky; left: 0; background-color: white; z-index: 1;"> Model </th>\n'
# header_row += '    <th style="width: 250px; vertical-align: middle; text-align: center; position: sticky; left: 0; background-color: white; z-index: 1;"> Text </th>\n'
header_row += '    <th style="width: 100px; vertical-align: middle; text-align: center; background-color: white; z-index: 1;"> Model </th>\n'
header_row += '    <th style="width: 250px; vertical-align: middle; text-align: center; background-color: white; z-index: 1;"> Text </th>\n'
header_row += '  </tr><thead/>'
rows.append(header_row)

# Subsequent rows: model name and corresponding text for each model
for idx in range(len(next(iter(transcript.values())))):
    # First row for the audio
    audio_row = f'  <tr>\n'
    audio_path = f'{audio_path_root}/{idx}.wav'
    # audio_row += f'    <td colspan="2" style="width: 100px; vertical-align: middle; text-align: center; position: sticky; left: 0; background-color: white; z-index: 1;">\n'
    audio_row += f'    <td colspan="2" style="width: 100px; vertical-align: middle; text-align: center; background-color: white; z-index: 1;">\n'
    audio_row += f'      <audio controls style="width: 250px;">\n'
    audio_row += f'        <source src="{audio_path}" />\n'
    audio_row += f'        Your browser does not support the audio element.\n'
    audio_row += f'      </audio>\n'
    audio_row += f'    </td>\n'
    audio_row += f'  </tr>'
    rows.append(audio_row)

    # Rows for each model and its corresponding text
    for model in models:
        text = transcript[model][idx]
        # if the text is include [ or ], we need to highlight it
        if '[' in text or ']' in text:
            text = text.replace('[', '<span style="color: red;">[').replace(']', ']</span>')
        row = f'  <tr>\n'
        # row += f'    <td style="width: 100px; vertical-align: middle; text-align: center; position: sticky; left: 0; background-color: white; z-index: 1;">{models[model]}</td>\n'
        row += f'    <td style="width: 100px; vertical-align: middle; text-align: center; background-color: white; z-index: 1;">{models[model]}</td>\n'
        row += f'    <td style="width: 250px; vertical-align: middle; text-align: center;">{text}</td>\n'
        row += f'  </tr>'
        rows.append(row)

# Output the complete HTML (only the tbody part, for easier embedding)
tbody_html = '<tbody>\n' + '\n'.join(rows[1:]) + '\n</tbody>'

tabel_html = rows[0] + '\n' + tbody_html

# Output HTML to a file or stdout
print(tabel_html)