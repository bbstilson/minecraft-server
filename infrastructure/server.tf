data "doppler_secrets" "secrets" {
  project = "mineos-server"
  config = "prod"
}

resource "digitalocean_droplet" "mineos_server" {
  image = "docker-20-04"
  name = "mineos-server"
  region = "sfo2"
  size = "s-2vcpu-2gb"
  monitoring = true
  ssh_keys = [ data.doppler_secrets.secrets.map.DIGITAL_OCEAN_SSH_KEY_ID ]
  user_data = file("userdata.sh")
}
