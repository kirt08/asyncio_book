### asyncio.gather
**Время выполнение**: max(time(cor1), time(cor2), time(cor3))
**Главный недостаток**: Мы ждем выполение всех запросов даже если у нас 2 запроса выполня.тся 1 секунду, а третий 100 секунд.

*return_exception*: bool -> gather вернет список из результатов выполнения сопрограмм, если указать этот аргумент False, исключения будут возбуждаться, в случае True, исключения будут хранится в списке и мы можем наткнуться на него при итерации, поэтому можно использовать, например, isinstance(exception)


### asyncio.as_completed
**Главный плюс**: решает проблему gather -> можем обрабатывать результаты по мере выполнения таски, однако платим за это хаотичным порядком возврата, мы не знаем результат от какой таски нам пришел, можно использвоать только когда порядок НЕ важен!


### asyncio.wait
**Время выполнения** может варироваться от установленного значения в параметр *return_when*

Такая функция позволяет очень хорошо контрилорать происходящие процессы и писать логику самостоятельно. 
```python
@async_timed
async def fetch_status(url: str, session: ClientSession, delay: int):
    await asyncio.sleep(delay)
    async with session.get(url) as response:
        return response.status


async def main():
    async with ClientSession() as session:
        fetchers = [
            asyncio.create_task(fetch_status(url, session, 1)),
            asyncio.create_task(fetch_status(url, session, 2)),
            asyncio.create_task(fetch_status("bad://ptyhon", session, 2)),
            asyncio.create_task(fetch_status(url, session, 3)),
        ]

        done, pending = await asyncio.wait(fetchers, return_when=asyncio.FIRST_EXCEPTION)

        for done_task in done:
            if done_task.exception() is None:
                print(done_task.result())
            else:
                print("Exception was found")

        for pending_task in pending:
            pending_task.cancel()

asyncio.run(main())
```

