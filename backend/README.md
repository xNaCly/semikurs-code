# Backend - REST*ful*Api
`http://xnaclyy.pythonanywhere.com/` current api host url

## Features 4 simple endpoints:

#### /:
- ~currently redirects to this repo~ 
- Isn't an endpoint nomore
#### /all:
- displays all available questions
```
example (shortend):

"Was bedeuted FAT?": [
    "File Allocation Table",
    "Freaking Amazing Tower",
    "FAT Joe",
    "Factory Acceptance Test"
  ],
```
#### /random:
- displays a random question
```
{
  "antworten": [
    "Android",
    "OpenBSD",
    "Windows",
    "macOS"
  ],
  "frage": "Welches OS wird am meisten verwendet?",
  "richtigeAntwort": "Android"
}
```
#### /endpoints:
- displays an overview about all available endpoints
```
[
  "/all",
  "/random",
  "/endpoints"
]
```
