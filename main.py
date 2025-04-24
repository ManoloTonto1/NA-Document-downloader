import click
import os

from fetch import fetchArchiveBlock, fetchDossier, downloadFile
from parser import getAllDossierHrefs, getAllFileUrls, getDossierHrefByUnitID
from pdfgen import generatePdfFromImages
from fpdf import FPDF


# Get the absolute path of the directory relative to where the CLI is run
def createDirectory(directory: str):
    abs_directory = os.path.abspath(directory)

    click.echo(f"Set version: {set}")
    click.echo(f"Directory: {abs_directory}")

    if not os.path.exists(abs_directory):
        click.echo("Directory does not exist, creating...")
        os.makedirs(abs_directory)


def limitDossiers(dossiers: list[str], limit: int) -> list[str]:
    if limit > 0:
        return dossiers[:limit]


@click.command()
@click.option(
    "--set",
    "set",
    required=True,
    help="The set number to fetch data from, this can be gotten from the Archive block page. it should look something like '2.19.185'",
)
@click.option(
    "--dossier",
    "dossier",
    required=False,
    help="the inventarisnummer of the dossier, this is used to fetch the dossier directly",
    default=None,
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
def start(
    set: str | None, directory: str, limit: int, verbose: bool, dossier: str | None
):
    if dossier is not None and limit > 0:
        click.echo("You can only use one of --dossier or --limit", err=True)
        return

    createDirectory(directory)
    """CLI that makes a call to the set number and saves files to the specified directory."""

    block = fetchArchiveBlock(set=set)
    if block is None:
        click.echo("Failed to fetch archive block", err=True)
        return
    dossiers: list[str] = []
    if dossier is None:
        click.echo(f"Fetching the first {limit} dossiers...")
        dossiers = getAllDossierHrefs(block)
        if dossiers is None:
            click.echo("Failed to get dossiers", err=True)
            exit(1)
        dossiers = limitDossiers(dossiers, limit)
    else:
        click.echo(f"Fetching dossier with unit ID {dossier}")
        dossiers = getDossierHrefByUnitID(block, dossier)
        if dossiers is None:
            click.echo("Failed to get dossiers", err=True)
            exit(1)
    if verbose:
        click.echo(f"Found {len(dossiers)} dossiers")
        click.echo(f"dossiers: {dossiers}")

    if len(dossiers) == 0:
        click.echo("No dossiers found", err=True)
        exit(1)
    for dossier in dossiers:
        dossierUUID = dossier.split("/")[-1]
        dossierXml = fetchDossier(dossier)
        if dossierXml is None:
            click.echo("Failed to fetch dossier", err=True)

        file = getAllFileUrls(dossierXml, verbose=verbose)

        if file is None:
            click.echo("Failed to get files", err=True)
            continue
        # split the fileURLS into two parts, the the first part of the array are the images (jpeg, png) and the second part are the rest
        imageFiles = [
            file
            for file in file
            if file.mimeType is not None and file.mimeType.startswith("image/")
        ]
        otherFiles = [
            file
            for file in file
            if file.mimeType is not None and not file.mimeType.startswith("image/")
        ]
        if verbose:
            click.echo(
                f"Found {len(imageFiles)} images and {len(otherFiles)} other files"
            )
        else:
            click.echo(f"Found {len(file)} files")

        if len(imageFiles) > 0:
            pdf: FPDF = generatePdfFromImages(
                imageUrls=[image.url for image in imageFiles],
            )
            pdf.output(f"{directory}/{dossierUUID}.pdf", "F")
        for file in otherFiles:
            downloadFile(
                directory=directory,
                fileUrl=[image.url for image in imageFiles],
                dossierUUID=dossierUUID,
            )
            if verbose:
                click.echo(f"Downloaded file: {file}")
    click.echo("Finished downloading all files")


if __name__ == "__main__":
    start()
