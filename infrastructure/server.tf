data "doppler_secrets" "mineos" {
  project = "mineos-server"
  config = "prod"
}
data "doppler_secrets" "development" {
  project = "development"
  config = "all"
}

resource "digitalocean_droplet" "mineos" {
  image = "docker-20-04"
  name = "mineos"
  region = "sfo2"
  size = "s-4vcpu-8gb"
  monitoring = true
  ssh_keys = [ data.doppler_secrets.development.map.DIGITAL_OCEAN_SSH_KEY_ID ]
  user_data = templatefile("userdata.tpl", {
    MINEOS_UN = data.doppler_secrets.mineos.map.MINEOS_UN,
    MINEOS_PW = data.doppler_secrets.mineos.map.MINEOS_PW
  })
}
