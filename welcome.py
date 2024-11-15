import asyncio
import os

import streamlit as st
from asyncio import sleep
from autogen import ConversableAgent
from autogen import GroupChat
from autogen import GroupChatManager
from autogen import UserProxyAgent
from autogen import AssistantAgent
from autogen.coding import LocalCommandLineCodeExecutor
from autogen import register_function

import os
import sys

import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
azure_endpoint = os.environ.get('AZURE_ENDPOINT')

openai_config_list = [
  {
    "model": "gpt-4o",
    "api_key": OPENAI_API_KEY,
    "base_url": azure_endpoint,
  },
  {
    "model": "gpt-4-turbo",
    "api_key": OPENAI_API_KEY,
    "base_url": azure_endpoint,
  }
]

llm_config_openai = {
        "config_list": openai_config_list, 
    }

llm_config = llm_config_openai






config_list_openai = [
    {
        'base_url': 'http://aitools.cs.vt.edu:7860/openai/v1',
        'api_key': 'aitools',
        'model': 'gpt-4-turbo-preview',
    },
    {
        'base_url': 'http://aitools.cs.vt.edu:7860/openai/v1',
        'api_key': 'aitools',
        'model': 'gpt-3.5-turbo',
    }

]

llm_config_openai = {
    "timeout": 300,
    "seed": 42,
    "config_list": config_list_openai,
    "temperature": 0.1,
    "allow_format_str_template": True
}


DEFAULT_MODEL = "gpt-4-turbo-preview"
FAST_MODEL = "gpt-3.5-turbo"
# Regular expression for finding a code block
CODE_BLOCK_PATTERN = r"(.*?)```(\w*)\n(.*?)\n```"
WORKING_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "coding")
UNKNOWN = "unknown"
TIMEOUT_MSG = "Timeout"
DEFAULT_TIMEOUT = 600
WIN32 = sys.platform == "win32"
PATH_SEPARATOR = WIN32 and "\\" or "/"



Event_classifier = ConversableAgent(
    name="Event_classifier",
    system_message="""You are an event classifier. You perform the following functions:
     1. For a given event, you use a tool to look up its event category. If an event seems to belong multiple categories,
     you select a primary event category, and add one or more secondary categories, in the order of relevance.
     2. 
     """,
    llm_config=llm_config,
)

API_coder = AssistantAgent(
    name="API_coder",
    system_message="""You are an API coder. You perform the following functions:
    1. use a tool to find the correct API endpoints for a task by providing a system name.
    2. write python code to call the API endpoints from step 1, using the api key provided. The code should also parse the returned info
    """,
    llm_config=llm_config,
)

Code_critic = AssistantAgent(
    name="Code_critic",
    system_message="""You are a code critic. You perform the following functions:
    1. Review the API code written by API_coder 
    2. Fix any bugs that you discovered
    """,
    llm_config=llm_config,
)

Event_guide = AssistantAgent(
    name="Event_guide",
    system_message="""You are an event guide. You perform the following functions:
    1. Review the response returned by the API call 
    2. Write helpful and succint instructions to handle the event.
    """,
    llm_config=llm_config,
)

user_proxy = UserProxyAgent(
    name = "user_proxy",
    human_input_mode = "ALWAYS",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "") and x.get(
        "content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={
        # the executor to run the generated code
        "executor": LocalCommandLineCodeExecutor(work_dir="tmp_dir"),
    },
)



group_chat = GroupChat(
    agents = [user_proxy, Event_classifier, API_coder, Code_critic, Event_guide],
    messages = [],
    max_round = 6,
    send_introductions= True,
    speaker_selection_method = "auto",
)

group_chat_manager = GroupChatManager(
    groupchat = group_chat,
    llm_config = llm_config,
)


st.set_page_config(
    page_title="Event Router",
    page_icon="📄",
    layout="wide"
)



# async def run_blueprint(seed: int = 42) -> str:
#     await sleep(3)
#     await st.session_state.blueprint.initiate_work(message=task)
#     return st.session_state.blueprint.summary_result


st.markdown("# Run Disaster Agent")
st.markdown("The Disaster Agent is a tool to help you understand the type of event, is it critical that need emergency help, or is it a routine event. Then you take an appropriate actions through the following tasks.")
agents = st.button("Start the Agents!", type="primary")



results_ctr = st.empty()

import csv

with open("event_cat.txt", "r") as f:
        event_cat = f.read()

endpoint_file = "endpoints.csv"
def endpoint_lookup(system_name: str) -> str:

    with open(endpoint_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['system'] == system_name:
                print(row['endpoint'])
                return row['endpoint']
    return None


if agents:
    with results_ctr:
        st.status("Running the Disaster Agent...")

    

    text = asyncio.run(user_proxy.initiate_chat(
    group_chat_manager,
    message=f"""You are a team to collaborate to provide real time information on an event. You need to first 
    understand the type of event, is it critical that need emergency help, or is it a routine event. Then you take an 
    appropriate actions through the following tasks.
    
    Here is the list of tasks:
    0. First you wait for an event to be provided by the user
    1. Classify the event into one primary category using the available event categories in {event_cat}. Remember the system name and api key for this event. 
    If location information is available, remeber that
    2. Provide brief and immediate helpful instructions based on the information from Step 1 to help allievate the event if it is a critical or emergency event
    3. Construct the API endpoint by replacing the category with a real category
    4. Write python code to call the API endpoint to the system name identified in Step 1 to get instructions to help with the event
    5. Execute the code from Step 4
    6. From the information returned in Step 5 and infomration from Step 2, provide more detailed helpful instructions on how to act accordingly.
    Be very helpful and succinct.
    """,
    summary_method="reflection_with_llm",
    max_turns=5,
    clear_history=True,
))
    st.balloons()



    with results_ctr:
        st.markdown(text)

