# Infrastructure

Terraform is used to manage the infrastructure. If you don't have that, you'll need to [install it](https://learn.hashicorp.com/tutorials/terraform/install-cli).

You'll need the following environment variables in your shell to run the Terraform plans:

- `DIGITALOCEAN_TOKEN` - Personal access token.
- `DOPPLER_TOKEN` - Personal access token.

To preview changes, run:

```bash
terraform plan \
  -var digitalocean_token=$DIGITALOCEAN_TOKEN \
  -var doppler_token=$DOPPLER_TOKEN
```

To apply changes, run:

```bash
terraform apply \
  -var digitalocean_token=$DIGITALOCEAN_TOKEN \
  -var doppler_token=$DOPPLER_TOKEN
```

## Debugging

SSH is available using the `digital_ocean` key.

```bash
ssh -i ~/.ssh/digital_ocean root@<ip-address>
```
