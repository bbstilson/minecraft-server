import os
from datetime import datetime
import time

import click
import digitalocean


UP = "up"
DOWN = "down"
CHOICES = [UP, DOWN]
SERVER_NAME = "mineos"


token = os.environ["DIGITALOCEAN_TOKEN"]
client = digitalocean.Manager(token=token)


@click.command()
@click.argument("direction", type=click.Choice(CHOICES), required=True)
def cli(direction: str):
    do_up() if direction == UP else do_down()
    print("Done!")


def do_up():
    snapshot = [
        snapshot
        for snapshot in client.get_droplet_snapshots()
        if snapshot.name.startswith(SERVER_NAME)
    ][0]
    print(f"Creating droplet from snapshot: {snapshot}")
    droplet = digitalocean.Droplet(
        token=token,
        name=SERVER_NAME,
        region="sfo2",
        image=snapshot.id,
        size_slug="s-4vcpu-8gb",
        tags=[SERVER_NAME],
        ssh_keys=[27681515],
        backups=False,
        monitoring=True,
    )
    droplet.create()

    actions = droplet.get_actions()
    droplet_ready = False
    while not droplet_ready:
        for action in actions:
            print(action)
            action.load()
            print(action)
            # Once it shows "completed", droplet is up and running
            print(action.status)
            droplet_ready = action.status == "completed"
        time.sleep(2)

    # patch cloudflare record
    # programmatically start the server???
    pass


def do_down():
    now = datetime.now().strftime("%m-%d-%Y")
    snapshot_name = f"{SERVER_NAME}-{now}"

    # Cache old snapshots.
    old_snapshots = [
        snapshot
        for snapshot in client.get_droplet_snapshots()
        if snapshot.name.startswith(SERVER_NAME)
    ]

    droplet = client.get_all_droplets(tag_name=SERVER_NAME)[0]

    print(
        f"Stopping droplet ({droplet.name}) and taking snapshot ({snapshot_name})."
    )

    droplet.take_snapshot(
        snapshot_name=snapshot_name, power_off=True, return_dict=False
    ).wait()

    print("Cleaning up old snapshots.")
    for snapshot in old_snapshots:
        input(f"    Destroying {snapshot}. Continue?")
        snapshot.destroy()

    input(f"Destroying droplet ({droplet.name}). Continue?")
    droplet.destroy()


if __name__ == "__main__":
    cli()
