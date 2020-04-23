import csv
import os


def save_to_csv(jobs):
    file = open("C:\\Users\\KSM\\Documents\\Github\\crawling_py\\jobs.csv",
                mode="w", encoding="UTF-8", newline="")
    writer = csv.writer(file)
    writer.writerow(["Name", "Company", "location", "link"])
    for job in jobs:
        writer.writerow(list(job.values()))
    return None
