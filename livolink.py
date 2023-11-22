import requests
import json
import os
from dotenv import load_dotenv

def configure():
    load_dotenv()

configure()

def inquiry(text):
  url = "https://test-api.livocloud.com/api/v1/auth/identities/login"

  payload = json.dumps({

    "meta": {

      "dataType": "AuthLogin"

    },

    "data": [

      {

        "type": "AuthLogin",

        "attributes": {

          "Login": os.getenv('login'),

          "Password": os.getenv('livopassword'),

          "Organization": "QA"

        }

      }

    ]

  })

  headers = {

    'Content-Type': 'application/json'

  }

  # 1. - logujemy się, pobieramy id organizacji oraz token dostępowy

  response = requests.request("POST", url, headers=headers, data=payload)

  resource = json.loads(response.text)

  loginResponseDto = resource['data'][0]['attributes']

  accessToken = loginResponseDto['AccessToken']

  organizationId = loginResponseDto['OrganizationInfos'][0]['id']

  # 2. - uzywając tokenu dostępowego tworzymy w organizacji QA dla klienta "Livo klient" zapytanie w imieniu jej pracownika ""

#def inquiry(text):

  url = "https://test-api.livocloud.com/api/v1/{organizationId}/inquiries".format(organizationId=organizationId)

  payload=json.dumps({

    "data": [

      {

        "type": "Inquiry",

        "attributes": {

          "CustomerRef": {

            "id": "d4c73999-fefc-4a16-8f61-4d1e3f7d4e3a"

          },

          "SubmitPersonRef": {

            "id": "bdc44010-3b46-4cab-9eb4-c8b8d722b74e"

          }

        }

      }

    ]

  })

  headers = {

    'Content-Type': 'application/json',

    'Authorization': 'Bearer ' + accessToken

  }

  response = requests.request("POST", url, headers=headers, data=payload)

  resource=json.loads(response.text)

  # 3. - w poprzedniej odpowiedzi mamy numer utworzonego zaptania, teraz poleceniem PATCH zaktualizujemy to zapytanie dodajac jakis tekst jako pole komentarza

  inquiryId = resource['data'][0]['id']

  url = f"https://test-api.livocloud.com/api/v1/75e2b6c7-8ea1-863c-e053-0c00f40ac702/inquiries/{inquiryId}"

  payload=json.dumps({

    "data": [

          {

              "id": inquiryId,

              "type": "Inquiry",

              "attributes": {

                  "InquiryRemarks": text ,

                  "Remarks": text

              }

          }

      ]

  })

  headers = {

    'Content-Type': 'application/json',

    'Authorization': 'Bearer ' + accessToken

  }

  response = requests.request("PATCH", url, headers=headers, data=payload)

  print(response.text)


def sendFile(file):
  url = "https://test-api.livocloud.com/api/v1/auth/identities/login"

  payload = json.dumps({

    "meta": {

      "dataType": "AuthLogin"

    },

    "data": [

      {

        "type": "AuthLogin",

        "attributes": {

          "Login": os.getenv('login'),

          "Password": os.getenv('livopassword'),

          "Organization": "QA"

        }

      }

    ]

  })

  headers = {

    'Content-Type': 'application/json'

  }

  # 1. - logujemy się, pobieramy id organizacji oraz token dostępowy

  response = requests.request("POST", url, headers=headers, data=payload)

  resource = json.loads(response.text)

  loginResponseDto = resource['data'][0]['attributes']

  accessToken = loginResponseDto['AccessToken']

  organizationId = loginResponseDto['OrganizationInfos'][0]['id']

  # 2. - uzywając tokenu dostępowego tworzymy w organizacji QA dla klienta "Livo klient" zapytanie w imieniu jej pracownika ""

  url = "https://test-api.livocloud.com/api/v1/{organizationId}/inquiries/82be25b0-6597-4da6-a898-17e2cea29d37/files?ContextFilterNames=TranslateFiles".format(organizationId=organizationId)
  
  payload=json.dumps({

    "data": [

          {

              "id": inquiryId,

              "type": "InquiryItemFile",

              "attributes": {

                  "Object": file

              }

          }

      ]

  })

  headers = {

    'Content-Type': 'application/json',

    'Authorization': 'Bearer ' + accessToken

  }

  response = requests.request("POST", url, headers=headers, data=payload)

  resource=json.loads(response.text)
