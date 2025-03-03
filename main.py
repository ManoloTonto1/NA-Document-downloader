import click
import os
import requests
from lxml import etree as ET
from lxml import html


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


# This function will return a list of all the href's of the dossiers in the archive block
# This list can then be used to fetch the dossiers
def getAllDossierHrefs(archiveBlockXml: str | None) -> list[str] | None:
    if archiveBlockXml is None:
        return None
    tree = ET.fromstring(archiveBlockXml)
    elementsWithHref = tree.xpath("//c[@level='file']/did/dao[@href]")
    hrefs = []
    for element in elementsWithHref:
        href = element.get("href")
        hrefs.append(href)
    return hrefs


def getAllFileHrefs(dossierXml: str | None, verbose: bool) -> list[str] | None:
    tree = ET.fromstring(dossierXml)

    namespaces = {"xlink": "http://www.w3.org/1999/xlink"}
    elements = tree.xpath("//*[@xlink:href]", namespaces=namespaces)
    hrefs = []
    for element in elements:
        href = element.get("{http://www.w3.org/1999/xlink}href")
        hrefs.append(href)
    if verbose:
        click.echo(f"Found files: {hrefs}")
    return hrefs


def extractLink(htmlStr: str):
    tree = html.fromstring(htmlStr)
    # Use XPath to extract the value of DEFAULT_URL from the <script> tag
    default_url = tree.xpath("string(//script[contains(text(), 'DEFAULT_URL')])")
    import re

    url_match = re.search(r"var DEFAULT_URL = '(https?://[^']+)';", default_url)
    if url_match:
        return url_match.group(1)


def saveFile(
    content: bytes, fileUrl: str, dossierUUID: str, directory: str, extension: str
):
    fileUUID = fileUrl.split("/")[-1].split("?")[0]
    with open(f"{directory}/{dossierUUID}_{fileUUID}.{extension}", "wb") as file:
        file.write(content)


def downloadFile(fileUrl: str, dossierUUID: str, directory: str):
    try:

        response = requests.get(fileUrl)
        response.raise_for_status()
        content = response.content
        # get mimetype and the file extension
        mimetype = response.headers["Content-Type"]
        extension = mimetype.split("/")[1]
        if mimetype == "application/octet-stream":
            return
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


@click.command()
@click.option(
    "--set",
    "set",
    required=True,
    help="The set number to fetch data from, this can be gotten from the Archive block page. it should look something like '2.19.185'",
)
@click.option(
    "--directory",
    "directory",
    required=True,
    help="Directory relative to where the CLI is run, here all the files will be saved",
)
@click.option(
    "--limit",
    "limit",
    required=False,
    help="Limit the amount of dossier's to fetch",
    default=0,
)
@click.option(
    "--verbose",
    "verbose",
    required=False,
    help="Print verbose output",
    default=False,
)
def start(set, directory, limit, verbose):
    """CLI that makes a call to the set number and saves files to the specified directory."""
    # Get the absolute path of the directory relative to where the CLI is run
    abs_directory = os.path.abspath(directory)

    click.echo(f"Set version: {set}")
    click.echo(f"Directory: {abs_directory}")

    if not os.path.exists(abs_directory):
        click.echo("Directory does not exist, creating...")
        os.makedirs(abs_directory)
    block = fetchArchiveBlock(set=set)
    if block is None:
        click.echo("Failed to fetch archive block", err=True)
        return
    dossiers = getAllDossierHrefs(block)
    if dossiers is None:
        click.echo("Failed to get dossiers", err=True)
        return
    if limit > 0:
        dossiers = dossiers[:limit]

    for dossier in dossiers:

        dossierXml = fetchDossier(dossier)
        if dossierXml is None:
            click.echo("Failed to fetch dossier", err=True)
        files = getAllFileHrefs(dossierXml, verbose=verbose)
        if files is None:
            click.echo("Failed to get files", err=True)
            continue
        for file in files:
            downloadFile(
                directory=directory, fileUrl=file, dossierUUID=dossier.split("/")[-1]
            )
            if verbose:
                click.echo(f"Downloaded file: {file}")
    click.echo("Finished downloading all files")


if __name__ == "__main__":
    start()
