import asyncio
import re
import os
from datetime import datetime, timedelta
from vkbottle.bot import Bot, Message
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("vk1.a.Fp7Pd6vVLbKNBF0tGsnUUH60x0qd4-5OvM9c3GrgXxlH5Dr5CNmcdPFBFS1ziCetdeCp9Zu56MRj_ozB6I2tnSjTAIt5GtVZ6urKvSzs87adwNtotBBYsoALx5LcJgnGTIPsFDGNWBg04CiNhAFly7RM655Bk10TziDrowpVayst1SYy9vqMFcGVCySSMU1m0gF47cF7tuVCoArHijEBzA")


bot = Bot(TOKEN)


reminders = []

async def send_reminder(user_id: int, text: str, delay: int):
    """Ждёт нужное время и отправляет напоминание."""
    await asyncio.sleep(delay)
    try:
        await bot.api.messages.send(
            peer_id=user_id,
            message=f"⏰ Напоминание: {text}",
            random_id=0
        )
    except Exception as e:
        print(f"Ошибка отправки: {e}")

@bot.on.message()
async def handle_message(message: Message):
    
    print(f"Получено сообщение: {message.text}")
    
    text = message.text.lower()
    

    match = re.search(r"напомни через (\d+)\s*(минут|мин|час|часов)\s*(.*)", text)
    
    if match:
        value = int(match.group(1))
        unit = match.group(2)
        reminder_text = match.group(3) or "Без текста"
        
        
        if "час" in unit:
            delay = value * 3600
        else:
            delay = value * 60
            
        
        asyncio.create_task(send_reminder(message.from_id, reminder_text, delay))
        
        await message.answer(
            f"✅ Принято! Напомню через {value} {unit}.\n"
            f"Текст: «{reminder_text}»"
        )
    else:
        
        await message.answer(
            "Я бот-напоминалка. Напиши: «напомни через 5 минут позвонить»"
        )

if __name__ == "__main__":
    print("Бот запущен...")
    bot.run_forever()