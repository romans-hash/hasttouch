import sys
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import warnings

sys.path.append("/content/")

# Импорт агента
from ev_agent.agent_handler.agent_01_ExecutionAgent import ExecutionAgent

# Игнорируем предупреждения о конфликте имен в pydantic
warnings.filterwarnings("ignore", category=UserWarning)

# Создание FastAPI приложения
app = FastAPI()

# Конфигурация API
MODEL_ID_FLASH = "Gemini 2.0 Flash"
NREL_API_KEY = "your_api_key_here"

# Определение схемы запроса
class MessageRequest(BaseModel):
    message: str

# Создание агента
agent = ExecutionAgent.create(
    client=None,
    model_name=MODEL_ID_FLASH, # Gemini 2.0 Flash
    api_key=NREL_API_KEY,
    debug=True,
    stage_output=True,
)

@app.post("/chat/")
async def chat(request: MessageRequest):
    try:
        response = agent.process_message(request.message)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Запуск приложения: если используете Google Colab, добавьте команду !uvicorn script_name:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    