"""
Python file that takes in a resume in PDF form and extracts key information. 

author: Omer Ahmed (omerahmed05) 
vesion: 09/17/2023
"""

# Imports
from pypdf import PdfReader as pdfReader
import json
import re

reader = pdfReader(r"C:\Users\omera\Downloads\Resume (1).pdf")


# Loop through pages
for i in range(len(reader.pages)):
  page = reader.pages[i]

  # Create resume file
  open("resume.txt", "w+")

  # Write to resume txt file
  with open("resume.txt", "w", encoding="utf-8") as resume_file:
    text = page.extract_text()
    resume_file.write(text)

  # Reading resume txt file
  with open("resume.txt", "r", encoding="utf-8") as resume:
    resume_text = resume.read()
    print(resume_text)

# Candidate Info
major = ""
candidate_skills = []
# Iterating through JSON file
with open('career-skills.json') as career_skills_file:
    career_skills_data = json.load(career_skills_file)
    
    # Determining Major
    if ("Electrical Engineering" in resume_text or "ElectricalEngineering" in resume_text):
       major = "Electrical Engineering"
    elif ("Computer Engineering" in resume_text or "ComputerEngineering" in resume_text):
       major = "Computer Engineering"
    elif ("Computer Science" in resume_text or "ComputerScience" in resume_text):
       major = "Computer Science"
    else:
       major = "Unknown"
       raise Exception("Unable to determine major!")

    # Determining technical skills
    for skill_type, skills in career_skills_data[major].items():
        for skill in skills:
            if skill in resume_text:
                if (len(skill) == 1):
                   if (resume_text[resume_text.index(skill) + 1] == ' ' or resume_text[resume_text.index(skill) + 1].isupper()):
                      candidate_skills.append(skill)
                   elif (resume_text[resume_text.index(skill) + 1].islower()):
                      continue
                   else:
                      raise Exception("Unable to categorize skill")
                else:
                   candidate_skills.append(skill)

# Print candidate information
print("Major:", major)
print("Candidate Skills:", candidate_skills)

# Finding GPA
gpa = None

# Regular expression pattern to match a decimal number
pattern = r'\d+\.\d+'

# Find all matches in the input string
matches = re.findall(pattern, resume_text)

# Print the first match (if any)
if matches:
    gpa = float(matches[0])
else:
    print("No decimal number found in the string.")

if (gpa != None):
   if (gpa < 3):
      print("Get that GPA up!")
   elif (gpa >= 3 and gpa < 3.4):
      print("Your GPA is ideal for jobs in this field")
   else:
      print("You're GPA really makes you stand out!")
else:
   raise Exception("Unable to find GPA in resume.")

# Rating
