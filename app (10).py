# 🌍 Food Wastage Management System - Complete Edition
# Combining all functionality from both files with 15+ comprehensive SQL queries
# FIXED: Text visibility issues in dropdowns and navigation
# FIXED: Chart readability and styling
# ADDED: Time series trend analysis

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os
import sqlite3
from sqlalchemy import create_engine, text

# Page Configuration
st.set_page_config(
    page_title="🌍 Food Wastage Management System",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# FIXED: Enhanced CSS for complete text visibility fix
st.markdown("""
<style>
    /* Sidebar styling - FIXED for visibility */
    section[data-testid="stSidebar"] {
        background-color: #f0f2f6 !important;
    }
    section[data-testid="stSidebar"] * {
        color: #0e1117 !important;
    }
    section[data-testid="stSidebar"] .stSelectbox > div[data-baseweb="select"] > div {
        color: #0e1117 !important;
        background-color: white !important;
    }
    section[data-testid="stSidebar"] .stSelectbox label {
        color: #0e1117 !important;
        font-weight: bold !important;
    }
    
    /* FIXED: Main content text visibility */
    .main .block-container {
        color: #0e1117 !important;
    }
    
    /* FIXED: Metric cards text visibility */
    .stMetric {
        background-color: white !important;
        padding: 1rem !important;
        border-radius: 8px !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
        border: 1px solid #e0e0e0 !important;
    }
    .stMetric > div {
        color: #0e1117 !important;
    }
    .stMetric label {
        color: #0e1117 !important;
        font-weight: bold !important;
        font-size: 14px !important;
    }
    .stMetric .metric-value {
        color: #0e1117 !important;
        font-weight: bold !important;
        font-size: 24px !important;
    }
    div[data-testid="metric-container"] {
        background-color: white !important;
        border: 1px solid #e0e0e0 !important;
        padding: 1rem !important;
        border-radius: 8px !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
    }
    div[data-testid="metric-container"] > div {
        color: #0e1117 !important;
    }
    div[data-testid="metric-container"] label {
        color: #0e1117 !important;
        font-weight: bold !important;
    }
    
    /* FIXED: Headers and text visibility */
    .main h1, .main h2, .main h3, .main h4, .main h5, .main h6 {
        color: #0e1117 !important;
        font-weight: bold !important;
    }
    .main p, .main div, .main span {
        color: #0e1117 !important;
    }
    
    /* FIXED: Dataframe text visibility */
    .stDataFrame {
        background-color: white !important;
    }
    .stDataFrame table {
        color: #0e1117 !important;
        background-color: white !important;
    }
    .stDataFrame th {
        background-color: #f8f9fa !important;
        color: #0e1117 !important;
        font-weight: bold !important;
    }
    .stDataFrame td {
        color: #0e1117 !important;
        background-color: white !important;
    }
    
    /* FIXED: Button text visibility */
    .stButton > button {
        color: white !important;
        background-color: #667eea !important;
        border: none !important;
        font-weight: bold !important;
    }
    .stButton > button:hover {
        background-color: #5a6fd8 !important;
        color: white !important;
    }
    
    /* FIXED: Input field text visibility */
    .stTextInput > div > div > input {
        color: #0e1117 !important;
        background-color: white !important;
        border: 1px solid #e0e0e0 !important;
    }
    .stTextInput label {
        color: #0e1117 !important;
        font-weight: bold !important;
    }
    .stNumberInput > div > div > input {
        color: #0e1117 !important;
        background-color: white !important;
        border: 1px solid #e0e0e0 !important;
    }
    .stNumberInput label {
        color: #0e1117 !important;
        font-weight: bold !important;
    }
    .stDateInput > div > div > input {
        color: #0e1117 !important;
        background-color: white !important;
        border: 1px solid #e0e0e0 !important;
    }
    .stDateInput label {
        color: #0e1117 !important;
        font-weight: bold !important;
    }
    .stTextArea > div > div > textarea {
        color: #0e1117 !important;
        background-color: white !important;
        border: 1px solid #e0e0e0 !important;
    }
    .stTextArea label {
        color: #0e1117 !important;
        font-weight: bold !important;
    }
    
    /* FIXED: Selectbox text visibility */
    .stSelectbox > div > div {
        background-color: white !important;
        color: #0e1117 !important;
        border: 1px solid #e0e0e0 !important;
    }
    .stSelectbox label {
        color: #0e1117 !important;
        font-weight: bold !important;
    }
    
    /* FIXED: Expander text visibility */

/* EXTRA: Ensure expander headers are readable in dark themes */
details[data-testid="stExpander"] > summary {
    color: #0e1117 !important;
    background-color: #ffffff !important;
    font-weight: 700 !important;
    border: 1px solid #e0e0e0 !important;
    border-radius: 8px !important;
}
details[data-testid="stExpander"] > summary * {
    color: #0e1117 !important;
}
details[data-testid="stExpander"] svg {
    color: #0e1117 !important;
    fill: #0e1117 !important;
}

    .stExpander {
        background-color: white !important;
        border: 1px solid #e0e0e0 !important;
    }
    .stExpander > div > div > div {
        color: #0e1117 !important;
    }
    
    /* FIXED: Tab text visibility */
    .stTabs [data-baseweb="tab-list"] {
        background-color: white !important;
    }
    .stTabs [data-baseweb="tab"] {
        color: #0e1117 !important;
        font-weight: bold !important;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: #667eea !important;
        color: white !important;
    }
    
    /* Main header styling */
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    .main-header h1 {
        color: white !important;
        margin-bottom: 0.5rem;
    }
    .main-header p {
        color: white !important;
        margin-bottom: 0.25rem;
    }
    
    /* FIXED: Info and warning boxes */
    .stInfo, .stWarning, .stError, .stSuccess {
        color: #0e1117 !important;
    }
    .stInfo > div {
        color: #0e1117 !important;
    }
    .stWarning > div {
        color: #0e1117 !important;
    }
    .stError > div {
        color: #0e1117 !important;
    }
    .stSuccess > div {
        color: #0e1117 !important;
    }
    
    /* FIXED: Chart container styling */
    .js-plotly-plot {
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        background-color: white !important;
        margin-bottom: 2rem;
    }
    
    /* FIXED: Footer text */
    .main footer {
        color: #666 !important;
    }
</style>
""", unsafe_allow_html=True)

# ========== DATABASE SETUP ==========
@st.cache_resource
def init_database():
    """Initialize SQLite database and create tables"""
    engine = create_engine('sqlite:///food_wastage.db', echo=False)
    return engine

engine = init_database()

# ========== DATA LOADING WITH COLUMN MAPPING ==========
@st.cache_data
def load_all_data():
    """Load CSV files with comprehensive column mapping"""
    data = {}
    loading_status = {}
    
    # Providers Data Loading
    try:
        providers_df = pd.read_csv('providers_data.csv')
        # Column mapping
        provider_column_mapping = {
            'Provider_ID': 'provider_id', 'ID': 'provider_id',
            'Name': 'name', 'Provider_Name': 'name',
            'Type': 'type', 'Provider_Type': 'type',
            'Address': 'address', 'City': 'city', 'Location': 'city',
            'Contact': 'contact', 'Phone': 'contact', 'Email': 'contact'
        }
        
        for old_col, new_col in provider_column_mapping.items():
            if old_col in providers_df.columns:
                providers_df = providers_df.rename(columns={old_col: new_col})
        
        # Ensure required columns
        required_cols = ['provider_id', 'name', 'type', 'city', 'contact']
        for col in required_cols:
            if col not in providers_df.columns:
                if col == 'provider_id':
                    providers_df['provider_id'] = range(1, len(providers_df) + 1)
                else:
                    providers_df[col] = 'N/A'
        
        data['providers'] = providers_df
        loading_status['providers'] = f"✅ Providers data loaded successfully"
        
    except Exception as e:
        data['providers'] = pd.DataFrame()
        loading_status['providers'] = f"❌ Could not load providers: {str(e)}"

    # Receivers Data Loading
    try:
        receivers_df = pd.read_csv('receivers_data.csv')
        receiver_column_mapping = {
            'Receiver_ID': 'receiver_id', 'ID': 'receiver_id',
            'Name': 'name', 'Receiver_Name': 'name',
            'Type': 'type', 'Receiver_Type': 'type',
            'City': 'city', 'Location': 'city',
            'Contact': 'contact', 'Phone': 'contact', 'Email': 'contact'
        }
        
        for old_col, new_col in receiver_column_mapping.items():
            if old_col in receivers_df.columns:
                receivers_df = receivers_df.rename(columns={old_col: new_col})
        
        required_cols = ['receiver_id', 'name', 'type', 'city', 'contact']
        for col in required_cols:
            if col not in receivers_df.columns:
                if col == 'receiver_id':
                    receivers_df['receiver_id'] = range(1, len(receivers_df) + 1)
                else:
                    receivers_df[col] = 'N/A'
        
        data['receivers'] = receivers_df
        loading_status['receivers'] = f"✅ Receivers data loaded successfully"
        
    except Exception as e:
        data['receivers'] = pd.DataFrame()
        loading_status['receivers'] = f"❌ Could not load receivers: {str(e)}"

    # Food Listings Data Loading
    try:
        food_df = pd.read_csv('food_listings_data.csv')
        food_column_mapping = {
            'Food_ID': 'food_id', 'ID': 'food_id',
            'Food_Name': 'food_name', 'Name': 'food_name',
            'Quantity': 'quantity', 'Amount': 'quantity',
            'Expiry_Date': 'expiry_date', 'Expiration': 'expiry_date',
            'Provider_ID': 'provider_id',
            'Food_Type': 'food_type', 'Type': 'food_type',
            'Meal_Type': 'meal_type', 'Meal': 'meal_type',
            'Location': 'location', 'City': 'location'
        }
        
        for old_col, new_col in food_column_mapping.items():
            if old_col in food_df.columns:
                food_df = food_df.rename(columns={old_col: new_col})
        
        # Date conversion and urgency calculation
        if 'expiry_date' in food_df.columns:
            food_df['expiry_date'] = pd.to_datetime(food_df['expiry_date'], errors='coerce')
            today = pd.Timestamp.now()
            food_df['days_until_expiry'] = (food_df['expiry_date'] - today).dt.days
            food_df['urgency'] = food_df['days_until_expiry'].apply(
                lambda x: 'Critical' if x <= 1 else 'Urgent' if x <= 3 else 'Soon' if x <= 7 else 'Normal'
            )
        
        data['food_listings'] = food_df
        loading_status['food_listings'] = f"✅ Food listings loaded successfully"
        
    except Exception as e:
        data['food_listings'] = pd.DataFrame()
        loading_status['food_listings'] = f"❌ Could not load food listings: {str(e)}"

    # Claims Data Loading
    try:
        if os.path.exists('claims_data.csv'):
            claims_df = pd.read_csv('claims_data.csv')
            claims_column_mapping = {
                'Claim_ID': 'claim_id', 'ID': 'claim_id',
                'Food_ID': 'food_id', 'Receiver_ID': 'receiver_id',
                'Status': 'status', 'Timestamp': 'timestamp',
                'Date': 'timestamp', 'Created_At': 'timestamp'
            }
            
            for old_col, new_col in claims_column_mapping.items():
                if old_col in claims_df.columns:
                    claims_df = claims_df.rename(columns={old_col: new_col})
            
            if 'timestamp' in claims_df.columns:
                claims_df['timestamp'] = pd.to_datetime(claims_df['timestamp'], errors='coerce')
        else:
            # Generate sample claims with realistic time series data
            if not data['food_listings'].empty and not data['receivers'].empty:
                sample_size = min(200, len(data['food_listings']))
                # Create realistic timestamp distribution over the last 6 months
                end_date = datetime.now()
                start_date = end_date - timedelta(days=180)
                timestamps = pd.date_range(start=start_date, end=end_date, periods=sample_size)
                
                claims_df = pd.DataFrame({
                    'claim_id': range(1, sample_size + 1),
                    'food_id': data['food_listings']['food_id'].sample(sample_size, replace=True).values,
                    'receiver_id': data['receivers']['receiver_id'].sample(sample_size, replace=True).values,
                    'status': (['Completed'] * int(sample_size * 0.65) + 
                              ['Pending'] * int(sample_size * 0.20) + 
                              ['Cancelled'] * int(sample_size * 0.15))[:sample_size],
                    'timestamp': timestamps
                })
            else:
                claims_df = pd.DataFrame()
        
        data['claims'] = claims_df
        loading_status['claims'] = f"✅ Claims data loaded successfully"
        
    except Exception as e:
        data['claims'] = pd.DataFrame()
        loading_status['claims'] = f"❌ Could not load claims: {str(e)}"

    return data, loading_status

# Load data and populate database
data, status = load_all_data()

def populate_database():
    """Populate SQLite database with CSV data"""
    try:
        for table_name, df in data.items():
            if not df.empty:
                df.to_sql(table_name, engine, if_exists='replace', index=False)
    except Exception as e:
        st.error(f"Database population error: {e}")

populate_database()


class CRUDOperations:
    """CRUD operations for all entities"""
    
    @staticmethod
    def add_provider(name, provider_type, city, contact, address=""):
        """Add new provider"""
        try:
            new_id = len(data['providers']) + 1
            new_provider = pd.DataFrame({
                'provider_id': [new_id],
                'name': [name],
                'type': [provider_type],
                'city': [city],
                'contact': [contact],
                'address': [address]
            })
            new_provider.to_sql('providers', engine, if_exists='append', index=False)
            st.cache_data.clear()
            return True, "Provider added successfully!"
        except Exception as e:
            return False, f"Error adding provider: {e}"

    @staticmethod
    def add_receiver(name, receiver_type, city, contact):
        """Add new receiver"""
        try:
            new_id = len(data['receivers']) + 1
            new_receiver = pd.DataFrame({
                'receiver_id': [new_id],
                'name': [name],
                'type': [receiver_type],
                'city': [city],
                'contact': [contact]
            })
            new_receiver.to_sql('receivers', engine, if_exists='append', index=False)
            st.cache_data.clear()
            return True, "Receiver added successfully!"
        except Exception as e:
            return False, f"Error adding receiver: {e}"

    @staticmethod
    def add_food_listing(food_name, quantity, expiry_date, provider_id, food_type, meal_type):
        """Add new food listing"""
        try:
            new_id = len(data['food_listings']) + 1
            new_food = pd.DataFrame({
                'food_id': [new_id],
                'food_name': [food_name],
                'quantity': [quantity],
                'expiry_date': [expiry_date],
                'provider_id': [provider_id],
                'food_type': [food_type],
                'meal_type': [meal_type]
            })
            new_food.to_sql('food_listings', engine, if_exists='append', index=False)
            st.cache_data.clear()
            return True, "Food listing added successfully!"
        except Exception as e:
            return False, f"Error adding food listing: {e}"

    @staticmethod
    def add_claim(food_id, receiver_id, status="Pending"):
        """Add new claim"""
        try:
            new_id = len(data['claims']) + 1
            new_claim = pd.DataFrame({
                'claim_id': [new_id],
                'food_id': [food_id],
                'receiver_id': [receiver_id],
                'status': [status],
                'timestamp': [datetime.now()]
            })
            new_claim.to_sql('claims', engine, if_exists='append', index=False)
            st.cache_data.clear()
            return True, "Claim added successfully!"
        except Exception as e:
            return False, f"Error adding claim: {e}"

# ========== COMPLETE SQL QUERIES CLASS (ALL 15+ QUERIES) ==========
class SQLQueries:
    """Complete SQL queries covering all project requirements and additional analysis"""
    
    @staticmethod
    def execute_query(query):
        """Execute SQL query and return results"""
        try:
            with engine.connect() as conn:
                result = pd.read_sql(query, conn)
                return result
        except Exception as e:
            st.error(f"Query execution error: {e}")
            return pd.DataFrame()


    @staticmethod
    def get_items_expiring_next_3_days():
        """14. Items expiring in the next 3 days with provider & city"""
        query = """
        SELECT 
            f.food_id, f.food_name, f.quantity, f.expiry_date,
            p.provider_id, p.name AS provider_name, p.city
        FROM food_listings f
        JOIN providers p ON f.provider_id = p.provider_id
        WHERE DATE(f.expiry_date) BETWEEN DATE('now') AND DATE('now','+3 days')
        ORDER BY f.expiry_date
        """
        return SQLQueries.execute_query(query)

    @staticmethod
    def get_provider_reliability_pct():
        """15. Provider reliability = % completed claims"""
        query = """
        SELECT 
            p.provider_id, p.name AS provider_name, p.city,
            COUNT(c.claim_id) AS total_claims,
            SUM(CASE WHEN LOWER(c.status)='completed' THEN 1 ELSE 0 END) AS completed_claims,
            ROUND(100.0 * SUM(CASE WHEN LOWER(c.status)='completed' THEN 1 ELSE 0 END) / NULLIF(COUNT(c.claim_id),0), 2) AS reliability_pct
        FROM providers p
        LEFT JOIN food_listings f ON p.provider_id = f.provider_id
        LEFT JOIN claims c ON f.food_id = c.food_id
        GROUP BY p.provider_id
        ORDER BY reliability_pct DESC NULLS LAST, total_claims DESC
        """
        return SQLQueries.execute_query(query)

    @staticmethod
    def get_food_type_wastage_pct():
        """16. Wastage % by food_type"""
        query = """
        SELECT 
            f.food_type,
            SUM(f.quantity) AS total_quantity,
            SUM(CASE WHEN DATE(f.expiry_date) < DATE('now') THEN f.quantity ELSE 0 END) AS wasted_quantity,
            ROUND(100.0 * SUM(CASE WHEN DATE(f.expiry_date) < DATE('now') THEN f.quantity ELSE 0 END) / NULLIF(SUM(f.quantity),0), 2) AS wastage_pct
        FROM food_listings f
        GROUP BY f.food_type
        ORDER BY wastage_pct DESC
        """
        return SQLQueries.execute_query(query)

    @staticmethod
    def get_highest_demand_locations_by_claims():
        """20. Highest demand locations by claims (city)"""
        query = """
        SELECT 
            p.city AS location,
            COUNT(c.claim_id) AS total_claims
        FROM claims c
        JOIN food_listings f ON c.food_id = f.food_id
        JOIN providers p ON f.provider_id = p.provider_id
        GROUP BY p.city
        ORDER BY total_claims DESC
        LIMIT 10
        """
        return SQLQueries.execute_query(query)

    @staticmethod
    def get_most_frequent_providers_contributions():
        """19. Most frequent providers & their contributions"""
        query = """
        SELECT 
            p.name AS provider_name,
            COUNT(f.food_id) AS total_listings,
            COALESCE(SUM(f.quantity),0) AS total_quantity
        FROM food_listings f
        JOIN providers p ON f.provider_id = p.provider_id
        GROUP BY p.name
        ORDER BY total_listings DESC
        LIMIT 10
        """
        return SQLQueries.execute_query(query)

    # ========== REQUESTED QUERIES 1-15 ==========
    @staticmethod
    def get_providers_receivers_per_city():
        """1. How many food providers and receivers are there in each city?"""
        query = """
        SELECT 
            COALESCE(p.city, r.city) as city,
            COUNT(DISTINCT p.provider_id) as total_providers,
            COUNT(DISTINCT r.receiver_id) as total_receivers,
            -- Provider type breakdown
            COUNT(DISTINCT CASE WHEN p.type = 'Restaurant' THEN p.provider_id END) as restaurants,
            COUNT(DISTINCT CASE WHEN p.type = 'Grocery Store' THEN p.provider_id END) as grocery_stores,
            COUNT(DISTINCT CASE WHEN p.type = 'Hotel' THEN p.provider_id END) as hotels,
            COUNT(DISTINCT CASE WHEN p.type = 'Supermarket' THEN p.provider_id END) as supermarkets,
            -- Receiver type breakdown
            COUNT(DISTINCT CASE WHEN r.type = 'NGO' THEN r.receiver_id END) as ngos,
            COUNT(DISTINCT CASE WHEN r.type = 'Food Bank' THEN r.receiver_id END) as food_banks,
            COUNT(DISTINCT CASE WHEN r.type = 'Shelter' THEN r.receiver_id END) as shelters,
            COUNT(DISTINCT CASE WHEN r.type = 'Charity' THEN r.receiver_id END) as charities,
            -- Total ecosystem strength
            (COUNT(DISTINCT p.provider_id) + COUNT(DISTINCT r.receiver_id)) as total_ecosystem_strength
        FROM providers p 
        LEFT JOIN receivers r ON p.city = r.city
        GROUP BY COALESCE(p.city, r.city)
        HAVING COUNT(DISTINCT p.provider_id) > 0 OR COUNT(DISTINCT r.receiver_id) > 0
        ORDER BY total_ecosystem_strength DESC, total_providers DESC
        """
        return SQLQueries.execute_query(query)

    @staticmethod
    def get_provider_type_contributions():
        """2. Which type of food provider contributes the most food?"""
        query = """
        SELECT 
            p.type as provider_type,
            COUNT(DISTINCT p.provider_id) as total_providers,
            COUNT(f.food_id) as total_food_listings,
            SUM(f.quantity) as total_quantity_contributed,
            AVG(f.quantity) as avg_quantity_per_listing,
            -- Diversity metrics
            COUNT(DISTINCT f.food_type) as food_types_offered,
            COUNT(DISTINCT f.meal_type) as meal_types_offered,
            -- Success metrics
            COUNT(c.claim_id) as total_claims_received,
            COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) as successful_distributions,
            ROUND(100.0 * COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) / NULLIF(COUNT(c.claim_id), 0), 2) as success_rate,
            SUM(CASE WHEN LOWER(c.status) = 'completed' THEN f.quantity ELSE 0 END) as total_food_distributed,
            -- Impact per provider
            ROUND(SUM(f.quantity) / COUNT(DISTINCT p.provider_id), 2) as avg_contribution_per_provider,
            -- Ranking
            ROW_NUMBER() OVER (ORDER BY SUM(f.quantity) DESC) as contribution_rank
        FROM providers p 
        LEFT JOIN food_listings f ON p.provider_id = f.provider_id
        LEFT JOIN claims c ON f.food_id = c.food_id
        GROUP BY p.type
        HAVING COUNT(f.food_id) > 0
        ORDER BY total_quantity_contributed DESC
        """
        return SQLQueries.execute_query(query)

    @staticmethod
    def get_provider_contacts_by_city(city_name=None):
        """3. What is the contact information of food providers in a specific city?"""
        if city_name:
            where_clause = f"WHERE LOWER(p.city) = LOWER('{city_name}')"
        else:
            where_clause = ""
        
        query = f"""
        SELECT 
            p.provider_id,
            p.name as provider_name,
            p.type as provider_type,
            p.city,
            p.contact,
            COALESCE(p.address, 'N/A') as address,
            -- Activity metrics
            COUNT(f.food_id) as active_food_listings,
            SUM(f.quantity) as total_quantity_available,
            COUNT(DISTINCT f.food_type) as food_types_offered,
            -- Recent activity
            COUNT(CASE WHEN DATE(f.expiry_date) >= DATE('now') THEN 1 END) as fresh_items_available,
            COUNT(CASE WHEN DATE(f.expiry_date) < DATE('now') THEN 1 END) as expired_items,
            -- Claims received
            COUNT(c.claim_id) as claims_received,
            COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) as successful_claims,
            -- Status indicator
            CASE 
                WHEN COUNT(CASE WHEN DATE(f.expiry_date) >= DATE('now') THEN 1 END) > 0 THEN '🟢 Active'
                WHEN COUNT(f.food_id) > 0 THEN '🟡 Has Listings'
                ELSE '🔴 Inactive'
            END as status
        FROM providers p 
        LEFT JOIN food_listings f ON p.provider_id = f.provider_id
        LEFT JOIN claims c ON f.food_id = c.food_id
        {where_clause}
        GROUP BY p.provider_id, p.name, p.type, p.city, p.contact, p.address
        ORDER BY active_food_listings DESC, total_quantity_available DESC
        """
        return SQLQueries.execute_query(query)

    @staticmethod
    def get_top_claiming_receivers():
        """4. Which receivers have claimed the most food?"""
        query = """
        SELECT 
            r.receiver_id,
            r.name as receiver_name,
            r.type as receiver_type,
            r.city,
            r.contact,
            -- Claiming activity
            COUNT(c.claim_id) as total_claims_made,
            COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) as successful_claims,
            COUNT(CASE WHEN LOWER(c.status) = 'pending' THEN 1 END) as pending_claims,
            COUNT(CASE WHEN LOWER(c.status) = 'cancelled' THEN 1 END) as cancelled_claims,
            ROUND(100.0 * COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) / NULLIF(COUNT(c.claim_id), 0), 2) as success_rate,
            -- Food quantity metrics
            SUM(CASE WHEN LOWER(c.status) = 'completed' THEN f.quantity ELSE 0 END) as total_food_received,
            AVG(CASE WHEN LOWER(c.status) = 'completed' THEN f.quantity END) as avg_food_per_successful_claim,
            -- Food diversity
            COUNT(DISTINCT CASE WHEN LOWER(c.status) = 'completed' THEN f.food_type END) as food_types_received,
            COUNT(DISTINCT CASE WHEN LOWER(c.status) = 'completed' THEN f.meal_type END) as meal_types_received,
            -- Recent activity (last 30 days)
            COUNT(CASE WHEN DATE(c.timestamp) >= DATE('now', '-30 days') THEN 1 END) as recent_claims,
            -- Performance rating
            CASE 
                WHEN COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) >= 20 
                     AND (100.0 * COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) / NULLIF(COUNT(c.claim_id), 0)) >= 80 
                THEN '⭐⭐⭐ Excellent Receiver'
                WHEN COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) >= 10 
                     AND (100.0 * COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) / NULLIF(COUNT(c.claim_id), 0)) >= 60 
                THEN '⭐⭐ Good Receiver'
                WHEN COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) >= 1 
                THEN '⭐ Active Receiver'
                ELSE '❌ Inactive'
            END as receiver_rating
        FROM receivers r 
        LEFT JOIN claims c ON r.receiver_id = c.receiver_id
        LEFT JOIN food_listings f ON c.food_id = f.food_id
        GROUP BY r.receiver_id, r.name, r.type, r.city, r.contact
        HAVING COUNT(c.claim_id) > 0
        ORDER BY total_food_received DESC, total_claims_made DESC
        LIMIT 25
        """
        return SQLQueries.execute_query(query)

    @staticmethod
    def get_total_food_quantity_available():
        """5. What is the total quantity of food available from all providers?"""
        query = """
        SELECT 
            'System-Wide Food Availability' as metric_category,
            -- Overall availability
            COUNT(f.food_id) as total_food_items,
            SUM(f.quantity) as total_quantity_available,
            AVG(f.quantity) as avg_quantity_per_item,
            -- By freshness
            COUNT(CASE WHEN DATE(f.expiry_date) >= DATE('now') THEN 1 END) as fresh_items,
            SUM(CASE WHEN DATE(f.expiry_date) >= DATE('now') THEN f.quantity ELSE 0 END) as fresh_quantity,
            COUNT(CASE WHEN DATE(f.expiry_date) < DATE('now') THEN 1 END) as expired_items,
            SUM(CASE WHEN DATE(f.expiry_date) < DATE('now') THEN f.quantity ELSE 0 END) as expired_quantity,
            -- By urgency
            COUNT(CASE WHEN julianday(f.expiry_date) - julianday('now') <= 1 THEN 1 END) as urgent_items,
            SUM(CASE WHEN julianday(f.expiry_date) - julianday('now') <= 1 THEN f.quantity ELSE 0 END) as urgent_quantity,
            COUNT(CASE WHEN julianday(f.expiry_date) - julianday('now') BETWEEN 1 AND 7 THEN 1 END) as soon_expiring_items,
            SUM(CASE WHEN julianday(f.expiry_date) - julianday('now') BETWEEN 1 AND 7 THEN f.quantity ELSE 0 END) as soon_expiring_quantity,
            -- Distribution metrics
            COUNT(DISTINCT p.provider_id) as contributing_providers,
            COUNT(DISTINCT p.city) as cities_covered,
            COUNT(DISTINCT f.food_type) as food_types_available,
            COUNT(DISTINCT f.meal_type) as meal_types_available,
            -- Claims impact
            COUNT(c.claim_id) as total_claims,
            SUM(CASE WHEN LOWER(c.status) = 'completed' THEN f.quantity ELSE 0 END) as quantity_distributed,
            ROUND(100.0 * SUM(CASE WHEN LOWER(c.status) = 'completed' THEN f.quantity ELSE 0 END) / NULLIF(SUM(f.quantity), 0), 2) as distribution_rate,
            -- Efficiency metrics
            ROUND(SUM(f.quantity) / NULLIF(COUNT(DISTINCT p.provider_id), 0), 2) as avg_quantity_per_provider,
            ROUND(SUM(f.quantity) / NULLIF(COUNT(DISTINCT p.city), 0), 2) as avg_quantity_per_city
        FROM food_listings f 
        LEFT JOIN providers p ON f.provider_id = p.provider_id
        LEFT JOIN claims c ON f.food_id = c.food_id
        """
        return SQLQueries.execute_query(query)

    @staticmethod
    def get_cities_by_food_listings():
        """6. Which city has the highest number of food listings?"""
        query = """
        SELECT 
            p.city,
            COUNT(f.food_id) as total_food_listings,
            SUM(f.quantity) as total_quantity,
            AVG(f.quantity) as avg_quantity_per_listing,
            -- Provider diversity
            COUNT(DISTINCT p.provider_id) as unique_providers,
            COUNT(DISTINCT p.type) as provider_types,
            -- Food diversity
            COUNT(DISTINCT f.food_type) as food_types_available,
            COUNT(DISTINCT f.meal_type) as meal_types_available,
            -- Freshness analysis
            COUNT(CASE WHEN DATE(f.expiry_date) >= DATE('now') THEN 1 END) as fresh_listings,
            COUNT(CASE WHEN DATE(f.expiry_date) < DATE('now') THEN 1 END) as expired_listings,
            ROUND(100.0 * COUNT(CASE WHEN DATE(f.expiry_date) >= DATE('now') THEN 1 END) / COUNT(f.food_id), 2) as freshness_rate,
            -- Claims activity
            COUNT(c.claim_id) as total_claims,
            COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) as successful_claims,
            ROUND(100.0 * COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) / NULLIF(COUNT(c.claim_id), 0), 2) as claim_success_rate,
            -- City ranking
            ROW_NUMBER() OVER (ORDER BY COUNT(f.food_id) DESC) as listings_rank,
            ROW_NUMBER() OVER (ORDER BY SUM(f.quantity) DESC) as quantity_rank,
            -- City performance score (composite)
            ROUND(
                (COUNT(f.food_id) * 0.4) + 
                (SUM(f.quantity) * 0.3 / 100) + 
                (COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) * 0.3)
                , 2) as city_performance_score
        FROM providers p 
        JOIN food_listings f ON p.provider_id = f.provider_id
        LEFT JOIN claims c ON f.food_id = c.food_id
        GROUP BY p.city
        ORDER BY total_food_listings DESC, total_quantity DESC
        LIMIT 20
        """
        return SQLQueries.execute_query(query)

    @staticmethod
    def get_most_common_food_types():
        """7. What are the most commonly available food types?"""
        query = """
        SELECT 
            f.food_type,
            COUNT(f.food_id) as total_items,
            SUM(f.quantity) as total_quantity,
            AVG(f.quantity) as avg_quantity_per_item,
            -- Availability metrics
            COUNT(CASE WHEN DATE(f.expiry_date) >= DATE('now') THEN 1 END) as available_items,
            SUM(CASE WHEN DATE(f.expiry_date) >= DATE('now') THEN f.quantity ELSE 0 END) as available_quantity,
            -- Provider diversity
            COUNT(DISTINCT p.provider_id) as unique_providers,
            COUNT(DISTINCT p.type) as provider_types,
            COUNT(DISTINCT p.city) as cities_available,
            -- Meal type breakdown
            COUNT(DISTINCT f.meal_type) as meal_types,
            -- Demand analysis
            COUNT(c.claim_id) as total_claims,
            COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) as successful_claims,
            ROUND(100.0 * COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) / NULLIF(COUNT(c.claim_id), 0), 2) as claim_success_rate,
            -- Supply vs demand ratio
            ROUND(CAST(COUNT(f.food_id) AS FLOAT) / NULLIF(COUNT(c.claim_id), 0), 2) as supply_demand_ratio,
            -- Popularity ranking
            ROW_NUMBER() OVER (ORDER BY COUNT(f.food_id) DESC) as popularity_rank,
            ROW_NUMBER() OVER (ORDER BY COUNT(c.claim_id) DESC) as demand_rank,
            -- Market share
            ROUND(100.0 * COUNT(f.food_id) / (SELECT COUNT(*) FROM food_listings), 2) as market_share_percentage
        FROM food_listings f 
        LEFT JOIN providers p ON f.provider_id = p.provider_id
        LEFT JOIN claims c ON f.food_id = c.food_id
        GROUP BY f.food_type
        ORDER BY total_items DESC, total_quantity DESC
        """
        return SQLQueries.execute_query(query)

    @staticmethod
    def get_claims_per_food_item():
        """8. How many food claims have been made for each food item?"""
        query = """
        SELECT 
            f.food_id,
            f.food_name,
            f.food_type,
            f.meal_type,
            f.quantity,
            f.expiry_date,
            p.name as provider_name,
            p.type as provider_type,
            p.city as provider_city,
            -- Claims analysis
            COUNT(c.claim_id) as total_claims,
            COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) as completed_claims,
            COUNT(CASE WHEN LOWER(c.status) = 'pending' THEN 1 END) as pending_claims,
            COUNT(CASE WHEN LOWER(c.status) = 'cancelled' THEN 1 END) as cancelled_claims,
            -- Success metrics
            ROUND(100.0 * COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) / NULLIF(COUNT(c.claim_id), 0), 2) as success_rate,
            -- Timing analysis
            ROUND(AVG(julianday(f.expiry_date) - julianday(c.timestamp)), 1) as avg_days_before_expiry_when_claimed,
            -- Competition analysis
            ROUND(CAST(COUNT(c.claim_id) AS FLOAT) / f.quantity, 2) as claims_per_unit,
            -- Status
            CASE 
                WHEN DATE(f.expiry_date) < DATE('now') THEN '🔴 Expired'
                WHEN COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) > 0 THEN '🟢 Distributed'
                WHEN COUNT(c.claim_id) > 0 THEN '🟡 Has Claims'
                WHEN julianday(f.expiry_date) - julianday('now') <= 1 THEN '🟠 Urgent'
                ELSE '⚪ Available'
            END as item_status
        FROM food_listings f 
        JOIN providers p ON f.provider_id = p.provider_id
        LEFT JOIN claims c ON f.food_id = c.food_id
        GROUP BY f.food_id, f.food_name, f.food_type, f.meal_type, f.quantity, f.expiry_date, p.name, p.type, p.city
        ORDER BY total_claims DESC, f.food_id
        """
        return SQLQueries.execute_query(query)

    @staticmethod
    def get_provider_highest_successful_claims():
        """9. Which provider has had the highest number of successful food claims?"""
        query = """
        SELECT 
            p.provider_id,
            p.name as provider_name,
            p.type as provider_type,
            p.city,
            p.contact,
            -- Food provision metrics
            COUNT(f.food_id) as total_food_listings,
            SUM(f.quantity) as total_quantity_provided,
            COUNT(DISTINCT f.food_type) as food_types_diversity,
            -- Claims success metrics
            COUNT(c.claim_id) as total_claims_received,
            COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) as successful_claims,
            COUNT(CASE WHEN LOWER(c.status) = 'pending' THEN 1 END) as pending_claims,
            COUNT(CASE WHEN LOWER(c.status) = 'cancelled' THEN 1 END) as cancelled_claims,
            ROUND(100.0 * COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) / NULLIF(COUNT(c.claim_id), 0), 2) as success_rate,
            -- Impact metrics
            SUM(CASE WHEN LOWER(c.status) = 'completed' THEN f.quantity ELSE 0 END) as total_food_distributed,
            COUNT(DISTINCT CASE WHEN LOWER(c.status) = 'completed' THEN c.receiver_id END) as unique_receivers_served,
            -- Efficiency metrics
            ROUND(COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) / NULLIF(COUNT(f.food_id), 0), 2) as claims_per_listing,
            ROUND(SUM(CASE WHEN LOWER(c.status) = 'completed' THEN f.quantity ELSE 0 END) / NULLIF(COUNT(f.food_id), 0), 2) as avg_distributed_per_listing,
            -- Time efficiency
            ROUND(AVG(CASE WHEN LOWER(c.status) = 'completed' THEN julianday(f.expiry_date) - julianday(c.timestamp) END), 1) as avg_days_before_expiry_distributed,
            -- Recent performance (last 30 days)
            COUNT(CASE WHEN DATE(c.timestamp) >= DATE('now', '-30 days') AND LOWER(c.status) = 'completed' THEN 1 END) as recent_successful_claims,
            -- Awards/Recognition
            CASE 
                WHEN COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) >= 50 
                     AND (100.0 * COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) / NULLIF(COUNT(c.claim_id), 0)) >= 85 
                THEN '🏆 Champion Provider'
                WHEN COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) >= 25 
                     AND (100.0 * COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) / NULLIF(COUNT(c.claim_id), 0)) >= 75 
                THEN '⭐⭐⭐ Excellent Provider'
                WHEN COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) >= 10 
                     AND (100.0 * COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) / NULLIF(COUNT(c.claim_id), 0)) >= 60 
                THEN '⭐⭐ Good Provider'
                WHEN COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) >= 1 
                THEN '⭐ Active Provider'
                ELSE '❌ Inactive'
            END as provider_recognition
        FROM providers p 
        LEFT JOIN food_listings f ON p.provider_id = f.provider_id
        LEFT JOIN claims c ON f.food_id = c.food_id
        GROUP BY p.provider_id, p.name, p.type, p.city, p.contact
        HAVING COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) > 0
        ORDER BY successful_claims DESC, total_food_distributed DESC
        LIMIT 25
        """
        return SQLQueries.execute_query(query)

    @staticmethod
    def get_claims_completion_percentages():
        """10. What percentage of food claims are completed vs. pending vs. canceled?"""
        query = """
        SELECT 
            c.status,
            COUNT(*) as claim_count,
            ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM claims), 2) as percentage,
            -- Quantity analysis
            SUM(f.quantity) as total_quantity_involved,
            AVG(f.quantity) as avg_quantity_per_claim,
            -- Geographic distribution
            COUNT(DISTINCT p.city) as cities_involved,
            COUNT(DISTINCT p.provider_id) as providers_involved,
            COUNT(DISTINCT r.receiver_id) as receivers_involved,
            -- Food type diversity
            COUNT(DISTINCT f.food_type) as food_types_in_status,
            COUNT(DISTINCT f.meal_type) as meal_types_in_status,
            -- Time analysis
            ROUND(AVG(julianday('now') - julianday(c.timestamp)), 1) as avg_days_since_claim,
            ROUND(AVG(CASE WHEN LOWER(c.status) = 'completed' THEN julianday(f.expiry_date) - julianday(c.timestamp) END), 1) as avg_days_before_expiry_when_completed,
            -- Recent trends (last 30 days)
            COUNT(CASE WHEN DATE(c.timestamp) >= DATE('now', '-30 days') THEN 1 END) as recent_claims,
            ROUND(100.0 * COUNT(CASE WHEN DATE(c.timestamp) >= DATE('now', '-30 days') THEN 1 END) / 
                  NULLIF((SELECT COUNT(*) FROM claims WHERE DATE(timestamp) >= DATE('now', '-30 days')), 0), 2) as recent_percentage,
            -- Impact calculation
            CASE c.status 
                WHEN 'Completed' THEN SUM(f.quantity) 
                ELSE 0 
            END as food_impact_kg,
            -- Status insights
            CASE c.status 
                WHEN 'Completed' THEN '✅ Successfully distributed food to those in need'
                WHEN 'Pending' THEN '⏳ Awaiting pickup or processing'
                WHEN 'Cancelled' THEN '❌ Claims that did not proceed - investigate reasons'
                ELSE '❓ Unknown status'
            END as status_insight
        FROM claims c 
        JOIN food_listings f ON c.food_id = f.food_id
        JOIN providers p ON f.provider_id = p.provider_id
        LEFT JOIN receivers r ON c.receiver_id = r.receiver_id
        GROUP BY c.status
        ORDER BY claim_count DESC
        """
        return SQLQueries.execute_query(query)

    @staticmethod
    def get_avg_quantity_per_receiver():
        """11. What is the average quantity of food claimed per receiver?"""
        query = """
        SELECT 
            r.receiver_id,
            r.name as receiver_name,
            r.type as receiver_type,
            r.city,
            -- Claiming metrics
            COUNT(c.claim_id) as total_claims,
            COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) as successful_claims,
            SUM(CASE WHEN LOWER(c.status) = 'completed' THEN f.quantity ELSE 0 END) as total_food_received,
            ROUND(AVG(CASE WHEN LOWER(c.status) = 'completed' THEN f.quantity END), 2) as avg_quantity_per_successful_claim,
            ROUND(SUM(CASE WHEN LOWER(c.status) = 'completed' THEN f.quantity ELSE 0 END) / NULLIF(COUNT(c.claim_id), 0), 2) as avg_quantity_per_total_claim,
            -- Efficiency metrics
            ROUND(100.0 * COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) / NULLIF(COUNT(c.claim_id), 0), 2) as claim_success_rate,
            -- Food diversity received
            COUNT(DISTINCT CASE WHEN LOWER(c.status) = 'completed' THEN f.food_type END) as food_types_received,
            COUNT(DISTINCT CASE WHEN LOWER(c.status) = 'completed' THEN f.meal_type END) as meal_types_received,
            -- Provider diversity
            COUNT(DISTINCT CASE WHEN LOWER(c.status) = 'completed' THEN p.provider_id END) as providers_claimed_from,
            -- Time analysis
            ROUND(AVG(CASE WHEN LOWER(c.status) = 'completed' THEN julianday(f.expiry_date) - julianday(c.timestamp) END), 1) as avg_days_before_expiry_received,
            -- Recent activity
            COUNT(CASE WHEN DATE(c.timestamp) >= DATE('now', '-30 days') THEN 1 END) as recent_claims,
            SUM(CASE WHEN DATE(c.timestamp) >= DATE('now', '-30 days') AND LOWER(c.status) = 'completed' THEN f.quantity ELSE 0 END) as recent_food_received,
            -- Receiver category based on activity
            CASE 
                WHEN SUM(CASE WHEN LOWER(c.status) = 'completed' THEN f.quantity ELSE 0 END) >= 500 THEN '🏆 Major Recipient'
                WHEN SUM(CASE WHEN LOWER(c.status) = 'completed' THEN f.quantity ELSE 0 END) >= 200 THEN '⭐⭐⭐ High Volume'
                WHEN SUM(CASE WHEN LOWER(c.status) = 'completed' THEN f.quantity ELSE 0 END) >= 50 THEN '⭐⭐ Regular'
                WHEN SUM(CASE WHEN LOWER(c.status) = 'completed' THEN f.quantity ELSE 0 END) >= 1 THEN '⭐ Occasional'
                ELSE '❌ No Success'
            END as receiver_category
        FROM receivers r 
        LEFT JOIN claims c ON r.receiver_id = c.receiver_id
        LEFT JOIN food_listings f ON c.food_id = f.food_id
        LEFT JOIN providers p ON f.provider_id = p.provider_id
        GROUP BY r.receiver_id, r.name, r.type, r.city
        HAVING COUNT(c.claim_id) > 0
        ORDER BY total_food_received DESC, avg_quantity_per_successful_claim DESC
        """
        return SQLQueries.execute_query(query)

    @staticmethod
    def get_most_claimed_meal_types():
        """12. Which meal type is claimed the most?"""
        query = """
        SELECT 
            f.meal_type,
            -- Claiming metrics
            COUNT(c.claim_id) as total_claims,
            COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) as successful_claims,
            COUNT(CASE WHEN LOWER(c.status) = 'pending' THEN 1 END) as pending_claims,
            COUNT(CASE WHEN LOWER(c.status) = 'cancelled' THEN 1 END) as cancelled_claims,
            ROUND(100.0 * COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) / NULLIF(COUNT(c.claim_id), 0), 2) as success_rate,
            -- Quantity metrics
            SUM(CASE WHEN LOWER(c.status) = 'completed' THEN f.quantity ELSE 0 END) as total_quantity_distributed,
            AVG(CASE WHEN LOWER(c.status) = 'completed' THEN f.quantity END) as avg_quantity_per_successful_claim,
            -- Supply vs demand analysis
            COUNT(DISTINCT f.food_id) as total_items_available,
            ROUND(CAST(COUNT(c.claim_id) AS FLOAT) / NULLIF(COUNT(DISTINCT f.food_id), 0), 2) as demand_supply_ratio,
            -- Provider and receiver diversity
            COUNT(DISTINCT p.provider_id) as providers_offering,
            COUNT(DISTINCT r.receiver_id) as receivers_claiming,
            COUNT(DISTINCT p.city) as cities_with_supply,
            -- Food type diversity within meal type
            COUNT(DISTINCT f.food_type) as food_types_in_meal,
            -- Time analysis
            ROUND(AVG(julianday(f.expiry_date) - julianday('now')), 1) as avg_shelf_life_days,
            ROUND(AVG(CASE WHEN LOWER(c.status) = 'completed' THEN julianday(f.expiry_date) - julianday(c.timestamp) END), 1) as avg_days_before_expiry_claimed,
            -- Market share
            ROUND(100.0 * COUNT(c.claim_id) / (SELECT COUNT(*) FROM claims), 2) as claim_market_share,
            -- Popularity ranking
            ROW_NUMBER() OVER (ORDER BY COUNT(c.claim_id) DESC) as demand_rank,
            ROW_NUMBER() OVER (ORDER BY COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) DESC) as success_rank,
            -- Recent trends (last 30 days)
            COUNT(CASE WHEN DATE(c.timestamp) >= DATE('now', '-30 days') THEN 1 END) as recent_claims,
            -- Meal time insights
            CASE f.meal_type 
                WHEN 'Breakfast' THEN '🌅 Morning meals - typically fresh items needed'
                WHEN 'Lunch' THEN '🌞 Midday meals - highest volume period'
                WHEN 'Dinner' THEN '🌙 Evening meals - often hearty dishes'
                WHEN 'Snacks' THEN '🍪 Light items - good for quick distribution'
                WHEN 'Beverages' THEN '🥤 Drinks - long shelf life items'
                ELSE '🍽️ Mixed meal items'
            END as meal_type_insight
        FROM food_listings f 
        LEFT JOIN claims c ON f.food_id = c.food_id
        LEFT JOIN providers p ON f.provider_id = p.provider_id
        LEFT JOIN receivers r ON c.receiver_id = r.receiver_id
        GROUP BY f.meal_type
        ORDER BY total_claims DESC, successful_claims DESC
        """
        return SQLQueries.execute_query(query)

    @staticmethod
    def get_total_donations_per_provider():
        """13. What is the total quantity of food donated by each provider?"""
        query = """
        SELECT 
            p.provider_id,
            p.name as provider_name,
            p.type as provider_type,
            p.city,
            p.contact,
            -- Donation metrics
            COUNT(f.food_id) as total_food_items_listed,
            SUM(f.quantity) as total_quantity_donated,
            AVG(f.quantity) as avg_quantity_per_donation,
            -- Distribution success
            COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) as items_successfully_distributed,
            SUM(CASE WHEN LOWER(c.status) = 'completed' THEN f.quantity ELSE 0 END) as quantity_successfully_distributed,
            ROUND(100.0 * SUM(CASE WHEN LOWER(c.status) = 'completed' THEN f.quantity ELSE 0 END) / NULLIF(SUM(f.quantity), 0), 2) as distribution_success_rate,
            -- Wastage analysis
            COUNT(CASE WHEN julianday('now') - julianday(f.expiry_date) > 0 THEN 1 END) as expired_items,
            SUM(CASE WHEN julianday('now') - julianday(f.expiry_date) > 0 THEN f.quantity ELSE 0 END) as wasted_quantity,
            ROUND(100.0 * SUM(CASE WHEN julianday('now') - julianday(f.expiry_date) > 0 THEN f.quantity ELSE 0 END) / NULLIF(SUM(f.quantity), 0), 2) as wastage_rate,
            -- Food diversity
            COUNT(DISTINCT f.food_type) as food_types_donated,
            COUNT(DISTINCT f.meal_type) as meal_types_donated,
            -- Impact metrics
            COUNT(DISTINCT r.receiver_id) as unique_receivers_served,
            COUNT(DISTINCT CASE WHEN LOWER(c.status) = 'completed' THEN r.receiver_id END) as receivers_successfully_served,
            -- Time efficiency
            ROUND(AVG(julianday(f.expiry_date) - julianday('now')), 1) as avg_donation_shelf_life,
            ROUND(AVG(CASE WHEN LOWER(c.status) = 'completed' THEN julianday(f.expiry_date) - julianday(c.timestamp) END), 1) as avg_days_before_expiry_distributed,
            -- Recent activity (last 30 days)
            COUNT(CASE WHEN DATE(f.expiry_date) >= DATE('now', '-30 days') THEN 1 END) as recent_donations,
            SUM(CASE WHEN DATE(f.expiry_date) >= DATE('now', '-30 days') THEN f.quantity ELSE 0 END) as recent_donation_quantity,
            -- Provider impact score
            ROUND(
                (SUM(CASE WHEN LOWER(c.status) = 'completed' THEN f.quantity ELSE 0 END) * 0.6) +
                (COUNT(DISTINCT r.receiver_id) * 10 * 0.2) +
                (COUNT(DISTINCT f.food_type) * 5 * 0.2)
                , 2) as provider_impact_score,
            -- Recognition level
            CASE 
                WHEN SUM(CASE WHEN LOWER(c.status) = 'completed' THEN f.quantity ELSE 0 END) >= 1000 
                     AND (100.0 * SUM(CASE WHEN LOWER(c.status) = 'completed' THEN f.quantity ELSE 0 END) / NULLIF(SUM(f.quantity), 0)) >= 80 
                THEN '🏆 Champion Donor'
                WHEN SUM(CASE WHEN LOWER(c.status) = 'completed' THEN f.quantity ELSE 0 END) >= 500 
                     AND (100.0 * SUM(CASE WHEN LOWER(c.status) = 'completed' THEN f.quantity ELSE 0 END) / NULLIF(SUM(f.quantity), 0)) >= 70 
                THEN '⭐⭐⭐ Excellent Donor'
                WHEN SUM(CASE WHEN LOWER(c.status) = 'completed' THEN f.quantity ELSE 0 END) >= 200 
                     AND (100.0 * SUM(CASE WHEN LOWER(c.status) = 'completed' THEN f.quantity ELSE 0 END) / NULLIF(SUM(f.quantity), 0)) >= 60 
                THEN '⭐⭐ Good Donor'
                WHEN SUM(CASE WHEN LOWER(c.status) = 'completed' THEN f.quantity ELSE 0 END) >= 1 
                THEN '⭐ Active Donor'
                ELSE '❌ Inactive'
            END as donor_recognition
        FROM providers p 
        LEFT JOIN food_listings f ON p.provider_id = f.provider_id
        LEFT JOIN claims c ON f.food_id = c.food_id
        LEFT JOIN receivers r ON c.receiver_id = r.receiver_id
        GROUP BY p.provider_id, p.name, p.type, p.city, p.contact
        HAVING COUNT(f.food_id) > 0
        ORDER BY total_quantity_donated DESC, quantity_successfully_distributed DESC
        """
        return SQLQueries.execute_query(query)

    @staticmethod
    def get_food_wastage_trends_comprehensive():
        """14. Enhanced food wastage trends with all insights"""
        query = """
        SELECT 
            food_type,
            COUNT(*) as total_listings,
            SUM(quantity) as total_quantity,
            AVG(quantity) as avg_quantity_per_listing,
            -- Wastage calculations
            COUNT(CASE WHEN julianday('now') - julianday(expiry_date) > 0 THEN 1 END) as expired_items,
            SUM(CASE WHEN julianday('now') - julianday(expiry_date) > 0 THEN quantity ELSE 0 END) as wasted_quantity,
            ROUND(100.0 * COUNT(CASE WHEN julianday('now') - julianday(expiry_date) > 0 THEN 1 END) / COUNT(*), 2) as wastage_percentage,
            ROUND(100.0 * SUM(CASE WHEN julianday('now') - julianday(expiry_date) > 0 THEN quantity ELSE 0 END) / SUM(quantity), 2) as quantity_wastage_percentage,
            -- Urgency analysis
            COUNT(CASE WHEN julianday(expiry_date) - julianday('now') BETWEEN 0 AND 1 THEN 1 END) as critical_items,
            COUNT(CASE WHEN julianday(expiry_date) - julianday('now') BETWEEN 1 AND 3 THEN 1 END) as urgent_items,
            COUNT(CASE WHEN julianday(expiry_date) - julianday('now') BETWEEN 3 AND 7 THEN 1 END) as soon_items,
            COUNT(CASE WHEN julianday(expiry_date) - julianday('now') > 7 THEN 1 END) as safe_items,
            -- Claims impact
            COUNT(c.claim_id) as total_claims,
            COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) as successful_distributions,
            SUM(CASE WHEN LOWER(c.status) = 'completed' THEN quantity ELSE 0 END) as quantity_saved_through_claims,
            ROUND(100.0 * SUM(CASE WHEN LOWER(c.status) = 'completed' THEN quantity ELSE 0 END) / SUM(quantity), 2) as saved_percentage,
            -- Provider diversity
            COUNT(DISTINCT p.provider_id) as contributing_providers,
            COUNT(DISTINCT p.city) as cities_offering
        FROM food_listings f 
        LEFT JOIN claims c ON f.food_id = c.food_id
        LEFT JOIN providers p ON f.provider_id = p.provider_id
        GROUP BY food_type
        ORDER BY wasted_quantity DESC, total_quantity DESC
        """
        return SQLQueries.execute_query(query)

    @staticmethod
    def get_comprehensive_system_analysis():
        """15. Comprehensive analysis with all outputs and insights"""
        query = """
        WITH provider_stats AS (
            SELECT 
                p.type as provider_type,
                COUNT(DISTINCT p.provider_id) as provider_count,
                SUM(f.quantity) as total_contribution,
                COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) as successful_distributions
            FROM providers p 
            LEFT JOIN food_listings f ON p.provider_id = f.provider_id
            LEFT JOIN claims c ON f.food_id = c.food_id
            GROUP BY p.type
        ),
        city_stats AS (
            SELECT 
                p.city,
                COUNT(DISTINCT p.provider_id) as providers,
                COUNT(DISTINCT r.receiver_id) as receivers,
                COUNT(c.claim_id) as total_claims,
                SUM(CASE WHEN LOWER(c.status) = 'completed' THEN f.quantity ELSE 0 END) as food_distributed
            FROM providers p 
            LEFT JOIN receivers r ON p.city = r.city
            LEFT JOIN food_listings f ON p.provider_id = f.provider_id
            LEFT JOIN claims c ON f.food_id = c.food_id
            GROUP BY p.city
        ),
        food_stats AS (
            SELECT 
                f.food_type,
                COUNT(f.food_id) as total_items,
                SUM(f.quantity) as total_quantity,
                COUNT(CASE WHEN julianday('now') - julianday(f.expiry_date) > 0 THEN 1 END) as wasted_items,
                SUM(CASE WHEN julianday('now') - julianday(f.expiry_date) > 0 THEN f.quantity ELSE 0 END) as wasted_quantity
            FROM food_listings f 
            GROUP BY f.food_type
        )
        SELECT 
            'COMPREHENSIVE SYSTEM ANALYSIS' as analysis_category,
            -- Overall metrics
            (SELECT COUNT(*) FROM providers) as total_providers,
            (SELECT COUNT(*) FROM receivers) as total_receivers,
            (SELECT COUNT(*) FROM food_listings) as total_food_items,
            (SELECT SUM(quantity) FROM food_listings) as total_food_quantity,
            (SELECT COUNT(*) FROM claims) as total_claims,
            -- Performance metrics
            (SELECT COUNT(*) FROM claims WHERE LOWER(status) = 'completed') as successful_distributions,
            (SELECT ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM claims), 2) FROM claims WHERE LOWER(status) = 'completed') as success_rate,
            -- Top provider type
            (SELECT provider_type FROM provider_stats ORDER BY total_contribution DESC LIMIT 1) as top_provider_type_by_contribution,
            (SELECT total_contribution FROM provider_stats ORDER BY total_contribution DESC LIMIT 1) as top_provider_contribution,
            -- Top city
            (SELECT city FROM city_stats ORDER BY food_distributed DESC LIMIT 1) as top_city_by_distribution,
            (SELECT food_distributed FROM city_stats ORDER BY food_distributed DESC LIMIT 1) as top_city_distribution,
            -- Most wasted food type
            (SELECT food_type FROM food_stats ORDER BY wasted_quantity DESC LIMIT 1) as most_wasted_food_type,
            (SELECT wasted_quantity FROM food_stats ORDER BY wasted_quantity DESC LIMIT 1) as highest_waste_quantity,
            -- System health indicators
            (SELECT ROUND(100.0 * SUM(wasted_quantity) / SUM(total_quantity), 2) FROM food_stats) as overall_wastage_rate,
            (SELECT COUNT(*) FROM city_stats WHERE providers > 0 AND receivers > 0) as cities_with_complete_ecosystem,
            -- Key insights
            CASE 
                WHEN (SELECT ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM claims), 2) FROM claims WHERE LOWER(status) = 'completed') >= 80 
                THEN 'System performing excellently'
                WHEN (SELECT ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM claims), 2) FROM claims WHERE LOWER(status) = 'completed') >= 60 
                THEN 'System performing well with room for improvement'
                ELSE 'System needs significant optimization'
            END as overall_system_health,
            -- Action recommendations
            'Focus on ' || (SELECT food_type FROM food_stats ORDER BY wasted_quantity DESC LIMIT 1) || ' wastage reduction' as primary_action_needed,
            'Expand operations in ' || (SELECT city FROM city_stats ORDER BY (providers + receivers) ASC LIMIT 1) || ' for better coverage' as expansion_recommendation
        """
        return SQLQueries.execute_query(query)

    # ========== NEW: TIME SERIES ANALYSIS QUERIES ==========
    @staticmethod
    def get_time_series_claims_trends():
        """NEW: Time series analysis of claims trends"""
        query = """
        SELECT 
            DATE(c.timestamp) as claim_date,
            COUNT(*) as total_claims,
            COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) as completed_claims,
            COUNT(CASE WHEN LOWER(c.status) = 'pending' THEN 1 END) as pending_claims,
            COUNT(CASE WHEN LOWER(c.status) = 'cancelled' THEN 1 END) as cancelled_claims,
            SUM(f.quantity) as total_quantity_claimed,
            SUM(CASE WHEN LOWER(c.status) = 'completed' THEN f.quantity ELSE 0 END) as quantity_distributed,
            ROUND(100.0 * COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) / COUNT(*), 2) as daily_success_rate,
            -- Day of week analysis
            CASE strftime('%w', c.timestamp)
                WHEN '0' THEN 'Sunday'
                WHEN '1' THEN 'Monday'
                WHEN '2' THEN 'Tuesday'
                WHEN '3' THEN 'Wednesday'
                WHEN '4' THEN 'Thursday'
                WHEN '5' THEN 'Friday'
                WHEN '6' THEN 'Saturday'
            END as day_of_week,
            -- Month analysis
            strftime('%Y-%m', c.timestamp) as year_month
        FROM claims c 
        JOIN food_listings f ON c.food_id = f.food_id
        WHERE c.timestamp IS NOT NULL
        GROUP BY DATE(c.timestamp)
        ORDER BY claim_date
        """
        return SQLQueries.execute_query(query)

    @staticmethod
    def get_time_series_food_listings_trends():
        """NEW: Time series analysis of food listings by expiry trends"""
        query = """
        SELECT 
            DATE(f.expiry_date) as expiry_date,
            COUNT(*) as items_expiring,
            SUM(f.quantity) as quantity_expiring,
            COUNT(DISTINCT f.food_type) as food_types_expiring,
            COUNT(DISTINCT p.provider_id) as providers_affected,
            -- Claims before expiry
            COUNT(c.claim_id) as claims_made,
            COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) as items_saved,
            SUM(CASE WHEN LOWER(c.status) = 'completed' THEN f.quantity ELSE 0 END) as quantity_saved,
            -- Wastage calculation
            COUNT(*) - COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) as items_wasted,
            SUM(f.quantity) - SUM(CASE WHEN LOWER(c.status) = 'completed' THEN f.quantity ELSE 0 END) as quantity_wasted,
            ROUND(100.0 * COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) / COUNT(*), 2) as save_rate,
            -- Week analysis
            strftime('%Y-W%W', f.expiry_date) as year_week,
            strftime('%Y-%m', f.expiry_date) as year_month
        FROM food_listings f 
        LEFT JOIN providers p ON f.provider_id = p.provider_id
        LEFT JOIN claims c ON f.food_id = c.food_id
        WHERE f.expiry_date IS NOT NULL
        GROUP BY DATE(f.expiry_date)
        ORDER BY expiry_date
        """
        return SQLQueries.execute_query(query)

    @staticmethod
    def get_monthly_performance_trends():
        """NEW: Monthly performance trends analysis"""
        query = """
        SELECT 
            strftime('%Y-%m', c.timestamp) as month,
            COUNT(*) as total_claims,
            COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) as completed_claims,
            SUM(f.quantity) as total_quantity_involved,
            SUM(CASE WHEN LOWER(c.status) = 'completed' THEN f.quantity ELSE 0 END) as quantity_distributed,
            COUNT(DISTINCT p.provider_id) as active_providers,
            COUNT(DISTINCT r.receiver_id) as active_receivers,
            COUNT(DISTINCT p.city) as cities_involved,
            ROUND(100.0 * COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) / COUNT(*), 2) as monthly_success_rate,
            ROUND(AVG(julianday(f.expiry_date) - julianday(c.timestamp)), 1) as avg_days_before_expiry,
            -- Growth metrics
            LAG(COUNT(*)) OVER (ORDER BY strftime('%Y-%m', c.timestamp)) as prev_month_claims,
            ROUND(100.0 * (COUNT(*) - LAG(COUNT(*)) OVER (ORDER BY strftime('%Y-%m', c.timestamp))) / 
                  NULLIF(LAG(COUNT(*)) OVER (ORDER BY strftime('%Y-%m', c.timestamp)), 0), 2) as claims_growth_rate
        FROM claims c 
        JOIN food_listings f ON c.food_id = f.food_id
        JOIN providers p ON f.provider_id = p.provider_id
        LEFT JOIN receivers r ON c.receiver_id = r.receiver_id
        WHERE c.timestamp IS NOT NULL
        GROUP BY strftime('%Y-%m', c.timestamp)
        ORDER BY month
        """
        return SQLQueries.execute_query(query)

# ========== ENHANCED CHART STYLING FUNCTION ==========
def apply_readable_chart_style(fig, title, x_label=None, y_label=None):
    """Apply consistent readable styling to all charts"""
    fig.update_layout(
        # Title styling
        title={
            'text': title,
            'x': 0.5,
            'xanchor': 'center',
            'font': {
                'size': 20,
                'color': '#1f2937',
                'family': 'Arial, sans-serif'
            }
        },
        
        # Plot area styling
        plot_bgcolor='white',
        paper_bgcolor='white',
        
        # Font styling
        font={
            'size': 12,
            'color': '#374151',
            'family': 'Arial, sans-serif'
        },
        
        # Margins
        margin=dict(l=80, r=80, t=100, b=80),
        
        # Grid
        xaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='#e5e7eb',
            title=dict(
                text=x_label if x_label else "",
                font=dict(size=14, color='#1f2937')
            ),
            tickfont=dict(size=11, color='#374151')
        ),
        yaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='#e5e7eb',
            title=dict(
                text=y_label if y_label else "",
                font=dict(size=14, color='#1f2937')
            ),
            tickfont=dict(size=11, color='#374151')
        ),
        
        # Legend styling
        legend=dict(
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor='#d1d5db',
            borderwidth=1,
            font=dict(size=11, color='#374151')
        ),
        
        # Hover styling
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family="Arial",
            bordercolor='#d1d5db'
        )
    )
    
    # Update traces for better visibility
    fig.update_traces(
        textfont=dict(size=11, color='#1f2937'),
        hoverlabel=dict(
            bgcolor="white",
            font=dict(color='#1f2937')
        )
    )
    
    return fig

