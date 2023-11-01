import streamlit as st
import openai
from youtube_transcript_api import YouTubeTranscriptApi
from streamlit_chat import message

st.title('''Dr. Lee - Co-Pilot''')
st.sidebar.image('https://clipground.com/images/miami-dade-college-logo-7.png', width=100)
st.sidebar.header("Instructions")
st.sidebar.info(
    '''This is a web application that serves as a Teaching Assistant for Dr. Ernesto Lee.
       Enter a **query** in the **text boxes** and **press enter** to receive 
       a **response**.
       '''
    )


model_engine = 'text-davinci-003'

openai.api_key = st.secrets["api_key"]

# Add a function for each tab

def code_help_tab():
    default_value = "Write a one line hello world in python"
    user_query = st.text_input("Tell me the code you want to write using plain English: ", value=default_value)
    if user_query != ":q" or user_query != "" or user_query !=default_value:
        response = ChatGPT(user_query)
        # st.code('for i in range(8): foo()')
        return st.code(f"{response}")

def ChatGPT(user_query):
    completion = openai.Completion.create(
                                  engine = model_engine,
                                  prompt = user_query,
                                  max_tokens = 1024,
                                  n = 1,
                                  temperature = 0.5,
                                      )
    response = completion.choices[0]["text"]
    lines = response.split("\n")
    indented_lines = ['    ' + line for line in lines]
    indented_response = '\n'.join(indented_lines)
    return indented_response

def concept_tab():
    default_value = "Explain Quantum Chromodynamics in 5 sentences"
    user_query = st.text_input("Describe a concept that you would like to understand: ", value=default_value)
    
    if user_query != ":q" or user_query != "":
        prompt = "Explain this concept at the level of a 16 year old.  Use analogies, real world examples, and provide an easy, creative intuitive explanation: " + user_query
        chatgpt = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=1024)
        # print(chatgpt.choices[0]['text'])
        # print(type(chatgpt.choices[0]['text']))
        response = chatgpt.choices[0]["text"].replace("\n", "") # to remonve all the \n - Courtesy of Alex Z.
        # response = get_sentiment(user_query)
        return st.write(f"{response}")

def explain_code_tab():
    st.title("Code Editor")
    
    default_value = '''
    print("Miami Dade College - Data Analytics!")
    '''
    
    code_input = st.text_area("Paste your code snippet here and it will be explained: ", value=default_value)

    if code_input:
        st.write("Output:")
        st.code(code_input)
    prompt = "Explain this code by adding extensive and easy to understand comments in the original code: " + code_input
    chatgpt = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=1024)
    response = chatgpt.choices[0]["text"]
    lines = response.split("\n")
    indented_lines = ['    ' + line for line in lines]
    indented_response = '\n'.join(indented_lines)
    # return indented_response
    return st.code(f"{indented_response}")

def explain_code_with_words_tab():
    st.title("Code Editor")
    default_value = '''
    print("Miami Dade College - Data Analytics!")
    print("This is default text")
    '''
    code_input = st.text_area("Paste your code here and it will be explained: ", value=default_value)

    if code_input:
        st.write("Output:")
        st.code(code_input)
    prompt = "Explain this code using words with a very intuitive and cheerful tone: " + code_input
    chatgpt = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=1024)
    response = chatgpt.choices[0]["text"].replace("\n", "") # to remonve all the \n - Courtesy of Alex Z.
    return st.write(f"{response}")

def bug_fix_tab():
    default_value = '''
    print("Miami Dade College - Data Analytics!)
    '''
    st.title("Find the bug!")

    code_input = st.text_area("Paste your code here",value=default_value)

    if code_input:
        st.write("Output:")
        st.code(code_input)
    prompt = "Find the bug in this code and provide a fix with comments explaining the bug and the fix: " + code_input
    chatgpt = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=1024)
    response = chatgpt.choices[0]["text"]
    lines = response.split("\n")
    indented_lines = ['    ' + line for line in lines]
    indented_response = '\n'.join(indented_lines)
    # return indented_response
    return st.code(f"{indented_response}")

def sentiment_tab():
    default_value = '''
    I woke up this morning feeling great!  Then I lost a chess game on chess.com.
    '''
    user_query = st.text_input("Place a passage or tweet here and we will decide the sentiment",value=default_value)
    if user_query != ":q" or user_query != "":
        prompt = "Decide the sentiment of a passage as positive,neutral, or negative and give the percent confidence: " + user_query
        chatgpt = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=1024)
        # print(chatgpt.choices[0]['text'])
        # print(type(chatgpt.choices[0]['text']))
        response = chatgpt.choices[0]["text"].replace("\n", "") # to remonve all the \n - Courtesy of Alex Z.
        # response = get_sentiment(user_query)
        return st.write(f"{response}")
def generate_response(prompt):
    completion=openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )
    message=completion.choices[0].text
    return message

def chat_tab():
    st.title("ChatGPT-like Web App")
    #storing the chat
    if 'generated' not in st.session_state:
        st.session_state['generated'] = []
    if 'past' not in st.session_state:
        st.session_state['past'] = []
    user_input=st.text_input("You:",key='input')
    # time.sleep(15)
    # user_input=st.text_input("You:",key='input')
    if user_input:
        output=generate_response(user_input)
        #store the output
        st.session_state['past'].append(user_input)
        st.session_state['generated'].append(output)

    if st.session_state['generated']:
        for i in range(len(st.session_state['generated'])-1, -1, -1):
            message(st.session_state["generated"][i], key=str(i))
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
    

