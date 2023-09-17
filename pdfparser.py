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
    print(resume_text)
  

    
