import repository, config
import requests
from datetime import datetime
import json
import csv

API_URL = "https://XXXXX-advocate.symplicity.com/api/public/v1/incidents"
API_KEY = "YOUR_KEY"

repo = repository.Repository()
config = config.Config()


def fetch_data(start_date, end_date):
    with open('C:\\PATH_TO_FILE\\filename.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['IR#', 'StudentID', 'CreateDate', 'IncidentDate', 'IsArchived'])

        headers = {"Authorization": f"Token {API_KEY}"}
        params = {
            "created": json.dumps([start_date, end_date]),
            "perPage": 100
        }

        page = 1
        isLast = False;

        while True:
            params["page"] = page

            response = requests.get(API_URL, headers = headers, params = params)

            if response.status_code == 200:
                data = response.json()

                if len(data.get("models", [])) < params["perPage"]:
                    isLast = True
                page += 1

                if not data or "models" not in data:
                    print("no data to parse")
                    return []

                for record in data["models"]:
                    record_number = record.get("reportNumber")
                    create_date = record.get("created")
                    incident_date = record.get("incidentDate")
                    is_archived = record.get("archived")

                # need the "parent" incident report only, which has 10 digit record number
                if len(record_number) == 10:
                    for student in record.get("student", []):
                        student_rcd = student["label"]

                        # label is formatted as "student name, , (xxxxxxxxx)"
                        empl_id = student_rcd[-10:-1]

                        writer.writerow([record_number, empl_id, create_date, incident_date, False])

            else:
                print(f"Error:{response.status_code}")
                return None

            if isLast:
                break


def main():
    start_end_date = repo.get_dates()
    start_date, end_date = start_end_date[0]

    api_data = fetch_data(start_date, end_date)

if __name__ == "__main__":
    main()