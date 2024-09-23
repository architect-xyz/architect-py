import requests
from bs4 import BeautifulSoup, element


from json_ws_server import JsonWsServer


def scrape_tradingview_indices(url: str):
    # url = "https://www.tradingview.com/markets/indices/quotes-all/"
    # url = https://www.tradingview.com/markets/indices/quotes-us/

    # Set headers to mimic a browser request
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0",
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to retrieve data: {response.status_code}")
        return

    soup = BeautifulSoup(response.content, "html.parser")

    indices_data = []

    # Find the table containing the indices data
    table = soup.find("table", {"class": "table-Ngq2xrcG"})

    if not isinstance(table, element.Tag):
        print("Failed to find the data table.")
        return

    # Extract table headers
    headers = [header.text for header in table.find_all("th")]

    # Extract table rows
    rows = table.find_all("tr")[1:]  # Skip the header row

    for row in rows:
        columns = row.find_all("td")
        index_data = {headers[i]: columns[i].text.strip() for i in range(len(columns))}
        indices_data.append(index_data)

    # Print or store the extracted data
    for index in indices_data:
        print(index)


def start_service():
    url = "https://www.tradingview.com/markets/indices/quotes-us/"
    scrape_tradingview_indices(url)

    JsonWsServer().start()


if __name__ == "__main__":
    url = https://www.tradingview.com/markets/indices/quotes-us/
    scrape_tradingview_indices(url)