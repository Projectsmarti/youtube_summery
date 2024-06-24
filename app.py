import streamlit as st
from dotenv import load_dotenv
from pytube import YouTube

load_dotenv()  ##load all the nevironment variables
import os
import google.generativeai as genai

from youtube_transcript_api import YouTubeTranscriptApi

prompt = """You are Youtube video summarizer. You will be taking the transcript text and summarizing the entire video and providing
the overall summary get the major points discussed, never mention the name of the person
1.keypoint.....

within 250 words in following format. Please provide the summary of the text given here:  """


## getting the transcript data from yt videos
def generate_gemini_content(transcript_text, prompt):
    global response
    try:
        os.environ['GOOGLE_API_KEY'] = 'AIzaSyB5JjP_KNtiZAfB48zB3b4-qQa1XQqb70k'  # Replace with your API key
        genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

        models = [m for m in genai.list_models() if "text-bison" in m.name]
        model = models[0].name

        # Generate text using the specified model
        completion = genai.generate_text(
            model=model,
            prompt=transcript_text + prompt,
            temperature=0.1,
            max_output_tokens=800)

        output = completion.result.split('\n')
        response = "\n".join(output)
        return response
    except Exception as e:
        print(f"An error occurred in the get_palm_response function: {str(e)}")
        e = e
        return e


def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]

        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)

        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]

        return transcript

    except Exception as e:
        raise e


def get_video_duration(youtube_video_url):
    try:
        # Fetch video details using pytube
        yt = YouTube(youtube_video_url)
        duration = yt.length  # Duration in seconds

        # Convert duration to minutes and seconds
        minutes, seconds = divmod(duration, 60)
        duration_formatted = f"{minutes} minutes and {seconds} seconds"

        return duration_formatted

    except Exception as e:
        raise e


# Change title color using HTML
st.markdown(
    """
    <style>
    .centered-title {
        text-align: center;
        color: #044599;
    }
    </style>
    <h1 class='centered-title'>YouTube Transcription and Summarization</h1>
    """,
    unsafe_allow_html=True
)
youtube_link = st.text_input("Enter YouTube Video Link Address:")

st.markdown(
    """
    <style>
    .stButton > button {
        display: block;
        margin: 0 auto;
    }
    </style>
    """, unsafe_allow_html=True)

if youtube_link:
    video_id = youtube_link.split("=")[1]
    st.video(f"https://www.youtube.com/watch?v={video_id}")

if st.button("Get Summary"):
    try:
        transcript_text = extract_transcript_details(youtube_link)
        dur = get_video_duration(youtube_link)
        # st.write(dur)
        st.write(f"Runtime: {dur}")
        if transcript_text:
            summary = generate_gemini_content(transcript_text, prompt)
            st.markdown("### Detailed Notes:")
            st.write(summary)
        # else:
        #     st.write(e)
    except:
        st.error('Error: Unable to retrieve transcript or generate summary.')
