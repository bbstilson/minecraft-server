resource "digitalocean_firewall" "mineos" {
  name = "only-22-80-443"

  droplet_ids = [digitalocean_droplet.mineos.id]

  ###################
  ## INBOUND RULES ##
  ###################

  # SSH
  inbound_rule {
    protocol         = "tcp"
    port_range       = 22
    source_addresses = ["0.0.0.0/0", "::/0"]
  }

  # HTTPS
  inbound_rule {
    protocol = "tcp"
    port_range = 443
    source_addresses = ["0.0.0.0/0", "::/0"]
  }

  # HTTP
  inbound_rule {
    protocol = "tcp"
    port_range = 80
    source_addresses = ["0.0.0.0/0", "::/0"]
  }

  # HTTPS port for MineOS web interface is 8443 by default, but we
  # remap it in the userdata.tpl via Docker's port exposure.
  #
  # Minecraft server ports. 25565 is the default, but is you plan
  # on running multiple servers at the same time, each will need
  # a unique port unless you are using bungiecord.
  inbound_rule {
    protocol = "tcp"
    port_range = 25565
    source_addresses = ["0.0.0.0/0", "::/0"]
  }

  ####################
  ## OUTBOUND RULES ##
  ####################

  # HTTPS
  outbound_rule {
    protocol = "tcp"
    port_range = 443
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }

  outbound_rule {
    protocol = "tcp"
    port_range = 53
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }

  outbound_rule {
    protocol = "udp"
    port_range = 53
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }
}
