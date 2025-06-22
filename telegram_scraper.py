from telethon import TelegramClient
import csv
import os
from dotenv import load_dotenv
import re

# Load environment variables once
load_dotenv('.env')
api_id = os.getenv('TG_API_ID')
api_hash = os.getenv('TG_API_HASH')
phone = os.getenv('phone')

def extract_entities(message):
    entities = {}

    # PRODUCT: Look for lines with uppercase or English words + Size
    product_lines = [line for line in message.split('\n') if re.search(r'[A-Za-z]', line) and 'size' in line.lower()]
    # entities['PRODUCT_NAME'] = product_lines[0] if product_lines else None
    lines = [line.strip() for line in message.split('\n') if line.strip()]
    product_name = None
    for i, line in enumerate(lines):
        if 'size' in line.lower():
            if i > 0:
                product_name = f"{lines[i - 1]} {line}"
            else:
                product_name = line
            break
    entities['PRODUCT_NAME'] = product_name

    # LOCATION
    location_match = re.search(r'አድራሻ\s*(.*)', message)
    entities['LOCATION'] = location_match.group(1) if location_match else None

    # CONTACT INFO
    phones = re.findall(r'(?:\+251|0)(?:7\d{8}|9\d{8})', message)
    telegrams = re.findall(r'@[\w\d_]+', message)
    entities['CONTACT_INFO'] = phones + telegrams

    # HOUSE NUMBERS
    house_match = re.search(r'የቤት\s*ቁጥር\s*(.*)', message)
    entities['HOUSE_NO'] = house_match.group(1) if house_match else None

    # DELIVERY
    if 'delivery' in message.lower() or 'ትእዛዝ' in message:
        if 'ነፃ' in message or 'free' in message:
            entities['DELIVERY_FEE'] = 'Free'
        else:
            delivery_fee = re.findall(r'(\d+)\s*ብር.*(delivery|ትእዛዝ)', message)
            entities['DELIVERY_FEE'] = delivery_fee[0][0] + ' ብር' if delivery_fee else None

    return entities

def clean_message(text):
    # Remove telegram links
    text = re.sub(r'https?://t\.me/\S+', '', text)
    text = re.sub(r'[-_~]{3,}', '', text)
    # Remove emojis (including flags, icons)
    emoji_pattern = re.compile(
        "[" 
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F700-\U0001F77F"  # alchemical symbols
        "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
        "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
        "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
        "\U0001FA00-\U0001FA6F"  # Chess Symbols
        "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
        "\U00002702-\U000027B0"  # Dingbats
        "\u2600-\u26FF"          # Misc symbols
        "\u2700-\u27BF"          # Dingbats
        "™©®"                    # Remove TM, ©, ®
        "━⊰⊱┃〰"                # Custom decorative chars
        "]+", flags=re.UNICODE)
    text = emoji_pattern.sub(r'', text)
    
    # Remove duplicate lines
    lines = text.split('\n')
    unique_lines = list(dict.fromkeys([line.strip() for line in lines if line.strip()]))
    text = '\n'.join(unique_lines)

    return text

# Function to scrape data from a single channel

async def scrape_channel(client, channel_username, writer, media_dir):
    entity = await client.get_entity(channel_username)
    channel_title = entity.title  # Extract the channel's title
    async for message in client.iter_messages(entity, limit=6):
        media_path = None
        if message.media and hasattr(message.media, 'photo'):
            # Create a unique filename for the photo
            filename = f"{channel_username}_{message.id}.jpg"
            media_path = os.path.join(media_dir, filename)
            # Download the media to the specified directory if it's a photo
            await client.download_media(message.media, media_path)
        
        mes=clean_message(message.message)
      
        # Write the channel title along with other data
        if mes:
            #print(extract_entities(clean_message(message.message)))
            writer.writerow([channel_title, channel_username, message.id,mes, message.date, media_path])
            
        
# Initialize the client once
client = TelegramClient('scraping_session', api_id, api_hash)

async def main():
    await client.start()
    
    # Create a directory for media files
    media_dir = 'photos'
    os.makedirs(media_dir, exist_ok=True)

    # Open the CSV file and prepare the writer
    with open('telegram_data.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Channel Title', 'Channel Username', 'ID', 'Message', 'Date', 'Media Path'])  # Include channel title in the header
        
        # List of channels to scrape
        channels = [
            '@Shewabrand', 
           '@belaclassic',
           '@marakibrand',
           '@classybrands',
           '@Fashiontera'   
        ]
        
        # Iterate over channels and scrape data into the single CSV file
        for channel in channels:
            await scrape_channel(client, channel, writer, media_dir)
            print(f"Scraped data from {channel}")

with client:
    client.loop.run_until_complete(main())


