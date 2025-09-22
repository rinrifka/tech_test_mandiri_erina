# Technical Test_Mandiri Sekuritas_2025
This repository contains the answers for the Mandiri Sekuritas Data Engineer technical test in 2025 by Erina Rifka

## Tools & Programming Language :
Python 3.X, PostgreSQL

## Folder
    ├─  task1_load_data/                  # Virtual environment with Python and libraries
        ├─ CRMCallCenterLogs.csv #source data
        ├─ CRMEvents.csv         #source data
        ├─ task1.py              #script for load data to PostgreSQL
        ├─ queries.sql           #Queries for analysis
    ├─ task2_dash/      
    ├─ LuxuryLoanPortfolio.csv   #source data
    ├─ task2.py                  #script for build dashboard
    ├─ requirements.txt          #contains packages that need to be install

## Notes
1. You need to adjust code before you run the script
   -- task1_load_data script.py :

  # Load csv
  csv_events = "path/CRMEvents.csv"
  csv_logs = "path/CRMCallCenterLogs.csv"
  csv_loan = "path/LuxuryLoanPortfolio.csv"

  # Connecction to  PostgreSQL
  db_user = "postgres" #your_username
  db_pass = "password" #your_pass
  db_host = "localhost"
  db_port = "5432"
  db_name = "task1" #anything


  --task2_dash.py :
  # Load data & rename columns
  csv_loan    = pd.read_csv("path/LuxuryLoanPortfolio.csv", delimiter=",")

  --queries.sql :
  Run query on PostgreSQL
  
