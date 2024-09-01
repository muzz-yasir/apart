import streamlit as st
import requests
import base64
from datetime import datetime

HCVS_API_URL = "http://localhost:8000/v1"

def get_logo_svg():
    return """
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
      <rect width="100" height="100" fill="#f0f0f0"/>
      <text x="50" y="75" font-family="Arial, sans-serif" font-size="80" font-weight="bold" fill="black" text-anchor="middle">T</text>
    </svg>
    """

def get_verification_badge(score):
    color = "green" if score > 0.8 else "orange" if score > 0.5 else "red"
    svg = f"""
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
      <rect width="100" height="100" fill="{color}"/>
      <text x="50" y="20" font-family="Arial, sans-serif" font-size="12" font-weight="bold" fill="white" text-anchor="middle">HCVS: {score:.2f}</text>
      <g transform="translate(50,50) scale(0.7)">
        <path d="M0 -40 L-20 -15 L-10 -15 L-20 5 L-10 5 L-30 30 L-10 30 L-20 60 L20 60 L10 30 L30 30 L10 5 L20 5 L10 -15 L20 -15 Z" fill="black"/>
        <rect x="-5" y="60" width="10" height="20" fill="black"/>
      </g>
    </svg>
    """
    return f"data:image/svg+xml;base64,{base64.b64encode(svg.encode('utf-8')).decode('utf-8')}"



def main():
    icon_svg = get_logo_svg()
    icon_base64 = base64.b64encode(icon_svg.encode('utf-8')).decode('utf-8')
    icon_url = f"data:image/svg+xml;base64,{icon_base64}"
    
    st.set_page_config(page_title="TruthBlog", page_icon=icon_url, layout="wide")

    st.title("TruthBlog")

    st.sidebar.image(icon_url, width=100)
    st.sidebar.title("TruthBlog")
    page = st.sidebar.radio("Navigate", ["Home", "New Post", "About HCVS"])

    if page == "Home":
        st.header("Recent Blog Posts")
        
        response = requests.get(f"{HCVS_API_URL}/posts")
        if response.status_code == 200:
            posts = response.json()
            for post in reversed(posts):
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.subheader(post["title"])
                    st.write(f"Author: {post['author']}")
                    st.write(f"Published: {post['timestamp']}")
                    st.write(post["content"])
                with col2:
                    badge_url = get_verification_badge(post['human_score'])
                    st.image(badge_url, width=100)
                
                st.markdown("---")

            if not posts:
                st.info("No posts yet. Be the first to create a post!")
        else:
            st.error("Failed to fetch posts. Please try again later.")

    elif page == "New Post":
        st.header("Create a New Blog Post")
        title = st.text_input("Post Title")
        content = st.text_area("Post Content")
        author = st.text_input("Your Name")
        
        if st.button("Publish"):
            if title and content and author:
                response = requests.post(f"{HCVS_API_URL}/verify", json={
                    "content": content,
                    "type": "text",
                    "metadata": {"author": author, "title": title}
                })
                
                if response.status_code == 200:
                    result = response.json()
                    st.success("Post published successfully!")
                    st.write(f"Human Score: {result['human_score']:.2f}")
                else:
                    st.error("Failed to publish post. Please try again.")
            else:
                st.warning("Please fill in all fields.")

    elif page == "About DarkForest":
        st.header("About DarkForest's Human Content Verification System (HCVS)")
        st.write("""
        DarkForest's Human Content Verification System (HCVS) is an innovative solution designed to ensure the authenticity of online content. 
        It uses an ensemble of advanced algorithms to distinguish between human-generated and AI-generated content, providing a trust score for each post.

        Key features:
        - Real-time content verification
        - Blockchain-based immutable record keeping
        - Easy-to-understand verification badges

        DarkForest helps maintain the integrity of online platforms by promoting genuine human interaction and creativity.
        """)

    st.sidebar.info("TruthBlog is powered by DarkForest")

if __name__ == "__main__":
    main()