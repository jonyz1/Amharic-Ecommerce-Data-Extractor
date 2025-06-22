import csv

def csv_to_conll(input_csv='labeled_tokens.csv', output_txt='conll_dataset.txt'):
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


# import re
# import csv

# def auto_label_token(token, next_token=None):
#     # Telegram username
#     # if re.match(r'^@[\w\d_]+$', token):
#     #     return 'O'
    
#     # # Phone numbers: starting with +251 or 09 and 9 more digits
#     # if re.match(r'^(?:\+251|0)(?:9|7)\d{8}$', token):
#     #     return 'O'
    
#     # Price numbers followed by 'ብር' or 'Br' or 'ETB' (next token)
#     if token.isdigit() and next_token and next_token.lower() in ['ብር', 'br', 'etb']:
#         return 'B-PRICE'
#     if token.lower()=='price' and next_token and next_token.isdigit():
#         return 'B-PRICE'
#     # Just standalone numbers that look like prices (optional, comment if unsure)
#     # if token.isdigit():
#     #     return 'B-PRICE'
    
#     return 'O'


# def process_csv(input_csv, output_csv):
#     with open(input_csv, 'r', encoding='utf-8') as f_in, \
#          open(output_csv, 'w', encoding='utf-8', newline='') as f_out:
        
#         reader = csv.reader(f_in)
#         writer = csv.writer(f_out)
#         rows = list(reader)

#         if rows and rows[0][0].lower() == 'token':
#             rows = rows[1:]  # Skip header

#         i = 0
#         while i < len(rows):
#             # Skip and write a blank line for message separator
#             if not rows[i] or not rows[i][0].strip():
#                 writer.writerow([])
#                 i += 1
#                 continue
            
#             # Start of a new message
#             msg_tokens = []
#             while i < len(rows) and rows[i] and rows[i][0].strip():
#                 msg_tokens.append(rows[i][0].strip())
#                 i += 1

#             for j, token in enumerate(msg_tokens):
#                 next_token = msg_tokens[j+1] if j+1 < len(msg_tokens) else None

#                 if j == 0:
#                     label = 'B-Product'
#                 elif j in [1, 2, 3]:
#                     label = 'I-Product'
#                 else:
#                     label = auto_label_token(token, next_token)

#                 writer.writerow([token, label])
            
#             writer.writerow([])  

# if __name__ == "__main__":
#     input_file = 'tokens_for_labeling.csv'      # Replace with your input token CSV file path
#     output_file = 'labeled_tokens.csv'
#     process_csv(input_file, output_file)
#     print(f"Auto-labeling done. Output saved to {output_file}")
