import aiohttp
import asyncio
import datetime
import sys

argument = sys.argv[1]
async def fetch_exchange_rate(session, date, currency_code):
    url = f'https://api.privatbank.ua/p24api/exchange_rates?json&date={date}'

    try:
        async with session.get(url) as response:
            response.raise_for_status()

            result = await response.json()
            rates = result.get('exchangeRate')
            exc, = [element for element in rates if element['currency'] == currency_code]
            return f'{currency_code}: buy: {exc["purchaseRateNB"]}, sale: {exc["saleRateNB"]}, date: {date}'
    except aiohttp.ClientError as e:
        return f'Error fetching data for date {date}: {str(e)}'


async def get_response(days, currency_code):
    async with aiohttp.ClientSession() as session:
        current_date = datetime.datetime.today()

        tasks = []
        for day in range(1, days + 1):
            target_date = current_date - datetime.timedelta(days=day)
            formatted_date = target_date.strftime("%d.%m.%Y")
            tasks.append(fetch_exchange_rate(session, formatted_date, currency_code))

        results = await asyncio.gather(*tasks)

    return results


async def main():
    results = await get_response(int(argument), "USD")
    for result in results:
        print(result)


if __name__ == "__main__":
    asyncio.run(main())
