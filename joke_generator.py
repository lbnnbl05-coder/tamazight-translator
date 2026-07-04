import streamlit as st
import requests
import json
from datetime import datetime
import time

st.set_page_config(
    page_title="🎭 Random Joke Generator",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .joke-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 30px;
        border-radius: 15px;
        color: white;
        margin: 20px 0;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    }
    .joke-text {
        font-size: 24px;
        font-weight: bold;
        margin: 15px 0;
        line-height: 1.6;
    }
    .punchline {
        font-size: 20px;
        font-style: italic;
        margin-top: 20px;
        padding-top: 15px;
        border-top: 2px solid rgba(255,255,255,0.3);
    }
    .category-badge {
        display: inline-block;
        background-color: rgba(255,255,255,0.2);
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 12px;
        margin: 5px 5px 5px 0;
    }
    .stats-box {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .error-box {
        background-color: #ffcccc;
        border: 2px solid #ff0000;
        color: #cc0000;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .success-box {
        background-color: #ccffcc;
        border: 2px solid #00cc00;
        color: #006600;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# JOKE GENERATOR APP
# ============================================================================

st.title("🎭 Random Joke Generator")
st.markdown("Get random jokes from multiple sources! 😄")

# ============================================================================
# SIDEBAR CONFIGURATION
# ============================================================================

with st.sidebar:
    st.header("⚙️ Settings")
    
    joke_type = st.selectbox(
        "📌 Select Joke Type:",
        [
            "Random Joke (Mixed)",
            "Programming Jokes",
            "Dad Jokes",
            "Chuck Norris Jokes",
            "Knock-Knock Jokes",
        ]
    )
    
    st.divider()
    
    api_source = st.radio(
        "🔌 API Source:",
        [
            "JokeAPI (Multiple Types)",
            "Official Joke API",
            "Chuck Norris API",
            "Random Joke API",
        ]
    )
    
    st.divider()
    
    st.subheader("💾 Saved Jokes")
    if st.button("🗑️ Clear History"):
        st.session_state.joke_history = []
        st.success("History cleared!")

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

if "joke_history" not in st.session_state:
    st.session_state.joke_history = []

if "current_joke" not in st.session_state:
    st.session_state.current_joke = None

if "show_punchline" not in st.session_state:
    st.session_state.show_punchline = False

# ============================================================================
# API FUNCTIONS
# ============================================================================

def get_joke_from_jokeapi(joke_category="Any"):
    """Fetch joke from JokeAPI.dev"""
    try:
        category_map = {
            "Random Joke (Mixed)": "Any",
            "Programming Jokes": "Programming",
            "Dad Jokes": "Miscellaneous",
            "Knock-Knock Jokes": "Knock-knock",
        }
        
        category = category_map.get(joke_category, "Any")
        url = f"https://v2.jokeapi.dev/joke/{category}?type=single"
        
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        
        data = response.json()
        
        if data.get("error"):
            return None, "Could not fetch joke"
        
        joke = {
            "setup": data.get("setup", ""),
            "delivery": data.get("delivery", data.get("joke", "")),
            "category": data.get("category", "General"),
            "type": data.get("type", "single"),
            "source": "JokeAPI",
            "timestamp": datetime.now().isoformat()
        }
        return joke, None
    
    except Exception as e:
        return None, f"JokeAPI Error: {str(e)}"

def get_official_joke_api():
    """Fetch joke from Official Joke API"""
    try:
        url = "https://official-joke-api.appspot.com/random_joke"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        
        data = response.json()
        
        joke = {
            "setup": data.get("setup", ""),
            "delivery": data.get("punchline", ""),
            "category": data.get("type", "General"),
            "type": "two-part",
            "source": "Official Joke API",
            "timestamp": datetime.now().isoformat()
        }
        return joke, None
    
    except Exception as e:
        return None, f"Official Joke API Error: {str(e)}"

def get_chuck_norris_joke():
    """Fetch Chuck Norris joke"""
    try:
        url = "https://api.chucknorris.io/jokes/random"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        
        data = response.json()
        
        joke = {
            "setup": "",
            "delivery": data.get("value", ""),
            "category": "Chuck Norris",
            "type": "single",
            "source": "Chuck Norris API",
            "timestamp": datetime.now().isoformat()
        }
        return joke, None
    
    except Exception as e:
        return None, f"Chuck Norris API Error: {str(e)}"

def get_random_joke_api():
    """Fetch joke from Random Joke API"""
    try:
        url = "https://api.api-ninjas.com/v1/jokes"
        headers = {"X-Api-Key": "demo"}  # Using demo key
        
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        
        data = response.json()
        
        if isinstance(data, list) and len(data) > 0:
            joke_text = data[0].get("joke", "")
            joke = {
                "setup": "",
                "delivery": joke_text,
                "category": "General",
                "type": "single",
                "source": "Random Joke API",
                "timestamp": datetime.now().isoformat()
            }
            return joke, None
    
    except Exception as e:
        return None, f"Random Joke API Error: {str(e)}"

def get_programming_joke():
    """Fetch programming-specific joke"""
    try:
        url = "https://official-joke-api.appspot.com/jokes/programming/random"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        
        data = response.json()
        
        # Handle single joke vs list
        if isinstance(data, list):
            data = data[0]
        
        joke = {
            "setup": data.get("setup", ""),
            "delivery": data.get("punchline", ""),
            "category": "Programming",
            "type": data.get("type", "two-part"),
            "source": "Official Joke API",
            "timestamp": datetime.now().isoformat()
        }
        return joke, None
    
    except Exception as e:
        return None, f"Programming Joke Error: {str(e)}"

# ============================================================================
# MAIN CONTENT
# ============================================================================

col1, col2, col3 = st.columns(3)

with col1:
    fetch_button = st.button("🎲 Get Joke", use_container_width=True, type="primary")

with col2:
    reveal_button = st.button("🎭 Show Punchline", use_container_width=True)

with col3:
    save_button = st.button("💾 Save Joke", use_container_width=True)

# ============================================================================
# FETCH JOKE LOGIC
# ============================================================================

if fetch_button:
    with st.spinner("🔄 Fetching joke..."):
        joke = None
        error = None
        
        # Select API based on user choice
        if api_source == "JokeAPI (Multiple Types)":
            joke, error = get_joke_from_jokeapi(joke_type)
        
        elif api_source == "Official Joke API":
            if joke_type == "Programming Jokes":
                joke, error = get_programming_joke()
            else:
                joke, error = get_official_joke_api()
        
        elif api_source == "Chuck Norris API":
            joke, error = get_chuck_norris_joke()
        
        elif api_source == "Random Joke API":
            joke, error = get_random_joke_api()
        
        # Display result
        if joke:
            st.session_state.current_joke = joke
            st.session_state.show_punchline = False
            st.success("✅ Joke loaded!")
        else:
            st.markdown(f'<div class="error-box">❌ {error}</div>', unsafe_allow_html=True)

# ============================================================================
# DISPLAY CURRENT JOKE
# ============================================================================

if st.session_state.current_joke:
    joke = st.session_state.current_joke
    
    st.markdown(f'<div class="joke-container">', unsafe_allow_html=True)
    
    # Display category badge
    st.markdown(f'<span class="category-badge">📂 {joke.get("category", "General")}</span>', unsafe_allow_html=True)
    
    # Display setup (or full joke if single-part)
    if joke.get("setup"):
        st.markdown(f'<div class="joke-text">{joke["setup"]}</div>', unsafe_allow_html=True)
    
    # Punchline reveal button
    if reveal_button or st.session_state.show_punchline:
        st.session_state.show_punchline = True
        st.markdown(f'<div class="punchline">😂 {joke["delivery"]}</div>', unsafe_allow_html=True)
    else:
        if joke.get("setup"):
            st.markdown('<div class="punchline">👉 Click "Show Punchline" to reveal!</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="joke-text">{joke["delivery"]}</div>', unsafe_allow_html=True)
    
    st.markdown(f'<p style="font-size: 12px; margin-top: 15px; opacity: 0.8;">Source: {joke["source"]}</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# SAVE JOKE LOGIC
# ============================================================================

if save_button:
    if st.session_state.current_joke:
        st.session_state.joke_history.append(st.session_state.current_joke)
        st.markdown('<div class="success-box">✅ Joke saved to history!</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="error-box">❌ No joke to save. Fetch one first!</div>', unsafe_allow_html=True)

# ============================================================================
# SIDEBAR - JOKE HISTORY & STATS
# ============================================================================

with st.sidebar:
    if st.session_state.joke_history:
        st.divider()
        st.subheader("📚 Saved Jokes")
        
        for idx, saved_joke in enumerate(st.session_state.joke_history, 1):
            with st.expander(f"Joke #{idx} - {saved_joke.get('source', 'Unknown')}"):
                st.write(f"**Category:** {saved_joke.get('category', 'N/A')}")
                st.write(f"**Setup:** {saved_joke.get('setup', 'N/A')}")
                st.write(f"**Punchline:** {saved_joke.get('delivery', 'N/A')}")
                st.write(f"**Time:** {saved_joke.get('timestamp', 'N/A')}")
        
        # Export jokes
        st.divider()
        if st.button("📥 Export Jokes as JSON"):
            json_data = json.dumps(st.session_state.joke_history, indent=2)
            st.download_button(
                label="Download Jokes",
                data=json_data,
                file_name="my_jokes.json",
                mime="application/json"
            )

# ============================================================================
# STATISTICS
# ============================================================================

st.divider()
st.subheader("📊 Statistics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Jokes Saved", len(st.session_state.joke_history))

with col2:
    if st.session_state.joke_history:
        sources = [j.get("source") for j in st.session_state.joke_history]
        most_common = max(set(sources), key=sources.count)
        st.metric("Most Used API", most_common)
    else:
        st.metric("Most Used API", "N/A")

with col3:
    if st.session_state.joke_history:
        categories = [j.get("category") for j in st.session_state.joke_history]
        most_common_cat = max(set(categories), key=categories.count)
        st.metric("Most Common Category", most_common_cat)
    else:
        st.metric("Most Common Category", "N/A")

with col4:
    st.metric("Current Joke ID", len(st.session_state.joke_history) + 1)

# ============================================================================
# ABOUT SECTION
# ============================================================================

st.divider()
with st.expander("ℹ️ About This App"):
    st.markdown("""
    ### 🎭 Random Joke Generator
    
    This app fetches random jokes from multiple APIs and displays them in a fun way!
    
    **Features:**
    - 🎲 Multiple joke sources and categories
    - 🎭 Reveal punchlines with a click
    - 💾 Save your favorite jokes
    - 📥 Export jokes as JSON
    - 📊 View statistics
    
    **Supported APIs:**
    - **JokeAPI** - Multiple categories (Programming, Dad Jokes, etc.)
    - **Official Joke API** - General and programming jokes
    - **Chuck Norris API** - Chuck Norris facts & jokes
    - **Random Joke API** - Random jokes
    
    **How to use:**
    1. Select your preferred joke type and API source
    2. Click "Get Joke" to fetch a random joke
    3. Click "Show Punchline" to reveal the answer
    4. Click "Save Joke" to save it to your history
    5. Export your jokes as JSON for sharing
    
    ---
    Made with ❤️ using Streamlit
    """)
