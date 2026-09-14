output "droplet_ipv4" {
  description = "Public IPv4 address of the snippet-vault droplet."
  value       = digitalocean_droplet.vault.ipv4_address
}
