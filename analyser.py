# Kor!
from kor.extraction import create_extraction_chain
from kor.nodes import Object, Text, Number

# LangChain Models
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI

# Standard Helpers
import pandas as pdsource 
import requests
import time
import json
import os
from dotenv import load_dotenv
from datetime import datetime

# Text Helpers
from bs4 import BeautifulSoup
from markdownify import markdownify as md

# For token counting
from langchain.callbacks import get_openai_callback

def printOutput(output):
    print(json.dumps(output,sort_keys=True, indent=3))

def configure():
    load_dotenv()

configure()

openai_api_key = os.getenv('openai_api_key')

llm = ChatOpenAI(
    model_name="gpt-3.5-turbo", # Cheaper but less reliable
#   model_name="gpt-4",
    temperature=0,
    max_tokens=2000,
    openai_api_key=openai_api_key
)

schema = Object(
  id="translate_order",
  description=(
      "The user makes an order for a text to be translated by a translating system."
      "The user provides details of the order regarding languages, deadline of the order and attached documents."
      "The result is provided in Polish language."
  ),
  attributes=[
      Text(
          id="language_from",
          description="The language we are translating from in the 'ISO-639-1 - ISO 3166-1' format.",
          examples=[("I would like a translation of the attached Word from Polish into British, due by the end of next week", "pl - PL")],
          many=True,
      ),
      Text(
          id="language_to",
          description="Language to which we are translating, given in the abbreviated form 'ISO-639-1 - ISO 3166-1'.",
          examples=[("I would like a translation of the attached Word from Polish into British, due by the end of next week", "en - GB")],
          many=True,
      ),
      Text(
          id="document",
          description="Attached document.",
          examples=[("I would like a translation of the attached Word from Polish into British, due by the end of next week", "Word")],
          many=True,
      ),
      Text(
          id="deadline",
          description="The deadline for the execution of the order.",
          examples=[("I would like a translation of the attached Word from Polish into British, due by the end of next week", "do końca przyszłego tygodnia"),
                    ("Please translate the attached Word from Bengali to German, express order, we need to publish before April 5", "przed 5 kwietnia"),
                    ("I would like a translation of the attached Word from Bengali to German, due January 21st", "21 stycznia"),
                    ("I would like a translation of the attached PDF from Polish to German, as soon as possible", "jak najszybciej"),
                    ("Poprosze o tłumaczenie załaczonego Worda z bengalskiego na niemiecki, zlecenie ekspresowe, musimy opublikować przed 5 kwietnia", "przed 5 kwietnia")],
          many=True,
      ),
    ],
  many=False,
)

chain = create_extraction_chain(llm, schema, encoder_or_encoder_class='json')
#print("bef")
output = chain.predict_and_parse(text="poprosze o tłumaczenie załaczonego Worda na brytyjski angielski i amerykanski angielski, termin do konca przyszlego tygodnia")['data']
print("analyserpy")
print(type(output['translate_order']['deadline']))
printOutput(output['translate_order']['deadline'][0])

def analyseMail(content):
    return (chain.predict_and_parse(text=str(content))['data'])







