import requests
from bs4 import BeautifulSoup


def print_secret_message(doc_url):
    """
    - Retrieve Google Doc containing: x-coordinate,
    character and y-coordinate.
    - Construct the character grid.
    - Print the secret message.
    """
    try:
        response = requests.get(doc_url, timeout=30)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error retrieving document: {e}")
        return
    soup = BeautifulSoup(response.text, "html.parser")
    points = {}
    for row in soup.find_all("tr"):
        cols = row.find_all("td")
        if len(cols) != 3:
            continue
        try:
            x = int(cols[0].get_text(strip=True))
            char = cols[1].get_text()
            y = int(cols[2].get_text(strip=True))
            points[(x, y)] = char
        except ValueError:
            continue
    if not points:
        print("No coordinate data found.")
        return
    max_x = max(x for x, _ in points)
    max_y = max(y for _, y in points)
    grid = [
        [" " for _ in range(max_x + 1)]
        for _ in range(max_y + 1)
    ]
    for (x, y), char in points.items():
        grid[y][x] = char
    for y in range(max_y, -1, -1):
        print("".join(grid[y]))


if __name__ == "__main__":
    url = (
        "https://docs.google.com/document/d/e/"
        "2PACX-1vSvM5gDlNvt7npYHhp_XfsJvuntUhq184By5xO_pA4b_"
        "gCWeXb6dM6ZxwN8rE6S4ghUsCj2VKR21oEP/pub"
    )

    print_secret_message(url)
