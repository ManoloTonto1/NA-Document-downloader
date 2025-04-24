import click
import requests

from parser import extractLink


def saveFile(
    content: bytes, fileUrl: str, dossierUUID: str, directory: str, extension: str
):
    fileUUID = fileUrl.split("/")[-1].split("?")[0]
    with open(f"{directory}/{dossierUUID}_{fileUUID}.{extension}", "wb") as file:
        file.write(content)


def formatUrl(set):
    url = f"https://service.archief.nl/gaf/oai/!open_oai.OAIHandler?verb=ListRecords&set={set}&metadataPrefix=oai_ead"
    return url


def fetchArchiveBlock(set: str) -> str | None:
    url = formatUrl(set)  # Replace with actual URL
    click.echo(f"Fetching data from: {url}")
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        click.echo(f"Failed to fetch data: {e}", err=True)
        return None


#  This function will download the file from the given URL and save it to the specified directory
def downloadFile(fileUrl: str, dossierUUID: str, directory: str):
    try:

        response = requests.get(fileUrl)
        response.raise_for_status()
        content = response.content
        # get mimetype and the file extension
        mimetype = response.headers["Content-Type"]
        extension = mimetype.split("/")[1]
        if mimetype == "application/octet-stream":
            return None
        if mimetype == "text/html":
            linkUrl = extractLink(response.text)
            downloadFile(linkUrl, dossierUUID, directory)
            return
        saveFile(
            content=content,
            fileUrl=fileUrl,
            dossierUUID=dossierUUID,
            directory=directory,
            extension=extension,
        )

    except requests.exceptions.RequestException as e:
        click.echo(f"Failed to download file: {e}", err=True)


def fetchDossier(href: str | None):
    """
    Fetches the content of a dossier from the given URL.

    Args:
        href (str | None): The URL of the dossier to fetch. If None, the function returns None.

    Returns:
        bytes | None: The content of the dossier as bytes if the request is successful,
                      or None if the URL is None or the request fails.

    Logs:
        - Logs the UUID of the dossier being fetched.
        - Logs an error message if the request fails.

    Raises:
        None: All exceptions are handled internally and logged.
    """
    if href is None:
        return None
    click.echo(f"Fetching dossier with UUID: {href.split('/')[-1]}")
    try:
        response = requests.get(href)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        click.echo(f"Failed to fetch data: {e}", err=True)
        return None
