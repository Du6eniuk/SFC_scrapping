import requests 
from bs4 import BeautifulSoup
import pandas as pd

# Function to scrape the website
def get_url(link):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        response = requests.get(link, headers=headers)
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            b_tag = soup.find('b', text='Website:')
            if b_tag:
                td_tag = b_tag.find_next('td')
                if td_tag:
                    address = td_tag.text.strip()
                    return address
                else:
                    return "Website address not found"
            else:
                return "Website label not found"
        else:
            return f"Request failed with status code {response.status_code}"
    except requests.RequestException as e:
        return f"Request failed: {e}"

# Function to process a list of URLs and save the results in a DataFrame
def process_urls_from_csv(input_csv, output_csv):
    # Read the CSV file into a DataFrame
    input_df = pd.read_csv(input_csv)

    # Assuming the column containing URLs is named 'URL'
    data = []
    for url in input_df['URL']:
        address = get_url(url)
        data.append({'URL': url, 'Address': address})
    
    # Creating a DataFrame
    output_df = pd.DataFrame(data)

    # Save the DataFrame to a CSV file
    output_df.to_csv(output_csv, index=False)

    return output_df

# Example usage
input_csv = 'SFC_input.csv'  
output_csv = 'SFC_output.csv' 

result_df = process_urls_from_csv(input_csv, output_csv)