import html
from pathlib import Path

models = {
    "ref": "Prompt", "dia": "Dia", "cosyvoice2": "CosyVoice2", "f5tts": "F5-TTS",
    "capspeech": "F5-TTS + <br> Capspeech", "nonverbaltts": "F5-TTS + <br> NonVerbalTTS", "nonverbalspeech38k": "F5-TTS + <br> NonVerbalSpeech-38K (Ours)", "refined_aligned": "F5-TTS + <br> NonVerbalSpeech-38K (Ours) + <br> Refined + Aligned"
}

language = "en"  # Change to "zh" for Chinese

transcript_path = f"./audios/{language}/transcript.txt"

# Escape < and > in the text content
def escape(text):
    return html.escape(text.strip())

# Read the transcript
transcript = {}
with open(transcript_path, "r") as f:
    for line in f:
        parts = line.strip().split(" | ")
        assert len(parts) >= 2
        filename, text = parts[0].strip(), parts[1].strip()
        # transcript[filename] = escape(text)
        transcript[filename] = text

# Generate HTML table content
rows = []

# gen head
# <thead>
# <tr>
#     <th style="width: 220px; vertical-align: middle; text-align: center; position: sticky; left: 0; background-color: white; z-index: 2">
#     Text
#     </th>
#     <th style="vertical-align: middle; text-align: center; width: 200px;">Prompt</th>
#     <th style="vertical-align: middle; text-align: center; width: 200px;">Dia</th>
#     <th style="vertical-align: middle; text-align: center; width: 200px;">CosyVoice2</th>
#     <th style="vertical-align: middle; text-align: center; width: 200px;">F5-TTS</th>
#     <th style="vertical-align: middle; text-align: center; width: 200px;">F5-TTS + <br> Capspeech</th>
#     <th style="vertical-align: middle; text-align: center; width: 200px;">F5-TTS + <br> NonVerbalTTS</th>
#     <th style="vertical-align: middle; text-align: center; width: 200px;">F5-TTS + <br> NonVerbalSpeech-38K (Ours)</th>
# </tr>
# </thead>
thead_html = '<thead>\n'
thead_html += '  <tr>\n'
thead_html += '    <th style="width: 220px; vertical-align: middle; text-align: center; position: sticky; left: 0; background-color: white; z-index: 2;">\n'
thead_html += '      Text\n'
thead_html += '    </th>\n'
for model_key, model_name in models.items():
    thead_html += f'    <th style="vertical-align: middle; text-align: center; width: 200px;">{model_name}</th>\n'
thead_html += '  </tr>\n'
thead_html += '</thead>'

for filename, text in transcript.items():
    # if the text contains < or >, highlight it the content within <>
    assert "<" in text or ">" in text, f"Text does not contain < or >: {text}"
    if '<' in text or '>' in text:
        # text = text.replace('<', '&lt;').replace('>', '&gt;')
        # text = text.replace('&lt;', '<span style="color: red;">&lt;')
        # text = text.replace('&gt;', '&gt;</span>')
        text = text.replace('<', '<span style="color: red;">[').replace('>', ']</span>')
    row = f'  <tr>\n'
    row += f'    <td style="width: 220px; vertical-align: middle; text-align: center; position: sticky; left: 0; background-color: white; z-index: 1;">\n'
    row += f'      {text}\n'
    row += f'    </td>\n'

    for model in models:
        audio_path = f'audios/{language}/{model}/{filename}'
        row += f'    <td style="vertical-align: middle; text-align: center;">\n'
        row += f'      <audio controls style="width: 190px;">\n'
        row += f'        <source src="{audio_path}" />\n'
        row += f'        Your browser does not support the audio element.\n'
        row += f'      </audio>\n'
        row += f'    </td>\n'

    row += f'  </tr>'
    rows.append(row)

# Output the complete HTML (only the tbody part, for easier embedding)
tbody_html = '<tbody>\n' + '\n'.join(rows) + '\n</tbody>'

html_table = f'{thead_html}\n{tbody_html}'
# Output HTML to a file or stdout
print(html_table)