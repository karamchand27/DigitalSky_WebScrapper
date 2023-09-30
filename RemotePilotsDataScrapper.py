import requests
import csv

# Define the base URL of the API endpoint
base_url = "https://digitalsky.dgca.gov.in/digital-sky/public/pilots/certified"

# Define the headers with the required "source" header
headers = {
    "source": "https://digitalsky.dgca.gov.in/remote_pilots"
}

# Initialize an empty list to store the relevant data
relevant_data = []

# Initialize page_number to 1
page_number = 1

# Fetch data until there are no more pages
while True:
    # Define the URL for the current page
    page_url = f"{base_url}?pageNo={page_number}&size=1500"

    # Send an HTTP GET request to the URL with the headers
    response = requests.get(page_url, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        PilotData = response.json()

        # Extract the relevant data and append it to the list
        for pilot in PilotData.get('pilotDataViewModelList', []):
            # Check if Gender is missing and set it to "Male"
            gender = pilot.get('gender', 'Male')  # Set default to "Male"

            relevant_data.append({
                "S.No.": pilot.get('serialNumber', ''),
                "Name": pilot.get('name', ''),
                "Gender": gender,
                "RPC Number": pilot.get('pilotCertificateNumber', ''),
                "Issued By": pilot.get('issuedBy', ''),
                "Issued On": pilot.get('issuedOn', '')
            })

        # Check if there are more pages to fetch
        if page_number >= PilotData.get('totalPageCount', 0):
            break  # Break the loop if there are no more pages
        else:
            page_number += 1  # Move to the next page
    else:
        # Handle the case where the request was not successful
        print(f"Failed to retrieve data for page {page_number}. Status code: {response.status_code}")

# Now, relevant_data contains the extracted data from all pages, and the loop stops automatically

# Save the extracted data to a CSV file
csv_file_name = 'pilot_data.csv'
with open(csv_file_name, 'w', newline='') as csv_file:
    fieldnames = ["S.No.", "Name", "Gender", "RPC Number", "Issued By", "Issued On"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()  # Write the header row
    for data in relevant_data:
        writer.writerow(data)  # Write data rows

print(f"Data saved to '{csv_file_name}' file.")
