import streamlit as st  

# Save an example HTML file to be downloaded
html_content = "<html><body><h1>YouTube Video Summary</h1></body></html>"
# Define ShadCN Button CSS once at the beginning of your app
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

/* Additional styles for submit buttons */
.submit-form {
    display: none; /* Hide the form */
}

.stButton button {
    display: none; /* Hide the standard button */
}
</style>
""", unsafe_allow_html=True)

# Get the URL input
yt_url = st.text_input("Enter YouTube URL:", "")

# Create a hidden Streamlit button that will be triggered by our custom button
submit_button_placeholder = st.empty()
is_processing = submit_button_placeholder.button("Submit", key="process_video")

# Create our custom styled button
st.markdown("""
<form class="submit-form" id="form1" onsubmit="document.getElementById('button_process_video').click(); return false">
    <input type="submit" value="Submit">
</form>

<a href="#" onclick="document.getElementById('form1').dispatchEvent(new Event('submit')); return false" class="shadcn-button">
    <svg width="15" height="15" viewBox="0 0 15 15" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M8 2.75C8 2.47386 7.77614 2.25 7.5 2.25C7.22386 2.25 7 2.47386 7 2.75V7H2.75C2.47386 7 2.25 7.22386 2.25 7.5C2.25 7.77614 2.47386 8 2.75 8H7V12.25C7 12.5261 7.22386 12.75 7.5 12.75C7.77614 12.75 8 12.5261 8 12.25V8H12.25C12.5261 8 12.75 7.77614 12.75 7.5C12.75 7.22386 12.5261 7 12.25 7H8V2.75Z" fill="white"/>
    </svg>
    Submit
</a>
""", unsafe_allow_html=True)