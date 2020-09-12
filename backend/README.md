# jsonBackend - REST*ful*Api

`http://xnaclyy.pythonanywhere.com/` current api host url

## Endpoints:

| path:       | description:                                | params:                  | returns:      |
| ----------- | ------------------------------------------- | ------------------------ | ------------- |
| ~~/all~~        | !endpoint disabled! ~~`get all questions`~~ | :x:                      | ~~JSON-dict~~ |
| /random     | `get a random question with answers`        | :x:                      | JSON-dict     |
| /endpoints  | `get all endpoints`                         | :x:                      | Array         |
| /scoreboard | `get scoreboard`                            | [?top=True]              | csv/JSON-dict |
| /stats      | `get stats`                                 | :x:                      | JSON-dict     |
| /check      | `get answer for a question`                 | `?q=<question>&a=<answer>` | JSON-dict     |

### Returns in Detail:

#### /all:

- JSON-dict

  ```json
  {
   "question": [
     "answer1",
     "answer2",
     "answer3",
     "answer4"
   ],
   "nextquestion":[]
  }
  ```

#### /random:

- JSON-dict

  ```json
  {
    "answers": [
    	"awnser1",
  	  "awnser2",
      "awnser3",
      "awnser4"
    ],
    "question": ""
  }
  ```

#### /endpoints:

- Array

  ```json
  [
    "/all",
    "/random",
    "/endpoints",
    "/scoreboard",
    "/stats",
    "/check"
  ]
  ```

#### /scoreboard:

- without `?top=True`:

  - csv

    ```
    name,score,uuiduuid
    player,score,uuid
    ```

- with `?top=True`:
  - JSON-dict

  ```
  {
    "content": {
      "0": "player,score,uuid",
      "1": "player,score,uuid",
      "2": "player,score,uuid",
      "3": "player,score,uuid",
      "4": "player,score,uuid",
      "5": "player,score,uuid",
      "6": "player,score,uuid",
      "7": "player,score,uuid",
      "8": "player,score,uuid",
      "9": "player,score,uuid"
    },
    "status": 200
  }
  ```

#### /stats:

- JSON-dict

  ```json
  {
    "all_scores_sorted": [],
    "all_scores_unsorted": [],
    "highest_score": 0,
    "lowest_score": 0,
    "players": 0,
    "registered_players":0 
  }
  ```

#### /check:

- JSON-dict

- if answer is valid:

  ```json
  {
    "content": {
      "feedback": "<answer> is right",
      "success": true
    },
    "status": 200
  }
  ```

- if answer isnt valid:

  ```json
  {
    "content": {
      "error": "<answer> isnt right",
      "success": false
    },
    "status": 409
  }
  ```

  
