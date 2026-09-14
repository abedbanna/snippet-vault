variable "ssh_public_key_path" {
  description = "Path to the SSH public key that gets root access to the droplet."
  type        = string
  default     = "~/.ssh/id_ed25519.pub"
}
