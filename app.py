import streamlit as st
from streamlit_option_menu import option_menu
import urllib.parse
import pandas as pd

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

# --- 2. APP SETUP & CUSTOM CSS ---
st.set_page_config(page_title="Growth Dashboard", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
        html, body, [class*="css"] { font-family: 'Inter', sans-serif; color: #1E293B; }
        #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
        
        /* Mobile-Friendly Adjustments */
        .block-container {
            padding-top: 1rem !important;
            padding-bottom: 5rem !important;
        }
        
        /* Card Styling */
        .metric-card {
            background-color: #FFFFFF; padding: 20px; border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); border: 1px solid #E2E8F0; margin-bottom: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# --- 3. SIDEBAR (SETTINGS ONLY) ---
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    selected_client_name = st.selectbox("Active Account", list(CLIENTS.keys()))
    st.info("Use the menu at the top to navigate.")

data = CLIENTS[selected_client_name]

# --- 4. TOP NAVIGATION BAR (VISIBLE ON MOBILE) ---
selected = option_menu(
    menu_title=None, 
    options=["Review Gen", "Database", "Rankings", "Leads"], 
    icons=["star-fill", "table", "geo-alt-fill", "search"], 
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#FFFFFF"},
        "icon": {"color": "#0066cc", "font-size": "14px"}, 
        "nav-link": {"font-size": "12px", "text-align": "center", "margin":"0px", "--hover-color": "#eef2ff"},
        "nav-link-selected": {"background-color": "#0F172A", "color": "white"},
    }
)

st.write("") # Spacer

# --- PAGE: REVIEW GENERATOR ---
if selected == "Review Gen":
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.subheader("📝 Text a Client")
    st.caption("Enter a name to generate a text message link.")
    
    col1, col2 = st.columns(2)
    with col1: customer_name = st.text_input("Name", placeholder="Jane")
    with col2: service_type = st.selectbox("Service", data["services"])

    if customer_name:
        link = data["review_link"]
        message_text = (f"Hi {customer_name}! Thanks for choosing {selected_client_name}. "
                        f"We'd love a 5-star rating if you have a second: {link}")
        encoded_msg = urllib.parse.quote(message_text)
        
        st.markdown(f'''
            <a href="sms:?&body={encoded_msg}" target="_blank" style="text-decoration:none;">
                <div style="background-color:#22C55E; color:white; padding:15px; border-radius:8px; text-align:center; font-weight:bold; margin-top:10px;">
                    📨 Text {customer_name}
                </div>
            </a>
        ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- PAGE: CLIENT DATABASE ---
if selected == "Database":
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.subheader("📂 Client List")
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.success(f"Loaded {len(df)} clients.")
            st.markdown("---")
            for index, row in df.iterrows():
                name = row.get('Name', 'Client')
                service = row.get('Service', 'Cleaning')
                
                link = data["review_link"]
                msg = (f"Hi {name}! Thanks for using {selected_client_name}. Review us? {link}")
                encoded = urllib.parse.quote(msg)
                
                st.markdown(f"""
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                    <div>
                        <b>{name}</b><br>
                        <span style="font-size:12px; color:grey;">{service}</span>
                    </div>
                    <a href="sms:?&body={encoded}" target="_blank">
                        <button style="background-color:#22C55E; color:white; border:none; padding:8px 12px; border-radius:5px;">Text</button>
                    </a>
                </div>
                <hr style="margin:5px 0;">
                """, unsafe_allow_html=True)
                
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.info("Upload a CSV with columns: 'Name' and 'Service'")
    st.markdown('</div>', unsafe_allow_html=True)

# --- PAGE: RANK CHECKER ---
if selected == "Rankings":
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.subheader("📍 Rank Check")
    target_keyword = st.text_input("Keyword", value=data["services"][0])
    
    st.write("Check ranking in:")
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
    st.subheader("🕵️ Lead Hunter")
    if "fb_groups" in data:
        keywords = ["recommend", "needed"]
        for group_name, group_id in data["fb_groups"].items():
            st.markdown(f"**{group_name}**")
            c1, c2 = st.columns(2)
            for i, kw in enumerate(keywords):
                full_search = f"{data['services'][0]} {kw}"
                magic_suffix = "&filters=eyJzb3J0aW5nIjoie1widmFsdWVcIjpcImNocm9ub19kZXNjZW5kaW5nXCJ9In0%3D"
                encoded_kw = urllib.parse.quote(full_search)
                url = f"https://www.facebook.com/groups/{group_id}/search/?q={encoded_kw}{magic_suffix}"
                
                # FIXED: Unstacked lines
                if i == 0: 
                    with c1: 
                        st.link_button(f"Find '{kw}'", url, use_container_width=True)
                if i == 1: 
                    with c2: 
                        st.link_button(f"Find '{kw}'", url, use_container_width=True)
            st.write("")
    st.markdown('</div>', unsafe_allow_html=True)
