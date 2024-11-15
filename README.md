# AI-powered automated event-routing and response system

This system takes a user event message and determines the category of the event. An event could be a critical emergency event or a routine event, as determined by the user. From that it will construct the API endpoint and generate Python code to call the endpoint. The system will then make the API call to get a response and provide instructions how to handle the event to users.

The system is instantiated by Autogen with 4 AI agents:
- Event_classifier: classify the event to a category, return category, system name, and api key
- API_coder: look up the API endpoint for the system name, construct Python code to perform the API call
- Code_critic: review the code and fix any errors
- Event_guide: parse the API return and provide helpful and succint instructions to handle the event

The fastapi is provided for testing purpose. To start the service, run:
fastapi dev service/main.py

You may need to install the package before that:
pip install fastapi

