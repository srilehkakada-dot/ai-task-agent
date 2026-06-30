"""
sample_data.py
Dummy email data used to simulate an inbox, since this version
does not connect to a real Gmail account. This keeps the agent
demo-able instantly without any OAuth setup.
"""

SAMPLE_EMAILS = [
    {
        "from": "prof.kumar@aditya.edu",
        "subject": "Project Review Meeting - Monday 10 AM",
        "body": "Hi Pooja, please prepare your AI agent project demo for the review on Monday at 10 AM. Bring your progress report and be ready to explain your architecture."
    },
    {
        "from": "hr@techcorp-internships.com",
        "subject": "Internship Application Deadline Extended",
        "body": "We are pleased to inform you that the deadline for the Summer Internship Program has been extended to July 15th. Please complete your application and upload your resume before this date."
    },
    {
        "from": "noreply@coursera.org",
        "subject": "Your course certificate is ready",
        "body": "Congratulations! Your certificate for 'Google AI Essentials' is now available for download. This is just a notification, no action needed."
    },
    {
        "from": "team-lead@hackathon2026.com",
        "subject": "URGENT: Submit your hackathon project by tonight",
        "body": "Reminder that all hackathon submissions close tonight at 11:59 PM. Please upload your GitHub repo link and a short demo video before the deadline. Late submissions will not be accepted."
    },
    {
        "from": "library@aditya.edu",
        "subject": "Book return reminder",
        "body": "This is a reminder that you have a book due for return by next Friday. Please return it on time to avoid a late fee."
    },
    {
        "from": "placement.cell@aditya.edu",
        "subject": "Mock Interview Sign-up - Limited Slots",
        "body": "The placement cell is conducting mock interviews next week to help students prepare for campus placements. Sign up by Wednesday as slots are limited. This is a great opportunity to practice before the actual season."
    },
]