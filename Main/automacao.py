import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from pprint import pprint

# qual o tipo de acesso que queremos
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# Informações da planilha
id_planilha = "1X1OZgLJGHxK_j3zsplVmg1k56P0jyDB1rhP_YE0BFPM"
aba_trabalho = "Fluxo de Edição - Trabalhos!A:Q"
aba_certificado = "Mala Direta Certificados!A:N"

def conectar_google_sheets():
    # Fazer a autenticação/logiin
  creds = None
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  return creds

def ler_dados(creds):
  try:
    service = build("sheets", "v4", credentials=creds)
    sheet = service.spreadsheets()

    # Ler informações do google sheets
    resultado = (
        sheet.values()
        .get(spreadsheetId=id_planilha, range=aba_trabalho)
        .execute()
    )

    valores = resultado["values"];

    # exibir as informações
    for linhas in valores:
      print(linhas)

  except HttpError as err:
    print(err)

def escrever_dados(creds):
  try:
    service = build("sheets", "v4", credentials=creds)
    sheet = service.spreadsheets()

    # Escrever informações no google sheets
    valores = [
      ["11", "teste1"], 
      ["12", "teste2"]
      ]
    
    resultado = (
        sheet.values()
        .update(
            spreadsheetId=id_planilha,
            range=aba_certificado,
            valueInputOption="RAW",
            body={"values": valores},
        )
        .execute()
    )

  except HttpError as err:
    print(err)


def main():
  credencial = conectar_google_sheets()

  # Ler dados
  ler_dados(credencial)

  # Escrever dados
  # escrever_dados(creds)

if __name__ == "__main__":
  main()