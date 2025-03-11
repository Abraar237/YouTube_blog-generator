import re
import requests
from bs4 import BeautifulSoup
from youtube_transcript_api import YouTubeTranscriptApi
from google import genai
from google.genai import types
import streamlit as st

def summarize(result):
    """Summarize the transcript using Gemini API"""
    
    sys_instruct = f"You are a YouTube Notes Maker who creates notes or docs based on the transcript provided. Use only the transcript to make notes in {language} language, highlight the main topics, and structure it with subheadings.  dont mention anything else except like explaantion in ur reponse just mention the video title {result.get('title')} tumbnail url {result.get('thumbnail_url')} at top and nothing else write in more detail 3-4 subtitles minimum make sure it conatins important topics and subheadings can be question highlighting important topic as well"
    client = genai.Client(api_key=st.secrets["KEY"])

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        config=types.GenerateContentConfig(
            system_instruction=sys_instruct
        ),
        contents=[result.get("transcript")]  # Ensure contents is a list
    ).candidates[0].content.parts[0].text
    with open("response.txt", "w") as f:
        f.write(response)
    return response




def html_generator(response):
    sys_instruct = '''you are website designer specialising in html css tailwind take the follwoing html template and design the same for the below contents which is the summary of the youtube video design accordingly to the template below. only repond with html file nothing else
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Video Summary Template</title>
  <!-- Tailwind CSS CDN -->
  <link
    rel="stylesheet"
    href="https://unpkg.com/tailwindcss@2.2.19/dist/tailwind.min.css"
  />
  <!-- Google Font -->
  <link rel="preconnect" href="https://fonts.gstatic.com" />
  <link
    href="https://fonts.googleapis.com/css2?family=Patrick+Hand&display=swap"
    rel="stylesheet"
  />
  <style>
    body {
      background-color: #f7fafc;
      font-family: 'Patrick Hand', sans-serif;
    }
    h1, h2 {
      font-weight: 700;
      margin-bottom: 0.5rem;
    }
    ul, ol {
      margin-left: 1.5rem;
      margin-bottom: 1.5rem;
    }
    li {
      margin-bottom: 1rem;
    }
     .point-title-1 {
    
      font-size: 1.2em;
    }
    .point-title-2 {
      
      font-size: 1.2em;
    }
    .point-title-3 {
      
      font-size: 1.2em;
    }
    .bullet-content {
      font-size: 1.0em;
    }
  </style>
</head>
<body class="min-h-screen flex items-center justify-center p-4">
  <div class="max-w-2xl w-full bg-white rounded-2xl shadow-lg p-6">
    <!-- Attribution header -->
    <div class="mb-6 text-right text-gray-500 text-sm">
      Generated by Abraar
      <a href="https://github.com/Abraar237/YouTube_blog-generator" class="underline hover:text-gray-700">
        App Name
      </a>
    </div>
    
    <!-- Video Title -->
    <h1 class="text-4xl text-gray-800 mb-4">[Video Title]</h1>
    
    <!-- Thumbnail/Image -->
    <img
      src="[Thumbnail URL]"
      alt="Video Thumbnail"
      class="rounded-xl mb-6"
    />
    
    <!-- Summary Section -->
    <h2 class="text-3xl text-gray-800 mb-4">[Summary Subtitle]</h2>
    <ul class="text-gray-600">
      <li>
        <strong class="point-title-1">[Point Title]</strong><br />
        <div class="bullet-content">[Point description]</div>
      </li>
      <li>
        <strong class="point-title-2">[Point Title]</strong><br />
        <div class="bullet-content">[Point description]</div>
      </li>
      <!-- Add more points as needed -->
    </ul>
  </div>
</body>
</html>


    '''
    client1 = genai.Client(st.secrets["KEY"])

    op = client1.models.generate_content(
        model="gemini-2.0-flash",
        config=types.GenerateContentConfig(
            system_instruction=sys_instruct
        ),
        contents=response # Ensure contents is a list
    ).candidates[0].content.parts[0].text
    return op



def extract_video_id(url):
    """Extract YouTube video ID from URL"""
    pattern = r'(?:v=|\/)([0-9A-Za-z_-]{11})'
    match = re.search(pattern, url)
    return match.group(1) if match else None

def get_video_info(url):
    """Get video title, transcript and thumbnail"""
    video_id = extract_video_id(url)
    if not video_id:
        return {"error": "Invalid YouTube URL"}
    
    try:
        # Get title using BeautifulSoup
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        title_tag = soup.find('title')
        title = title_tag.text.replace(" - YouTube", "")
        
        # Get thumbnail
        thumbnail_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
        
        # Get transcript
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = " ".join([entry["text"] for entry in transcript_list])
        
        return {
            "title": title,
            "transcript": transcript,
            "thumbnail_url": thumbnail_url,
            "video_id": video_id
        }
    except Exception as e:
        return {"error": str(e)}

def save_html_file(response, file_name="output.html"):
    # Ensure the content starts from <!DOCTYPE html>
    start_index = response.find("<!DOCTYPE html>")
    if start_index != -1:
        html_content = response[start_index:]
    else:
        raise ValueError("Invalid HTML content: <!DOCTYPE html> not found.")
    
    # Save the cleaned HTML content to a file
    with open(file_name, "w", encoding="utf-8") as html_file:
        html_file.write(html_content)
    print(f"HTML content has been saved to {file_name}.")
    return file_name


# Streamlit UI

st.set_page_config(
    page_title="YouTube Video Summarizer",  # Title shown on the browser tab
    page_icon="📺",  # Can be an emoji or a URL to an image
    layout="centered",  # Other options: "wide"
)

