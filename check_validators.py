import asyncio
import aiohttp
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)

url_nodes = [
    'https://node.decimalchain.com/rest'  # Ваши REST-узлы
]

async def fetch_data(session, urls, endpoint):
    for url in urls:
        full_url = f"{url}{endpoint}"
        try:
            async with session.get(full_url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                else:
                    logging.error(f"Error fetching data from {full_url}: {response.status}")
        except aiohttp.ClientConnectionError as e:
            logging.error(f"Ошибка подключения: {e}")
        except aiohttp.ClientResponseError as e:
            logging.error(f"Ошибка ответа: {e}")
        except asyncio.TimeoutError as e:
            logging.error(f"Тайм-аут: {e}")
        except Exception as e:
            logging.error(f"Неизвестная ошибка: {e}")
    return None

async def validator_info_cosmos(session, validator):
    endpoint = f"/decimal/validator/v1/validators/{validator}"
    data = await fetch_data(session, url_nodes, endpoint)
    if data:
        return data['validator']
    return None

async def fetch_validators(session):
    endpoint = "/decimal/validator/v1/validators"
    data = await fetch_data(session, url_nodes, endpoint)
    if data:
        return data['validators']
    return []

async def read_validators(session):
    for moniker, drc20address, cosmos_address, emoji in validators_list:  # Убедитесь, что validators_list определен
        validator_info = await fetch_validators(session)
        if validator_info:
            option_info = await validator_info_cosmos(session, cosmos_address)
            if option_info:
                # Обработка информации о валидаторе
                # (Здесь ваш существующий код по обработке информации)
                pass  # Замените на вашу логику

async def start():
    async with aiohttp.ClientSession() as session:  # Создаем одну сессию для всех запросов
        while True:
            await read_validators(session)
            await asyncio.sleep(30)

if __name__ == '__main__':
    asyncio.run(start())