# ========== ENHANCED VISUALIZATION FUNCTIONS ==========
def create_project_required_charts():
    """Create all charts required by the project with enhanced readability"""
    charts = {}
    try:
        # 1. Food Wastage Trends by Category - ENHANCED
        category_data = SQLQueries.get_food_wastage_trends_comprehensive()
        if not category_data.empty:
            fig = px.bar(category_data.head(10), 
                        x='food_type', 
                        y='total_quantity',
                        color='wasted_quantity',
                        hover_data=['total_listings', 'wastage_percentage', 'critical_items', 'wasted_quantity'],
                        color_continuous_scale='Reds',
                        labels={
                            'food_type': 'Food Type',
                            'total_quantity': 'Total Quantity (kg)',
                            'wasted_quantity': 'Wasted Quantity (kg)'
                        })
            
            fig = apply_readable_chart_style(fig, 
                                           "📊 Food Wastage Analysis by Category", 
                                           "Food Type", 
                                           "Total Quantity (kg)")
            charts['category_trends'] = fig

        # 2. Provider Type Contributions - ENHANCED
        provider_type_data = SQLQueries.get_provider_type_contributions()
        if not provider_type_data.empty:
            fig = px.bar(provider_type_data, 
                        x='provider_type', 
                        y='total_quantity_contributed',
                        color='success_rate',
                        hover_data=['total_providers', 'food_types_offered', 'successful_distributions', 'success_rate'],
                        color_continuous_scale='Blues',
                        labels={
                            'provider_type': 'Provider Type',
                            'total_quantity_contributed': 'Total Contribution (kg)',
                            'success_rate': 'Success Rate (%)'
                        })
            
            fig = apply_readable_chart_style(fig, 
                                           "🏢 Food Contributions by Provider Type", 
                                           "Provider Type", 
                                           "Total Contribution (kg)")
            charts['provider_type_contributions'] = fig

        # 3. Cities by Food Listings - ENHANCED
        city_data = SQLQueries.get_cities_by_food_listings()
        if not city_data.empty:
            fig = px.bar(city_data.head(10), 
                        x='city', 
                        y='total_food_listings',
                        color='city_performance_score',
                        hover_data=['total_quantity', 'unique_providers', 'claim_success_rate', 'freshness_rate'],
                        color_continuous_scale='Viridis',
                        labels={
                            'city': 'City',
                            'total_food_listings': 'Number of Food Listings',
                            'city_performance_score': 'Performance Score'
                        })
            
            fig.update_layout(xaxis={'categoryorder':'total descending'})
            fig = apply_readable_chart_style(fig, 
                                           "🌍 Top Cities by Food Availability", 
                                           "City", 
                                           "Number of Food Listings")
            charts['city_listings'] = fig

        # 4. Food Types Distribution - ENHANCED
        food_type_data = SQLQueries.get_most_common_food_types()
        if not food_type_data.empty:
            fig = px.pie(food_type_data.head(8), 
                        values='total_items', 
                        names='food_type',
                        hover_data=['total_quantity', 'claim_success_rate', 'supply_demand_ratio'],
                        color_discrete_sequence=px.colors.qualitative.Set3)
            
            fig.update_traces(
                textposition='inside', 
                textinfo='percent+label',
                textfont_size=12
            )
            
            fig = apply_readable_chart_style(fig, "🍽️ Food Types Distribution")
            charts['food_type_distribution'] = fig

        # 5. Claims Status Analysis - ENHANCED
        claims_data = SQLQueries.get_claims_completion_percentages()
        if not claims_data.empty:
            colors = {
                'Completed': '#10b981',    # Green
                'Pending': '#f59e0b',      # Orange  
                'Cancelled': '#ef4444'     # Red
            }
            
            fig = px.pie(claims_data, 
                        values='claim_count', 
                        names='status',
                        hover_data=['percentage', 'total_quantity_involved', 'avg_quantity_per_claim'],
                        color='status',
                        color_discrete_map=colors)
            
            fig.update_traces(
                textposition='inside', 
                textinfo='percent+label',
                textfont_size=14,
                textfont_color='white'
            )
            
            fig = apply_readable_chart_style(fig, "📈 Food Claims Status Distribution")
            charts['claims_analysis'] = fig

        # 6. Meal Type Demand - ENHANCED
        meal_data = SQLQueries.get_most_claimed_meal_types()
        if not meal_data.empty:
            fig = px.bar(meal_data.head(8), 
                        x='meal_type', 
                        y='total_claims',
                        color='success_rate',
                        hover_data=['total_quantity_distributed', 'demand_supply_ratio', 'success_rate'],
                        color_continuous_scale='Greens',
                        labels={
                            'meal_type': 'Meal Type',
                            'total_claims': 'Total Claims',
                            'success_rate': 'Success Rate (%)'
                        })
            
            fig = apply_readable_chart_style(fig, 
                                           "🍴 Most Demanded Meal Types", 
                                           "Meal Type", 
                                           "Number of Claims")
            charts['meal_claims'] = fig

        # 7. System Overview - ENHANCED
        system_data = SQLQueries.get_comprehensive_system_analysis()
        if not system_data.empty:
            metrics = ['total_providers', 'total_receivers', 'total_food_items', 'successful_distributions']
            values = [system_data.iloc[0][metric] for metric in metrics]
            labels = ['Food Providers', 'Food Receivers', 'Food Items Listed', 'Successful Distributions']
            
            fig = px.bar(x=labels, y=values,
                        color=values,
                        color_continuous_scale='RdYlBu_r',
                        labels={
                            'x': 'System Components',
                            'y': 'Count'
                        })
            
            # Add value labels on bars
            fig.update_traces(
                text=values,
                texttemplate='%{text:,}',
                textposition='outside',
                textfont=dict(size=14, color='#1f2937')
            )
            
            fig = apply_readable_chart_style(fig, 
                                           "📊 System Overview Dashboard", 
                                           "System Components", 
                                           "Count")
            charts['system_overview'] = fig

    except Exception as e:
        st.error(f"Error creating enhanced charts: {e}")
        charts['error'] = str(e)
    
    return charts

