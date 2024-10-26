from invoke import task

BACKUP_DEST = "/media/ccaroon/KrakenBackup/kraken"


@task
def status(ctx):
    """ Status of a Duplicity Backup Collection """
    ctx.run(f"duplicity collection-status file://{BACKUP_DEST}")
