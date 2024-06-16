from itertools import cycle
import asyncio
from pathlib import Path

import curl_cffi
from better_proxy import Proxy
import twitter

from bybit_social_tasks.random_world.random_world import get_random_world

TWITTERS_TXT = Path("twitters.txt")
PROXIES_TXT = Path("proxies.txt")
RESULTS_TXT = Path("results.txt")

MAKE_ZERO = False
MAKE_BUBBLE = False
MAKE_SPEC = True


for filepath in (
    TWITTERS_TXT,
    PROXIES_TXT,
    RESULTS_TXT,
):
    filepath.touch(exist_ok=True)


TWITTER_ACCOUNTS = twitter.account.load_accounts_from_file(TWITTERS_TXT)
PROXIES = Proxy.from_file(PROXIES_TXT)

if not PROXIES:
    PROXIES = [None]


QUOT_ZEROLEND_TWEET_URL = 'https://x.com/Bybit_Official/status/1795785918910996696'
QUOT_SPEC_TWEET_URL = 'https://x.com/Bybit_Official/status/1800437819367645277'
QUOT_BUBBLE_TWEET_URL = 'https://x.com/Bybit_Official/status/1800800207598153909'

USER_IDS_TO_FOLLOW = [
    999947328621395968,   # https://twitter.com/Bybit_Official
    1363534411694702592,  # ZEROLEND
    1252249857512755201,  # SPEC
    1478769546207006720,  # BUBBLE
]


async def main():

    proxy_to_account_list = list(zip(cycle(PROXIES), TWITTER_ACCOUNTS))

    for (
        (proxy, twitter_account),
    ) in zip(
        proxy_to_account_list,
    ):  # type: (Proxy, twitter.Account), str, str, Path,
        try:
            async with twitter.Client(twitter_account, proxy=proxy) as twitter_client:
                try:
                    await twitter_client.establish_status()
                    final_message = f'{twitter_account.auth_token} '
                    # Подписка
                    for user_id in USER_IDS_TO_FOLLOW:
                        await twitter_client.follow(user_id)
                        print(f"{twitter_account} Подписался на {user_id}")
                        await asyncio.sleep(3)

                    if MAKE_ZERO:
                    # Твит MODE
                        zerolend_tweet = await twitter_client.quote(
                            QUOT_ZEROLEND_TWEET_URL, get_random_world()
                        )
                        print(f"{twitter_account} Сделал Quote твит (ZEROLEND): {zerolend_tweet.url}")
                        print(f"\tТекст: {zerolend_tweet.text}")
                        final_message = f'{final_message} {zerolend_tweet.url}'
                        await asyncio.sleep(3)

                    if MAKE_SPEC:
                        #Твит HLG
                        spec_tweet = await twitter_client.quote(
                            QUOT_SPEC_TWEET_URL, get_random_world()
                        )
                        print(f"{twitter_account} Сделал Quote твит (SPEC): {spec_tweet.url}")
                        print(f"\tТекст: {spec_tweet.text}")
                        final_message = f'{final_message} {spec_tweet.url}'
                        await asyncio.sleep(3)

                    if MAKE_BUBBLE:
                        # Твит VENOM
                        bubble_tweet = await twitter_client.quote(
                            QUOT_BUBBLE_TWEET_URL, get_random_world()
                        )
                        print(f"{twitter_account} Сделал Quote твит (BUBBLE): {bubble_tweet.url}")
                        print(f"\tТекст: {bubble_tweet.text}")
                        final_message = f'{final_message} {bubble_tweet.url}'
                        await asyncio.sleep(3)

                    with open(RESULTS_TXT, "a") as results_file:
                        results_file.write(
                            f"{final_message}\n"
                        )

                except curl_cffi.requests.errors.RequestsError as exc:
                    print(f"Ошибка запроса. Возможно, плохой прокси: {exc}")
                    continue
                except Exception as exc:
                    print(f"Что-то очень плохое: {exc}")
                    continue
        except Exception as err:
            print(err)
            continue
if __name__ == "__main__":
    asyncio.run(main())
