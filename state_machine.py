    def handle_action(self, action: str):
        # ... existing actions ...

        elif action.startswith("equip_accessory:"):
            acc_name = action.split(":", 1)[1]
            self.pet.equip_accessory(acc_name)
            self.display.show_notification(f"{self.pet.name} puts on the {acc_name.lower()} ✨")