# ========== NEW: ENHANCED TIME SERIES CHARTS ==========
def create_time_series_charts():
    """Create enhanced time series trend charts with improved readability"""
    charts = {}
    try:
        # 1. Claims Trends Over Time - ENHANCED
        claims_trends = SQLQueries.get_time_series_claims_trends()
        if not claims_trends.empty:
            fig = go.Figure()
            
            # Total claims line
            fig.add_trace(go.Scatter(
                x=claims_trends['claim_date'],
                y=claims_trends['total_claims'],
                mode='lines+markers',
                name='Total Claims',
                line=dict(color='#3b82f6', width=3),
                marker=dict(size=6, color='#3b82f6'),
                hovertemplate='<b>Date:</b> %{x}<br><b>Total Claims:</b> %{y}<extra></extra>'
            ))
            
            # Completed claims line
            fig.add_trace(go.Scatter(
                x=claims_trends['claim_date'],
                y=claims_trends['completed_claims'],
                mode='lines+markers',
                name='Completed Claims',
                line=dict(color='#10b981', width=3),
                marker=dict(size=6, color='#10b981'),
                hovertemplate='<b>Date:</b> %{x}<br><b>Completed:</b> %{y}<extra></extra>'
            ))
            
            fig = apply_readable_chart_style(fig, 
                                           "📈 Food Claims Trends Over Time", 
                                           "Date", 
                                           "Number of Claims")
            charts['claims_time_series'] = fig

        # 2. Food Wastage vs Savings Timeline - ENHANCED
        food_trends = SQLQueries.get_time_series_food_listings_trends()
        if not food_trends.empty:
            fig = go.Figure()
            
            # Quantity saved (positive impact)
            fig.add_trace(go.Scatter(
                x=food_trends['expiry_date'],
                y=food_trends['quantity_saved'],
                mode='lines+markers',
                name='Food Saved (kg)',
                line=dict(color='#10b981', width=3),
                fill='tozeroy',
                fillcolor='rgba(16, 185, 129, 0.2)',
                marker=dict(size=5, color='#10b981'),
                hovertemplate='<b>Date:</b> %{x}<br><b>Food Saved:</b> %{y} kg<extra></extra>'
            ))
            
            # Quantity wasted (negative impact)
            fig.add_trace(go.Scatter(
                x=food_trends['expiry_date'],
                y=food_trends['quantity_wasted'],
                mode='lines+markers',
                name='Food Wasted (kg)',
                line=dict(color='#ef4444', width=3),
                marker=dict(size=5, color='#ef4444'),
                hovertemplate='<b>Date:</b> %{x}<br><b>Food Wasted:</b> %{y} kg<extra></extra>'
            ))
            
            fig = apply_readable_chart_style(fig, 
                                           "🗑️ Food Wastage vs Savings Timeline", 
                                           "Expiry Date", 
                                           "Quantity (kg)")
            charts['wastage_timeline'] = fig

        # 3. Monthly Performance Dashboard - ENHANCED
        monthly_data = SQLQueries.get_monthly_performance_trends()
        if not monthly_data.empty:
            fig = go.Figure()
            
            # Claims bar chart
            fig.add_trace(go.Bar(
                x=monthly_data['month'],
                y=monthly_data['total_claims'],
                name='Total Claims',
                marker_color='rgba(59, 130, 246, 0.7)',
                marker_line=dict(color='#3b82f6', width=1),
                yaxis='y',
                hovertemplate='<b>Month:</b> %{x}<br><b>Claims:</b> %{y}<extra></extra>'
            ))
            
            # Success rate line
            fig.add_trace(go.Scatter(
                x=monthly_data['month'],
                y=monthly_data['monthly_success_rate'],
                mode='lines+markers',
                name='Success Rate (%)',
                line=dict(color='#10b981', width=3),
                marker=dict(size=8, color='#10b981'),
                yaxis='y2',
                hovertemplate='<b>Month:</b> %{x}<br><b>Success Rate:</b> %{y}%<extra></extra>'
            ))
            
            fig.update_layout(
                yaxis=dict(
                    title='Number of Claims',
                    side='left',
                    showgrid=True,
                    gridcolor='#e5e7eb'
                ),
                yaxis2=dict(
                    title='Success Rate (%)',
                    side='right',
                    overlaying='y',
                    showgrid=False,
                    range=[0, 100]
                )
            )
            
            fig = apply_readable_chart_style(fig, 
                                           "📊 Monthly Performance & Success Trends", 
                                           "Month", 
                                           "Claims / Success Rate")
            charts['monthly_trends'] = fig

    except Exception as e:
        st.error(f"Error creating time series charts: {e}")
        charts['error'] = str(e)
    
    return charts

