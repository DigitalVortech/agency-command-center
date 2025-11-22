import streamlit as st
from streamlit_option_menu import option_menu
import urllib.parse
import pandas as pd
import re 

# --- 1. CONFIGURATION & DATA ---
CLIENTS = {
    "Prime Shine Cleaning": {
        "review_link": "https://g.page/r/YOUR_PRIME_SHINE_LINK/review",
        "services": ["House Clean", "Move-out Clean", "Deep Clean"],
        "competitors": {"Prime Shine": 16, "Maids of Movher": 151, "Live Clean Today": 70},
        "locations": {
            "Mead": "Mead, WA",
            "North Spokane": "North Spokane, WA",
            "South Hill": "South Hill, Spokane, WA"
        },
        "fb_groups": {
             "Spokane Mom's": "123456789", 
             "Mead Community": "987654321"
        }
    }
}

# --- 2. APP SETUP & DESIGN SYSTEM ---
st.set_page_config(page_title="AgencyOS", page_icon="https://img.icons8.com/color/48/000000/squared-menu-1.png", layout="wide")

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
            background-color: #F1F5F9; 
            color: #0F172A;
        }

        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        div[data-testid="stToolbar"] {visibility: hidden;}

        .block-container {
            padding-top: 0rem !important;
            padding-bottom: 5rem !important;
            padding-left: 0rem !important;
            padding-right: 0rem !important;
            max-width: 100%;
        }

        .custom-header {
            background: #0F172A;
            padding: 24px 20px;
            border-bottom: 1px solid #334155;
            color: white;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }
        
        .header-title { font-size: 20px; font-weight: 700; margin: 0; color: #F8FAFC; }
        .header-subtitle { font-size: 10px; text-transform: uppercase; letter-spacing: 1.5px; color: #94A3B8; font-weight: 600; margin-bottom: 4px; }

        .client-avatar {
            width: 40px; height: 40px; background: #3B82F6; border-radius: 8px;
            display: flex; align-items: center; justify-content: center;
            font-weight: 700; font-size: 14px; color: white;
            box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2);
        }

        .metric-card {
            background-color: #FFFFFF; padding: 24px; margin: 16px;
            border-radius: 8px; border: 1px solid #E2E8F0;
            box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        }

        .section-label {
            font-size: 11px; text-transform: uppercase; letter-spacing: 1.2px;
            color: #64748B; font-weight: 700; margin-bottom: 12px; display: block;
        }

        .stButton button {
            width: 100%; background-color: #0F172A; color: white; border: none;
            padding: 12px; font-weight: 600; font-size: 13px; border-radius: 6px;
        }
    </style>
""", unsafe_allow_html=True)

# --- 3. LOGIC & SIDEBAR ---
with st.sidebar:
    st.markdown('<span class="section-label">SYSTEM SETTINGS</span>', unsafe_allow_html=True)
    selected_client_name = st.selectbox("Account", list(CLIENTS.keys()))

data = CLIENTS[selected_client_name]
initials = "".join([word[0] for word in selected_client_name.split()[:2]]).upper()

# --- 4. HEADER ---
st.markdown(f"""
    <div class="custom-header">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <div>
                <p class="header-subtitle">AGENCY OS &trade;</p>
                <h1 class="header-title">{selected_client_name}</h1>
            </div>
            <div class="client-avatar">
                {initials}
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- 5. NAVIGATION ---
selected = option_menu(
    menu_title=None, 
    options=["Growth", "Database", "Rankings", "Leads"], 
    icons=["graph-up-arrow", "people-fill", "geo-alt-fill", "search"], 
    orientation="horizontal",
    styles={
        "container": {"padding": "5px", "background-color": "#FFFFFF", "margin": "0px 10px 10px 10px", "border-radius": "8px", "border": "1px solid #E2E8F0"},
        "icon": {"color": "#64748B", "font-size": "14px"}, 
        "nav-link": {"font-size": "11px", "text-align": "center", "margin":"0px", "color": "#475569"},
        "nav-link-selected": {"background-color": "#F1F5F9", "color": "#0F172A", "font-weight": "600"},
    }
)

# --- PAGE: GROWTH ---
if selected == "Growth":
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown('<span class="section-label">QUICK ACTIONS</span>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1: customer_name = st.text_input("Customer Name", placeholder="e.g. Mike")
    with col2: service_type = st.selectbox("Service", data["services"])

    if customer_name:
        link = data["review_link"]
        message_text = (f"Hi {customer_name}! Thanks for choosing {selected_client_name}. "
                        f"We'd love a 5-star rating: {link}")
        encoded_msg = urllib.parse.quote(message_text)
        
        st.markdown(f'''
            <a href="sms:?&body={encoded_msg}" target="_blank" style="text-decoration:none;">
                <div style="background: #2563EB; color:white; padding:14px; border-radius:6px; text-align:center; font-weight:600; font-size:14px; margin-top:10px;">
                    Send Text Message
                </div>
            </a>
        ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- PAGE: DATABASE ---
if selected == "Database":
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown('<span class="section-label">CLIENT REGISTRY</span>', unsafe_allow_html=True)
    
    # --- TEMPLATE GENERATOR ---
    # Create a sample dataframe
    sample_df = pd.DataFrame([
        {"Name": "John Doe", "Service": "House Clean", "Phone": "555-123-4567"},
        {"Name": "Jane Smith", "Service": "Deep Clean", "Phone": "(509) 555-0199"}
    ])
    # Convert to CSV
    csv_data = sample_df.to_csv(index=False).encode('utf-8')
    
    # Download Button
    st.download_button(
        label="📄 Download Excel/CSV Template",
        data=csv_data,
        file_name="client_template.csv",
        mime="text/csv",
        help="Click to download a blank file to fill out."
    )
    st.markdown("---")
    
    # --- UPLOADER ---
    uploaded_file = st.file_uploader("Import Completed CSV", type=["csv"])
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            st.success(f"Loaded {len(df)} contacts.")
            
            for _, row in df.iterrows():
                # Get Data
                name = str(row.get('Name', 'Client'))
                service = str(row.get('Service', 'Cleaning'))
                raw_phone = str(row.get('Phone', ''))
                
                # Clean Phone Number
                phone_digits = re.sub(r'\D', '', raw_phone)
                
                # Generate Links
                link = data["review_link"]
                msg = (f"Hi {name}! Thanks for using {selected_client_name} for your {service}. Review us? {link}")
                encoded_msg = urllib.parse.quote(msg)
                
                # Decide link type (with or without phone number)
                if phone_digits:
                    sms_href = f"sms:{phone_digits}?&body={encoded_msg}"
                else:
                    sms_href = f"sms:?&body={encoded_msg}"
                
                st.markdown(f"""
                <div style="display:flex; justify-content:space-between; align-items:center; padding: 12px 0; border-bottom:1px solid #F1F5F9;">
                    <div>
                        <div style="font-weight:600; font-size:13px; color:#0F172A;">{name}</div>
                        <div style="font-size:11px; color:#64748B;">{service}</div>
                    </div>
                    <a href="{sms_href}" target="_blank">
                        <button style="background:#F8FAFC; color:#0F172A; border:1px solid #E2E8F0; padding:6px 12px; border-radius:4px; font-weight:600; font-size:11px; cursor:pointer;">
                           Text {name}
                        </button>
                    </a>
                </div>""", unsafe_allow_html=True)
        except Exception as e:
             st.error(f"CSV Error: {e}")
    else:
        st.info("Upload your CSV file to start texting.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- PAGE: RANKINGS ---
if selected == "Rankings":
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown('<span class="section-label">GEO-GRID AUDIT</span>', unsafe_allow_html=True)
    
    target_keyword = st.text_input("Target Keyword", value=data["services"][0])
    cols = st.columns(2)
    for index, (name, location_query) in enumerate(data["locations"].items()):
        query = f"{target_keyword} in {location_query}"
        encoded_query = urllib.parse.quote(query)
        search_url = f"https://www.google.com/search?q={encoded_query}"
        with cols[index % 2]:
            st.link_button(f"🔍 {name}", search_url, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- PAGE: LEADS ---
if selected == "Leads":
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown('<span class="section-label">SOCIAL RADAR</span>', unsafe_allow_html=True)
    
    if "fb_groups" in data:
        keywords = ["recommend", "needed"]
        for group_name, group_id in data["fb_groups"].items():
            st.markdown(f"<div style='font-size:13px; font-weight:600; margin-bottom:8px;'>{group_name}</div>", unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            for i, kw in enumerate(keywords):
                full_search = f"{data['services'][0]} {kw}"
                magic_suffix = "&filters=eyJzb3J0aW5nIjoie1widmFsdWVcIjpcImNocm9ub19kZXNjZW5kaW5nXCJ9In0%3D"
                encoded_kw = urllib.parse.quote(full_search)
                url = f"https://www.facebook.com/groups/{group_id}/search/?q={encoded_kw}{magic_suffix}"
                
                # FIXED INDENTATION LOGIC HERE
                if i == 0: 
                    with c1: 
                        st.link_button(f"Find '{kw}'", url, use_container_width=True)
                if i == 1: 
                    with c2: 
                        st.link_button(f"Find '{kw}'", url, use_container_width=True)
            st.write("")
    st.markdown('</div>', unsafe_allow_html=True)
