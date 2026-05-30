import sys
import asyncio
import json
from datetime import datetime, timedelta

import aiohttp


class PrivatBankAPI:
    BASE_URL = "https://api.privatbank.ua/p24api/exchange_rates?json&date="

    async def fetch_rate(self, session, date: str):
        url = f"{self.BASE_URL}{date}"

        try:
            async with session.get(url) as response:
                if response.status != 200:
                    print(f"HTTP Error: {response.status}")
                    return None

                return await response.json()

        except aiohttp.ClientError as e:
            print(f"Network error: {e}")
            return None


class CurrencyService:
    def __init__(self, currencies):
        self.api = PrivatBankAPI()
        self.currencies = currencies

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

                rates = {}

                for rate in data.get("exchangeRate", []):
                    currency = rate.get("currency")

                    if currency in self.currencies:
                        rates[currency] = {
                            "sale": rate.get("saleRate"),
                            "purchase": rate.get("purchaseRate")
                        }

                results.append({
                    data["date"]: rates
                })

        return results


async def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <days> [currencies]")
        return

    try:
        days = int(sys.argv[1])

        if days < 1 or days > 10:
            print("You can request only up to 10 days")
            return

    except ValueError:
        print("Days must be a number")
        return

    currencies = sys.argv[2:] or ["EUR", "USD"]

    service = CurrencyService(currencies)

    result = await service.get_rates(days)

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    asyncio.run(main())
