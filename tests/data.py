TRAINING_DATA = [
    (
        {
            "id": "113171648429213722",
            "sensitive": False,
            "spoiler_text": "",
            "visibility": "public",
            "language": "en",
            "content": '<p>A quick guide to iOS power-user features: The new Control Center and beyond</p><p>Never mind emojis—here’s some stuff that makes iOS more efficient.</p><p><a href="https://arstechnica.com/gadgets/2024/09/a-quick-guide-to-ios-power-user-features-the-new-control-center-and-beyond/?utm_brand=arstechnica&amp;utm_social-type=owned&amp;utm_source=mastodon&amp;utm_medium=social" rel="nofollow noopener noreferrer" translate="no" target="_blank"><span class="invisible">https://</span><span class="ellipsis">arstechnica.com/gadgets/2024/0</span><span class="invisible">9/a-quick-guide-to-ios-power-user-features-the-new-control-center-and-beyond/?utm_brand=arstechnica&amp;utm_social-type=owned&amp;utm_source=mastodon&amp;utm_medium=social</span></a></p>',
            "media_attachments": [
                {
                    "id": "113171648404330005",
                    "type": "image",
                    "url": "https://mastodon.acm.org/system/cache/media_attachments/files/113/171/648/404/330/005/original/c78e5d1566091565.jpeg",
                    "preview_url": "https://mastodon.acm.org/system/cache/media_attachments/files/113/171/648/404/330/005/small/c78e5d1566091565.jpeg",
                    "remote_url": "https://files.mastodon.social/media_attachments/files/113/171/648/170/804/267/original/bc8e08495333439b.jpeg",
                    "preview_remote_url": None,
                    "text_url": None,
                    "meta": {
                        "original": {
                            "width": 640,
                            "height": 411,
                            "size": "640x411",
                            "aspect": 1.5571776155717763,
                        },
                        "small": {
                            "width": 599,
                            "height": 385,
                            "size": "599x385",
                            "aspect": 1.5558441558441558,
                        },
                    },
                    "description": None,
                    "blurhash": "UDCGZB4n9E?IX4S1t8t700.8xu9FoJbYoIoN",
                }
            ],
            "tags": ["Cool", "Test"],
            "mentions": [],
        },
        0,
    ),
    (
        {
            "id": "113171194079620613",
            "sensitive": False,
            "spoiler_text": "",
            "visibility": "public",
            "language": "en",
            "content": '<p>NEW: Surveillance tech maker Sandvine announced it is leaving 56 "non-democratic" countries.</p><p>Move comes after U.S. government put Sandvine on a blocklist for helping Egypt with mass censorship and surveillance. </p><p>Company also sold to Belarus, Egypt, Eritrea, the United Arab Emirates, and Uzbekistan, according to investigations by Bloomberg. </p><p><a href="https://techcrunch.com/2024/09/20/internet-surveillance-firm-sandvine-says-its-leaving-56-non-democratic-countries/" rel="nofollow noopener noreferrer" translate="no" target="_blank"><span class="invisible">https://</span><span class="ellipsis">techcrunch.com/2024/09/20/inte</span><span class="invisible">rnet-surveillance-firm-sandvine-says-its-leaving-56-non-democratic-countries/</span></a></p>',
            "media_attachments": [],
            "tags": ["Tech", "Test"],
            "mentions": [],
        },
        0,
    ),
    (
        {
            "id": "113171206365051746",
            "sensitive": False,
            "spoiler_text": "",
            "visibility": "unlisted",
            "language": "en",
            "content": '<p><span class="h-card" translate="no"><a href="https://infosec.exchange/@lorenzofb" class="u-url mention" rel="nofollow noopener noreferrer" target="_blank">@<span>lorenzofb</span></a></span> Counting the days before the totally not related "Sand Vine Export" company appears...</p>',
            "media_attachments": [],
            "tags": [],
            "mentions": [
                {
                    "id": "109580464369578205",
                    "username": "lorenzofb",
                    "url": "https://infosec.exchange/@lorenzofb",
                    "acct": "lorenzofb@infosec.exchange",
                }
            ],
        },
        1,
    ),
]

TEST_DATA = {
    "id": "11318092291909999",
    "sensitive": False,
    "spoiler_text": "",
    "visibility": "public",
    "language": "en",
    "content": "<p>Surveillance tech is bad</p>",
    "mentions": [],
    "tags": [],
    "media_attachments": [],
}


