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
        if option_info:
            moniker = validator_info['moniker']
            delegator = validator_info['delegators']
            fee = float(str(validator_info['fee'])) * 100
            slots = validator_info['slots']
            mins = int(validator_info['mins'])
            if mins > 0:
                mins = mins / 10**18
            stake = int(validator_info['stake']) / 10**18
            pictures = validator_info['identity']
            # status = validator_info['status']
            status = option_info['online']
            status_text_ = "Online" if status else "Offline"
            evmAddress = validator_info['evmAddress']
            full_info = {'moniker': moniker,
                         'status': status_text_,
                         'fee': int(fee),
                         'delegators': delegator,
                         'slots': slots,
                         'mins': int(mins),
                         'stake': int(stake),
                         'pictures': pictures,
                         'cosmos_address': cosmos_address,
                         'evmAddress': evmAddress,
                         'emoji': emoji
                         }
            get_status = await read_status(full_info['moniker'], full_info['status'])
            if get_status != full_info['status']:
                text = f"✅ Включение валидатора <a href='https://explorer.decimalchain.com/validators/" \
                       f"{full_info['evmAddress']}'>{full_info['moniker']}</a>"
                if full_info['status'] == 'Offline':
                    text = f"⚠️ Отключение валидатора <a href='https://explorer.decimalchain.com/validators/" \
                           f"{full_info['evmAddress']}'>{full_info['moniker']}</a>"
                print(text)
            await asyncio.sleep(0.5)
    await asyncio.sleep(0.5)

async def start():
    async with aiohttp.ClientSession() as session:  # Создаем одну сессию для всех запросов
        while True:
            await read_validators(session)
            await asyncio.sleep(30)

if __name__ == '__main__':
    asyncio.run(start())
