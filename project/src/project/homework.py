import sys
import asyncio
from datetime import datetime, timedelta

import aiohttp


class PrivatBankAPI:
    BASE_URL = "https://api.privatbank.ua/p24api/exchange_rates?json&date="

    async def fetch_rate(self, session, date: str):
        url = f"{self.BASE_URL}{date}"

        try:
            async with session.get(url) as response:
                if response.status != 200:
                    print(f"Помилка HTTP: {response.status}")
                    return None

                return await response.json()

        except aiohttp.ClientError as e:
            print(f"Помилка мережі: {e}")
            return None


class CurrencyService:
    CURRENCIES = ["EUR", "USD"]

    def __init__(self):
        self.api = PrivatBankAPI()

    async def get_rates(self, days: int):
        results = []

        async with aiohttp.ClientSession() as session:
            tasks = []

            for i in range(days):
                date = (
                    datetime.now() - timedelta(days=i)
                ).strftime("%d.%m.%Y")

                tasks.append(self.api.fetch_rate(session, date))

            responses = await asyncio.gather(*tasks)

            for data in responses:
                if not data:
                    continue

                day_result = {}
                rates = {}

                for rate in data.get("exchangeRate", []):
                    currency = rate.get("currency")

                    if currency in self.CURRENCIES:
                        rates[currency] = {
                            "sale": rate.get("saleRate"),
                            "purchase": rate.get("purchaseRate")
                        }

                day_result[data["date"]] = rates
                results.append(day_result)

        return results


async def main():
    if len(sys.argv) != 2:
        print("Використання: py main.py <кількість_днів>")
        return

    try:
        days = int(sys.argv[1])

        if days < 1 or days > 10:
            print("Можна отримати курс тільки за останні 10 днів")
            return

    except ValueError:
        print("Аргумент має бути числом")
        return

    service = CurrencyService()
    result = await service.get_rates(days)

    print(result)


if __name__ == "__main__":
    asyncio.run(main())
