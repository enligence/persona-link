# FastAPI app for persona_link that is secured by an API Key
# it will have ways to manage API keys and for each account

"""
A REST API to provide end points for avatar interaction.
Route that will take avatarId, text to speak and return the video our audio information
Route that will take in the applicationId, what user said and pass it on to the webhook
of the calling application.

Later we may want to port these to grpc for better performance.
"""


