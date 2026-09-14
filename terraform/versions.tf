terraform {
  required_version = ">= 1.5"

  required_providers {
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "~> 2.0"
    }
  }
}

# No `token` argument on purpose: the provider reads DIGITALOCEAN_TOKEN from
# the environment. Never put the token in a .tf or .tfvars file.
provider "digitalocean" {}
