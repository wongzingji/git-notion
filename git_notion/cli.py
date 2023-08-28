"""Console script for git_notion."""
import sys
import click
import git_notion


@click.command()
@click.option('--dir', default=".", help='The directory of the wiki folder you want to sync')
def main(dir):
    """Console script for git_notion."""
    click.echo("running sync")
    git_notion.sync_to_notion(dir)
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
