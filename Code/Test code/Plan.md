# New Plan
## How the system works:
1. At an interval, capture all keystrokes. 
2. Form these keystrokes into words
3. Choose a certain number of words that are evenly spaced throughout the data in the interval
4. Convert these individual words into KD Signals
5. Check if these words have been sampled before.
    - If they have then use DTW on both the signal from before and the signal noww
    - If not then select a different word in the data
    - If no words exist in the dataset and in the sample, then add the KD Signal for that word into the dataset.
6. For each word, apply Dynamic Time Warping on both signals.
7. Then use two similarity measures on them both.
    1. Eucialidaian distance - simple, quick....
    2. 2D correlation co-efficant - more detailed
8. If both agree they are the same person then, do nothing and repeat the process. Otherwise, prompt the user to re-enter their password.

# Interview plan
- Have a bunch of data already stored.
- Have 2 "intervals worth of data"
    - One of me typing normally
    - One of an "imposter"
- Load them in one by one
    - It should work perfectly and not kick the user out on the first one
    - It should kick the user out for the second one.
- Should show what I need it to show


