import time
import random
import logging

def random_sleep(mu = 5, sigma = 0.4):
    secs = random.normalvariate(mu, sigma)
    if secs <= 0:
        secs = mu
    logging.info("random sleep" + str(secs) + " s")
    time.sleep(secs)