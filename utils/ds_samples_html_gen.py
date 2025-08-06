import os

samples_dir = "./dataset_demos"

# for each subdir in the samples_dir, read the files split by |, with the first part as wav file and the rest as text

text_list = []
audio_path_list = []
audio_segment_list = []
for subdir, dirs, files in os.walk(samples_dir):
    for file in files:
        if file.endswith(".txt"):
            with open(os.path.join(subdir, file), 'r') as f:
                lines = f.readlines()
                for line in lines:
                    parts = line.strip().split('|')
                    assert len(parts) == 2, "Line should not be empty"
                    audio_path = (parts[0]).strip()
                    text = (parts[1]).strip()
                    text_list.append(text)
                    
                    label_name = os.path.basename(subdir)
                    segmetn_suffix = "segment"
                    seg_path = f"{audio_path}_{label_name}_{segmetn_suffix}.wav"
                    seg_path = os.path.join(subdir, seg_path)
                    assert os.path.exists(seg_path), f"Audio file {audio_path} does not exist"
                    audio_segment_list.append(seg_path)

                    full_wav = f"{audio_path}_{label_name}.wav"
                    full_wav = os.path.join(subdir, full_wav)
                    assert os.path.exists(full_wav), f"Full audio file {full_wav} does not exist"
                    audio_path_list.append(full_wav)


assert len(text_list) == len(audio_path_list) == len(audio_segment_list), "Text and audio lists should have the same length"
# print(f"Total samples: {len(text_list)}")

# generate html file

# Generate HTML table content
rows = []


thead_html = '<thead>\n'
thead_html += '  <tr>\n'
thead_html += '    <th style="width: 220px; vertical-align: middle; text-align: center; background-color: white; z-index: 2;">\n'
thead_html += '      Caption\n'
thead_html += '    </th>\n'
thead_html += '    <th style="width: 190px; vertical-align: middle; text-align: center; background-color: white; z-index: 2;">\n'
thead_html += '      Audio\n'
thead_html += '    </th>\n'
thead_html += '    <th style="width: 190px; vertical-align: middle; text-align: center; background-color: white; z-index: 2;">\n'
thead_html += '      Non-Verbal Segments Detected\n'
thead_html += '    </th>\n'
thead_html += '  </tr>\n'
thead_html += '</thead>'

for text, audio_path, audio_segment in zip(text_list, audio_path_list, audio_segment_list):
    # if the text contains < or >, highlight the content within <>
    # if '<' in text or '>' in text or '[' in text or ']' in text:
        # text = text.replace('[', '&lt;').replace(']', '&gt;')
        # text = text.replace('<', '&lt;').replace('>', '&gt;')
        # text = text.replace('&lt;', '<span style="color: red;">&lt;')
        # text = text.replace('&gt;', '&gt;</span>')
        
    text = text.replace('[', '<span style="color: red;">[')
    text = text.replace(']', ']</span>')
    text = text.replace('<B>', '<span style="color: red;">&lt;B&gt;</span>')
    text = text.replace('</B>', '<span style="color: red;">&lt;/B&gt;</span>')
    
    row = f'  <tr>\n'
    row += f'    <td style="width: 220px; vertical-align: middle; text-align: center; background-color: white; z-index: 1;">\n'
    row += f'      {text}\n'
    row += f'    </td>\n'

    # Add audio column for the full audio
    row += f'    <td style="vertical-align: middle; text-align: center;">\n'
    row += f'      <audio controls style="width: 190px;">\n'
    row += f'        <source src="{audio_path}" />\n'
    row += f'        Your browser does not support the audio element.\n'
    row += f'      </audio>\n'
    row += f'    </td>\n'

    # Add audio column for the non-verbal segment
    row += f'    <td style="vertical-align: middle; text-align: center;">\n'
    row += f'      <audio controls style="width: 190px;">\n'
    row += f'        <source src="{audio_segment}" />\n'
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