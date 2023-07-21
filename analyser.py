# Kor!
from kor.extraction import create_extraction_chain
from kor.nodes import Object, Text, Number

# LangChain Models
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI

# Standard Helpers
import pandas as pd
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
  id="tlumaczenie_zlecenie",
  description=(
      "Użytkownik składa zlecenie na tłumaczenie tekstu przez tłumacza."
      "Użytkownik podaje szczegóły zlecenia dotyczące języków, terminu wykonania i załączonych dokumentów."
  ),
  attributes=[
      Text(
          id="jezyk_z",
          description="Język, z którego tłumaczymy.",
          examples=[("Poprosze o tłumaczenie załaczonego Worda z polskiego na brytyjski, termin do konca przyszlego tygodnia", "polski")],
          many=True,
      ),
      Text(
          id="jezyk_na",
          description="Język, na który tłumaczymy.",
          examples=[("Poprosze o tłumaczenie załaczonego Worda z polskiego na brytyjski, termin do konca przyszlego tygodnia", "brytyjski")],
          many=True,
      ),
      Text(
          id="dokument",
          description="Załączony dokument.",
          examples=[("Poprosze o tłumaczenie załaczonego Worda z polskiego na brytyjski, termin do konca przyszlego tygodnia", "Word")],
          many=True,
      ),
      Text(
          id="termin",
          description="Termin wykonania zlecenia.",
          examples=[("Poprosze o tłumaczenie załaczonego Worda z polskiego na brytyjski, termin do konca przyszlego tygodnia", "do konca przyszlego tygodnia"),
                    ("Poprosze o tłumaczenie załaczonego Worda z bengalskiego na niemiecki, zlecenie ekspresowe, musimy opublikować przed 5 kwietnia", "przed 5 kwietnia"),
                    ("Poprosze o tłumaczenie załaczonego Worda z bengalskiego na niemiecki, termin 21 stycznia", "21 stycznia"),
                    ("Poprosze o tłumaczenie załaczonego Worda z bengalskiego na niemiecki, zlecenie ekspresowe, musimy opublikować przed 5 kwietnia", "przed 5 kwietnia"),],
          many=True,
      ),
    ],
  many=False,
)

chain = create_extraction_chain(llm, schema, encoder_or_encoder_class='json')
output = chain.predict_and_parse(text="poprosze o tłumaczenie załaczonego Worda na brytyjski angielski i amerykanski angielski, termin do konca przyszlego tygodnia")['data']

printOutput(output)