# ========== MAIN HEADER ==========
st.markdown("""
<div class="main-header">
    <h1>🌍 Food Wastage Management System</h1>
    <p>Connecting food providers with those in need • Reducing waste • Building community</p>
</div>
""", unsafe_allow_html=True)

# ========== SIDEBAR NAVIGATION (FIXED) ==========
with st.sidebar:
    st.title("🧭 Navigation")
    current_page = st.selectbox(
        "Choose a page:",
        ["📊 Dashboard", "🏢 Providers", "🤝 Receivers", "🥗 Food Listings", "📦 Claims", "📈 Analytics", "⏰ Time Series"]
    )

# ========== MAIN CONTENT ROUTER (FIXED) ==========
if current_page == "📊 Dashboard":
    st.header("📊 Dashboard Overview")
    
    # Display key metrics with enhanced visibility
    col1, col2, col3, col4 = st.columns(4)
    
    try:
        system_data = SQLQueries.get_total_food_quantity_available()
        if not system_data.empty:
            row = system_data.iloc[0]
            
            with col1:
                st.metric("Total Food Items", f"{row['total_food_items']:,}")
            with col2:
                st.metric("Fresh Items", f"{row['fresh_items']:,}")
            with col3:
                st.metric("Total Providers", f"{row['contributing_providers']:,}")
            with col4:
                st.metric("Cities Covered", f"{row['cities_covered']:,}")
    except Exception as e:
        st.warning("Loading dashboard metrics...")
    
    # Display enhanced charts
    st.subheader("📈 Analytics Overview")
    charts = create_project_required_charts()
    
    for chart_name, chart in charts.items():
        if chart_name != 'error' and chart is not None:
            try:
                st.plotly_chart(chart, use_container_width=True, config={'displayModeBar': False})
            except Exception as e:
                st.error(f"Error displaying chart {chart_name}: {e}")

