"""
Contains the ResumeCog class.

author: Omer Ahmed (omerahmed05), Muhammad Nabil (myn55), Jonathan Woodbury (jonathanw22), Kishore (kishore09)
version: 09/16/2023
"""

import discord, nltk, json, re
from discord.commands import slash_command
from nltk.corpus import stopwords
from .base_cog import CCog
from pypdf import PdfReader
from datetime import datetime
from collections import Counter

with open('resources\\career-skills.json', 'r') as f:
    CAREER_SKILLS = json.load(f)

with open('resources\\academic-skills.json', 'r') as f:
    ACADEMIC_SKILLS = json.load(f)

with open('resources\\social-skills.json', 'r') as f:
    SOCIAL_SKILLS = json.load(f)

def extract_key_terms(text : str):
    """
    Extracts all known/hypothesized nouns and adjectives from the given text.
    """

    # Tokenize into individual words
    tokens = nltk.word_tokenize(text)

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word.lower() not in stop_words]

    # Get nouns and adjectives
    tagged = nltk.pos_tag(filtered_tokens)
    key_terms = [word for word, pos in tagged if pos.startswith('N') or pos.startswith('J')]

    return key_terms

class ResumeCog(CCog):
    """
    Contains the main functions of the bot such as parsing resumes.
    """

    @slash_command(name="check", description="Checks your resume.")
    async def check(self, ctx : discord.ApplicationContext,
                   resume : discord.Option(discord.SlashCommandOptionType.attachment,
                                           name="resume",
                                           description="The resume to check (PDF format)"),
                    career : discord.Option(discord.SlashCommandOptionType.string,
                                            name="career",
                                            description="The discipline of the career to check the resume against.",
                                            choices=CAREER_SKILLS.keys())):
        """
        Checks the resume and compares it to the given career.
        """

        # Check if it's a PDF file
        url = resume.url
        if not url.endswith('pdf'):
            await ctx.respond(content="The file you provided is not a PDF.", ephemeral=True)
            return

        content = await resume.read()

        # Write the PDF
        with open('metadata.pdf', 'wb') as pdf:
            pdf.write(content)
        
        # Now check it
        with open('metadata.pdf', 'rb') as pdf:
            reader = PdfReader(pdf)
            key_terms = []
            pdfText = '\n\n'.join([page.extract_text() for page in reader.pages])
            key_terms = extract_key_terms(pdfText)

            key_terms = [x.lower() for x in key_terms]

            infoBlob = f"# [{resume.filename}]({url}) x {career}\n{len(key_terms)} tokens scraped from PDF.\n"

            infoEmbed = discord.Embed(
                title=f"{resume.filename} x {career}",
                color=discord.Colour(0xffffff),
                description=f"{len(key_terms)} tokens scraped from PDF.\nDisplaying matching skills:"
            )
            infoEmbed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)

            # Check career skills
            infoBlob += "## Career Skills\n"
            count = {}
            for category in CAREER_SKILLS[career].keys():
                count[category] = []
                for skill in CAREER_SKILLS[career][category]:
                    if skill.lower() in key_terms:
                        count[category].append(skill)
                skills = count[category]

                embedSkills = (', '.join(skills) if len(skills) > 0 else 'None')
                infoEmbed.add_field(name=category, value=embedSkills, inline=False)

                """blob_career_skills = ('\n'.join([' - '+s for s in skills]) if len(skills) > 0 else ' - *None*')
                infoBlob += (f"- **{category}**:\n{blob_career_skills}\n")"""

            # Check social skills
            infoBlob += "## Social Skills\n"
            count['Social Skills'] = []
            for skill in SOCIAL_SKILLS:
                if skill.lower() in key_terms:
                    count['Social Skills'].append(skill)
            infoEmbed.add_field(
                name='Social Skills',
                value=(', '.join(count['Social Skills']) if len(count['Social Skills']) > 0 else 'None'),
            )
            """skills = count['Social Skills']

            blob_social_skills = ('\n'.join([' - '+s for s in skills]) if len(skills) > 0 else ' - *None*')
            infoBlob += (f"- **Social Skills**:\n{blob_social_skills}\n")"""

            # Check academic skills
            infoBlob += "## Academic Skills\n"
            count['Academic Skills'] = []
            for skill in ACADEMIC_SKILLS:
                if skill.lower() in key_terms:
                    count['Academic Skills'].append(skill)
            # Cheeky spacing trick
            infoEmbed.add_field(name=" ", value="", inline=False )
            infoEmbed.add_field(
                name='Academic Skills',
                value=(', '.join(count['Academic Skills']) if len(count['Academic Skills']) > 0 else 'None'),
            )
            infoEmbed.add_field(name=" ", value="", inline=False )
            """skills = count['Academic Skills']

            blob_academic_skills = ('\n'.join([' - '+s for s in skills]) if len(skills) > 0 else ' - *None*')
            infoBlob += (f"- **Academic Skills**:\n{blob_academic_skills}\n")"""

            # Include totals
            total_career_skills = sum([len(count[category]) for category in CAREER_SKILLS[career].keys()])
            total_social_skills = len(count['Social Skills'])
            total_academic_skills = len(count['Academic Skills'])
            infoEmbed.add_field(
                name=f"{total_career_skills} career/technical skills",
                value="",
            )
            infoEmbed.add_field(
                name=f"{total_social_skills} social skills",
                value=""
            )
            infoEmbed.add_field(
                name=f"{total_academic_skills} academic skills",
                value=""
            )
            infoEmbed.add_field(name=" ", value="", inline=False )
            #infoBlob += f"\n*__{total_career_skills} total career skills, {total_social_skills} total social skills, {total_academic_skills} total academic skills__*\n"

            # Include additional info
            gpaMatches = re.findall(r'\d\.\d\d', pdfText)
            if gpaMatches:
                gpa = float(gpaMatches[0])
            else:
                gpa = "Not found"

            hokieMatch = "Virginia Tech" in pdfText or "VT" in pdfText
            
            infoEmbed.add_field(
                name="Additional Info",
                value=f"GPA: {gpa}\n{'Hokie detected!' if hokieMatch else ''}",
                inline=False
            )
            #infoBlob += f"## Additional Info\nGPA: {gpa}\n{'Hokie detected!' if hokieMatch else ''}"

            await ctx.respond(embed=infoEmbed)

            # Construct criticism
            summary = "**Overall, with the resume and career discipline you provided:**\n"

            barks = []
            if type(gpa) == str:
                barks.append("Specify your GPA!")
            elif gpa > 3.50:
                barks.append("Perfect GPA! Keep it up!")
            elif gpa >= 3.00 and gpa <= 3.50:
                barks.append("Not a bad GPA! But you could do better...")
            else:
                barks.append("Get that GPA up!")

            # 40% career, 30% academics, 20% social
            total_skills = total_career_skills + total_social_skills + total_academic_skills
            career_skill_percentage = total_career_skills/total_skills * 100
            social_skill_percentage = total_social_skills/total_skills * 100
            academic_skill_percentage = total_academic_skills/total_skills * 100

            if career_skill_percentage < 20:
                barks.append("Only **{:.2f}%** of your skills are related to your career! Expand your horizons!".format(career_skill_percentage))
            elif career_skill_percentage >= 20 and career_skill_percentage <= 40:
                barks.append("**{:.2f}%** of your skills are related to your career, nice!".format(career_skill_percentage))
            elif career_skill_percentage > 40:
                barks.append("Woah, **{:.2f}%** of your skills are related to your career. You must be pretty good.".format(career_skill_percentage))

            if social_skill_percentage < 10:
                barks.append("Only **{:.2f}%** of your skills have to do with people! Don't be shy, there is strength in numbers!".format(social_skill_percentage))
            elif social_skill_percentage >= 10 and social_skill_percentage <= 20:
                barks.append("**{:.2f}%** of your skills are social, nice!".format(social_skill_percentage))
            elif social_skill_percentage > 20:
                barks.append("**{:.2f}%** of your skills are social, try throwing some technical experience into the mix.".format(social_skill_percentage))

            if academic_skill_percentage < 15:
                barks.append("Only **{:.2f}%** of your skills have to do with academics, start locking in and pursue opportunities like undergraduate research!".format(academic_skill_percentage))
            elif academic_skill_percentage >= 15 and academic_skill_percentage <= 30:
                barks.append("**{:.2f}%** of your skills are academic-related, nice!".format(academic_skill_percentage))
            elif academic_skill_percentage > 40:
                barks.append("**{:.2f}%** of your skills are academic-related. You're an academic weapon, but try putting in some technical/professional experience.".format(academic_skill_percentage))

            summary += ('\n'.join(['- '+bark for bark in barks]))

            await ctx.channel.send(summary)

    @slash_command(name="read", description="Reads a PDF attachment file.\nUsed for debugging.", guilds=[1152451000079220897])
    async def read(self, ctx : discord.ApplicationContext,
                   resume : discord.Option(discord.SlashCommandOptionType.attachment,
                                           name="resume",
                                           description="The resume to scan (PDF format)"),
                    verbose : discord.Option(discord.SlashCommandOptionType.boolean,
                                             name="verbose",
                                             description="Whether to display extra PDF information or not.",
                                             default = False)):
        """
        Interprets the text of the attached PDF file along with its metadata.
        Debugging command.
        """

        # Check if it's a PDF file
        url = resume.url
        if not url.endswith('pdf'):
            await ctx.respond(content="The file you provided is not a PDF.", ephemeral=True)
            return
        
        await ctx.respond("Reading PDF...")

        content = await resume.read()

        # Write the PDF
        with open('metadata.pdf', 'wb') as pdf:
            pdf.write(content)
        
        with open('metadata.pdf', 'rb') as pdf:
            reader = PdfReader(pdf)
            md = reader.metadata

            # Send verbose info
            if verbose:
                infoEmbed = discord.Embed(title=resume.filename)
                infoEmbed.set_author(name=(md.author or 'Unknown author'))

                infoEmbed.add_field(
                    name="Title",
                    value=(md.title or 'None'),
                    inline=False
                )

                infoEmbed.add_field(
                    name="Creator",
                    value=(md.creator or 'Not specified')
                )

                infoEmbed.add_field(
                    name="Producer",
                    value=(md.producer or 'Not specified')
                )

                infoEmbed.add_field(
                    name="Creation Date",
                    value=str(md.creation_date or 'Not specified'),
                    inline=False
                )

                await ctx.channel.send(embed=infoEmbed)
            
            # Extracttext
            for i in range(len(reader.pages)):
                page = reader.pages[i]
                text = page.extract_text()

                # 2k character limit on Discord messages
                await ctx.channel.send(f'Text excerpt from page {i+1}: ```{text[0:1920]}```')