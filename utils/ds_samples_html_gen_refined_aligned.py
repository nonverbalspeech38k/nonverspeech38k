import os

samples_dir = "./dataset_demos"

# for each subdir in the samples_dir, read the files split by |, with three parts: wav file, text, refined text
text_list = []
text_refined_list = []
audio_path_list = []
audio_segment_list = []

for subdir, dirs, files in os.walk(samples_dir):
    for file in files:
        if file.endswith(".txt"):
            with open(os.path.join(subdir, file), 'r') as f:
                lines = f.readlines()
                for line in lines:
                    parts = line.strip().split('|')
                    assert len(parts) == 3, f"Line format error: {line}"
                    audio_path = (parts[0]).strip()
                    text = (parts[1]).strip()
                    text_refined = (parts[2]).strip()

                    text_list.append(text)
                    text_refined_list.append(text_refined)
                    
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


assert len(text_list) == len(text_refined_list) == len(audio_path_list) == len(audio_segment_list), \
    "Text, refined text and audio lists should have the same length"

# Generate HTML table content
rows = []



thead_html = '<thead>\n'
thead_html += '  <tr>\n'
thead_html += '    <th style="width: 190px; text-align: center; background-color: white;">Audio</th>\n'
thead_html += '    <th style="width: 190px; text-align: center; background-color: white;">Non-Verbal Segments Detected</th>\n'
thead_html += '  </tr>\n'
thead_html += '</thead>'


for text, text_refined, audio_path, audio_segment in zip(text_list, text_refined_list, audio_path_list, audio_segment_list):
    def highlight(txt):
        txt = txt.replace('[', '<span style="color: red;">[')
        txt = txt.replace(']', ']</span>')
        txt = txt.replace('<B>', '<span style="color: red;">&lt;B&gt;</span>')
        txt = txt.replace('</B>', '<span style="color: red;">&lt;/B&gt;</span>')
        return txt

    text = highlight(text)
    text_refined = highlight(text_refined)

    # 第一行：音频
    row = f'  <tr>\n'
    row += f'    <td style="text-align: center;">\n'
    row += f'      <audio controls style="width: 190px;">\n'
    row += f'        <source src="{audio_path}" />\n'
    row += f'      </audio>\n'
    row += f'    </td>\n'

    row += f'    <td style="text-align: center;">\n'
    row += f'      <audio controls style="width: 190px;">\n'
    row += f'        <source src="{audio_segment}" />\n'
    row += f'      </audio>\n'
    row += f'    </td>\n'
    row += f'  </tr>\n'

    # 第二行：合并两列，放 caption
    row += f'  <tr>\n'
    row += f'    <td colspan="2" style="text-align: left; white-space: normal; word-wrap: break-word; background-color: #f9f9f9;">\n'
    # row += f'      <div><b style="white-space: pre;">                    Original:</b> {text}</div>\n'
    row += f'      <div><b> Timestamp-Based Ordering (TBO): </b> {text}</div>\n'
    row += f'    </td>\n'
    row += f'  </tr>\n'
    row += f'  <tr>\n'
    row += f'    <td colspan="2" style="text-align: left; white-space: normal; word-wrap: break-word; background-color: #f9f9f9;">\n'
    # row += f'      <div><b>Refined + Aligned:</b> {text_refined}</div>\n'
    row += f'      <div><b> Temporal-Semantic Alignment (TSA) :</b> {text_refined}</div>\n'
    row += f'    </td>\n'
    row += f'  </tr>\n'

    rows.append(row)


# thead_html = '<thead>\n'
# thead_html += '  <tr>\n'
# thead_html += '    <th style="width: 300px; vertical-align: middle; text-align: center; background-color: white; z-index: 2;">\n'
# thead_html += '      Caption (Original / Refined + Aligned)\n'
# thead_html += '    </th>\n'
# thead_html += '    <th style="width: 190px; vertical-align: middle; text-align: center; background-color: white; z-index: 2;">\n'
# thead_html += '      Audio\n'
# thead_html += '    </th>\n'
# thead_html += '    <th style="width: 190px; vertical-align: middle; text-align: center; background-color: white; z-index: 2;">\n'
# thead_html += '      Non-Verbal Segments Detected\n'
# thead_html += '    </th>\n'
# thead_html += '  </tr>\n'
# thead_html += '</thead>'

# for text, text_refined, audio_path, audio_segment in zip(text_list, text_refined_list, audio_path_list, audio_segment_list):
#     # Highlight markers in text and refined text
#     def highlight(txt):
#         txt = txt.replace('[', '<span style="color: red;">[')
#         txt = txt.replace(']', ']</span>')
#         txt = txt.replace('<B>', '<span style="color: red;">&lt;B&gt;</span>')
#         txt = txt.replace('</B>', '<span style="color: red;">&lt;/B&gt;</span>')
#         return txt

#     text = highlight(text)
#     text_refined = highlight(text_refined)

#     row = f'  <tr>\n'
#     row += f'    <td style="width: 300px; vertical-align: middle; text-align: left; background-color: white; z-index: 1; white-space: normal; word-wrap: break-word;">\n'
#     row += f'      <div style="white-space: pre;"><b>                    Original:</b> {text}</div>\n'
#     row += f'      <div><b>Refined + Aligned:</b> {text_refined}</div>\n'
#     row += f'    </td>\n'

#     # Add audio column for the full audio
#     row += f'    <td style="vertical-align: middle; text-align: center;">\n'
#     row += f'      <audio controls style="width: 190px;">\n'
#     row += f'        <source src="{audio_path}" />\n'
#     row += f'        Your browser does not support the audio element.\n'
#     row += f'      </audio>\n'
#     row += f'    </td>\n'

#     # Add audio column for the non-verbal segment
#     row += f'    <td style="vertical-align: middle; text-align: center;">\n'
#     row += f'      <audio controls style="width: 190px;">\n'
#     row += f'        <source src="{audio_segment}" />\n'
#     row += f'        Your browser does not support the audio element.\n'
#     row += f'      </audio>\n'
#     row += f'    </td>\n'

#     row += f'  </tr>'
#     rows.append(row)

# Output the complete HTML (only the tbody part, for easier embedding)
tbody_html = '<tbody>\n' + '\n'.join(rows) + '\n</tbody>'
html_table = f'{thead_html}\n{tbody_html}'

# Output HTML to a file or stdout
print(html_table)
