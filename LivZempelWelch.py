
### Liv-Zempel-Welch
### implemented in Python 2.7

###############################
# Function: lzw - compress text using the Liv-Zempel-Welch Algorithm
#
# Arg: text - either the text that needs to be compressed or the path to a file containing the text
# Arg: is_file - a boolean, TRUE if the text is in a file, FALSE if it is passed in directly
#
# Assumption: all characters in the text belong to the UTF-8 character set
###############################
def lzw(text, is_file):

    # if argument is a text file, read the text from the file
    if is_file:
        file = open(text, 'r')
        text = file.read()
        file.close()

    # initialize the dictionary with all ASCII characters
    d = { }
    for i in range(0, 255):
        d[chr(i)] = i + 1

    # initialize loop variables
    prev = ''
    output = []

    # loop through every character in the uncompressed text
    for c in text:

        # the current word becomes the previous word plus the current character
        curr = prev + c

        # if the current word is in the dictionary, we are done with the loop
        # except for setting the previous word to the current one
        if curr in d:
            prev = curr

        # if the current word is not in the dictionary, add it, and send the
        # previous word to the output.  Also, reset the word to consist of the
        # current character only
        else:
            output.append(d[prev])
            d[curr] = len(d)+1
            prev = c

    # the loop will have terminated without the final word so add it
    if len(prev) > 0:
        output.append(d[prev])
    
    return output

###############################
# Function: wzl - decompress text that was compressed using lzw(), a function that performs Liv-Zempel-Welch compression
#
# Arg: input - the compressed output from lzw()
#
# Assumption: all characters in the original text belong to the UTF-8 character set
###############################
def wzl(input):

    # initialize the dictionary with all ASCII characters
    d = { }
    for i in range(0, 255):
        d[i + 1] = chr(i)

    # initialize loop variables
    output = ''
    prev = ''

    # loop through all element in the input; each element represents an index/key in the dictionary
    # that we will construct while we are decompressing
    for index in input:

        # if the index is not in the dictionary, this is a special case involve repeating
        # characters: create a new dictionary entry that is the previous entry with its first
        # character repeated
        if index not in d:
            d[index] = prev + prev[0]

        # now we know that in all cases, the current index will be in the dictionary so retrieve
        # the current word from the dictionary
        curr = d[index]

        # construct a value for the dictionary (to be added if it doesn't yet exist) in a manner
        # that reproduces what the original compression algorithm would have done
        value = prev + curr[0]

        # if the value is not in the collection of dictionary values (not keys), create a new dictionary
        # entry with this value.  Each dictionary key is constructed to be unique simply by making the
        # key match the new length of the dictionary.
        if value not in d.values():
            d[len(d) + 1] = value

        # append the current word to the output, shift the current value over to the previous value, and iterate
        output += curr
        prev = curr
    
    return output

###############################
# Function: test_lzw_one - run a single test of the lzw() and wzl() functions and print out the compression ratio
###############################
def test_lzw_one(num, text):

    output = "Test: {0}, String length: {1}".format(num, len(text))

    # run a round-trip of the text to compressed and back to decompressed forms
    compressed = lzw(text, False)
    decompressed = wzl(compressed)

    # report failure or report the compression ratio as (old-new)/old
    if text != decompressed:
        print(output + " **FAIL**")
    else:
        old_bytes = len(text) # 1 byte per character
        new_bytes = len(compressed) * 2 # 2 bytes per number
        compression = 0
        if old_bytes > 0:
            compression = (old_bytes - new_bytes) / float(old_bytes)
        print(output + ", Compression ratio: {0}%".format(int(compression*100)))

