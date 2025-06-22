import csv
import re

def tokenize_amharic_text(text):
    return re.findall(r'[@#]?\w+|[,:፡]', text, re.UNICODE)

def create_token_csv(input_csv='telegram_data.csv', output_csv='tokens_for_labeling.csv'):
    with open(input_csv, 'r', encoding='utf-8') as infile, \
         open(output_csv, 'w', encoding='utf-8', newline='') as outfile:

        reader = csv.DictReader(infile)
        writer = csv.writer(outfile)
        writer.writerow(['Token', 'Label'])

        for row in reader:
            message = row.get('Message', '')
            tokens = tokenize_amharic_text(message)
            for token in tokens:
                writer.writerow([token, ''])
            writer.writerow([])  # Empty line between messages

    print(f"✅ Tokens written to {output_csv}")

if __name__ == "__main__":
    create_token_csv()