st.markdown("""
        <div class="container">
            <div class="row">
            <div class="col text-center">

<h1 style='font-family: "Copperplate", serif; font-weight: 400;font-size : 35px'>
    Youtube Blog Generator
</h1>

   
        """, 
            unsafe_allow_html=True)
st.markdown("""
    <style>
    .stChatMessage div[data-testid="stMarkdownContainer"] {
        color: black !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar
st.sidebar.title("Settings")

# Language Selection
st.sidebar.subheader("🌍 Language Selection")
language = st.sidebar.selectbox("Choose Output Language", ["English", "Spanish", "French", "German", "Hindi", "Chinese"], index=0)

# Customization Options




# Apply custom CSS
st.markdown("""
    <style>
        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        }
        [data-testid="stSidebar"] h1 {
            color: #333;
            font-size: 22px;
            font-weight: bold;
        }
        [data-testid="stSidebar"] p {
            color: #666;
            font-size: 16px;
            line-height: 1.5;
        }
        [data-testid="stSidebar"] a {
            color: #007bff;
            font-size: 16px;
            text-decoration: none;
            font-weight: bold;
        }
        [data-testid="stSidebar"] a:hover {
            text-decoration: underline;
        }
                  .sidebar-footer {
            font-size: 14px;
            color: #555;
            font-style: italic;
            margin-top: auto;
          
        }
        </style>
    """, unsafe_allow_html=True)

    # s
st.markdown(
    "<script>window.scrollTo(0, document.body.scrollHeight);</script>",
    unsafe_allow_html=True,
)
yt_url = st.text_input("Enter YouTube URL:", "")
st.markdown("""
    <style>
        div[data-testid="stButton"] > button {
            background-color: #1e1e1e !important;
            color: white !important;
            padding: 10px 11px !important;
            border-radius: 6px !important;
            font-weight: 600 !important;
            cursor: pointer !important;
            transition: all 0.2s ease-in-out !important;
            border: 1px solid transparent !important;
            box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1) !important;
            font-size: 16px !important;
            width: 19% !important;
            text-align: center !important;
        }
        div[data-testid="stButton"] > button:hover {
            background-color: #27272a !important;
            border-color: #3f3f46 !important;
        }
        div[data-testid="stButton"] > button:active {
            transform: scale(0.98) !important;
        }
    </style>
    """, unsafe_allow_html=True)

# Streamlit button with ShadCN styling
if st.button("Submit", key="process_video"):
    if yt_url:
        # Create containers in the correct order
        download_container = st.container()  # Container for download buttons at the top
        spinner_container = st.container()   # Container for spinners/progress
        content_container = st.container()   # Container for content (image, etc.)
        sidebar_download_container = st.sidebar.container()  # Sidebar container
        
        # Initialize progress indicator in the spinner container
        with spinner_container:
            progress = st.progress(0)
            status_text = st.empty()  # Placeholder for status messages
        
        # Process starts
        with spinner_container:
            status_text.text("Fetching video information...")
            video_info = get_video_info(yt_url)
            progress.progress(25)
        
        if video_info:
          # Update progress
          with spinner_container:
              status_text.text("Summarizing transcript...")
              progress.progress(50)
              summary = summarize(video_info)
              
              status_text.text("Generating HTML file...")
              progress.progress(75)
              html_content = html_generator(summary)
              file_path = save_html_file(html_content)
              progress.progress(100)
              status_text.text("Processing complete!")
          
          # First display the image
          with content_container:
              st.image(video_info["thumbnail_url"], caption=video_info["title"], use_container_width=True)
              
              # Then add the styled download button below the image
              # Define ShadCN Button CSS
              st.markdown("""
              <style>
              .shadcn-button {
                  display: inline-flex;
                  align-items: center;
                  justify-content: center;
                  border-radius: 0.375rem;
                  font-size: 0.875rem;
                  height: 2.5rem;
                  padding-left: 1rem;
                  padding-right: 1rem;
                  background-color: hsl(240, 5.9%, 10%);
                  color: hsl(0, 0%, 98%) !important;  /* Ensures white font */
                  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
                  cursor: pointer;
                  transition: background-color 0.2s, color 0.2s, box-shadow 0.2s;
                  border: none;
                  width: 25%;
                  margin: 0.5rem 0;
                  text-decoration: none !important;  /* Removes underline */
                  font-weight: 600;
              }
              
              .shadcn-button:hover {
                  background-color: hsl(240, 4.9%, 15%);
              }
              
              .shadcn-button:focus {
                  outline: 2px solid hsl(240, 5.9%, 10%);
                  outline-offset: 2px;
              }
              
              .shadcn-button svg {
                  margin-right: 0.5rem;
              }
              </style>
              """, unsafe_allow_html=True)
              
              # Create a downloadable link for output.html
              with open(file_path, "r", encoding="utf-8") as file:
                  html_string = file.read()
              
              # URL encode the HTML content
              import urllib.parse
              encoded_html = urllib.parse.quote(html_string)
              download_link = f"data:text/html;charset=utf-8,{encoded_html}"
              
              # Add ShadCN button with a real download link
              st.markdown(f"""
              <a href="{download_link}" download="output.html" class="shadcn-button">
                  <svg width="15" height="15" viewBox="0 0 15 15" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M7.5 10.625L3.75 6.875L4.5 6.125L7 8.625V0H8V8.625L10.5 6.125L11.25 6.875L7.5 10.625ZM0 15V5H3V6H1V14H14V6H12V5H15V15H0Z" fill="white"/>
                  </svg>
                  Download HTML
              </a>
              """, unsafe_allow_html=True)
          
          # Sidebar download button
          with sidebar_download_container:
              with open(file_path, "rb") as file:
                  file_content = file.read()
                  st.download_button(
                      label="Download HTML",
                      file_name="output_sidebar.html",
                      data=file_content,
                      mime="text/html"
                  )
      
