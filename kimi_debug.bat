#!/bin/bash

# Step 1: Clone the repository
# echo "Cloning the repository..."
# git clone https://github.com/CRAJKUMARSINGH/Priyanka_Tender_Final.git
# cd Priyanka_Tender_Final

# Step 2: Check Python and Streamlit installation
echo "Checking Python and Streamlit versions..."
python --version > version_log.txt 2>&1
streamlit --version >> version_log.txt 2>&1

# Step 3: Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt > install_log.txt 2>&1

# Step 4: Run the application
echo "Running the application..."
streamlit run app.py > run_log.txt 2>&1

# Check if the application started successfully
if grep -q "Running as a Streamlit app" run_log.txt; then
  echo "Application started successfully."
else
  echo "Application failed to start. Check the logs for details."
  cat run_log.txt
