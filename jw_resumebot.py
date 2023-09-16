"""
Discord bot which reads in the resume pdf of a discord user

author: Omer Ahmed (omerahmed05), Jonathan Woodbury (jonathanw22)
vesion: 09/16/2023
"""

import discord
from pypdf import PdfReader as pdfReader
# import dotenv
# import os
# from dotenv import load_dotenv

# Creates a bot that registers hash commands
# dotenv.load_dotenv() # loads variables from env file

# Code for pdfparser

# Getting location of resume and reading it
def parse_pdf(pdf_path):
    # path = input("Enter the PATH of the resume: ")
    reader = pdfReader(pdf_path)

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
    # await ctx.send(to_file(resume))



# Code for discord bot
bot = discord.Bot()

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!!!")

# Bot responds with a greeting
@bot.slash_command(guild_ids=[1152451000079220897], description = "Say hello to the bot")
async def hello(ctx):
    await ctx.respond("Hello! Happy Hackathon!!!")

# Tests whether pdf file was read
@bot.slash_command(guild_ids=[1152451000079220897], description = "Reads in a pdf file & outputs it back into channel")
async def test_parsefile(ctx, pdf_path):
    await ctx.respond("Reading PDF...")

# Bot takes in the pdf from discord member
@bot.slash_command(guild_ids=[1152451000079220897], description = "Reads in a pdf file")
async def parsefile(ctx, pdf_path):
    await ctx.respond("Parsing PDF...")
    parse_pdf(pdf_path)

# bot.run(str(os.getenv("TOKEN")))
bot.run("Insert TOKEN here")