resource "digitalocean_ssh_key" "deploy" {
  name       = "snippet-vault-deploy"
  public_key = file(pathexpand(var.ssh_public_key_path))
}

resource "digitalocean_droplet" "vault" {
  name     = "snippet-vault"
  region   = "fra1"
  size     = "s-1vcpu-2gb"
  image    = "ubuntu-24-04-x64"
  ssh_keys = [digitalocean_ssh_key.deploy.fingerprint]
}

# Inbound: SSH, HTTP and HTTPS only. Outbound: everything.
resource "digitalocean_firewall" "vault" {
  name        = "snippet-vault"
  droplet_ids = [digitalocean_droplet.vault.id]

  dynamic "inbound_rule" {
    for_each = ["22", "80", "443"]
    content {
      protocol         = "tcp"
      port_range       = inbound_rule.value
      source_addresses = ["0.0.0.0/0", "::/0"]
    }
  }

  outbound_rule {
    protocol              = "tcp"
    port_range            = "1-65535"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }

  outbound_rule {
    protocol              = "udp"
    port_range            = "1-65535"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }

  outbound_rule {
    protocol              = "icmp"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }
}
