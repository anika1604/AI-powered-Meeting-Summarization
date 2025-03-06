import os
from dotenv import load_dotenv, dotenv_values
from flask import Flask
from groq import Groq


load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")


client = Groq(
    api_key=my_api_key,
)

