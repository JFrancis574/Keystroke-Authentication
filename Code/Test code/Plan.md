# New Plan
## How the new works:
1. At an interval, capture all keystrokes. 
2. Form these keystrokes into words with all the info associated (Hold time and float time)
3. Check these against the words that the user has enterer when 100% them
4. At a certain banding, accept the user. Change if not.
5. After verifying update the list of words for that user.
6. Words that are most commonly used by the user, will be added to a faster smaller table to ease performance issues
7. Continue on

## Why this approach?
1. Gurranteed to work
2. Old approach was misleading in how it worked. Never showed dataset and the fact that it required same character string each time
3. Maybe could interconnect the two???? Use the algorithms on the words???

## Sample Running of Current:
### Input:
Input is read from a pickle file and this test data is gathered over 60 seconds. Its comprised of:
>cover hand rest rock game eyee snow found stand idea hot four toward any table well study note inch typing fina laugh wiood deep travel speed dog special page ling on givern place your point east hourse great true had clear have goouyp still r3ect boat usual night string word book family children check best plain lead mark earlty

This is represented inside my current prototype as an array consisting of key events for each invidual key. They are then put in pairs with each up and down action linked together. The pair output looks like this:

```
[
    ['t', 9.06619119644165, 9.150348424911499]
    ['a', 9.774295806884766, 9.84916877746582]
]
```
The first value in the array is the key being pressed, the second is the time the key is pressed and the third value the time the key is released. Pairing the data like this has many advantages and allows calculation of other metrics such as holdtime and floattime much easier.

My current holdtime calculation is immensely simple as the pair data is easy to work with. For example, with the data presented above, the function will just do:
```python
for x in pairs:
    holdTime = x[2] - x[1]
```

FloatTime is a little more complex. One of the things that makes it a more complex is the fact that the user can be pressing more than 1 key at once which makes calculating the time difference a lot harder. More work is needed on this metric for me. A potential solution may be to do the calculation normally for most keys, but when two down events are in a row, then calculate the floattime from each down time to another. As above, I need to do more work on this.

Finally my words 'finder'. This works with the pairs function output as described above.

``` python
def words(pairs):
    currentWord = []
    output = []
    for i in pairs:
        if i[0] not in [',','!','space', 'enter', ';',"'",'(',')']:
            if i[0] == 'backspace':
                currentWord.pop(len(currentWord)-1)
            else:
                currentWord.append(i)
        else:
            output.append(currentWord)
            currentWord = []
    return output
```
This function so far returns the correct words in the correct order. I need to generate more test data in order for this function to test properly.

### KDS:

The current KDS output looks like this:

![kds](https://campus.cs.le.ac.uk/gitlab/ug_project/21-22/jtf10/-/blob/main/Code/Test%20code/60SecondTestDataKDS.png)

A more detailed 10 second look at the same data looks like this:

![kds](/60SecondTestDataKDS10Seconds.png)

A more detailed view is here.

### Plan for the next month
- [ ] Fix FloatTime
- [ ] Build the user typing analyser
- [ ] Build the user checker

