from vk_bot import VkBot
import config


def main():
    bot = VkBot(config.token, config.group_id)
    bot.start()


if __name__ == '__main__':
    main()
