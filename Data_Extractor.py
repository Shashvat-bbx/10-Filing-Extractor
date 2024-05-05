
from bs4 import BeautifulSoup
import re
import pandas as pd
from sec_edgar_downloader import Downloader 
import os
from xhtml2pdf import pisa  

def convert_html_to_pdf(html_string, pdf_path):   # This function is used to convert Extracted HTML to PDF
    with open(pdf_path, "wb") as pdf_file:
        pisa_status = pisa.CreatePDF(html_string, dest=pdf_file)        
    return not pisa_status.err

def file_processor(submission_file_path):        
    with open(submission_file_path, 'r') as file:
        raw_10k=file.read()
        
    soup = BeautifulSoup(raw_10k, 'html.parser')

    # Find all <table> tags in the HTML document
    tables = soup.find_all('table')

    # Print the tables or do whatever you need with them
    final_string=""
    for table in tables:
        final_string+=str(table)
    html_content=final_string     

   

    # Generate PDF and store them in a directory which contains the ticker name
    directory_path = f'{company_ticker}'   

    # Check if the directory already exists
    if not os.path.exists(directory_path):
        # Create the directory
        os.makedirs(directory_path)
        print("Directory created successfully")

    pdf_path = f'{directory_path}/{submission_file_path[39:-27]}.pdf'
    print(pdf_path)
    try:
        if convert_html_to_pdf(html_content, pdf_path):
            print(f"PDF generated and saved at {pdf_path}")
        else:
            print("PDF generation failed")
    except:
        print(f'something failed {submission_file_path}')
    






company_ticker=input("Enter the Company ticker: ")   
dl = Downloader("MyCompanyName", "my.email@domain.com")
dl.get("10-K", company_ticker, after="1995-01-01", before="2023-03-25")   # Extracting data from SEC-EDGAR from 1995 to 2023



folder_path = f'sec-edgar-filings/{company_ticker}/10-K'

for folder_name in os.listdir(folder_path):
    folder_full_path = os.path.join(folder_path, folder_name)
    if os.path.isdir(folder_full_path):
        submission_file_path = os.path.join(folder_full_path, "full-submission.txt")

        if os.path.exists(submission_file_path):
            file_processor(submission_file_path)
            print(submission_file_path)


