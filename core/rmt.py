import requests
from bs4 import BeautifulSoup

def fetch_top5_prices(url="https://www.yxdr.com/bijiaqi/dnf/youxibi/shanghai2"):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table")
    if not table:
        return []

    # Find the header row with "单价 (1元比例)"
    headers = [th.get_text(strip=True) for th in table.find_all("th")]
    if "单价 (1元比例)" not in headers:
        return []

    # Find the index of the header
    price_idx = headers.index("单价 (1元比例)")

    # Get all data rows
    rows = table.find_all("tr")[1:]  # skip header
    results = []
    for row in rows:
        cols = [td.get_text(strip=True) for td in row.find_all("td")]
        if len(cols) > price_idx:
            results.append(cols[price_idx])
        if len(results) >= 5:
            break
    return results

# Example usage:
if __name__ == "__main__":
    top5 = fetch_top5_prices()
    print(top5)