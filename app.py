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
        
        /* Dropdown Styling */
        div[data-baseweb="select"] > div {
            border-radius: 6px;
            border-color: #E2E8F0;
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

# --- PAGE: GROWTH (Manual Entry) ---
if selected == "Growth":
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown('<span class="section-label">MANUAL ENTRY</span>', unsafe_allow_html=True)
    
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

# --- PAGE: DATABASE (The Picker) ---
if selected == "Database":
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown('<span class="section-label">CLIENT REGISTRY</span>', unsafe_allow_html=True)
    
    # 1. TEMPLATE DOWNLOAD
    sample_df = pd.DataFrame([{"Name": "John Doe", "Service": "House Clean", "Phone": "555-123-4567"}])
    csv_data = sample_df.to_csv(index=False).encode('utf-8')
    st.download_button(label="📄 Download CSV Template", data=csv_data, file_name="template.csv", mime="text/csv")
    
    st.markdown("---")
    
    # 2. FILE UPLOAD
    uploaded_file = st.file_uploader("Import CSV File", type=["csv"])
    
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            st.success(f"✓ {len(df)} Contacts Loaded")
            
            # 3. THE CLIENT PICKER (Dropdown)
            # Create a list of names for the dropdown
            client_list = df['Name'].tolist()
            selected_person = st.selectbox("Select Client to Text:", client_list)
            
            if selected_person:
                # Find the row for the selected person
                person_data = df[df['Name'] == selected_person].iloc[0]
                
                # Extract Data
                p_service = str(person_data.get('Service', 'Service'))
                p_phone = str(person_data.get('Phone', ''))
                
                # Clean Phone
                phone_digits = re.sub(r'\D', '', p_phone)
                
                # Generate Link
                link = data["review_link"]
                msg = (f"Hi {selected_person}! Thanks for using {selected_client_name} for your {p_service}. Review us? {link}")
                encoded_msg = urllib.parse.quote(msg)
                
                # Logic for SMS link (Android/iOS compatibility)
                if phone_digits:
                    sms_href = f"sms:{phone_digits}?&body={encoded_msg}"
                else:
                    sms_href = f"sms:?&body={encoded_msg}"
                
                # 4. BIG ACTION CARD
                st.markdown(f"""
                <div style="background-color:#F8FAFC; border:1px solid #E2E8F0; border-radius:8px; padding:15px; margin-top:15px;">
                    <div style="font-size:12px; color:#64748B; font-weight:600; margin-bottom:5px;">READY TO SEND</div>
                    <div style="font-size:16px; font-weight:700; color:#0F172A; margin-bottom:2px;">{selected_person}</div>
                    <div style="font-size:13px; color:#475569; margin-bottom:15px;">{p_phone if p_phone else 'No phone number found'}</div>
                    
                    <a href="{sms_href}" target="_blank" style="text-decoration:none;">
                        <div style="background: #2563EB; color:white; padding:12px; border-radius:6px; text-align:center; font-weight:600; font-size:14px; box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.3);">
                            📨 Send Text Now
                        </div>
                    </a>
                </div>
                """, unsafe_allow_html=True)

        except Exception as e:
             st.error(f"CSV Error: {e}")
    else:
        st.info("Upload your CSV file to unlock the client picker.")
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
                
                if i == 0: 
                    with c1: 
                        st.link_button(f"Find '{kw}'", url, use_container_width=True)
                if i == 1: 
                    with c2: 
                        st.link_button(f"Find '{kw}'", url, use_container_width=True)
            st.write("")
    st.markdown('</div>', unsafe_allow_html=True)
