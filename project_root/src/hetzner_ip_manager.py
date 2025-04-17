
import os
import requests
from src.accounts_config import AccountStateManager


class HetznerIPManager:
    def __init__(self):
        self.api_token = os.getenv("HETZNER_API_TOKEN")
        self.base_url = "https://api.hetzner.cloud/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }
        self.state_manager = AccountStateManager()

    def create_floating_ip_if_needed(self, account_id: int) -> str:
        """
        If the specified account's Floating IP has not been created yet,
        create a new one via API and record the ID in account_state.json.
        If already created, do nothing and return that ID.
        """
        fip_id = self.state_manager.get_floating_ip_id(account_id)
        if fip_id:
            print(f"[HetznerIPManager] Account {account_id} already has Floating IP ID={fip_id}")
            return fip_id

        home_location = os.getenv(f"HETZNER_HOME_LOCATION_{account_id}")
        if not home_location:
            raise ValueError(f"HETZNER_HOME_LOCATION_{account_id} not set in .env")

        payload = {
            "type": "ipv4",
            "home_location": home_location,
            "description": f"Auto-FIP-Account{account_id}"
        }
        try:
            resp = requests.post(f"{self.base_url}/floating_ips", headers=self.headers, json=payload)
            resp.raise_for_status()
            data = resp.json()
            new_fip_id = data["floating_ip"]["id"]

            self.state_manager.set_floating_ip_id(account_id, new_fip_id)

            print(f"[HetznerIPManager] Created new Floating IP ID={new_fip_id} for account {account_id}")
            return new_fip_id

        except Exception as e:
            print(f"[HetznerIPManager] Failed to create Floating IP: {e}")
            return None

    def get_ip_for_account(self, account_id: int) -> str:
        """
        Get the Floating IP ID stored in account_state.json,
        and return the actual IP address (string) for that ID.
        """
        fip_id = self.state_manager.get_floating_ip_id(account_id)
        if not fip_id:
            raise ValueError(f"No Floating IP found for account {account_id} - create it first!")

        url = f"{self.base_url}/floating_ips/{fip_id}"
        try:
            resp = requests.get(url, headers=self.headers)
            resp.raise_for_status()
            data = resp.json()
            ip_address = data["floating_ip"]["ip"]
            return ip_address
        except Exception as e:
            print(f"[HetznerIPManager] Failed to get IP address for Floating IP ID={fip_id}: {e}")
            return None

    def assign_floating_ip(self, account_id: int, server_id: int):
        """
        POST /floating_ips/{id}/actions/assign to attach to a specific server
        """
        fip_id = self.state_manager.get_floating_ip_id(account_id)
        if not fip_id:
            raise ValueError(f"No Floating IP for account {account_id}")

        url = f"{self.base_url}/floating_ips/{fip_id}/actions/assign"
        payload = {"server": server_id}
        try:
            resp = requests.post(url, headers=self.headers, json=payload)
            resp.raise_for_status()
            print(f"[HetznerIPManager] Assigned Floating IP {fip_id} -> server {server_id}")
        except Exception as e:
            print(f"[HetznerIPManager] Failed to assign Floating IP: {e}")

    def unassign_floating_ip(self, account_id: int):
        """
        POST /floating_ips/{id}/actions/unassign to detach from server
        """
        fip_id = self.state_manager.get_floating_ip_id(account_id)
        if not fip_id:
            raise ValueError(f"No Floating IP for account {account_id}")

        url = f"{self.base_url}/floating_ips/{fip_id}/actions/unassign"
        try:
            resp = requests.post(url, headers=self.headers)
            resp.raise_for_status()
            print(f"[HetznerIPManager] Unassigned Floating IP {fip_id}")
        except Exception as e:
            print(f"[HetznerIPManager] Failed to unassign Floating IP: {e}")

    def delete_floating_ip(self, account_id: int):
        """
        DELETE /floating_ips/{id} to delete the Floating IP resource itself
        (expected to be called manually when no longer needed)
        """
        fip_id = self.state_manager.get_floating_ip_id(account_id)
        if not fip_id:
            print(f"No Floating IP to delete for account {account_id}")
            return

        url = f"{self.base_url}/floating_ips/{fip_id}"
        try:
            resp = requests.delete(url, headers=self.headers)
            resp.raise_for_status()
            print(f"[HetznerIPManager] Deleted Floating IP {fip_id}")
            self.state_manager.set_floating_ip_id(account_id, None)  # Remove from account_state.json
        except Exception as e:
            print(f"[HetznerIPManager] Failed to delete Floating IP: {e}")
