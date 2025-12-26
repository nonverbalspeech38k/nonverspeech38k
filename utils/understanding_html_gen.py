import html
from pathlib import Path
import json
import sys

# en setting
# models = {
#     "nonverbaltts": "GT (NonVerbalTTS)",
#     "qwen2audio": "Qwen2-Audio",
#     "capspeech_qwen2": "Qwen2-Audio + <br> CapSpeech",
#     "tbo_qwen2": "Qwen2-Audio + <br> NonVerbalSpeech-38K(TBO) (Ours)",
#     "tsa_qwen2": "Qwen2-Audio + <br> NonVerbalSpeech-38K(TSA) (Ours)",
#     "whisper_large_v3": "Whisper-Large-V3",
#     "capspeech_whisper": "Whisper-Large-V3 + <br> CapSpeech",
#     "tbo_whisper": "Whisper-Large-V3 + <br> NonVerbalSpeech-38K(TBO) (Ours)",
#     "tsa_whisper": "Whisper-Large-V3 + <br> NonVerbalSpeech-38K(TSA) (Ours)",
# }
# file_dir = "nv_caption/en_settting"
# idx_list = [0, 1, 4]

# zh setting
models = {
    "smiip_nv_mnv_17": "GT (SMIIP-NV|MNV-17)",
    "qwen2audio": "Qwen2-Audio",
    "nvspeech_qwen2": "Qwen2-Audio + <br> NVSpeech",
    "tbo_qwen2": "Qwen2-Audio + <br> NonVerbalSpeech-38K(TBO) (Ours)",
    "tsa_qwen2": "Qwen2-Audio + <br> NonVerbalSpeech-38K(TSA) (Ours)",
    "whisper_large_v3": "Whisper-Large-V3",
    "nvspeech_whisper": "Whisper-Large-V3 + <br> NVSpeech",
    "tbo_whisper": "Whisper-Large-V3 + <br> NonVerbalSpeech-38K(TBO) (Ours)",
    "tsa_whisper": "Whisper-Large-V3 + <br> NonVerbalSpeech-38K(TSA) (Ours)",
}
idx_list = [0, 1, 2]
file_dir = "nv_caption/zh_settting"

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
audio_path_root = f'{file_dir}/audios/'

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
    if idx not in idx_list:
        continue
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