import pandas as pd
import re
from sqlalchemy import create_engine, Table, Column, MetaData, DATE, TEXT, VARCHAR, TIME, INT, NUMERIC
from sqlalchemy.dialects.postgresql import INTERVAL

# Load csv
csv_events = "path/CRMEvents.csv"
csv_logs = "path/CRMCallCenterLogs.csv"
csv_loan = "path/LuxuryLoanPortfolio.csv"

# Change column names
def change_column_name(col_name):
    col = col_name.strip().lower()
    col = re.sub(r'\W+', '_', col)
    col = col.strip('_')
    return col

df_crm_events = pd.read_csv(csv_events)
df_crm_logs = pd.read_csv(csv_logs)
df_loan_porto = pd.read_csv(csv_loan)

df_crm_events.columns = [change_column_name(col) for col in df_crm_events.columns]
df_crm_logs.columns = [change_column_name(col) for col in df_crm_logs.columns]
df_loan_porto.columns = [change_column_name(col) for col in df_loan_porto.columns]

# Connecction to  PostgreSQL
db_user = "postgres"
db_pass = "password" #your_pass
db_host = "localhost"
db_port = "5432"
db_name = "task1"

engine = create_engine(f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}")
metadata = MetaData()

# Define crm_events table
crm_events = Table('crm_events', metadata,
    Column('date_received', DATE),
    Column('product', VARCHAR(255)),
    Column('sub_product', VARCHAR(255)),
    Column('issue', VARCHAR(255)),
    Column('sub_issue', VARCHAR(255)),
    Column('consumer_complaint_narrative', TEXT),
    Column('tags', VARCHAR(255)),
    Column('consumer_consent_provided', VARCHAR(50)),
    Column('submitted_via', VARCHAR(100)),
    Column('date_sent_to_company', DATE),
    Column('company_response_to_consumer', VARCHAR(255)),
    Column('timely_response', VARCHAR(10)),
    Column('consumer_disputed', VARCHAR(10)),
    Column('complaint_id', VARCHAR(20)),
    Column('client_id', VARCHAR(20))
)

# Define crm_call_center_logs table
crm_call_center_logs = Table('crm_call_center_logs', metadata,
    Column('date_received', DATE),
    Column('complaint_id', VARCHAR(20)),
    Column('rand_client', VARCHAR(20)),
    Column('phonefinal', VARCHAR(20)),
    Column('vru_line', VARCHAR(20)),
    Column('call_id', VARCHAR(50)),
    Column('priority', INT),
    Column('type', VARCHAR(50)),
    Column('outcome', VARCHAR(50)),
    Column('server', VARCHAR(50)),
    Column('ser_start', TIME),
    Column('ser_exit', TIME),
    Column('ser_time', INTERVAL)
)

# Define loan_porto table
loan_porto = Table('loan_porto', metadata,
    Column('loan_id', VARCHAR(20), primary_key=True),
    Column('funded_amount', NUMERIC(12,2)),
    Column('funded_date', DATE),
    Column('duration_years', INT),
    Column('duration_months', INT),
    Column('10_yr_treasury_index_date_funded', NUMERIC(5,2)),
    Column('interest_rate_percent', NUMERIC(5,3)),
    Column('interest_rate', NUMERIC(7,5)),
    Column('payments', NUMERIC(12,2)),
    Column('total_past_payments', INT),
    Column('loan_balance', NUMERIC(12,2)),
    Column('property_value', NUMERIC(12,2)),
    Column('purpose', VARCHAR(100)),
    Column('firstname', VARCHAR(50)),
    Column('middlename', VARCHAR(50)),
    Column('lastname', VARCHAR(50)),
    Column('social', VARCHAR(15)),
    Column('phone', VARCHAR(15)),
    Column('title', VARCHAR(150)),
    Column('employment_length', INT),
    Column('building_class_category', VARCHAR(100)),
    Column('tax_class_at_present', VARCHAR(10)),
    Column('building_class_at_present', VARCHAR(10)),
    Column('address_1', VARCHAR(100)),
    Column('address_2', VARCHAR(50)),
    Column('zip_code', VARCHAR(10)),
    Column('city', VARCHAR(50)),
    Column('state', VARCHAR(2)),
    Column('total_units', INT),
    Column('land_square_feet', VARCHAR(20)),
    Column('gross_square_feet', VARCHAR(20)),
    Column('tax_class_at_time_of_sale', VARCHAR(10))
)
# Create table in database 
metadata.create_all(engine)
print("Semua tabel berhasil dibuat")

# Insert data CSV to tabel
df_crm_events.to_sql('crm_events', engine, if_exists='append', index=False)
df_crm_logs.to_sql('crm_call_center_logs', engine, if_exists='append', index=False)
df_loan_porto.to_sql('loan_porto', engine, if_exists='append', index=False)

print("Data berhasil dimuat ke tabel crm_events, crm_call_center_logs dan loan_porto")
