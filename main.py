import requests
from bs4 import BeautifulSoup
from termcolor import colored

# Set the target URL
url = 'Inter the web URL you want to find API'

# Send a GET request to the URL
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Look for URLs in <a> tags
api_endpoints = []
for link in soup.find_all('a'):
    if 'api' in str(link):
        api_endpoints.append((link['href'], colored('GET', '#0f6ab4')))

# Look for APIs in <form> tags
for form in soup.find_all('form'):
    if 'api' in str(form):
        method = form.get('method', 'GET')
        api_url = form.get('action')
        color = ''
        if method == 'POST':
            color = '#10a54a'
        elif method == 'PUT':
            color = '#c5862b'
        elif method == 'DELETE':
            color = '#a41e22'
        elif method == 'PATCH':
            color = '#D38042'
        elif method == 'HEAD':
            color = '#ffd20f'
        api_endpoints.append((api_url, colored(method, color)))

        # Look for <input> tags
        for input_tag in form.find_all('input'):
            input_type = input_tag.get('type', 'text')
            input_name = input_tag.get('name', '')
            if input_type == 'hidden' and 'csrf' not in input_name:
                api_endpoints[-1] = (api_endpoints[-1][0], api_endpoints[-1][1], {input_name: input_tag.get('value', '')})

        # Look for <button> tags
        for button_tag in form.find_all('button'):
            button_name = button_tag.get('name', '')
            if button_name:
                if len(api_endpoints[-1]) < 3:
                    api_endpoints[-1] = (api_endpoints[-1][0], api_endpoints[-1][1], {})
                api_endpoints[-1][2][button_name] = button_tag.get('value', '')

# Print the API endpoints and their methods
for api_endpoint in api_endpoints:
    print(f"{api_endpoint[1]} {api_endpoint[0]}")
    if len(api_endpoint) == 3 and api_endpoint[2]:
        print(f"Payload: {api_endpoint[2]}")
    print()