###############################
# Function: test_lzw_many - run a number of tests, included special cases, of the lzw() and wzl() functions
###############################
def test_lzw_many():
    test_lzw_one(1, '')
    test_lzw_one(2, 'A')
    test_lzw_one(3, 'AA')
    test_lzw_one(4, 'AAA')
    test_lzw_one(5, 'AB')
    test_lzw_one(6, 'ABA')
    test_lzw_one(7, 'ABBA')
    test_lzw_one(8, 'ABBBBBBBBBBBBBBBBBA')
    test_lzw_one(9, 'AAAAAAAAAAAAAAAAAAA')
    test_lzw_one(10, 'ABCABCABCABCABCABC')
    test_lzw_one(11, 'The brown dog jumped over the lazy fox or something like that')
    test_lzw_one(12, 
        'TGATGATGAAGACATCAGCATTGAAGGGCTGATGGAACACATCCCGGGGCCGGAC' +
        'TTCCCGACGGCGGCAATCATTAACGGTCGTCGCGGTATTGAAGAAGCTTACCGTA' +
        'CCGGTCGCGGCAAGGTGTATATCCGCGCTCGCGCAGAAGTGGAAGTTGACGCCAA' +
        'CCGGTCGTGAAACCATTATCGTCCACGAAATTCCGTATCAGGTAAACAAAGCGAA' +
        'CGCCTGATCGAGAAGATTGCGGAACTGGTAAAAGAAAAACGCGTGGAAGGCATCA' +
        'GCGCGCTGCGTGACGAGTCTGACAAAGACGGTATGCGCATCGTGATTGAAGTGAA' +
        'ACGCGATGCGGTCGGTGAAGTTGTGCTCAACAACCTCTACTCCCAGACCCAGTTG' +
        'CAGGTTTCTTTCGGTATCAACATGGTGGCATTGCACCATGGTCAGCCGAAGATCA' +
        'TGAACCTGAAAGACATCATCGCGGCGTTTGTTCGTCACCGCCGTGAAGTGGTGAC' +
        'CCGTCGTACTATTTTCGAACTGCGTAAAGCTCGCGATCGTGCTCATATCCTTGAA' +
        'GCATTAGCCGTGGCGCTGGCGAACATCGACCCGATCATCGAACTGATCCGTCATG' +
        'CGCCGACGCCTGCAGAAGCGAAAACTGCGCTGGTTGCTAATCCGTGGCAGCTGGG' +
        'CAACGTTGCCGCGATGCTCGAACGTGCTGGCGACGATGCTGCGCGTCCGGAATGG' +
        'CTGGAGCCAGAGTTCGGCGTGCGTGATGGTCTGTACTACCTGACCGAACAGCAAG' +
        'CTCAGGCGATTCTGGATCTGCGTTTGCAGAAACTGACCGGTCTTGAGCACGAAAA' +
        'ACTGCTCGACGAATACAAAGAGCTGCTGGATCAGATCGCGGAACTGTTGCGTATT' +
        'CTTGGTAGCGCCGATCGTCTGATGGAAGTGATCCGTGAAGAGCTGGAGCTGGTTC' +
        'GTGAACAGTTCGGTGACAAACGTCGTACTGAAATCACCGCCAACAGCGCAGACAT')
    
    lp_text = ('Linear programming, surprisingly, is not directly related to ' +
        'computer programming. The term was introduced in the 1950s when ' +
        'computers were few and mostly top secret, and the word programming '
        'was a military term that, at that time, referred to plans or ' +
        'schedules for training, logistical supply, or deployment of men. ' +
        'The word linear suggests that feasible plans are restricted by ' +
        'linear constraints (inequalities), and also that the quality of the ' +
        'plan (e.g., costs or duration) is also measured by a linear function ' +
        'of the considered quantities. In a similar spirit, linear programming ' +
        'soon started to be used for planning all kinds of economic activities, ' +
        'such as transport of raw materials and products among factories, sowing ' +
        'various crop plants, or cutting paper rolls into shorter ones in sizes ' +
        'ordered by customers. The phrase planning with linear constraints would ' +
        'perhaps better capture this original meaning of linear programming. ' +
        'However, the term linear programming has been well established for many ' +
        'years, and at the same time, it has acquired a considerably broader ' +
        'meaning: Not only does it play a role only in mathematical economy, it ' +
        'appears frequently in computer science and in many other ﬁelds.')
    test_lzw_one(13, lp_text)

    lp_text = lp_text + lp_text # 2 copies
    lp_text = lp_text + lp_text # 4 copies
    lp_text = lp_text + lp_text # 8 copies
    lp_text = lp_text + lp_text # 16 copies
    test_lzw_one(14, lp_text)

test_lzw_many()
