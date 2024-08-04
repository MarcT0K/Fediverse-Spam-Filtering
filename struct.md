# API

- [POST] Filter: JSON with message information -> Spam score [0,1]
- [GET] Unclassified Outliars: None -> List[JSON with word counts and message ID]
- [POST] Outliar classification: Message, Decision -> None
- [GET] Filtering confirmation: None -> List[JSON with word counts and message ID]
- [POST] Filtering confirmation: Message ID, Decision -> None
- [POST] Refresh: None -> None

# DB tables

- Model weights: Key=Word, Value=Count
- Preprocessed classified messages: Key=Message ID, Value=JSON with counts
- Outliars: Key=Message ID, Value=JSON with counts