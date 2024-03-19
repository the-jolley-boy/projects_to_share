class GlobalVariables():
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.advisorDict = None
            cls._instance.staff_pings = {
                "ashton": "<@!310135558460669972>",
                "kian": "<@!100108221280186368>",
                "dooley": "<@!297893394691260418>",
                "eddy": "<@!719973042134056980>",
                "kang": "<@!708445384774778881>",
                "moumou": "<@!243617717809053707>",
                "nef": "<@!208479361664286721>",
                "sloth": "<@!380544631600840705>",
                "vorlin": "<@!143113639371603968>",
                "warchief": "<@!729093172222754837>"
            }
            cls._instance.staff_emotes = {
                "kian": "<:notify:909914857552359494>",
                "kang": "<:notifyorange:909914892650307604>",
                "dooley": "<:notifygrey:909914869065723915>",
                "eddy": "<:notifyblack:976277026560426024>",
                "ashton": "<:notifypurple:909914913324011570>",
                "moumou": "<:notifylime:909914882755932271>",
                "nef": "<:notifyrustpink:976278693414572052>",
                "sloth": "<:notifyblue:909914478789926942>",
                "vorlin": "<:notifyswamp:976278067687342090>",
                "warchief": "<:notifyskyblue:909914923553935391>",
            }
            cls._instance.other_emotes = {
                "redcheck": '<:redcheck:910001694740463657>',
                "redx": '<:redx:910002046755827752>'
            }
            cls._instance.id_to_member = {
                100108221280186368: "kian",
                708445384774778881: "kang",
                297893394691260418: "dooley",
                719973042134056980: "eddy",
                310135558460669972: "ashton",
                243617717809053707: "moumou",
                208479361664286721: "nef",
                380544631600840705: "sloth",
                143113639371603968: "vorlin",
                729093172222754837: "warchief"
            }
            # Sneaker, Flips, Amazon, Sports, General
            cls._instance.staff_session_types = {
                100108221280186368: [1, 1, 0, 0, 0],
                708445384774778881: [1, 1, 1, 0, 0],
                297893394691260418: [1, 0, 0, 0, 0],
                719973042134056980: [1, 0, 0, 1, 0],
                310135558460669972: [1, 0, 0, 0, 0],
                243617717809053707: [1, 1, 0, 0, 0],
                208479361664286721: [0, 0, 1, 0, 1],
                380544631600840705: [1, 0, 0, 0, 0],
                143113639371603968: [1, 1, 0, 0, 0],
                729093172222754837: [1, 0, 1, 0, 0]
            }
            cls._instance.pingchannels = {}
            cls._instance.pingchannelslist = []
            cls._instance.channel_cooldowns = {}
        return cls._instance