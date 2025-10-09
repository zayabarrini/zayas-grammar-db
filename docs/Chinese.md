Final Chinese Rules Distribution:
Level | Count | Description
------|-------|-------------
    1 |    11 | Beginner
    3 |    35 | Intermediate
    4 |     5 | Advanced
    2 |    44 | Elementary

Total rules: 95
Level 1: 11 rules (11.6%)
Level 2: 44 rules (46.3%)
Level 3: 35 rules (36.8%)
Level 4: 5 rules (5.3%)
❯ curl http://localhost:8000/grammar/rules/zh | jq 'group_by(.difficulty_level) | map({level: .[0].difficulty_level, count: length}) | sort_by(.level)'

  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 89223  100 89223    0     0  1045k      0 --:--:-- --:--:-- --:--:-- 1049k
[
  {
    "level": 1,
    "count": 11
  },
  {
    "level": 2,
    "count": 44
  },
  {
    "level": 3,
    "count": 35
  },
  {
    "level": 4,
    "count": 5
  }
]
