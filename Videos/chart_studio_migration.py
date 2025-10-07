import requests
import json
# https://youtu.be/ioS5u2XDxxE


def fetch_plotly_data(url):
    """
    Fetch data from a Plotly Chart Studio URL.

    Args:
        url (str): The Plotly Chart Studio URL (e.g., https://chart-studio.plotly.com/~AndyWoods/15.json)

    Returns:
        dict: The JSON data from the chart
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes

        data = response.json()
        return data

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return None


def main():
    # Prompt user for URL
    print("Enter the Plotly Chart Studio URL:")
    url = input("> ").strip()

    # Fetch the data
    print(f"\nFetching data from: {url}")
    data = fetch_plotly_data(url)

    if data:
        print("\n✓ Data fetched successfully!")
        print(f"\nData structure: {type(data)}")
        print(f"Top-level keys: {list(data.keys()) if isinstance(data, dict) else 'N/A'}")

        # You can now work with the data
        # Example: Access plot data
        if 'data' in data:
            print(f"\nNumber of traces: {len(data['data'])}")

        # Return data for further use
        return data
    else:
        print("\n✗ Failed to fetch data")
        return None


if __name__ == "__main__":
    chart_data = main()

    print(json.dumps(chart_data, indent=2))