MODEL_EXPORT = {
    "feature_counts": {
        "content#56": [1, 0],
        "content#according": [1, 0],
        "content#also": [1, 0],
        "content#announced": [1, 0],
        "content#appears": [0, 1],
        "content#arab": [1, 0],
        "content#belarus": [1, 0],
        "content#beyond": [1, 0],
        "content#blocklist": [1, 0],
        "content#bloomberg": [1, 0],
        "content#censorship": [1, 0],
        "content#center": [1, 0],
        "content#comes": [1, 0],
        "content#company": [1, 1],
        "content#control": [1, 0],
        "content#counting": [0, 1],
        "content#countries": [1, 0],
        "content#days": [0, 1],
        "content#democratic": [1, 0],
        "content#efficient": [1, 0],
        "content#egypt": [1, 0],
        "content#emirates": [1, 0],
        "content#emojis": [1, 0],
        "content#eritrea": [1, 0],
        "content#export": [0, 1],
        "content#features": [1, 0],
        "content#government": [1, 0],
        "content#guide": [1, 0],
        "content#helping": [1, 0],
        "content#investigations": [1, 0],
        "content#ios": [1, 0],
        "content#leaving": [1, 0],
        "content#maker": [1, 0],
        "content#makes": [1, 0],
        "content#mass": [1, 0],
        "content#mind": [1, 0],
        "content#move": [1, 0],
        "content#never": [1, 0],
        "content#new": [2, 0],
        "content#non": [1, 0],
        "content#power": [1, 0],
        "content#put": [1, 0],
        "content#quick": [1, 0],
        "content#related": [0, 1],
        "content#sand": [0, 1],
        "content#sandvine": [1, 0],
        "content#sold": [1, 0],
        "content#stuff": [1, 0],
        "content#surveillance": [1, 0],
        "content#tech": [1, 0],
        "content#totally": [0, 1],
        "content#u": [1, 0],
        "content#united": [1, 0],
        "content#user": [1, 0],
        "content#uzbekistan": [1, 0],
        "content#vine": [0, 1],
        "media": [1, 0],
        "mentions": [0, 1],
        "sensitive": [0, 0],
        "tag#cool": [1, 0],
        "tag#tech": [1, 0],
        "tag#test": [2, 0],
        "urls#": [2, 0],
    },
    "nb_samples": [2, 1],
}

OUTLIAR = {
    "id": "113181206365051836",
    "sensitive": False,
    "spoiler_text": "",
    "visibility": "unlisted",
    "language": "en",
    "content": "<p>abc dkeke azpazk eeijarze aekharre aelrkn jfion oin pm. iujhg, sdjoi oihnk iopjom qsudfjg ekrhj izekhri hiukhb k.</p>",
    "media_attachments": [],
    "tags": [],
    "mentions": [],
}


FEATURE_COUNTS = {
    "content#56": [
        1,
        0,
    ],
    "content#according": [
        1,
        0,
    ],
    "content#also": [
        1,
        0,
    ],
    "content#announced": [
        1,
        0,
    ],
    "content#appears": [
        0,
        1,
    ],
    "content#arab": [
        1,
        0,
    ],
    "content#belarus": [
        1,
        0,
    ],
    "content#beyond": [
        1,
        0,
    ],
    "content#blocklist": [
        1,
        0,
    ],
    "content#bloomberg": [
        1,
        0,
    ],
    "content#censorship": [
        1,
        0,
    ],
    "content#center": [
        1,
        0,
    ],
    "content#comes": [
        1,
        0,
    ],
    "content#company": [
        1,
        1,
    ],
    "content#control": [
        1,
        0,
    ],
    "content#counting": [
        0,
        1,
    ],
    "content#countries": [
        1,
        0,
    ],
    "content#days": [
        0,
        1,
    ],
    "content#democratic": [
        1,
        0,
    ],
    "content#efficient": [
        1,
        0,
    ],
    "content#egypt": [
        1,
        0,
    ],
    "content#emirates": [
        1,
        0,
    ],
    "content#emojis": [
        1,
        0,
    ],
    "content#eritrea": [
        1,
        0,
    ],
    "content#export": [
        0,
        1,
    ],
    "content#features": [
        1,
        0,
    ],
    "content#government": [
        1,
        0,
    ],
    "content#guide": [
        1,
        0,
    ],
    "content#helping": [
        1,
        0,
    ],
    "content#investigations": [
        1,
        0,
    ],
    "content#ios": [
        1,
        0,
    ],
    "content#leaving": [
        1,
        0,
    ],
    "content#maker": [
        1,
        0,
    ],
    "content#makes": [
        1,
        0,
    ],
    "content#mass": [
        1,
        0,
    ],
    "content#mind": [
        1,
        0,
    ],
    "content#move": [
        1,
        0,
    ],
    "content#never": [
        1,
        0,
    ],
    "content#new": [
        2,
        0,
    ],
    "content#non": [
        1,
        0,
    ],
    "content#power": [
        1,
        0,
    ],
    "content#put": [
        1,
        0,
    ],
    "content#quick": [
        1,
        0,
    ],
    "content#related": [
        0,
        1,
    ],
    "content#sand": [
        0,
        1,
    ],
    "content#sandvine": [
        1,
        0,
    ],
    "content#sold": [
        1,
        0,
    ],
    "content#stuff": [
        1,
        0,
    ],
    "content#surveillance": [
        1,
        0,
    ],
    "content#tech": [
        1,
        0,
    ],
    "content#totally": [
        0,
        1,
    ],
    "content#u": [
        1,
        0,
    ],
    "content#united": [
        1,
        0,
    ],
    "content#user": [
        1,
        0,
    ],
    "content#uzbekistan": [
        1,
        0,
    ],
    "content#vine": [
        0,
        1,
    ],
    "media": [
        1,
        0,
    ],
    "mentions": [
        0,
        1,
    ],
    "sensitive": [
        0,
        0,
    ],
    "tag#cool": [
        1,
        0,
    ],
    "tag#tech": [
        1,
        0,
    ],
    "tag#test": [
        2,
        0,
    ],
    "urls#": [
        2,
        0,
    ],
}
