from datetime import datetime

def generate_filename(data: dict) -> str:
    date = datetime.today().strftime("%Y-%m-%d")
    return f"{date}_{data['type']}_{data['counterparty']}.pdf"
