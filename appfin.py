import hashlib
import pandas as pd
import streamlit as st
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import plotly.express as px
import time
from PIL import Image
import pytesseract
import requests
from bs4 import BeautifulSoup
import numpy as np

# Custom CSS for animations and styling
st.markdown("""
<style>
@keyframes float {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-20px); }
    100% { transform: translateY(0px); }
}

@keyframes gradientBackground {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

body {
    background: linear-gradient(-45deg, #ff7e5f, #feb47b, #ff6a6a, #ffcc5c);
    background-size: 400% 400%;
    animation: gradientBackground 15s ease infinite;
}

.hero {
    text-align: center;
    padding: 4rem 0;
    background: rgba(255, 255, 255, 0.2);
    color: white;
    border-radius: 15px;
    animation: float 6s ease-in-out infinite;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.3);
}

.feature-card {
    padding: 1.5rem;
    background: rgba(255, 255, 255, 0.2);
    border-radius: 10px;
    margin: 1rem 0;
    transition: transform 0.3s, box-shadow 0.3s;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.3);
}

.feature-card:hover {
    transform: scale(1.05);
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3);
}

.section-title {
    border-left: 5px solid #ff6f61;
    padding-left: 1rem;
    margin: 2rem 0;
    color: white;
}

.stButton>button {
    background: linear-gradient(45deg, #ff6f61, #ffcc5c);
    color: white;
    border: none;
    border-radius: 25px;
    padding: 0.75rem 2rem;
    font-size: 1rem;
    transition: transform 0.3s, box-shadow 0.3s;
}

.stButton>button:hover {
    transform: scale(1.05);
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3);
}

.stTextInput>div>div>input {
    background: rgba(255, 255, 255, 0.2);
    color: white;
    border: 1px solid rgba(255, 255, 255, 0.3);
    border-radius: 10px;
    padding: 0.5rem 1rem;
}

.stTextInput>div>div>input::placeholder {
    color: rgba(255, 255, 255, 0.5);
}

.stSelectbox>div>div>select {
    background: rgba(255, 255, 255, 0.2);
    color: white;
    border: 1px solid rgba(255, 255, 255, 0.3);
    border-radius: 10px;
    padding: 0.5rem 1rem;
}

.stRadio>div>label {
    color: white;
}

.stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
    color: white;
}

.animation-3d {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: -1;
    background: url('https://www.transparenttextures.com/patterns/diamond-upholstery.png');
    animation: rotate3D 60s linear infinite;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state for user management
if 'users' not in st.session_state:
    st.session_state['users'] = {}

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if 'current_user' not in st.session_state:
    st.session_state['current_user'] = None

# Password Hashing Function
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Signup Page
def signup_page():
    st.title("Sign Up for Finsight 💼")
    st.markdown("Create your account to access AI-powered financial insights.")

    with st.form("signup_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        
        if st.form_submit_button("Sign Up"):
            if username in st.session_state['users']:
                st.error("Username already exists. Please choose a different username.")
            elif password != confirm_password:
                st.error("Passwords do not match. Please try again.")
            elif len(password) < 8:
                st.error("Password must be at least 8 characters long.")
            else:
                st.session_state['users'][username] = hash_password(password)
                st.success("Account created successfully! Please log in.")
                time.sleep(1)
                st.session_state['current_page'] = "login"
                st.rerun()

# Login Page
def login_page():
    st.title("Login to Finsight 💼")
    st.markdown("Welcome back! Please log in to continue.")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.form_submit_button("Login"):
            if username in st.session_state['users'] and st.session_state['users'][username] == hash_password(password):
                st.session_state['logged_in'] = True
                st.session_state['current_user'] = username
                st.success("Logged in successfully!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Invalid username or password.")

# Logout Function
def logout():
    st.session_state['logged_in'] = False
    st.session_state['current_user'] = None
    st.success("Logged out successfully!")
    time.sleep(1)
    st.rerun()

# Sidebar Navigation
def sidebar():
    st.sidebar.title("Navigation")
    options = ["Home", "Smart Document Analysis", "Education Loan Eligibility"]
    selection = st.sidebar.radio("Go to", options)
    
    if st.session_state['logged_in']:
        if st.sidebar.button("Logout"):
            logout()
    
    return selection

# Enhanced Home Page
def home_page():
    st.markdown("""
    <div class="hero">
        <h1 style="font-size:3.5rem; margin-bottom:1rem; background: linear-gradient(45deg, #fff, #ff6f61); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Finsight 💼</h1>
        <h3 style="font-weight:300;">AI-Powered Financial Intelligence Platform</h3>
    </div>
    
    <div style="text-align: center; margin: 3rem 0;">
        <h2>Transform Your Financial Future</h2>
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-top: 2rem;">
            <div class="feature-card">
                <h4>📚 Smart Analysis</h4>
                <p>Advanced document processing powered by AI</p>
            </div>
            <div class="feature-card">
                <h4>🎓 Education Loans</h4>
                <p>Personalized loan eligibility assessment</p>
            </div>
            <div class="feature-card">
                <h4>📈 Financial Insights</h4>
                <p>Data-driven recommendations for success</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Document Analysis Functions
def process_unstructured_data():
    st.header("📑 Unstructured Data Analysis (CSV)")

    uploaded_file = st.file_uploader("Upload Unstructured CSV File", type=["csv"])

    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            st.write("### Uploaded Data:")
            st.write(df)

            if "Frequency" in df.columns and "Price range" in df.columns:
                st.subheader("K-Means Clustering Analysis")
                process_kmeans_clustering(df)
            else:
                st.error("CSV file must contain 'Frequency' and 'Price range' columns.")
        
        except Exception as e:
            st.error(f"Error: {str(e)}")

def process_kmeans_clustering(df):
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(df[["Frequency", "Price range"]])

    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    df["cluster"] = kmeans.fit_predict(scaled_data)
    
    st.subheader("Updated Dataset with Clusters:")
    st.write(df)

    st.subheader("Cluster Interpretations")
    cluster_info = {
        0: "Cluster 0: Low Frequency, Low Price Range",
        1: "Cluster 1: High Frequency, High Price Range",
        2: "Cluster 2: Medium Frequency, Medium Price Range"
    }

    for cluster, meaning in cluster_info.items():
        st.write(f"{meaning}")
    
    plt.figure(figsize=(10, 6))
    scatter = plt.scatter(df["Frequency"], df["Price range"], c=df["cluster"], cmap="viridis", edgecolors="k")
    plt.colorbar(scatter, label="Cluster")
    plt.xlabel("Frequency of Purchases")
    plt.ylabel("Price Range")
    plt.title("K-Means Clustering of Items")
    st.pyplot(plt)
    
    st.markdown("""
    **Clustering Visualization Analysis:**
    - Each point represents an item's purchasing pattern
    - **X-Axis:** Frequency of purchases (normalized scale)
    - **Y-Axis:** Price range of items (normalized scale)
    - **Color Mapping:** 
      - Purple: Cluster 0 (Low frequency, low price)
      - Yellow: Cluster 1 (High frequency, high price)
      - Green: Cluster 2 (Medium frequency, medium price)
    - **Business Insight:** Identify high-value frequent purchase items for inventory optimization
    """)

def process_structured_data():
    st.header("📑 Structured Data Analysis")
    file_type = st.selectbox("Select Data Type", ["Cash Flow", "Payslips", "Bank Statements", "Profit and Loss", "Invoices"])

    uploaded_file = st.file_uploader("Upload Structured Document", type=["jpg", "png"])
    if uploaded_file:
        try:
            img = Image.open(uploaded_file)
            st.image(img, caption="Uploaded Document", use_container_width=True)

            with st.spinner("🔍 Extracting Text..."):
                extracted_text = pytesseract.image_to_string(img)
                time.sleep(1)

            if extracted_text.strip():
                with st.expander("📄 View Extracted Text"):
                    st.code(extracted_text, language="text")
                process_structured_analysis(file_type, extracted_text)
            else:
                st.warning("No text found in the document")
        except Exception as e:
            st.error(f"Error: {str(e)}")

def process_structured_analysis(file_type, extracted_text):
    st.subheader("Structured Data Analysis Example")
    st.write(f"Processing {file_type} data...")

    if file_type == "Cash Flow":
        data = {
            "Month": ["January", "February", "March", "April"],
            "Income": [5000, 5500, 6000, 6500],
            "Expenses": [3000, 3500, 4000, 4500]
        }
        df = pd.DataFrame(data)
        fig = px.bar(df, x='Month', y=['Income', 'Expenses'], title="Cash Flow Analysis", color_discrete_sequence=px.colors.qualitative.Dark24)
        st.plotly_chart(fig)
        fig_pie = px.pie(df, names='Month', values='Income', title="Income Distribution by Month", color_discrete_sequence=px.colors.qualitative.Dark24)
        st.plotly_chart(fig_pie)
   

    elif file_type == "Bank Statements":
        data = {
            "Date": ["01/01", "02/01", "03/01", "04/01"],
            "Debit": [200, 300, 250, 350],
            "Credit": [1000, 1200, 1100, 1300]
        }
        df = pd.DataFrame(data)
       
        fig_bar = px.bar(df, x='Date', y=['Debit', 'Credit'], title="Bank Statement Overview", color_discrete_sequence=px.colors.qualitative.Dark24)
        st.plotly_chart(fig_bar)
        
        fig_pie = px.pie(df, names='Date', values='Credit', title="Credit Distribution", color_discrete_sequence=px.colors.qualitative.Dark24)
        st.plotly_chart(fig_pie)

    elif file_type == "Payslips":
        data = {
            "Month": ["Jan", "Feb", "Mar", "Apr"],
            "Basic Salary": [30000, 31000, 32000, 33000],
            "Deductions": [5000, 5200, 5400, 5600]
        }
        df = pd.DataFrame(data)
       
        fig = px.bar(df, x="Month", y=["Basic Salary", "Deductions"], title="Salary Breakdown", color_discrete_sequence=px.colors.qualitative.Dark24)
        st.plotly_chart(fig)
        
        fig_pie = px.pie(df, names="Month", values="Basic Salary", title="Salary Distribution by Month", color_discrete_sequence=px.colors.qualitative.Dark24)
        st.plotly_chart(fig_pie)

    elif file_type == "Profit and Loss":
        data = {
            "Category": ["Revenue", "COGS", "Operating Expenses", "Net Profit"],
            "Amount": [100000, 40000, 30000, 30000]
        }
        df = pd.DataFrame(data)
   
        fig_pie = px.pie(df, names="Category", values="Amount", title="Profit & Loss Distribution", color_discrete_sequence=px.colors.qualitative.Dark24)
        st.plotly_chart(fig_pie)
        
        fig_bar = px.bar(df, x="Category", y="Amount", title="Profit & Loss Breakdown", color_discrete_sequence=px.colors.qualitative.Dark24)
        st.plotly_chart(fig_bar)

    elif file_type == "Invoices":
        data = {
            "Item": ["Hourly Car Rental", "Weekly Car Rent", "Monthly Car Rental"],
            "Amount": [88.00, 328.00, 1410.00]
        }
        df = pd.DataFrame(data)
        
        fig_bar = px.bar(df, x='Item', y='Amount', title="Invoice Amount Breakdown", color_discrete_sequence=px.colors.qualitative.Dark24)
        st.plotly_chart(fig_bar)
        
        fig_pie = px.pie(df, names='Item', values='Amount', title="Invoice Amount Distribution", color_discrete_sequence=px.colors.qualitative.Dark24)
        st.plotly_chart(fig_pie)

def scrape_semi_structured_data(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            st.write("Successfully fetched the page!")
            soup = BeautifulSoup(response.text, "html.parser")

            rows = []
            table = soup.find('table', class_='datatable-v2_table__93S4Y')
            if table:
                table_rows = table.find_all('tr')
                for row in table_rows[1:]:
                    columns = row.find_all('td')
                    if len(columns) > 1:
                        stock_name = columns[1].text.strip()
                        stock_price = columns[2].text.strip()
                        stock_change = columns[5].text.strip()
                        rows.append({"Stock Name": stock_name, "Price(₹)": stock_price, "Change": stock_change})

                df = pd.DataFrame(rows)
                return df
        else:
            st.error(f"Failed to retrieve webpage. Status Code: {response.status_code}")
    except Exception as e:
        st.error(f"Error: {str(e)}")
    return None

import pandas as pd
import plotly.express as px
import streamlit as st
from bs4 import BeautifulSoup
import requests

def scrape_semi_structured_data(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            st.write("Successfully fetched the page!")
            soup = BeautifulSoup(response.text, "html.parser")

            rows = []
            table = soup.find('table', class_='datatable-v2_table__93S4Y')
            if table:
                table_rows = table.find_all('tr')
                for row in table_rows[1:]:
                    columns = row.find_all('td')
                    if len(columns) > 1:
                        stock_name = columns[1].text.strip()
                        stock_price = columns[2].text.strip()
                        stock_change = columns[5].text.strip()
                        rows.append({"Stock Name": stock_name, "Price(₹)": stock_price, "Change": stock_change})

                df = pd.DataFrame(rows)
                return df
        else:
            st.error(f"Failed to retrieve webpage. Status Code: {response.status_code}")
    except Exception as e:
        st.error(f"Error: {str(e)}")
    return None

def scrape_semi_structured_data(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            st.write("Successfully fetched the page!")
            soup = BeautifulSoup(response.text, "html.parser")

            rows = []
            table = soup.find('table', class_='datatable-v2_table__93S4Y')
            if table:
                table_rows = table.find_all('tr')
                for row in table_rows[1:]:
                    columns = row.find_all('td')
                    if len(columns) > 1:
                        stock_name = columns[1].text.strip()
                        stock_price = columns[2].text.strip()
                        stock_change = columns[5].text.strip()
                        rows.append({"Stock Name": stock_name, "Price(₹)": stock_price, "Change": stock_change})

                df = pd.DataFrame(rows)
                return df
        else:
            st.error(f"Failed to retrieve webpage. Status Code: {response.status_code}")
    except Exception as e:
        st.error(f"Error: {str(e)}")
    return None

def scrape_semi_structured_data(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            st.write("Successfully fetched the page!")
            soup = BeautifulSoup(response.text, "html.parser")

            rows = []
            table = soup.find('table', class_='datatable-v2_table__93S4Y')
            if table:
                table_rows = table.find_all('tr')
                for row in table_rows[1:]:
                    columns = row.find_all('td')
                    if len(columns) > 1:
                        stock_name = columns[1].text.strip()
                        stock_price = columns[2].text.strip()
                        stock_change = columns[5].text.strip()
                        rows.append({"Stock Name": stock_name, "Price(₹)": stock_price, "Change": stock_change})

                df = pd.DataFrame(rows)
                return df
        else:
            st.error(f"Failed to retrieve webpage. Status Code: {response.status_code}")
    except Exception as e:
        st.error(f"Error: {str(e)}")
    return None

def scrape_semi_structured_data(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            st.write("Successfully fetched the page!")
            soup = BeautifulSoup(response.text, "html.parser")

            rows = []
            table = soup.find('table', class_='datatable-v2_table__93S4Y')
            if table:
                table_rows = table.find_all('tr')
                for row in table_rows[1:]:
                    columns = row.find_all('td')
                    if len(columns) > 1:
                        stock_name = columns[1].text.strip()
                        stock_price = columns[2].text.strip()
                        stock_change = columns[5].text.strip()
                        rows.append({"Stock Name": stock_name, "Price(₹)": stock_price, "Change": stock_change})

                df = pd.DataFrame(rows)
                return df
        else:
            st.error(f"Failed to retrieve webpage. Status Code: {response.status_code}")
    except Exception as e:
        st.error(f"Error: {str(e)}")
    return None

def process_semi_structured_data():
    st.header("📑 Semi-Structured Data Analysis")
    url = st.text_input("Enter the URL for Web Scraping", "https://www.investing.com/equities")

    # Initialize session state for scraped data and selected companies
    if 'scraped_data' not in st.session_state:
        st.session_state['scraped_data'] = None

    if 'selected_companies' not in st.session_state:
        st.session_state['selected_companies'] = []

    if st.button("Scrape Data"):
        st.session_state['scraped_data'] = scrape_semi_structured_data(url)

    if st.session_state['scraped_data'] is not None:
        df = st.session_state['scraped_data']

        # Clean the Price(₹) column (remove currency symbols and convert to numeric)
        if df["Price(₹)"].dtype == 'object':  # Check if the column is of type string
            df["Price(₹)"] = df["Price(₹)"].str.replace('₹', '').str.replace(',', '').astype(float)
        else:
            df["Price(₹)"] = df["Price(₹)"].astype(float)  # Ensure it's numeric

        # Drop rows with missing or invalid values in the Price(₹) column
        df = df.dropna(subset=["Price(₹)"])

        # Display scraped data
        st.write("Scraped Data:")
        st.write(df)

        # Line Chart for selected companies
        st.subheader("Individual Stock Price Trends")
        all_companies = df["Stock Name"].unique()
        selected_companies = st.multiselect("Select Companies", all_companies)

        if selected_companies:
            for company in selected_companies:
                # Generate random fluctuations for the selected company
                num_days = 30  # Number of days to simulate
                date_range = pd.date_range(start='2023-01-01', periods=num_days, freq='D')

                base_price = df[df["Stock Name"] == company]["Price(₹)"].values[0]
                fluctuations = np.random.normal(loc=0, scale=5, size=num_days)  # Random fluctuations
                prices = base_price + np.cumsum(fluctuations)  # Add fluctuations to base price

                # Create a DataFrame for the selected company
                company_data = pd.DataFrame({
                    "Date": date_range,
                    "Price(₹)": prices
                })

                # Debugging: Display the filtered data
                st.write(f"Data for {company}:")
                st.write(company_data)

                # Plot the line graph
                fig_line = px.line(
                    company_data,
                    x="Date",  # Use the Date column for the x-axis
                    y="Price(₹)",
                    title=f"{company} Stock Price Trend",
                    color_discrete_sequence=px.colors.qualitative.Dark24,
                    markers=True  # Add markers to the line chart
                )
                st.plotly_chart(fig_line)
        else:
            st.warning("Please select at least one company to view trends.")


# Enhanced Loan Eligibility Checker
def loan_checker():
    st.header("🎓 Education Loan Eligibility Checker")
    
    # Bank interest rate data
    bank_rates = [
        {"Bank Name": "State Bank of India", "Min Credit Score": 650, "Max Loan Amount": 1500000, "Base Rate": 8.5},
        {"Bank Name": "HDFC Bank", "Min Credit Score": 700, "Max Loan Amount": 2000000, "Base Rate": 9.0},
        {"Bank Name": "ICICI Bank", "Min Credit Score": 680, "Max Loan Amount": 1750000, "Base Rate": 8.75},
        {"Bank Name": "Axis Bank", "Min Credit Score": 670, "Max Loan Amount": 1600000, "Base Rate": 9.25},
    ]

    with st.form("loan_form"):
        # Personal Information
        st.subheader("Personal Information")
        col1, col2 = st.columns(2)
        with col1:
            full_name = st.text_input("Full Name")
            dob = st.date_input("Date of Birth", min_value=pd.to_datetime('1940-01-01'))
            country = st.selectbox("Country", ["India", "USA", "UK", "Canada", "Australia"])
        with col2:
            state = st.text_input("State")
            religion = st.selectbox("Religion", ["Hindu", "Muslim", "Christian", "Sikh", "Other"])
            caste = st.selectbox("Caste Category", ["General", "OBC", "SC", "ST", "Other"])
        
        family_income = st.number_input("Family Income (₹)", min_value=0, step=1000)

        # Academic Qualifications
        st.subheader("Academic Qualifications")
        school_name = st.text_input("School Name")
        tenth_percent = st.number_input("10th Percentage", min_value=0.0, max_value=100.0, step=0.1)
        
        st.markdown("### Higher Education Details")
        education_level = st.radio("Higher Education", ["12th", "Diploma", "Graduation"], horizontal=True)
        
        if education_level == "12th":
            twelveth_percent = st.number_input(" Percentage", min_value=0.0, max_value=100.0, step=0.1)
            twelveth_college = st.text_input(" College Name")
        elif education_level == "Diploma":
            diploma_percent = st.number_input("Diploma Percentage", min_value=0.0, max_value=100.0, step=0.1)
        else:
            grad_percent = st.number_input("Graduation Percentage", min_value=0.0, max_value=100.0, step=0.1)

        # Course Information
        st.subheader("Course Details")
        course_type = st.selectbox("Course Type", ["Engineering", "Medical", "MBA", "Law", "Arts", "Vocational Training", "PhD"])
        uni_name = st.text_input("University/Institution Name")
        uni_state = st.text_input("State of Institution")

        # Course Fee Information
        st.subheader("Fee Structure")
        tuition_fee = st.number_input("Tuition Fee (₹)", min_value=0, step=1000)
        exam_fee = st.number_input("Exam Fee (₹)", min_value=0, step=1000)
        living_type = st.radio("Living Type", ["Day Scholar", "Hosteller"], horizontal=True)
        
        if living_type == "Hosteller":
            hostel_fee = st.number_input("Hostel Fee (₹)", min_value=0, step=1000)
        else:
            travel_fee = st.number_input("Travel Fee (₹)/ Hostel fee(₹)", min_value=0, step=1000)

        # Parent Details
        st.subheader("Parent/Guardian Details")
        father_name = st.text_input("Father's Name")
        mother_name = st.text_input("Mother's Name")
        bank_name = st.text_input("Bank Name")
        branch_name = st.text_input("Branch Name")
        credit_score = st.number_input("Credit Score", min_value=300, max_value=900)

        if st.form_submit_button("Check Eligibility"):
            eligibility = True
            reasons = []
            
            if credit_score < 650:
                eligibility = False
                reasons.append("Credit score below 650")
                
            if family_income < 300000:
                eligibility = False
                reasons.append("Family income below ₹3L")
                
            if tenth_percent < 60:
                eligibility = False
                reasons.append("10th percentage below 60%")
                
            if "Engineering" in course_type and tuition_fee > 1000000:
                eligibility = False
                reasons.append("Engineering course fee exceeds limits")
                
            if eligibility:
                st.success("🎉 Congratulations! You're eligible for education loan!")
                
                # Calculate total loan requirement
                total_loan = tuition_fee + exam_fee + (hostel_fee if living_type == "Hosteller" else travel_fee)
                
                # Find eligible banks
                eligible_banks = []
                for bank in bank_rates:
                    if credit_score >= bank["Min Credit Score"] and total_loan <= bank["Max Loan Amount"]:
                        # Calculate final interest rate with caste benefits
                        final_rate = bank["Base Rate"]
                        if caste in ["SC", "ST"]:
                            final_rate -= 1.5
                        elif caste == "OBC":
                            final_rate -= 0.75
                        final_rate = max(final_rate, 7.5)  # Minimum rate
                        
                        eligible_banks.append({
                            "Bank Name": bank["Bank Name"],
                            "Interest Rate": f"{final_rate}%",
                            "Max Loan Amount": f"₹{bank['Max Loan Amount']:,}"
                        })

                # Display eligible banks
                st.subheader("Available Loan Options")
                if eligible_banks:
                    df = pd.DataFrame(eligible_banks)
                    st.dataframe(df.style.highlight_max(subset=['Interest Rate'], color='lightgreen'), 
                                 use_container_width=True)
                else:
                    st.warning("No banks found matching your criteria")
                
            else:
                st.error(f"⚠️ Eligibility not met. Reasons: {', '.join(reasons)}")
                st.markdown("💡 **Suggestions:** Improve credit score, explore scholarship options, or consider alternative funding sources.")

# Main Function
def main():
    if 'current_page' not in st.session_state:
        st.session_state['current_page'] = "login"

    if not st.session_state['logged_in']:
        if st.session_state['current_page'] == "login":
            login_page()
            if st.button("Don't have an account? Sign Up"):
                st.session_state['current_page'] = "signup"
                st.rerun()
        elif st.session_state['current_page'] == "signup":
            signup_page()
            if st.button("Already have an account? Log In"):
                st.session_state['current_page'] = "login"
                st.rerun()
    else:
        selection = sidebar()

        if selection == "Home":
            home_page()
        elif selection == "Smart Document Analysis":
            data_type = st.selectbox("Choose Data Type", ["Structured", "Semi-Structured", "Unstructured"])
            
            if data_type == "Structured":
                process_structured_data()
            elif data_type == "Semi-Structured":
                process_semi_structured_data()
            elif data_type == "Unstructured":
                process_unstructured_data()
        elif selection == "Education Loan Eligibility":
            loan_checker()

if __name__ == "__main__":
    main()