
# 10-K Data Extractor with RAG LLM Analysis


This project is designed to extract, process, and analyze 10-K filings of a given company ticker from 1995 to 2023. It consists of two main files:


**Data_Extractor.py** : This file extracts all the 10-K filings of the specified company ticker. Due to high processing time, the data from 10-K reports had to be significantly reduced. Various approaches were tried, including advanced REGEX to extract specific sections like 7 and 7a, but due to inconsistency in the filings, this method was not effective. Instead, all the table tags from the HTML markup were extracted using Beautiful Soup, as this method proved highly effective in extracting important numerical tabular data from the markup language. The final reduced processed markup code was then converted to PDF format for each year, as the RAG model has shown good results with PDFs.

**rag_code.py**: This file contains the code for indexing the PDFs and implementing the RAG pipeline using LLAMA 2 and GPT-3.5. This pipeline is used to extract data and generate insights from the processed 10-K filings.
Installation
To install the dependencies, run the following command:


## Note
The processing time for this project can be high due to the nature of the RAG model indexing and overall processing time for 10-K reports.


## Installation

Install the requirements using: 

```bash
  pip install -r requirements.txt
  
```
Run the Data_Extractor.py

```bash
  python Data_Extractor.py
  
```
