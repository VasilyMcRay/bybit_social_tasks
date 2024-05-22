from itertools import cycle
import asyncio
from pathlib import Path

import curl_cffi
from better_proxy import Proxy
import twitter

from bybit_social_tasks.random_world.random_world import get_random_world

CAPSOLVER_API_KEY = "CAP-FDA75BCC9B9FE44CABA786F815BCC375"

TWITTERS_TXT = Path("twitters.txt")
PROXIES_TXT = Path("proxies.txt")
RESULTS_TXT = Path("results.txt")

MAKE_VENOM = False
MAKE_MODE = False
MAKE_KIMONO = False
MAKE_CELO = False
MAKE_FOXY = False


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

QUOT_MODE_TWEET_URL = "https://twitter.com/Bybit_Official/status/1786349990094295457"
QUOT_KIMONO_TWEET_URL = "https://twitter.com/Bybit_Official/status/1785926272305995890"
QUOT_VENOM_TWEET_URL = "https://x.com/Bybit_Official/status/1788507961465135395"
QUOT_CELO_TWEET_URL = "https://twitter.com/Bybit_Official/status/1790350100868255759"
QUOT_FOXY_TWEET_URL = "https://twitter.com/Bybit_Official/status/1790653349122986054"

USER_IDS_TO_FOLLOW = [
    999947328621395968,   # https://twitter.com/Bybit_Official
    1549038204178911233,  # https://twitter.com/KAMINO
    1673713963056365576,  # https://twitter.com/modenetwork
    1489188578001309697,  #VENOM
    1009135067153616896,  #CELO
    1760308240628285440,  #FOXY
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
                    await twitter_client.update_account_info()
                    final_message = f'{twitter_account.auth_token} '
                    # Подписка
                    for user_id in USER_IDS_TO_FOLLOW:
                        await twitter_client.follow(user_id)
                        print(f"{twitter_account} Подписался на {user_id}")
                        await asyncio.sleep(3)

                    if MAKE_MODE:
                    # Твит MODE
                        mode_tweet = await twitter_client.quote(
                            QUOT_MODE_TWEET_URL, get_random_world()
                        )
                        print(f"{twitter_account} Сделал Quote твит (MODE): {mode_tweet.url}")
                        print(f"\tТекст: {mode_tweet.text}")
                        final_message = f'{final_message} {mode_tweet.url}'
                        await asyncio.sleep(3)

                    if MAKE_KIMONO:
                        #Твит KMNO
                        kimono_tweet = await twitter_client.quote(
                            QUOT_KIMONO_TWEET_URL, get_random_world()
                        )
                        print(f"{twitter_account} Сделал Quote твит (KMNO): {kimono_tweet.url}")
                        print(f"\tТекст: {kimono_tweet.text}")
                        final_message = f'{final_message} {kimono_tweet.url}'
                        await asyncio.sleep(3)

                    if MAKE_VENOM:
                        # Твит VENOM
                        venom_tweet = await twitter_client.quote(
                            QUOT_VENOM_TWEET_URL, get_random_world()
                        )
                        print(f"{twitter_account} Сделал Quote твит (VENOM): {venom_tweet.url}")
                        print(f"\tТекст: {venom_tweet.text}")
                        final_message = f'{final_message} {venom_tweet.url}'
                        await asyncio.sleep(3)

                    if MAKE_CELO:
                        celo_tweet = await twitter_client.quote(
                            QUOT_CELO_TWEET_URL, get_random_world()
                        )
                        print(f"{twitter_account} Сделал Quote твит (CELO): {celo_tweet.url}")
                        print(f"\tТекст: {celo_tweet.text}")
                        final_message = f'{final_message} {celo_tweet.url}'
                        await asyncio.sleep(3)

                    if MAKE_FOXY:
                        foxy_tweet = await twitter_client.quote(
                            QUOT_FOXY_TWEET_URL, get_random_world()
                        )
                        print(f"{twitter_account} Сделал Quote твит (FOXY): {foxy_tweet.url}")
                        print(f"\tТекст: {foxy_tweet.text}")
                        final_message = f'{final_message} {foxy_tweet.url}'
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
