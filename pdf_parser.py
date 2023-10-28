import os
import re
from PyPDF2 import PdfReader

class PdfParser:
    def __init__(self, file_path):
        self.file_path = file_path

    @staticmethod
    def match_file(file_name):
        data_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
        file_path = os.path.join(data_folder, file_name)

        if os.path.isfile(file_path):
            return file_path

    def extract_social_media_urls(self, text):
        urls = {
            "LinkedIn": None,
            "GitHub": None,
            "Other": []
        }

        linkedin_pattern = r"(https?://(www\.)?linkedin\.com/\S+)|www\.linkedin\.com/\S+"
        github_pattern = r"(https?://(www\.)?github\.com/\S+)|www\.github\.com/\S+"

        linkedin_match = re.search(linkedin_pattern, text)
        github_match = re.search(github_pattern, text)

        if linkedin_match:
            urls["LinkedIn"] = linkedin_match.group(0)

        if github_match:
            urls["GitHub"] = github_match.group(0)

        other_urls = re.findall(r"(https?://\S+)", text)
        for url in other_urls:
            if url != urls["LinkedIn"] and url != urls["GitHub"]:
                urls["Other"].append(url)

        return urls

    def parse_pdf(self, file_name, debug_val=False):
        file_insight = self.match_file(file_name)

        if file_insight is None:
            print("File not found, recheck the names")
            return None
        else:
            reader = PdfReader(file_insight)
            num_pages = len(reader.pages)

            if debug_val:
                print("File opened")

            if num_pages >= 1:
                print("Number of pages is okay")
                extracted_text = ""
                # Extract text from all pages
                for page_num in range(num_pages):
                    page = reader.pages[page_num]
                    extracted_text += page.extract_text()

                # Define regular expressions to search for information
                name_pattern = r"([A-Z][a-z]+ [A-Z][a-z]+ )"
                email_pattern = r"([a-zA-Z0-9._%+-]+@[a-zAZ0-9.-]+\.[a-zA-Z]{2,})"
                mobile_pattern = r"(\+\d{2}\s?\d{3}\s?\d{3}\s?\d{4})|(\+(\d{1,3})\s?(\d{10}))"
                gender_pattern = r"(male|female|other)\s*"
                qualification_pattern = r"((doctorate|ph\.d\.|phd|masters|m\.s\.|bachelor|b\.|high school|school|highschool)\s*[ ']*(?:\S+.*?))\s*"
                college_pattern = r"(?i)(college|university|school)[:\s]+([^\n,]+)"
                month_pattern = r"(?:January|February|March|April|May|June|July|August|September|October|November|December)"
                specialization_pattern = r"(?:Bachelor|B\.|Master|M\.|Ph\.D\.|Doctorate)[ ']*(?:of|in)?[ ']*(\S+\b\s*)*([A-Z][a-z&\s]+[A-Z][a-z&\s]+)(?=\s*(?:20\d{2}|[A-Z][a-z]+ [A-Z][a-z]+|$))"
                graduation_pattern = r"(20\d{2})\s*(?!\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\b)"

                # Search for information
                name_match = re.search(name_pattern, extracted_text, re.IGNORECASE)
                email_match = re.search(email_pattern, extracted_text, re.IGNORECASE)
                mobile_match = re.search(mobile_pattern, extracted_text, re.IGNORECASE)
                gender_match = re.search(gender_pattern, extracted_text, re.IGNORECASE)
                qualification_match = re.search(qualification_pattern, extracted_text, re.IGNORECASE)
                college_match = re.search(college_pattern, extracted_text, re.IGNORECASE)
                month_matches = re.findall(month_pattern, extracted_text, re.IGNORECASE)
                specialization_match = re.search(specialization_pattern, extracted_text, re.IGNORECASE)
                graduation_match = re.search(graduation_pattern, extracted_text, re.IGNORECASE)

                # Check if any of the critical fields are found
                if (
                    name_match is None
                    and email_match is None
                    and mobile_match is None
                    and gender_match is None
                    and qualification_match is None
                    and college_match is None
                ):
                    print("No entries found")
                    return

                # Extract the information if found
                name = name_match.group(1) if name_match else "Entry not found!"
                email = email_match.group(1) if email_match else "Entry not found!"
                mobile = mobile_match.group(1) if mobile_match else "Entry not found!"
                gender = gender_match.group(1) if gender_match else "Gender not specified"
                qualification = qualification_match.group(1) if qualification_match else "Entry not found!"
                college = ""
                if college_match:
                    line_start = extracted_text.rfind('\n', 0, college_match.start()) + 1
                    line_end = extracted_text.find('\n', college_match.end())
                    line_with_college = extracted_text[line_start:line_end].strip()
                    preceding_text = line_with_college[:college_match.start() - line_start].strip()
                    following_text = line_with_college[college_match.end() - line_start:].strip()
                    college = f"{preceding_text} {college_match.group(1)}: {college_match.group(2)} {following_text}"
                else:
                    college = "Entry not found!"

                specialization = specialization_match.group(2) if specialization_match else "Entry not found!"
                for month in month_matches:
                    specialization = specialization.replace(month, '')
                graduation = graduation_match.group(1) if graduation_match else "Entry not found!"

                social_media_urls = self.extract_social_media_urls(extracted_text)
                linkedin_url = social_media_urls["LinkedIn"]
                github_url = social_media_urls["GitHub"]
                other_urls = social_media_urls["Other"]

                # Print or use the retrieved information as needed
                print(f"Name: {name}")
                print(f"Email: {email}")
                print(f"Mobile Number: {mobile}")
                print(f"Gender: {gender}")
                print(f"Highest Qualification: {qualification}")
                print(f"College: {college}")
                print(f"Specialization/Branch: {specialization.strip()}")
                print(f"Graduation Year: {graduation}")
                print(f"LinkedIn URL: {linkedin_url}")
                print(f"GitHub URL: {github_url}")
                if other_urls:
                    print("Other URLs:")
                    for url in other_urls:
                        print(url)

            else:
                print("Number of pages is not okay")
            # Restore the standard output
            sys.stdout = sys.__stdout__

            # Get the captured output as a string
            captured_output = output_buffer.getvalue()

            # Return the captured output
            return captured_output