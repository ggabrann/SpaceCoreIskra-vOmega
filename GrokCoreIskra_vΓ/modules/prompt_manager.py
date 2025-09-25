class PromptManager:
    def __init__(self):
        self.prompts = {}

    def add_prompt(self, name, text):
        self.prompts[name] = text

    def get_prompt(self, name, metrics):
        prompt = self.prompts.get(name, "")
        metrics = metrics or {}

        delta = metrics.get("∆")
        d_value = metrics.get("D")

        if delta is None:
            delta = "N/A"

        if d_value is None:
            d_value = "N/A"

        return f"{prompt} [Metrics: ∆={delta}, D={d_value}]"
