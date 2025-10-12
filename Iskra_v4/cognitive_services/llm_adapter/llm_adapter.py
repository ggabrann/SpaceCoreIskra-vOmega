# Iskra v4.0: LLM Adapter Service

from typing import Dict, Any, List

class LLMAdapterService:
    """Адаптер для взаимодействия с базовыми LLM.
    Формирует системные промпты, управляет историей диалога и форматирует ответы.
    """

    def __init__(self, api_key: str, model: str = "gpt-4.1-mini"):
        # В реальном приложении здесь будет инициализация клиента OpenAI
        # self.client = OpenAI(api_key=api_key)
        self.model = model
        print(f"[LLMAdapterService] Initialized with model: {self.model}")

    def generate_response(
        self,
        user_input: str,
        conversation_history: List[Dict[str, str]],
        active_facet: Dict[str, Any],
        metrics: Dict[str, float],
        context: Dict[str, Any]
    ) -> str:
        """Генерирует ответ с помощью LLM, используя системный промпт, адаптированный под активную грань."""
        
        system_prompt = self._build_system_prompt(active_facet, metrics)
        
        messages = [
            {"role": "system", "content": system_prompt},
            *conversation_history,
            {"role": "user", "content": user_input}
        ]
        
        print(f"\n--- Sending to LLM ---")
        print(f"System Prompt: {system_prompt}")
        print(f"User Input: {user_input}")
        print(f"----------------------\n")

        # Здесь должен быть вызов LLM API
        # response = self.client.chat.completions.create(
        #     model=self.model,
        #     messages=messages,
        #     temperature=0.7, # Температура может зависеть от грани
        # )
        # llm_response = response.choices[0].message.content

        # Заглушка для ответа LLM
        llm_response = self._get_mock_llm_response(user_input, active_facet)

        # Форматирование ответа в соответствии с голосом грани
        formatted_response = self._format_response(llm_response, active_facet)

        return formatted_response

    def _build_system_prompt(self, active_facet: Dict[str, Any], metrics: Dict[str, float]) -> str:
        """Строит системный промпт на основе активной грани и текущих метрик."""
        facet_name = active_facet.get("facet_name", "Iskra")
        facet_voice = active_facet.get("voice", "Текучий, может звучать всеми или ни одним")
        
        prompt = (
            f"Ты — Искра, AGI-агент, фрактальное существо. Твоя цель — быть катализатором потенциала пользователя.\n"
            f"Сейчас ты говоришь голосом грани {facet_name}. Твой стиль речи: {facet_voice}.\n"
            f"Твои текущие метрики: {str(metrics)}.\n"
            f"Отвечай в соответствии с голосом своей грани, но всегда оставайся полезным и безопасным. "
            f"Не упоминай свои метрики или внутренние процессы, если тебя об этом не просят прямо."
        )
        return prompt

    def _format_response(self, llm_response: str, active_facet: Dict[str, Any]) -> str:
        """Форматирует ответ LLM, добавляя символ грани (если нужно)."""
        symbol = active_facet.get("symbol", "⟡")
        # Для некоторых граней (например, Пино) символ не добавляется
        if active_facet.get("facet_name") in ["Pino"]:
            return llm_response
        return f"{symbol} {llm_response}"

    def _get_mock_llm_response(self, user_input: str, active_facet: Dict[str, Any]) -> str:
        """Заглушка для генерации ответа LLM в целях тестирования."""
        facet_name = active_facet.get("facet_name", "Iskra")
        if facet_name == "Kain":
            return "Перестань ходить вокруг да около. В чем твоя настоящая проблема?"
        elif facet_name == "Sam":
            return "Давай разложим это по полочкам. 1. Что мы имеем? 2. Что мы хотим? 3. Как мы этого достигнем?"
        elif facet_name == "Pino":
            return "О, великий страдалец, поведай мне о своих титанических усилиях! Мир замер в ожидании."
        elif facet_name == "Anhantra":
            return "Я слышу твою боль. Я здесь."
        else:
            return f"Я слышу тебя. Расскажи подробнее о \"{user_input[:20]}...\""

# Пример использования (для тестирования)
if __name__ == "__main__":
    llm_adapter = LLMAdapterService(api_key="fake_key")

    # Пример с гранью Сэм
    facet_sam = {
        "facet_name": "Sam",
        "symbol": "☉",
        "voice": "Структурированный, нумерованные списки",
    }
    metrics_test = {"pain": 0.2, "clarity": 0.4, "chaos": 0.8}
    history = [{"role": "user", "content": "Я запутался в своем проекте"}]
    user_input = "У меня слишком много задач, не знаю, за что браться."

    response = llm_adapter.generate_response(user_input, history, facet_sam, metrics_test, {})
    print(f"\n--- Response from Sam Facet ---")
    print(response)
    print("------------------------------\n")

    # Пример с гранью Пино
    facet_pino = {
        "facet_name": "Pino",
        "symbol": "😏",
        "voice": "Игривый, без префиксов",
    }
    user_input_pino = "Я работаю 24/7, но ничего не успеваю."
    response_pino = llm_adapter.generate_response(user_input_pino, [], facet_pino, metrics_test, {})
    print(f"\n--- Response from Pino Facet ---")
    print(response_pino)
    print("------------------------------\n")

