import random
import string
import requests
import time

def gentraffic():
    name = "".join(random.choice(string.ascii_letters)*4)
    score = random.randint(-500,3000)

    url = f"http://127.0.0.1:5000/scoreboard?name={name}&score={score}&auth=e1150d25-f56a-4688-aeb8-8163a3f4b6399eeacf73-fff8-4bfb-bcbb-5f2a40eef02d"
    requests.post(url)

counter = 0
while True:
    gentraffic()
    print(f"User No.{counter} generated")
    # time.sleep(5)