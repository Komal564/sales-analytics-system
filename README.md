#### Sales Analytics System

Assignment Module 3 – Sales Data Processing, Analysis, and Reporting Using Python

## 1. Project Overview

This project has been developed as part of Assignment Module 3 of the data analytics program.
The Sales Analytics System is a Python-based application that demonstrates intermediate-level concepts of data handling, validation, analytical processing, API integration, and report generation.

The system reads raw sales transaction data, resolves common data quality issues, performs structured sales analysis, enriches the dataset using an external product API, and generates a professionally formatted sales analytics report.

The primary objective of Assignment Module 3 is to evaluate the ability to design a clean, modular, and automated data analysis workflow using Python.

## 2. Dataset Used
## 2.1 Input Sales Dataset

**Dataset File:** data/sales_data.txt

**Dataset Type:** Transactional sales data

**File Format:** Pipe-separated text file (|)

Each row in the dataset represents one individual sales transaction.

#### Dataset Schema

TransactionID | Date | ProductID | ProductName | Quantity | UnitPrice | CustomerID | Region

#### Sample Entry
T018|2024-12-29|P107|USB Cable|8|173|C009|South

## 2.2 Data Quality Issues in the Dataset

In accordance with Assignment Module 3 requirements, the dataset intentionally includes realistic data quality problems to test preprocessing logic. These issues include:

Product names containing commas

Numeric values (Quantity and UnitPrice) containing commas

Missing or incomplete fields

Zero or negative values in Quantity or UnitPrice

Invalid Transaction IDs not following the expected format

All such issues are automatically identified and handled during the data cleaning phase.

## 3. Project Folder Structure
The project follows a clear and modular directory structure.  
Each file and folder plays a specific role in the overall workflow.

sales-analytics-system/
│
│── main.py
│   → Main entry point of the Sales Analytics System
│   → Orchestrates the complete workflow of the application
│   → Calls utility modules for data processing, enrichment, and reporting
│
│── requirements.txt
│   → Contains all required Python libraries
│   → Used to install dependencies before running the project
│
│── README.md
│   → Project documentation
│   → Explains system overview, setup steps, and execution instructions
│
├── utils/
│   ├── file_handler.py
│   │   → Responsible for reading sales data files
│   │   → Handles different file encodings safely
│   │
│   ├── data_processor.py
│   │   → Performs data parsing, cleaning, and validation
│   │   → Executes sales analytics calculations
│   │   → Generates enriched data and final sales report
│   │
│   └── api_handler.py
│       → Communicates with external product API
│       → Fetches product details such as category, brand, and rating
│       → Builds mappings used for data enrichment
│
├── data/
│   ├── sales_data.txt
│   │   → Raw input sales dataset
│   │   → Original transaction data provided for business analysis
│   │   → Read by the system at the start of execution
│   │
│   └── enriched_sales_data.txt
│       → Enriched sales dataset generated after API processing
│       → Contains sales data combined with product information
│       → Includes category, brand, rating, and match status
│
├── output/
│   └── sales_report.txt
│       → Final sales analytics report
│       → Contains summarized insights, metrics, and analysis results
│       → Generated automatically after all processing is complete



## 4. system workflow

The application executes a structured and sequential workflow:

Data Ingestion
The raw sales file is read using multiple encoding formats to ensure compatibility.

Data Cleaning and Validation
Invalid, incomplete, or inconsistent records are detected and removed.

Sales Analysis
Revenue calculations, region-wise performance, customer analysis, product trends, and date-based insights are computed.

API Integration
External product information is fetched from an online API.

Data Enrichment
Sales records are enriched with product category, brand, rating, and match status.

Report Generation
A structured and professional sales analytics report is generated.

The entire process is fully automated and does not require user input.

5. API Used
External Product Data API

**API Name:** DummyJSON Products API

Purpose: Enrich sales data with product metadata

**Endpoint Used:**

https://dummyjson.com/products?limit=100

### API Fields Utilized
The following attributes from the API response are used during data enrichment:

- **Title** – Product name reference  
- **Category** – Product category classification  
- **Brand** – Manufacturer or brand information  
- **Rating** – Customer rating score  

These fields provide additional business context and are included in the enriched sales dataset.


## 6. Project Execution 

Step 1: Install Dependencies

Add the following dependency to requirements.txt:

requests


Install dependencies using:

pip install -r requirements.txt

Step 2: Run the Application
python main.py

Once executed, the system automatically performs all processing stages, including data cleaning, analysis, API enrichment, and report generation.

### 7. Output Files Generated

After successful execution, the system produces the following output files:

File Name	Description
enriched_sales_data.txt	Sales dataset enriched with external API product information
sales_report.txt	Final professionally formatted sales analytics report

The generated report includes consolidated summaries, analytical trends, performance insights, and details related to API-based data enrichment.


## 8. Conclusion

This project successfully fulfills the objectives of Assignment Module 3 by implementing a complete sales analytics pipeline using Python.
It demonstrates effective handling of data quality issues, structured analytical logic, external API usage, and professional report generation.

The project clearly reflects the skills and understanding expected at the Module Developed by Komal Kaur Ladhar as an academic project.
3 level and is suitable for academic evaluation and practical demonstration.

Project developed and maintained by Komal Kaur Ladhar.

