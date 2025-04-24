import click
from lxml import etree as ET
from lxml import html


class File:
    def __init__(
        self,
        url: str,
        mimeType: str,
    ):
        self.mimeType = mimeType
        self.url = url


def getAllDossierHrefs(archiveBlockXml: str | None) -> list[str] | None:
    """This function will return a list of all the href's of the dossiers in the archive block
    This list can then be used to fetch the dossiers
    """
    if archiveBlockXml is None:
        return None
    tree = ET.fromstring(archiveBlockXml)
    elementsWithHref = tree.xpath("//c[@level='file']/did/dao[@href]")
    hrefs = []
    for element in elementsWithHref:
        href = element.get("href")
        hrefs.append(href)
    return hrefs


def getDossierHrefByUnitID(archiveBlockXml: str | None, unitID: str | None):
    if archiveBlockXml is None:
        return None
    tree = ET.fromstring(archiveBlockXml)
    elementsWithHref = tree.xpath(f"//unitid[text()='{unitID}']/parent::did/dao[@href]")
    hrefs = []
    for element in elementsWithHref:
        href = element.get("href")
        hrefs.append(href)
    return hrefs


def getAllFileUrls(dossierXml: str | None, verbose: bool) -> list[File] | None:
    tree = ET.fromstring(dossierXml)

    namespaces = {"xlink": "http://www.w3.org/1999/xlink"}
    elements = tree.xpath("//*[@xlink:href]", namespaces=namespaces)

    files: list[File] = []
    for element in elements:
        href = element.get("{http://www.w3.org/1999/xlink}href")
        parent = element.getparent()
        mimetype = parent.get("MIMETYPE") if parent is not None else None
        files.append(File(href, mimetype))

    if verbose:
        click.echo(f"Found files: {len(files)}")
    return files


def extractLink(htmlStr: str):
    tree = html.fromstring(htmlStr)
    # Use XPath to extract the value of DEFAULT_URL from the <script> tag
    default_url = tree.xpath("string(//script[contains(text(), 'DEFAULT_URL')])")
    import re

    url_match = re.search(r"var DEFAULT_URL = '(https?://[^']+)';", default_url)
    if url_match:
        return url_match.group(1)
