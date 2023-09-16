"""
Python file that takes in a resume in PDF form and extracts key information. 

author: Omer Ahmed (omerahmed05) 
vesion: 09/16/2023
"""

# Imports
from pypdf import PdfReader as pdfReader

# Getting location of resume and reading it
path = input("Enter the PATH of the resume: ")
reader = pdfReader(path)

# Matchability variables
skills = {
    'programming_languages': [],
    'frameworks': [],
    'OS': [],
}

grade = None # Year of candidate
gpa = None # GPA of candidate
citizen = None # Citizenship status of candidate
degree = None # CS, CPE, or EE degree?
experience = None # Experience of candidate (determined by internships and jobs)

# Loop through pages
for i in range(len(reader.pages)):
    page = reader.pages[i]

    # Create resume file
    open("resume", "w+")

    # Write to resume txt file
    with open("resume", "w", encoding="utf-8") as resume:
        text = page.extract_text()
        resume.write(text)

    # Reading resume txt file
    with open("resume", "r", encoding="utf-8") as resume:
        for line in resume:
            print(line)