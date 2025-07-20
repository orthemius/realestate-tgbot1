import os
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SERVICE_ACCOUNT_FILE = 'google/service_account.json'
SCOPES = ['https://www.googleapis.com/auth/drive']
ROOT_FOLDER_ID = os.getenv("ROOT_FOLDER_ID")  # корневая папка проекта на Google Диске

def get_drive_service():
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return build('drive', 'v3', credentials=creds)

def find_or_create_folder(service, folder_name, parent_id=None):
    # Поиск папки
    query = f"name = '{folder_name}' and mimeType = 'application/vnd.google-apps.folder'"
    if parent_id:
        query += f" and '{parent_id}' in parents"
    results = service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
    items = results.get('files', [])
    if items:
        return items[0]['id']

    # Создание папки
    file_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [parent_id] if parent_id else []
    }
    file = service.files().create(body=file_metadata, fields='id').execute()
    return file.get('id')

def get_full_folder_path(service, client, obj, stage):
    client_folder = find_or_create_folder(service, client, ROOT_FOLDER_ID)
    object_folder = find_or_create_folder(service, obj, client_folder)
    stage_folder = find_or_create_folder(service, stage, object_folder)
    return stage_folder

def upload_file_to_drive(local_path: str, new_filename: str, folder_path: str) -> str:
    """
    Загружает файл в указанную папку (client/object/stage) на Google Диск.
    Возвращает ссылку на просмотр.
    """
    service = get_drive_service()
    client, obj, stage = folder_path.split("/")
    folder_id = get_full_folder_path(service, client, obj, stage)

    file_metadata = {
        'name': new_filename,
        'parents': [folder_id]
    }

    media = MediaFileUpload(local_path, resumable=True)
    uploaded_file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()

    # Дать доступ по ссылке (чтение)
    service.permissions().create(
        fileId=uploaded_file['id'],
        body={'role': 'reader', 'type': 'anyone'},
        fields='id'
    ).execute()

    return f"https://drive.google.com/file/d/{uploaded_file['id']}/view"

def list_files_in_folder_path(folder_path: str) -> list:
    """
    Возвращает список файлов в указанной папке (client/object/stage).
    Каждый файл: {'name': ..., 'link': ...}
    """
    service = get_drive_service()
    client, obj, stage = folder_path.split("/")
    folder_id = get_full_folder_path(service, client, obj, stage)

    query = f"'{folder_id}' in parents and trashed = false"
    results = service.files().list(q=query, fields="files(id, name)").execute()

    return [
        {
            "name": file["name"],
            "link": f"https://drive.google.com/file/d/{file['id']}/view"
        }
        for file in results.get("files", [])
    ]