elif current_page == "🏢 Providers":
    st.header("🏢 Food Providers Management")
    
    # Add new provider section
    with st.expander("➕ Add New Provider"):
        col1, col2 = st.columns(2)
        with col1:
            provider_name = st.text_input("Provider Name")
            provider_type = st.selectbox("Provider Type", 
                                       ["Restaurant", "Grocery Store", "Hotel", "Supermarket", "Bakery", "Other"])
            city = st.text_input("City")
        with col2:
            contact = st.text_input("Contact Information")
            address = st.text_area("Address (Optional)")
        
        if st.button("Add Provider"):
            if provider_name and provider_type and city and contact:
                success, message = CRUDOperations.add_provider(provider_name, provider_type, city, contact, address)
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
            else:
                st.error("Please fill in all required fields")
    
    # Display providers table
    st.subheader("📋 Current Providers")
    try:
        providers_df = SQLQueries.get_provider_contacts_by_city()
        if not providers_df.empty:
            st.dataframe(providers_df, use_container_width=True)
            
            # Display provider statistics
            st.subheader("📊 Provider Statistics")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Providers", len(providers_df))
            with col2:
                active_providers = len(providers_df[providers_df['status'] == '🟢 Active'])
                st.metric("Active Providers", active_providers)
            with col3:
                total_listings = providers_df['active_food_listings'].sum()
                st.metric("Total Food Listings", total_listings)
        else:
            st.info("No provider data available. Add some providers to get started!")
    except Exception as e:
        st.error(f"Error loading providers: {e}")

