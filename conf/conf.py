#!/usr/bin/env python3

import json
import subprocess


def get_host_ip():
    """Get the first IP from `hostname -I`."""
    result = subprocess.run(["hostname", "-I"], capture_output=True, text=True, check=True)
    ip = result.stdout.strip().split()[0]
    return ip


def generate_team_names():
    """Generate team names for i=1..30 where i % 3 == 1 or i % 3 == 0."""
    teams = []
    for i in range(1, 31):
        if i % 3 == 1 or i % 3 == 0:
            teams.append(f"team-{i:03d}")
    return teams


def main():
    ip = get_host_ip()
    teams = generate_team_names()

    config = {
        "participants": teams,
        "adminsNetworks": ["127.0.0.1/32", "10.0.0.0/8", "192.168.0.0/16"],
        "adminCredential": "your-secure-password",
        "peerConnectionConfig": {
            "iceServers": [
                {
                    "urls": f"turn:{ip}:3478",
                    "username": "admin",
                    "credential": "credential",
                }
            ]
        },
        "grabberPingInterval": 5,
        "serverPort": 13478,
        "serverTLSCrtFile": None,
        "serverTLSKeyFile": None,
        "codecs": [
            {
                "type": "video",
                "params": {
                    "mimeType": "video/VP8",
                    "clockRate": 90000,
                    "payloadType": 96,
                    "channels": 0,
                },
            },
            {
                "type": "audio",
                "params": {
                    "mimeType": "audio/opus",
                    "clockRate": 48000,
                    "payloadType": 111,
                    "channels": 2,
                },
            },
        ],
        "webcamTrackCount": 2,
    }

    with open("config.json", "w") as f:
        json.dump(config, f, indent=2)

    print(f"Resolved IP: {ip}")
    print(f"Generated {len(teams)} teams: {teams}")
    print("config.json written successfully.")


if __name__ == "__main__":
    main()

