"""
Program: pyfuzz.py
Date Created: 14-Sep-24
Date Last Modified: 14-Sep-24
Purpose: To assist ethical hacking (penetration testing) in web application exploitation through the use of fuzzing.
"""
import argparse
import requests

def run_requests(url, method, wordlist, status = "*", output=""):
    method = method.upper()

    with open(wordlist, 'r') as words:
        for word in words:
            word = word.strip()
            fuzz_url = f"{url}/{word}"
            
            try:
                if method == 'GET':
                    response = requests.get(fuzz_url)
                elif method == 'POST':
                    response = requests.post(url, data={"fuzz": word})
                elif method == 'PUT':
                    response = requests.put(url, data={"fuzz": word})
                elif method == 'HEAD':
                    response = requests.head(fuzz_url)
                else:
                    print(f"Unsupported HTTP method: {method}")
                    return
                
                if status == "*":
                # Print status and response text
                    print(f"Status Code: {response.status_code} | Fuzzed URL: {fuzz_url}")
                    if output != "":
                        open(output, 'a').write(f'Status Code: {response.status_code} | Fuzzed URL: {fuzz_url}\n')

                elif status != "*":
                    if response.status_code == int(status):
                        print(f"Status Code: {response.status_code} | Fuzzed URL: {fuzz_url}")
                        if output != "":
                            open(output, 'a').write(f'Status Code: {response.status_code} | Fuzzed URL: {fuzz_url}\n')
                    else:
                        pass
                
            except requests.exceptions.RequestException as e:
                print(f"Error with word '{word}': {e}")

def main():
    print("Running pyfuzz!")
    
    parser = argparse.ArgumentParser(
        prog='pyfuzz',
        description='Assists web application penetration testing through fuzzing techniques'
    )
    
    parser.add_argument('-u', '--url', help="URL to send fuzzing requests to", required=True)
    parser.add_argument('-r', '--request', help='Type of HTTP request method (POST, GET, PUT, HEAD)', required=True)
    parser.add_argument('-w', '--wordlist', help='Wordlist for fuzzing', required=True)
    parser.add_argument('-s', '--status', help="Filters the status based on whatever code you provide. (No filter by default)")
    parser.add_argument('-o', '--output', help="Outputs results to a the file specified")
    
    args = parser.parse_args()
    
    run_requests(url=args.url, method=args.request, wordlist=args.wordlist, status=args.status, output=args.output)
    
if __name__ == "__main__":
    main()
