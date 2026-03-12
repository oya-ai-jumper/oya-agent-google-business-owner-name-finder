import os
import json
import httpx
import re
from bs4 import BeautifulSoup


def extract_domain(url):
    try:
        domain = re.search(r"(?:https?:\/\/)?(?:www\.)?([a-zA-Z0-9.-]+)\/?", url).group(1)
        return domain
    except:
        return None


def hunter_io_lookup(domain, api_key):
    try:
        url = f"https://api.hunter.io/v2/domain-search?domain={domain}&api_key={api_key}"
        response = httpx.get(url)
        response.raise_for_status()
        data = response.json()

        if data and data.get("data") and data["data"].get("emails"):
            emails = data["data"]["emails"]
            for email in emails:
                if email.get("position") and "owner" in email["position"].lower():
                    return email["first_name"] + " " + email["last_name"]
        return None
    except Exception as e:
        print(f"Error during Hunter.io lookup: {e}")
        return None


def web_search(query):
    try:
        url = f"https://www.google.com/search?q={query}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
        response = httpx.get(url, headers=headers, follow_redirects=True)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error during web search: {e}")
        return None


def extract_owner_name_from_html(html, business_name):
    try:
        soup = BeautifulSoup(html, "html.parser")
        # Look for patterns like "Owner: [Name]" or "[Name], Owner"
        patterns = [
            r"Owner:\s*([A-Za-z]+\s+[A-Za-z]+)",
            r"([A-Za-z]+\s+[A-Za-z]+),\s*Owner",
            r"([A-Za-z]+\s+[A-Za-z]+)\s*-\s*Owner",
            r"([A-Za-z]+\s+[A-Za-z]+)\s*\(Owner\)",
            r"Owner of\s+([A-Za-z]+\s+[A-Za-z]+)"
        ]

        for pattern in patterns:
            matches = re.findall(pattern, html)
            if matches:
                for match in matches:
                    return match  # Return the first match
        return None

    except Exception as e:
        print(f"Error extracting owner name from HTML: {e}")
        return None


def main():
    try:
        input_json = json.loads(os.environ["INPUT_JSON"])
        placeId = input_json.get("placeId")
        website = input_json.get("website")
        address = input_json.get("address")
        business_name = input_json.get("business_name")
        hunterio_api_key = os.environ.get("HUNTERIO_API_KEY")

        owner_name = None

        if website and hunterio_api_key:
            domain = extract_domain(website)
            if domain:
                owner_name = hunter_io_lookup(domain, hunterio_api_key)

        if not owner_name:
            search_query = f"{business_name} owner"
            if address:
                search_query += f" {address}"

            search_results = web_search(search_query)
            if search_results:
                owner_name = extract_owner_name_from_html(search_results, business_name)

        if owner_name:
            print(json.dumps(owner_name))
        else:
            print(json.dumps("Not found"))

    except Exception as e:
        print(json.dumps({"error": str(e)}))


if __name__ == "__main__":
    main()