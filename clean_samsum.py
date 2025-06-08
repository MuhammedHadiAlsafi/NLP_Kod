import pandas as pd
import re
import os

def replace_emoticons(text):
    if not isinstance(text, str):
        return text

    replacements = {
        r'(:-\)|:\)|😊)': '[HAPPY]',
        r'(:-\(|:\()': '[SAD]',
        r'(:D|xD|😂)': '[LAUGH]',
        r'(:-/|-_-)': '[CONFUSED]',
        r'(👍)': '[OK]',
        r'(;\))': '[WINK]',
        r'(🙊)': '[SHY]'
    }

    for pattern, token in replacements.items():
        text = re.sub(pattern, token, text, flags=re.IGNORECASE)

    return text

def clean_text(text):
    if not isinstance(text, str):
        return text

    # Normalize boşluklar
    text = re.sub(r'\s+', ' ', text)

    # Çoklu tırnak sadeleştirme
    text = re.sub(r'"{2,}', '"', text)

    # Boşlukları temizle
    text = re.sub(r'\s+([.,;:!?])', r'\1', text)

    # Baş-son boşluklar
    text = text.strip()

    # Emoticon ve emoji yer tutucuya çevir
    text = replace_emoticons(text)

    return text

def clean_dialogue(dialogue):
    if not isinstance(dialogue, str):
        return dialogue

    dialogue = normalize_speakers(dialogue)  # 🔸 Bu satır kritik

    lines = dialogue.split('\n')
    cleaned_lines = []

    for line in lines:
        if not line.strip():
            continue
        cleaned_line = clean_text(line)
        if cleaned_line:
            cleaned_lines.append(cleaned_line)

    return '\n'.join(cleaned_lines)

def normalize_speakers(dialogue):
    if not isinstance(dialogue, str):
        return dialogue

    speaker_map = {}
    current_id = 1
    normalized_lines = []

    lines = dialogue.split('\n')

    for line in lines:
        # Eşleşme: "Name: metin"
        match = re.match(r'^([^:]+):\s*(.*)', line)
        if match:
            speaker, utterance = match.groups()
            speaker = speaker.strip()

            if speaker not in speaker_map:
                speaker_map[speaker] = f"#Person{current_id}#"
                current_id += 1

            normalized_line = f"{speaker_map[speaker]}: {utterance.strip()}"
            normalized_lines.append(normalized_line)
        else:
            # Konuşmacı etiketi olmayan satırlar direkt eklenir
            normalized_lines.append(line.strip())

    return '\n'.join(normalized_lines)

def contains_file_token(text):
    return bool(re.search(r'<file_\w+>', str(text)))

def process_file(input_file, output_file):
    print(f"Processing {input_file}...")

    # Veri setini oku
    df = pd.read_csv(input_file)

    # <file_...> içeren diyalogları sil
    df = df[~df['dialogue'].apply(contains_file_token)]

    # Temizleme işlemleri
    df['summary'] = df['summary'].apply(clean_text)
    df['dialogue'] = df['dialogue'].apply(clean_dialogue)

    # Eksik/boş olanları çıkar
    df = df.dropna(subset=['summary', 'dialogue'])

    # Temizlenmiş veriyi kaydet
    df.to_csv(output_file, index=False)
    print(f"Cleaned data saved to {output_file}")

def main():
    output_dir = "cleaned_data"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    samsum_files = [
        "DataSet/samsum(train).csv",
        "DataSet/samsum(test).csv",
        "DataSet/samsum(val).csv"
    ]

    for input_file in samsum_files:
        filename = os.path.basename(input_file)
        output_file = os.path.join(output_dir, f"cleaned_{filename}")
        process_file(input_file, output_file)

    print("All files have been processed!")

if __name__ == "__main__":
    main()