elif current_page == "🤝 Receivers":
    st.header("🤝 Food Receivers Management")
    
    # Add new receiver section
    with st.expander("➕ Add New Receiver"):
        col1, col2 = st.columns(2)
        with col1:
            receiver_name = st.text_input("Receiver Name")
            receiver_type = st.selectbox("Receiver Type", 
                                       ["NGO", "Food Bank", "Shelter", "Charity", "Community Center", "Other"])
        with col2:
            city = st.text_input("City")
            contact = st.text_input("Contact Information")
        
        if st.button("Add Receiver"):
            if receiver_name and receiver_type and city and contact:
                success, message = CRUDOperations.add_receiver(receiver_name, receiver_type, city, contact)
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
            else:
                st.error("Please fill in all required fields")
    
    # Display receivers table
    st.subheader("📋 Current Receivers")
    try:
        receivers_query = "SELECT * FROM receivers ORDER BY receiver_id"
        receivers_df = SQLQueries.execute_query(receivers_query)
        if not receivers_df.empty:
            st.dataframe(receivers_df, use_container_width=True)
            
            # Display receiver statistics
            st.subheader("📊 Receiver Statistics")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Receivers", len(receivers_df))
            with col2:
                receiver_types = receivers_df['type'].nunique()
                st.metric("Receiver Types", receiver_types)
            with col3:
                cities = receivers_df['city'].nunique()
                st.metric("Cities Served", cities)
                
            # Show top receivers
            st.subheader("🏆 Top Performing Receivers")
            top_receivers = SQLQueries.get_top_claiming_receivers()
            if not top_receivers.empty:
                st.dataframe(top_receivers.head(10), use_container_width=True)
        else:
            st.info("No receiver data available. Add some receivers to get started!")
    except Exception as e:
        st.error(f"Error loading receivers: {e}")

