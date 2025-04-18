
import os
import json


class AccountStateManager:
    def __init__(self, state_file="account_state.json"):
        self.state_file = state_file
        self.state = {}
        self._load_state()

    def _load_state(self):
        if os.path.exists(self.state_file):
            with open(self.state_file, "r", encoding="utf-8") as f:
                self.state = json.load(f)
        else:
            self.state = {}

    def _save_state(self):
        with open(self.state_file, "w", encoding="utf-8") as f:
            json.dump(self.state, f, ensure_ascii=False, indent=2)

    def get_part_number(self, account_index: int) -> int:
        key = f"account_{account_index}"
        return self.state.get(key, {}).get("part_number", 1)

    def increment_part_number(self, account_index: int):
        key = f"account_{account_index}"
        current = self.get_part_number(account_index)
        new_val = current + 1
        if key not in self.state:
            self.state[key] = {}
        self.state[key]["part_number"] = new_val
        self._save_state()

    def get_floating_ip_id(self, account_index: int) -> str:
        key = f"account_{account_index}"
        return self.state.get(key, {}).get("floating_ip_id", None)

    def set_floating_ip_id(self, account_index: int, fip_id: str):
        key = f"account_{account_index}"
        if key not in self.state:
            self.state[key] = {}
        self.state[key]["floating_ip_id"] = fip_id
        self._save_state()
