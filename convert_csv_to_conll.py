import csv

def csv_to_conll(input_csv='tokens_for_labeling.csv', output_txt='conll_dataset.txt'):
    with open(input_csv, 'r', encoding='utf-8') as infile, \
         open(output_txt, 'w', encoding='utf-8') as outfile:

        reader = csv.reader(infile)
        next(reader)  # Skip header

        for row in reader:
            if not row or not row[0].strip():
                outfile.write('\n')
            else:
                token, label = row[0], row[1] if len(row) > 1 else 'O'
                outfile.write(f"{token}\t{label if label else 'O'}\n")

    print(f"✅ CoNLL file saved to {output_txt}")

if __name__ == "__main__":
    csv_to_conll()
