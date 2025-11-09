import os

import streamlit as st
from dotenv import load_dotenv

from news_summarizer import NewsArticleSummarizer
from voice_assistant import VoiceAssistantRAG, setup_knowledge_base
from yt_summarizer import YoutubeVideoSummarizer

load_dotenv()
st.set_page_config(page_title="Multi-RAG Suite", layout="centered")
st.title("QuickView: News • YouTube • Voice")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
tab1, tab2, tab3 = st.tabs(["🗞 News Summarizer", "📺 YouTube Summarizer", "🎙 Voice Assistant"])

with tab1:
    st.subheader("News Article Summarizer")
    url = st.text_input("Enter article URL:")
    if st.button("Summarize Article"):
        if url:
            with st.spinner("Summarizing..."):
                ns = NewsArticleSummarizer(api_key=OPENAI_API_KEY)
                result = ns.summarize(url)
                if result:
                    st.success("Summary:")
                    st.write(result["summary"]["output_text"])
                else:
                    st.warning("Error summarizing article!")
        else:
            st.warning("Please enter a valid URL.")

with tab2:
    st.subheader("YouTube Video Summarizer")
    yt_url = st.text_input("Enter YouTube URL:")
    if st.button("Summarize Video"):
        if yt_url:
            with st.spinner("Processing video..."):
                ys = YoutubeVideoSummarizer()
                result = ys.process_video(yt_url)
                if result:
                    st.success("Summary:")
                    st.write(result["summary"]["output_text"])
                else:
                    st.warning("Error summarizing video!")

        else:
            st.warning("Please enter a YouTube URL.")

with tab3:
    st.subheader("Voice Assistant RAG")

    # "Setup Knowledge Base":
    vector_store = setup_knowledge_base()
    if vector_store:
        st.session_state.vector_store = vector_store

    # Voice Assistant page
    if "vector_store" not in st.session_state:
        st.error("Please setup knowledge base first!")
    else:
        # Initialize assistant
        assistant = VoiceAssistantRAG()
        # Initialize the vector store and QA chain
        assistant.setup_vector_store(st.session_state.vector_store)
        # Voice selection
        try:
            available_voices = assistant.voice_generator.available_voices
            if available_voices:
                selected_voice = st.selectbox(
                    "Select Voice",
                    available_voices,
                    index=(
                        available_voices.index("Rachel") if "Rachel" in available_voices else 0
                    ),  # todo: replace with voice_ids.
                )
                selected_voice = "pNInz6obpgDQGcFmaJgB"
            else:
                st.warning("No voices available. Using default voice.")
                selected_voice = "pNInz6obpgDQGcFmaJgB"
        except Exception as e:
            st.error(f"Error loading voices: {e}")
            selected_voice = "pNInz6obpgDQGcFmaJgB"

        # Recording duration
        duration = st.slider("Recording Duration (seconds)", 1, 10, 5)

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Start Recording"):
                with st.spinner(f"Recording for {duration} seconds..."):
                    audio_data = assistant.record_audio(duration)
                    st.session_state.audio_data = audio_data
                    st.success("Recording completed!")

        with col2:
            if st.button("Process Recording"):
                if "audio_data" not in st.session_state:
                    st.error("Please record audio first!")

                # Process recording
                with st.spinner("Transcribing..."):
                    query = assistant.transcribe_audio(st.session_state.audio_data)
                    st.write("You said:", query)

                with st.spinner("Generating response..."):
                    try:
                        response = assistant.generate_response(query)
                        st.write("Response:", response)
                        st.session_state.last_response = response
                    except Exception as e:
                        st.error(f"Error generating response: {str(e)}")

                with st.spinner("Converting to speech..."):
                    audio_file = assistant.voice_generator.generate_voice_response(
                        response, selected_voice
                    )
                    if audio_file:
                        st.audio(audio_file)
                        os.unlink(audio_file)
                    else:
                        st.error("Failed to generate voice response")
