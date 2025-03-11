# Design Document for YouTube Blog Generator

## Overview
The YouTube Blog Generator is a Streamlit-based application that processes a YouTube video URL, fetches the video information, generates a detailed summary of the transcript, and provides a downloadable HTML file styled with Tailwind CSS. The app incorporates multiple functionalities, including transcript fetching, language selection, and HTML file generation with an emphasis on user-friendly design.

## Features

1. **YouTube Video Information Retrieval**
   - Extracts video title, thumbnail, and transcript using:
     - Regular expressions to parse the video ID from the URL.
     - BeautifulSoup to scrape the video title.
     - YouTube Transcript API to fetch the transcript.
   - Assembles the extracted data into a structured dictionary.

2. **Transcript Summarization**
   - Uses Google Gemini API to process the transcript and generate a detailed summary with structured subheadings.
   - Customizable language selection for the summary output.

3. **HTML File Generation**
   - Converts the summary into a formatted HTML file using a predefined template with Tailwind CSS for styling.
   - Ensures the output HTML file adheres to a clean and professional design.

4. **Streamlit UI**
   - Interactive user interface for:
     - Inputting YouTube URLs.
     - Selecting the output language.
     - Downloading the generated HTML file.
   - Custom styling for buttons, sidebar, and main page layout using embedded CSS.

5. **File Download**
   - Provides an inline download link for the generated HTML file.
   - Offers a secondary download option via the sidebar.

---

## Design Components

### 1. **Frontend (Streamlit UI)**

#### Header
- Displays the app title styled with custom fonts and CSS.

#### Input Field
- Text input field for entering the YouTube URL.

#### Buttons
- A primary "Submit" button to trigger the processing pipeline.
- Styled with hover effects and focus outlines for better accessibility.

#### Sidebar
- Includes:
  - Language selection dropdown for transcript summarization.
  - Secondary download button for the HTML file.

#### Download Section
- Styled buttons (main and sidebar) for downloading the HTML file.

### 2. **Backend**

#### Video Information Retrieval
- Extracts video information such as:
  - **Title**: Scraped using BeautifulSoup.
  - **Thumbnail URL**: Constructed using the video ID.
  - **Transcript**: Fetched using the YouTube Transcript API and processed into a single text block.

#### Transcript Summarization
- Sends the transcript to the Gemini API with specific system instructions to generate structured notes.

#### HTML File Generation
- Utilizes the Gemini API to create an HTML file based on the summary content.
- Embeds a predefined HTML template styled with Tailwind CSS.

### 3. **Styling (CSS)**
- Custom styling for:
  - **Buttons**: ShadCN-inspired designs with hover and active states.
  - **Sidebar**: Soft shadows, rounded corners, and responsive layout.
  - **HTML Template**: Clean design with responsive elements and a focus on readability.

### 4. **Error Handling**
- Validates YouTube URL format.
- Catches and displays errors for missing transcripts or invalid URLs.

---

## Workflow

1. **Input YouTube URL**
   - User enters a valid YouTube video URL in the input field.

2. **Video Information Retrieval**
   - Extracts video title, thumbnail, and transcript.

3. **Summarization**
   - Processes the transcript through the Gemini API to generate structured notes.

4. **HTML Generation**
   - Converts the summary into a formatted HTML file.

5. **Download Options**
   - Provides the generated HTML file as a downloadable link on the main page and in the sidebar.

6. **Progress Indicators**
   - Displays progress updates during processing using Streamlit's progress bar and status text.

---

## Code Structure

### Main Functions
1. **`extract_video_id(url)`**
   - Extracts the video ID from the YouTube URL using regex.

2. **`get_video_info(url)`**
   - Fetches the video title, thumbnail URL, and transcript.

3. **`summarize(result)`**
   - Generates a detailed summary of the transcript using the Gemini API.

4. **`html_generator(response)`**
   - Converts the summary into an HTML file based on the predefined template.

5. **`save_html_file(response, file_name)`**
   - Saves the generated HTML content to a file.

6. **Streamlit Components**
   - Handles user inputs, progress indicators, and download links.

---

## Future Enhancements
1. **Enhanced Error Handling**
   - Add detailed error messages for API failures or invalid inputs.

2. **Customization Options**
   - Allow users to customize the HTML template (e.g., colors, fonts, layouts).

3. **Multi-language Support**
   - Expand language options for the user interface.

4. **Deployment**
   - Package the application for cloud deployment with scalability considerations.

---

## References
- [YouTube Transcript API Documentation](https://pypi.org/project/youtube-transcript-api/)
- [Google Gemini API Documentation](https://cloud.google.com/genai/)
- [Streamlit Documentation](https://docs.streamlit.io/)