elif current_page == "🥗 Food Listings":
    st.header("🥗 Food Listings Management")
    
    # Add new food listing section
    with st.expander("➕ Add New Food Listing"):
        col1, col2 = st.columns(2)
        with col1:
            food_name = st.text_input("Food Name")
            quantity = st.number_input("Quantity (kg)", min_value=0.1, step=0.1)
            expiry_date = st.date_input("Expiry Date", min_value=datetime.now().date())
        with col2:
            # Get provider options
            try:
                providers_query = "SELECT provider_id, name FROM providers ORDER BY name"
                providers_df = SQLQueries.execute_query(providers_query)
                if not providers_df.empty:
                    provider_options = {f"{row['name']} (ID: {row['provider_id']})": row['provider_id'] 
                                      for _, row in providers_df.iterrows()}
                    selected_provider = st.selectbox("Provider", options=list(provider_options.keys()))
                    provider_id = provider_options[selected_provider] if selected_provider else None
                else:
                    st.warning("No providers available. Add providers first.")
                    provider_id = None
            except:
                st.error("Error loading providers")
                provider_id = None
            
            food_type = st.selectbox("Food Type", 
                                   ["Vegetables", "Fruits", "Dairy", "Meat", "Grains", "Bakery", "Prepared Meals", "Other"])
            meal_type = st.selectbox("Meal Type", 
                                   ["Breakfast", "Lunch", "Dinner", "Snacks", "Beverages", "Other"])
        
        if st.button("Add Food Listing"):
            if food_name and quantity and expiry_date and provider_id and food_type and meal_type:
                success, message = CRUDOperations.add_food_listing(food_name, quantity, expiry_date, 
                                                                 provider_id, food_type, meal_type)
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
            else:
                st.error("Please fill in all required fields")
    
    # Display food listings
    st.subheader("📋 Current Food Listings")
    try:
        food_listings = SQLQueries.get_claims_per_food_item()
        if not food_listings.empty:
            st.dataframe(food_listings, use_container_width=True)
            
            # Display food statistics
            st.subheader("📊 Food Listing Statistics")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Listings", len(food_listings))
            with col2:
                total_quantity = food_listings['quantity'].sum()
                st.metric("Total Quantity (kg)", f"{total_quantity:,.1f}")
            with col3:
                food_types = food_listings['food_type'].nunique()
                st.metric("Food Types", food_types)
            with col4:
                urgent_items = len(food_listings[food_listings['item_status'] == '🟠 Urgent'])
                st.metric("Urgent Items", urgent_items)
        else:
            st.info("No food listings available. Add some food listings to get started!")
    except Exception as e:
        st.error(f"Error loading food listings: {e}")

