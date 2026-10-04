<!-- template: hosting.md v1 -->
<!-- docs/hosting.md: the contract between the product and the user's host. Every value here is a fact the code and the compose file must match. -->
# Hosting

## Hosts

| Host | Requirements | How it runs |
|---|---|---|
| macOS | <version, chip, memory, disk> | <the app runs the image> |
| Linux | <architectures, container runtime and version, memory, disk> | <compose file> |

## Network

<Ports the image listens on, what binds to localhost and what may be exposed on the LAN, outbound connections the
product makes and why, how the web UI is authenticated.>

## Data

<The data directory: where it is on each host, what it contains, what must be backed up, how to restore, how to
erase everything.>

## Configuration

<Every setting a host can change (environment variables, compose options), with its default; or None.>

## Resources

<Memory, CPU and disk budgets at idle and under load, and what the product does when it reaches a limit.>

## Upgrades

<How each host upgrades, how data migrates forward, that downgrades are not supported, what happens to a data
directory written by a newer version.>

## Uninstall

<How to remove the product and its data from each host.>
