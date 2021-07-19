from bs4 import BeautifulSoup
import requests
import time
import pandas as pd
import io

def find_jobs():
	html_text = requests.get(f"https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords={familiar_skill}&txtLocation=").text
	soup = BeautifulSoup(html_text, "lxml")
	jobs = soup.find_all("li", class_="clearfix job-bx wht-shd-bx")

	column_names = ["Company Name", "Experience Required", "Location", "Required Skills", "Job Description", "More Info"]
	df = pd.DataFrame(columns=column_names)

	with io.open(f"./jobs.txt", "w", encoding="utf-8") as f:
		for job in jobs:
			published_date = job.find("span", class_="sim-posted").span.text
			
			company_name = job.find("h3", class_="joblist-comp-name").text.strip()
			key_skills = job.find("span", class_="srp-skills").text.strip()		

			more_info = job.header.h2.a["href"]
			html_text = requests.get(more_info).text
			page = BeautifulSoup(html_text, "lxml")
			
			experience = page.find("ul", class_="top-jd-dtl clearfix").li.text.replace("card_travel", "").strip()[0:8].strip() + " yrs"
			pay = page.find("ul", class_="top-jd-dtl clearfix").select("ul > li")[1].text[1:].strip()
			location = page.find("ul", class_="top-jd-dtl clearfix").select("ul > li")[2].text.replace("location_on", "").strip()
			description = page.find("div", class_="jd-desc job-description-main").text.replace("Job Description", "").strip()

			df.loc[len(df.index)] = [company_name, experience, location, key_skills, description, more_info]
			f.write(f"Company Name: {company_name}\n")
			f.write(f"Required Skills: {key_skills}\n")
			f.write(f"Experience Required: {experience}\n")
			f.write(f"Expected Pay: {pay}\n")
			f.write(f"Location: {location}\n")
			f.write(f"Job Description: {description}\n")
			f.write(f"More Info: {more_info} \n\n\n\n")
	df.to_csv("jobs.csv", index=False)
	print(f"Data Updated!")

if __name__ == "__main__":
	print("Put some skill that you are familiar with")
	familiar_skill = input(">")
	print("Enter refresh time (hours)")
	time_wait = int(input(">"))
	print(f"Filtering out {familiar_skill}...")
	while True:
		find_jobs();
		print(f"Waiting {time_wait} hours...")
		time.sleep(time_wait*60*60)