elif current_page == "📦 Claims":
    st.header("📦 Food Claims Management")
    
    # Add new claim section
    with st.expander("➕ Add New Claim"):
        col1, col2 = st.columns(2)
        with col1:
            # Get food options
            try:
                food_query = "SELECT food_id, food_name FROM food_listings ORDER BY food_name"
                food_df = SQLQueries.execute_query(food_query)
                if not food_df.empty:
                    food_options = {f"{row['food_name']} (ID: {row['food_id']})": row['food_id'] 
                                  for _, row in food_df.iterrows()}
                    selected_food = st.selectbox("Food Item", options=list(food_options.keys()))
                    food_id = food_options[selected_food] if selected_food else None
                else:
                    st.warning("No food items available.")
                    food_id = None
            except:
                st.error("Error loading food items")
                food_id = None
        
        with col2:
            # Get receiver options
            try:
                receivers_query = "SELECT receiver_id, name FROM receivers ORDER BY name"
                receivers_df = SQLQueries.execute_query(receivers_query)
                if not receivers_df.empty:
                    receiver_options = {f"{row['name']} (ID: {row['receiver_id']})": row['receiver_id'] 
                                      for _, row in receivers_df.iterrows()}
                    selected_receiver = st.selectbox("Receiver", options=list(receiver_options.keys()))
                    receiver_id = receiver_options[selected_receiver] if selected_receiver else None
                else:
                    st.warning("No receivers available.")
                    receiver_id = None
            except:
                st.error("Error loading receivers")
                receiver_id = None
        
        claim_status = st.selectbox("Status", ["Pending", "Completed", "Cancelled"])
        
        if st.button("Add Claim"):
            if food_id and receiver_id:
                success, message = CRUDOperations.add_claim(food_id, receiver_id, claim_status)
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
            else:
                st.error("Please select both food item and receiver")
    
    # Display claims table
    st.subheader("📋 Current Claims")
    try:
        claims_query = """
        SELECT 
            c.claim_id,
            f.food_name,
            f.food_type,
            f.quantity,
            p.name as provider_name,
            r.name as receiver_name,
            c.status,
            c.timestamp
        FROM claims c
        JOIN food_listings f ON c.food_id = f.food_id
        JOIN providers p ON f.provider_id = p.provider_id
        LEFT JOIN receivers r ON c.receiver_id = r.receiver_id
        ORDER BY c.timestamp DESC
        """
        claims_df = SQLQueries.execute_query(claims_query)
        
        if not claims_df.empty:
            st.dataframe(claims_df, use_container_width=True)
            
            # Display claims statistics
            st.subheader("📊 Claims Statistics")
            claims_stats = SQLQueries.get_claims_completion_percentages()
            if not claims_stats.empty:
                col1, col2, col3, col4 = st.columns(4)
                for i, (_, row) in enumerate(claims_stats.iterrows()):
                    if i < 4:  # Only show first 4 statuses
                        with [col1, col2, col3, col4][i]:
                            st.metric(f"{row['status']} Claims", 
                                    f"{row['claim_count']} ({row['percentage']:.1f}%)")
                
                # Show detailed claims analysis
                st.subheader("📈 Detailed Claims Analysis")
                st.dataframe(claims_stats, use_container_width=True)
        else:
            st.info("No claims data available.")
    except Exception as e:
        st.error(f"Error loading claims: {e}")

elif current_page == "📈 Analytics":
    st.header("📈 Advanced Analytics")
    
    # Analytics tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🏢 Provider Analytics", "🤝 Receiver Analytics", "🍽️ Food Analytics", "🌍 City Analytics"])
    
    with tab1:
        st.subheader("Provider Performance Analysis")
        
        # Top providers by successful claims
        top_providers = SQLQueries.get_provider_highest_successful_claims()
        if not top_providers.empty:
            st.dataframe(top_providers.head(10), use_container_width=True)
        
        # Total donations per provider
        donations_data = SQLQueries.get_total_donations_per_provider()
        if not donations_data.empty:
            st.subheader("Provider Donation Analysis")
            st.dataframe(donations_data.head(10), use_container_width=True)
    

            # NEW: Provider Reliability (bar)
            reliability = SQLQueries.get_provider_reliability_pct()
            if not reliability.empty:
                st.subheader("✅ Provider Reliability (Completed % )")
                fig_rel = px.bar(reliability.head(20), x='provider_name', y='reliability_pct',
                                 color='reliability_pct', color_continuous_scale='Teal',
                                 title="Provider Reliability (%)")
                fig_rel.update_layout(xaxis_title='Provider', yaxis_title='Reliability %')
                st.plotly_chart(fig_rel, use_container_width=True)

            # NEW: Most Frequent Providers & Contributions
            freq = SQLQueries.get_most_frequent_providers_contributions()
            if not freq.empty:
                st.subheader("🏆 Most Frequent Providers & Their Contributions")
                fig_freq = px.bar(freq, x='provider_name', y='total_listings', 
                                  hover_data=['total_quantity'],
                                  color='total_listings', color_continuous_scale='Blues')
                fig_freq.update_layout(xaxis_title='Provider', yaxis_title='Total Listings')
                st.plotly_chart(fig_freq, use_container_width=True)

    with tab2:
        st.subheader("Receiver Performance Analysis")
        
        # Average quantity per receiver
        avg_quantity_data = SQLQueries.get_avg_quantity_per_receiver()
        if not avg_quantity_data.empty:
            st.dataframe(avg_quantity_data.head(10), use_container_width=True)
        
        # Top claiming receivers
        top_receivers = SQLQueries.get_top_claiming_receivers()
        if not top_receivers.empty:
            st.subheader("Top Claiming Receivers")
            st.dataframe(top_receivers.head(10), use_container_width=True)
    
    with tab3:
        st.subheader("Food Type Analysis")
        
        # Most common food types
        food_types = SQLQueries.get_most_common_food_types()
        if not food_types.empty:
            st.dataframe(food_types, use_container_width=True)
        
        # Most claimed meal types
        meal_types = SQLQueries.get_most_claimed_meal_types()
        if not meal_types.empty:
            st.subheader("Meal Type Demand Analysis")
            st.dataframe(meal_types, use_container_width=True)
    

        # NEW: Wastage % by Food Type
        wastage_pct = SQLQueries.get_food_type_wastage_pct()
        if not wastage_pct.empty:
            st.subheader("🗑️ Wastage % by Food Type")
            fig_wp = px.bar(wastage_pct, x='food_type', y='wastage_pct', 
                            color='wastage_pct', color_continuous_scale='Reds')
            fig_wp.update_layout(xaxis_title='Food Type', yaxis_title='Wastage %')
            st.plotly_chart(fig_wp, use_container_width=True)

        # NEW: Items expiring in next 3 days (table + small bar by city)
        exp3 = SQLQueries.get_items_expiring_next_3_days()
        if not exp3.empty:
            st.subheader("⏳ Items Expiring in Next 3 Days")
            st.dataframe(exp3, use_container_width=True)
            by_city = exp3.groupby('city', as_index=False)['food_id'].count().rename(columns={'food_id':'items'})
            fig_exp3 = px.bar(by_city, x='city', y='items', title='Urgent Items by City (≤3 days)')
            st.plotly_chart(fig_exp3, use_container_width=True)

    with tab4:
        st.subheader("City-wise Analysis")
        
        # Providers and receivers per city
        city_data = SQLQueries.get_providers_receivers_per_city()
        if not city_data.empty:
            st.dataframe(city_data, use_container_width=True)
        

        # NEW: Highest Demand Locations by Claims
        demand_locs = SQLQueries.get_highest_demand_locations_by_claims()
        if not demand_locs.empty:
            st.subheader("📍 Highest Demand Locations by Claims")
            fig_dem = px.bar(demand_locs, x='location', y='total_claims',
                             color='total_claims', color_continuous_scale='Viridis')
            fig_dem.update_layout(xaxis_title='City', yaxis_title='Total Claims')
            st.plotly_chart(fig_dem, use_container_width=True)

        # Cities by food listings
        city_listings = SQLQueries.get_cities_by_food_listings()
        if not city_listings.empty:
            st.subheader("Cities by Food Availability")
            st.dataframe(city_listings, use_container_width=True)

elif current_page == "⏰ Time Series":
    st.header("⏰ Time Series Analysis")
    
    # Enhanced time series charts
    time_charts = create_time_series_charts()
    
    for chart_name, chart in time_charts.items():
        if chart_name != 'error' and chart is not None:
            try:
                st.plotly_chart(chart, use_container_width=True, config={'displayModeBar': False})
            except Exception as e:
                st.error(f"Error displaying chart {chart_name}: {e}")
    
    # Time series data tables
    st.subheader("📊 Time Series Data")
    
    tab1, tab2, tab3 = st.tabs(["📈 Claims Trends", "🗑️ Wastage Trends", "📅 Monthly Performance"])
    
    with tab1:
        claims_trends = SQLQueries.get_time_series_claims_trends()
        if not claims_trends.empty:
            st.dataframe(claims_trends, use_container_width=True)
    

            # NEW: Provider Reliability (bar)
            reliability = SQLQueries.get_provider_reliability_pct()
            if not reliability.empty:
                st.subheader("✅ Provider Reliability (Completed % )")
                fig_rel = px.bar(reliability.head(20), x='provider_name', y='reliability_pct',
                                 color='reliability_pct', color_continuous_scale='Teal',
                                 title="Provider Reliability (%)")
                fig_rel.update_layout(xaxis_title='Provider', yaxis_title='Reliability %')
                st.plotly_chart(fig_rel, use_container_width=True)

            # NEW: Most Frequent Providers & Contributions
            freq = SQLQueries.get_most_frequent_providers_contributions()
            if not freq.empty:
                st.subheader("🏆 Most Frequent Providers & Their Contributions")
                fig_freq = px.bar(freq, x='provider_name', y='total_listings', 
                                  hover_data=['total_quantity'],
                                  color='total_listings', color_continuous_scale='Blues')
                fig_freq.update_layout(xaxis_title='Provider', yaxis_title='Total Listings')
                st.plotly_chart(fig_freq, use_container_width=True)

    with tab2:
        food_trends = SQLQueries.get_time_series_food_listings_trends()
        if not food_trends.empty:
            st.dataframe(food_trends, use_container_width=True)
    
    with tab3:
        monthly_trends = SQLQueries.get_monthly_performance_trends()
        if not monthly_trends.empty:
            st.dataframe(monthly_trends, use_container_width=True)

# ========== FOOTER ==========
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    🌍 Food Wastage Management System 
    Reducing food waste • Building communities • Making a difference
</div>
""", unsafe_allow_html=True)