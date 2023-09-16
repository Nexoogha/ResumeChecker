"""
Python file that takes in a resume in PDF form and extracts key information. 

author: Omer Ahmed (omerahmed05) 
vesion: 09/16/2023
"""

# Imports
from pypdf import PdfReader as pdfReader
import openai
import os

reader = pdfReader(r"resume_path")

# Matchability variables
skills = {
  'programming_languages': [],
  'frameworks': [],
  'OS': [],
}

grade = None # Year of candidate
gpa = 0 # GPA of candidate
citizen = None # Citizenship status of candidate
degree = None # CS, CPE, or EE degree?
experience = None # Experience of candidate (determined by internships and jobs)

# Setting up ChatGPT
openai.api_key = "yourapikey"

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
    resume_text = "".join(resume.readlines())

    # Request GPT-3.5 Turbo to extract technical skills from the resume text
    prompt = "Please extract technical skills and courses from the given resume text:\n\n" + resume_text
    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
          {"role": "system", "content": prompt},
      ],
      temperature = 0
    )

    candidate_knowledge = completion.choices[0].message.content

# Matchability Percentage = (Total Relevant Skills / Total Required Skills) ...