def image_tab():
    default_value = '''
    Graduation Day at Miami Dade College!
    '''
    user_query = st.text_input("Describe an image that you would like to see:",value=default_value)
    if user_query != ":q" or user_query != "":
        prompt = "photorealistic in the style of disney: " + user_query
        response = openai.Image.create(prompt=prompt, n=1,size="1024x1024")
        image_url = response['data'][0]['url']
        # return st.write(f"{image_url}")
        return st.image(image_url, width=400, # Manually Adjust the width of the image as per requirement
        )
diagnostics = 0
include_mentions = 0

def get_video_id_from_video_id_or_url(video_id_or_url):
    # a youtube video id is 11 characters long
    # if the video id is longer than that, then it's a url
    if len(video_id_or_url) > 11:
        # it's a url
        # the video id is the last 11 characters
        return video_id_or_url[-11:]
    else:
        # it's a video id
        return video_id_or_url

def get_chunks_from_youtube(video_id):
    # this function will get the transcript of a youtube video
    # and return it as an array of chunks
    # where each chunk is an array of lines

    # first get the transcript
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    print(transcript)

    chunks = []

    start_timestamp = 0.0
    current_timestamp_mins = 0.0

    current_chunk = []

    for entry in transcript:
        current_timestamp_mins = entry['start'] / 60.0

        # if the current timestamp is more than 10 minutes after the start timestamp
        # then we have a chunk
        if current_timestamp_mins - start_timestamp > 10:
            # add the current chunk to the list of chunks
            chunks.append(current_chunk)
            # reset the start timestamp
            start_timestamp = current_timestamp_mins
            # reset the current chunk
            current_chunk = []

        # add the line to the current chunk
        current_chunk.append(entry['text'])

    # add the last chunk
    if len(current_chunk) > 0:
        chunks.append(current_chunk)

    print(f"Found {len(chunks)} chunks")

    return chunks

def summarize_chunk(index, chunk):
    chunk_str = "\n".join(chunk)
    prompt = f"""The following is a section of the transcript of a youtube video. It is section #{index+1}:
    {chunk_str}
    Summarize this section of the transcript."""

    if diagnostics:
        # print each line of the prompt with a leading # so we can see it in the output
        for line in prompt.split('\n'):
            print(f"# {line}")

    completion = openai.Completion.create(
        engine="text-davinci-003", 
        max_tokens=500, 
        temperature=0.9,
        prompt=prompt,
        frequency_penalty=0
    )

    msg = completion.choices[0].text

    if diagnostics:
        print(f"# Response: {msg}")

    return msg

def summarize_the_summaries(summaries):

    summaries_str = ""
    for index, summary in enumerate(summaries):
        summaries_str += f"Summary of chunk {index+1}:\n{summary}\n\n"

    prompt = f"""The following are summaries of a youtube video in 10 minute chunks:"
    {summaries_str}
    Summarize the summaries."""

    if diagnostics:
        # print each line of the prompt with a leading # so we can see it in the output
        for line in prompt.split('\n'):
            print(f"# {line}")

    completion = openai.Completion.create(
        engine="text-davinci-003", 
        max_tokens=500, 
        temperature=0.2,
        prompt=prompt,
        frequency_penalty=0
    )

    msg = completion.choices[0].text

    if diagnostics:
        print(f"# Response: {msg}")

    return msg

def yt_summary_tab():
    default_value = "https://www.youtube.com/watch?v=TfBawacOaeg"
    user_query = st.text_input("Place a YouTube URL here and make sure CC is enabled: ", value=default_value)
    if user_query != ":q" or user_query != "":
        # prompt = "Decide the sentiment of a passage as positive,neutral, or negative and give the percent confidence: " + user_query
        # Get the transcript of the video
        video_id_or_url = user_query

        # if the video id or url is a url, extract the video id
        video_id = get_video_id_from_video_id_or_url(video_id_or_url)

        # chunks = get_chunks(transcript_file_name)
        chunks = get_chunks_from_youtube(video_id)

        if len(chunks) == 0:
            st.write("No chunks found")
        elif len(chunks) == 1:
            summary = summarize_chunk(0, chunks[0])
            st.write(f"\nSummary: {summary}")
        else:
            # Now we have the chunks, we can summarize each one
            summaries = []
            for index, chunk in enumerate(chunks):
                summary = summarize_chunk(index, chunk)
                summaries.append(summary)
                st.write(f"\nSummary of chunk {index+1}: {summary}")

            # Now we have the summaries, we can summarize the summaries
            summary_of_summaries = summarize_the_summaries(summaries)

            st.write(f"\nSummary of summaries: {summary_of_summaries}")


# Add the tabs to the app
st.sidebar.title("Navigation")
selected_tab = st.sidebar.radio("Select a tab", ["Code Help", "Concept Help", "Explain this code", "Sentiment","Image","Bug Fix","Chat","YouTube Summarizer","Explain Code with Words"])

if selected_tab == "Code Help":
    code_help_tab()
elif selected_tab == "Concept Help":
    concept_tab()
elif selected_tab == "Bug Fix":
    bug_fix_tab()
elif selected_tab == "Sentiment":
    sentiment_tab()
elif selected_tab == "Image":
    image_tab()
elif selected_tab == "Chat":
    chat_tab()
elif selected_tab == "YouTube Summarizer":
    yt_summary_tab()
elif selected_tab == "Explain Code with Words":
    explain_code_with_words_tab()
else:
    explain_code_tab()
