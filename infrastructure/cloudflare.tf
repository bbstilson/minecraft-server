data "cloudflare_zone" "brandonstilson" {
  name = "brandonstilson.com"
}

resource "cloudflare_record" "minecraft" {
  zone_id = data.cloudflare_zone.brandonstilson.id
  name    = "minecraft"
  value   = digitalocean_droplet.mineos.ipv4_address
  type    = "A"
  ttl     = 1 # automatic
  proxied = false
}
