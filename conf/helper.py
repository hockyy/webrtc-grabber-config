#!/usr/bin/env python3

import json
import subprocess


def get_host_ip():
    """Get the first IP from `hostname -I`."""
    result = subprocess.run(["hostname", "-I"], capture_output=True, text=True, check=True)
    ip = result.stdout.strip().split()[0]
    return ip


def load_config(config_path="config.json"):
    """Load config.json and return the parsed dict."""
    with open(config_path, "r") as f:
        return json.load(f)


def load_turn_users(config):
    """Extract all username=credential pairs from iceServers."""
    users = []
    ice_servers = config["peerConnectionConfig"]["iceServers"]
    for server in ice_servers:
        username = server.get("username")
        credential = server.get("credential")
        if username and credential:
            users.append(f"{username}={credential}")
    return users


def generate_cmd():
    ip = get_host_ip()
    config = load_config()
    users = load_turn_users(config)

    # Extract port from the first iceServer URL (e.g. "turn:10.x.x.x:3478")
    turn_url = config["peerConnectionConfig"]["iceServers"][0]["urls"]
    port = turn_url.rsplit(":", 1)[-1]

    # Admin credential from config
    admin_credential = config.get("adminCredential", "")

    parts = [
        "go run main.go",
        f"--public-ip={ip}",
        f"--port {port}",
    ]
    for user in users:
        parts.append(f"--users {user}")

    cmd = " ".join(parts)
    return cmd, admin_credential


def main():
    cmd, admin_credential = generate_cmd()
    print("Generated command:\n")
    print(cmd)
    print(f"\nAdmin credential: {admin_credential}")


if __name__ == "__main__":
    main()