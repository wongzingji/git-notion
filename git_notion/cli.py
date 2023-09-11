"""Console script for git_notion."""
import sys
import click
import git_notion


@click.command()
@click.option('--dir', default=".", help='The directory of the wiki folder you want to sync')
@click.option(
    '--append', is_flag=True, show_default=True, default=False, 
    help="Whether to append the content to to the page with the same name if it exists or to overwrite it"
    "Default to overwrite it"
)
def main(dir, append):
    """Console script for git_notion."""
    click.echo("running sync")
    git_notion.sync_to_notion(dir, append)
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
