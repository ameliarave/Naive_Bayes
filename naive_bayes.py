import os
import sys
import math
import random



def punct(s):
    result = []
    if s[-1] == ",":
        s = s[:-1]
        result.append(s)
        result.append(",")
        return result
    elif s[-1] == ".":
        if s.count(".") < 2:
            s = s[:-1]
            result.append(s)
            result.append(".")
            return result
        elif len(s) > 2 and s[-1] == "." and s[-2] == "." and s[-3] == ".":
            result.append(s[:-3])
            result.append("...")
            return result
        else:
            result.append(s)
            return result
    elif s[-1] == "'":
        if s[0] == "'":
            result.append("'")
            s = s[1:-1]
            result.append(s)
            result.append("'")
            return result
        else:
            s = s[:-1]
            result.append(s)
            result.append("'")
            return result
    elif s[-1] == '"':
        if s[0] == '"':
            result.append('"')
            s = s[1:-1]
            result.append(s)
            result.append('"')
            return result
        else:
            s = s[:-1]
            result.append(s)
            result.append('"')
            return result
    result.append(s)
    return result




def apostrophe(s):
    punct_sep = punct(s)
    Flag = False
    if(len(punct_sep) > 1):
        Flag = True
    result = []
    if s[-1] == "s" and s[-2] == "'":
        rand = random.randint(0, 1)
        result.append(s[:-2])
        if rand == 0:
            result.append("is")
        else:
            result.append("'s")
        if Flag:
            result.append(punct_sep[1])
        return result
    elif s[-1] == "m" and s[-2] == "'":
        result.append(s[:-2])
        result.append("am")
        if Flag:
            result.append(punct_sep[1])
        return result
    elif s[-1] == "d" and s[-2] == "'":
        rand = random.randint(0, 1)
        result.append(s[:-2])
        if rand == 0:
            result.append("would")
        else:
            result.append("had")
            if Flag:
                result.append(punct_sep[1])
        return result
    elif len(s) > 2 and s[-1] == "e" and s[-2] == "r" and s[-3] == "'":
        result.append(s[:-3])
        result.append("are")
        if Flag:
            result.append(punct_sep[1])
        return result
    elif len(s) > 2 and s[-1] == "e" and s[-2] == "v" and s[-3] == "'":
        result.append(s[:-3])
        result.append("have")
        if Flag:
            result.append(punct_sep[1])
        return result
    elif len(s) > 2 and s[-1] == "l" and s[-2] == "l" and s[-3] == "'":
        result.append(s[:-3])
        result.append("will")
        if Flag:
            result.append(punct_sep[1])
        return result
    elif len(s) > 2 and s[-1] == "t" and s[-2] == "'" and s[-3] == "n":
        result.append(s[:-3])
        result.append("not")
        if Flag:
            result.append(punct_sep[1])
        return result
    return result




def slash(s):
    punct_sep = punct(s)
    Flag = False
    if (len(punct_sep) > 1):
        Flag = True
    result = []
    sep = s.split("/")
    for i in sep:
        result.append(i)
        result.append("/")
    if Flag:
        result.append(punct_sep[1])
    return result




def tokenizeText(s):
    result = []
    first_list = s.split()
    for i in first_list:
        i = i.lower()
        if len(i) == 1:
            result.append(i)
            continue
        elif "/" in i:
            b_date = True
            for charac in i:
                if charac.isalpha():
                    b_date = False
            if not b_date:
                slashed = slash(i)
                result += slashed
                continue
        if "'" in i:
            appos = apostrophe(i)
            result += appos
            continue
        punct_sep = punct(i)
        Flag = False
        if (len(punct_sep) > 1):
            Flag = True
        if Flag:
            result.append(i[:-1])
            result.append(punct_sep[1])
        else:
            result.append(i)
    return result




class PorterStemmer:

    def __init__(self):
        """The main part of the stemming algorithm starts here.
        b is a buffer holding a word to be stemmed. The letters are in b[k0],
        b[k0+1] ... ending at b[k]. In fact k0 = 0 in this demo program. k is
        readjusted downwards as the stemming progresses. Zero termination is
        not in fact used in the algorithm.

        Note that only lower case sequences are stemmed. Forcing to lower case
        should be done before stem(...) is called.
        """

        self.b = ""  # buffer for word to be stemmed
        self.k = 0
        self.k0 = 0
        self.j = 0  # j is a general offset into the string

    def cons(self, i):
        """cons(i) is TRUE <=> b[i] is a consonant."""
        if self.b[i] == 'a' or self.b[i] == 'e' or self.b[i] == 'i' or self.b[i] == 'o' or self.b[i] == 'u':
            return 0
        if self.b[i] == 'y':
            if i == self.k0:
                return 1
            else:
                return (not self.cons(i - 1))
        return 1

    def m(self):
        """m() measures the number of consonant sequences between k0 and j.
        if c is a consonant sequence and v a vowel sequence, and <..>
        indicates arbitrary presence,

           <c><v>       gives 0
           <c>vc<v>     gives 1
           <c>vcvc<v>   gives 2
           <c>vcvcvc<v> gives 3
           ....
        """
        n = 0
        i = self.k0
        while 1:
            if i > self.j:
                return n
            if not self.cons(i):
                break
            i = i + 1
        i = i + 1
        while 1:
            while 1:
                if i > self.j:
                    return n
                if self.cons(i):
                    break
                i = i + 1
            i = i + 1
            n = n + 1
            while 1:
                if i > self.j:
                    return n
                if not self.cons(i):
                    break
                i = i + 1
            i = i + 1

    def vowelinstem(self):
        """vowelinstem() is TRUE <=> k0,...j contains a vowel"""
        for i in range(self.k0, self.j + 1):
            if not self.cons(i):
                return 1
        return 0

    def doublec(self, j):
        """doublec(j) is TRUE <=> j,(j-1) contain a double consonant."""
        if j < (self.k0 + 1):
            return 0
        if (self.b[j] != self.b[j - 1]):
            return 0
        return self.cons(j)

    def cvc(self, i):
        """cvc(i) is TRUE <=> i-2,i-1,i has the form consonant - vowel - consonant
        and also if the second c is not w,x or y. this is used when trying to
        restore an e at the end of a short  e.g.

           cav(e), lov(e), hop(e), crim(e), but
           snow, box, tray.
        """
        if i < (self.k0 + 2) or not self.cons(i) or self.cons(i - 1) or not self.cons(i - 2):
            return 0
        ch = self.b[i]
        if ch == 'w' or ch == 'x' or ch == 'y':
            return 0
        return 1

    def ends(self, s):
        """ends(s) is TRUE <=> k0,...k ends with the string s."""
        length = len(s)
        if s[length - 1] != self.b[self.k]:  # tiny speed-up
            return 0
        if length > (self.k - self.k0 + 1):
            return 0
        if self.b[self.k - length + 1:self.k + 1] != s:
            return 0
        self.j = self.k - length
        return 1

    def setto(self, s):
        """setto(s) sets (j+1),...k to the characters in the string s, readjusting k."""
        length = len(s)
        self.b = self.b[:self.j + 1] + s + self.b[self.j + length + 1:]
        self.k = self.j + length

    def r(self, s):
        """r(s) is used further down."""
        if self.m() > 0:
            self.setto(s)

    def step1ab(self):
        """step1ab() gets rid of plurals and -ed or -ing. e.g.

           caresses  ->  caress
           ponies    ->  poni
           ties      ->  ti
           caress    ->  caress
           cats      ->  cat

           feed      ->  feed
           agreed    ->  agree
           disabled  ->  disable

           matting   ->  mat
           mating    ->  mate
           meeting   ->  meet
           milling   ->  mill
           messing   ->  mess

           meetings  ->  meet
        """
        if self.b[self.k] == 's':
            if self.ends("sses"):
                self.k = self.k - 2
            elif self.ends("ies"):
                self.setto("i")
            elif self.b[self.k - 1] != 's':
                self.k = self.k - 1
        if self.ends("eed"):
            if self.m() > 0:
                self.k = self.k - 1
        elif (self.ends("ed") or self.ends("ing")) and self.vowelinstem():
            self.k = self.j
            if self.ends("at"):
                self.setto("ate")
            elif self.ends("bl"):
                self.setto("ble")
            elif self.ends("iz"):
                self.setto("ize")
            elif self.doublec(self.k):
                self.k = self.k - 1
                ch = self.b[self.k]
                if ch == 'l' or ch == 's' or ch == 'z':
                    self.k = self.k + 1
            elif (self.m() == 1 and self.cvc(self.k)):
                self.setto("e")

    def step1c(self):
        """step1c() turns terminal y to i when there is another vowel in the stem."""
        if (self.ends("y") and self.vowelinstem()):
            self.b = self.b[:self.k] + 'i' + self.b[self.k + 1:]

    def step2(self):
        """step2() maps double suffices to single ones.
        so -ization ( = -ize plus -ation) maps to -ize etc. note that the
        string before the suffix must give m() > 0.
        """
        if self.b[self.k - 1] == 'a':
            if self.ends("ational"):
                self.r("ate")
            elif self.ends("tional"):
                self.r("tion")
        elif self.b[self.k - 1] == 'c':
            if self.ends("enci"):
                self.r("ence")
            elif self.ends("anci"):
                self.r("ance")
        elif self.b[self.k - 1] == 'e':
            if self.ends("izer"):      self.r("ize")
        elif self.b[self.k - 1] == 'l':
            if self.ends("bli"):
                self.r("ble")  # --DEPARTURE--
            # To match the published algorithm, replace this phrase with
            #   if self.ends("abli"):      self.r("able")
            elif self.ends("alli"):
                self.r("al")
            elif self.ends("entli"):
                self.r("ent")
            elif self.ends("eli"):
                self.r("e")
            elif self.ends("ousli"):
                self.r("ous")
        elif self.b[self.k - 1] == 'o':
            if self.ends("ization"):
                self.r("ize")
            elif self.ends("ation"):
                self.r("ate")
            elif self.ends("ator"):
                self.r("ate")
        elif self.b[self.k - 1] == 's':
            if self.ends("alism"):
                self.r("al")
            elif self.ends("iveness"):
                self.r("ive")
            elif self.ends("fulness"):
                self.r("ful")
            elif self.ends("ousness"):
                self.r("ous")
        elif self.b[self.k - 1] == 't':
            if self.ends("aliti"):
                self.r("al")
            elif self.ends("iviti"):
                self.r("ive")
            elif self.ends("biliti"):
                self.r("ble")
        elif self.b[self.k - 1] == 'g':  # --DEPARTURE--
            if self.ends("logi"):      self.r("log")
        # To match the published algorithm, delete this phrase

    def step3(self):
        """step3() dels with -ic-, -full, -ness etc. similar strategy to step2."""
        if self.b[self.k] == 'e':
            if self.ends("icate"):
                self.r("ic")
            elif self.ends("ative"):
                self.r("")
            elif self.ends("alize"):
                self.r("al")
        elif self.b[self.k] == 'i':
            if self.ends("iciti"):     self.r("ic")
        elif self.b[self.k] == 'l':
            if self.ends("ical"):
                self.r("ic")
            elif self.ends("ful"):
                self.r("")
        elif self.b[self.k] == 's':
            if self.ends("ness"):      self.r("")

    def step4(self):
        """step4() takes off -ant, -ence etc., in context <c>vcvc<v>."""
        if self.b[self.k - 1] == 'a':
            if self.ends("al"):
                pass
            else:
                return
        elif self.b[self.k - 1] == 'c':
            if self.ends("ance"):
                pass
            elif self.ends("ence"):
                pass
            else:
                return
        elif self.b[self.k - 1] == 'e':
            if self.ends("er"):
                pass
            else:
                return
        elif self.b[self.k - 1] == 'i':
            if self.ends("ic"):
                pass
            else:
                return
        elif self.b[self.k - 1] == 'l':
            if self.ends("able"):
                pass
            elif self.ends("ible"):
                pass
            else:
                return
        elif self.b[self.k - 1] == 'n':
            if self.ends("ant"):
                pass
            elif self.ends("ement"):
                pass
            elif self.ends("ment"):
                pass
            elif self.ends("ent"):
                pass
            else:
                return
        elif self.b[self.k - 1] == 'o':
            if self.ends("ion") and (self.b[self.j] == 's' or self.b[self.j] == 't'):
                pass
            elif self.ends("ou"):
                pass
            # takes care of -ous
            else:
                return
        elif self.b[self.k - 1] == 's':
            if self.ends("ism"):
                pass
            else:
                return
        elif self.b[self.k - 1] == 't':
            if self.ends("ate"):
                pass
            elif self.ends("iti"):
                pass
            else:
                return
        elif self.b[self.k - 1] == 'u':
            if self.ends("ous"):
                pass
            else:
                return
        elif self.b[self.k - 1] == 'v':
            if self.ends("ive"):
                pass
            else:
                return
        elif self.b[self.k - 1] == 'z':
            if self.ends("ize"):
                pass
            else:
                return
        else:
            return
        if self.m() > 1:
            self.k = self.j

    def step5(self):
        """step5() removes a final -e if m() > 1, and changes -ll to -l if
        m() > 1.
        """
        self.j = self.k
        if self.b[self.k] == 'e':
            a = self.m()
            if a > 1 or (a == 1 and not self.cvc(self.k - 1)):
                self.k = self.k - 1
        if self.b[self.k] == 'l' and self.doublec(self.k) and self.m() > 1:
            self.k = self.k - 1

    def stem(self, p, i, j):
        """In stem(p,i,j), p is a char pointer, and the string to be stemmed
        is from p[i] to p[j] inclusive. Typically i is zero and j is the
        offset to the last character of a string, (p[j+1] == '\0'). The
        stemmer adjusts the characters p[i] ... p[j] and returns the new
        end-point of the string, k. Stemming never increases word length, so
        i <= k <= j. To turn the stemmer into a module, declare 'stem' as
        extern, and delete the remainder of this file.
        """
        # copy the parameters into statics
        self.b = p
        self.k = j
        self.k0 = i
        if self.k <= self.k0 + 1:
            return self.b  # --DEPARTURE--

        # With this line, strings of length 1 or 2 don't go through the
        # stemming process, although no mention is made of this in the
        # published algorithm. Remove the line to match the published
        # algorithm.

        self.step1ab()
        self.step1c()
        self.step2()
        self.step3()
        self.step4()
        self.step5()
        return self.b[self.k0:self.k + 1]




def trainNaiveBayes(listFiles):
    famous = {}
    famousWords = 0
    infamous = {}
    infamousWords = 0
    allWords = set()
    fFileCount = 0
    iFileCount = 0
    p = PorterStemmer()
    for file in listFiles:
        if file.name[0] == "i":
            iFileCount += 1
        else:
            fFileCount += 1
        f = open(file, encoding="ISO-8859-1")
        for line in f:
            words = tokenizeText(line)
            for word in words:
                if file.name[0] == 'i':
                    if word in infamous:
                        infamous[word] += 1
                    else:
                        infamous[word] = 1
                    infamousWords += 1
                else:
                    if word in famous:
                        famous[word] += 1
                    else:
                        famous[word] = 1
                    famousWords += 1
                if word not in allWords:
                    allWords.add(word)
    infamousProb = {}
    famousProb = {}
    vocab = len(allWords)
    for word in allWords:
        if word in famous:
            famousProb[word] = (famous[word] + 1) / (famousWords + vocab)
        else:
            famousProb[word] = (1) / (famousWords + vocab)
        if word in infamous:
            infamousProb[word] = (infamous[word] + 1) / (infamousWords + vocab)
        else:
            infamousProb[word] = (1) / (infamousWords + vocab)
    return famousProb, infamousProb, fFileCount, iFileCount




def trainConnotated(listFiles, positive, negative):
    famousWords = 0
    infamousWords = 0
    allWords = set()
    fFileCount = 0
    iFileCount = 0
    p = PorterStemmer()
    for file in listFiles:
        if file.name[0] == "i":
            iFileCount += 1
        else:
            fFileCount += 1
        f = open(file, encoding="ISO-8859-1")
        for line in f:
            tokens = tokenizeText(line)
            words = []
            for token in tokens:
                words.append(p.stem(token, 0, len(token) - 1))
            for word in words:
                inBucket = False
                if file.name[0] == 'i':
                    if word in negative:
                        negative[word] += 1
                        infamousWords += 1
                        inBucket = True
                else:
                    if word in positive:
                        positive[word] += 1
                        famousWords += 1
                        inBucket = True
                if word not in allWords and inBucket:
                    allWords.add(word)
    infamousProb = {}
    famousProb = {}
    vocab = len(allWords)
    for word in allWords:
        if word in positive:
            famousProb[word] = (positive[word] + 1) / (famousWords + vocab)
        if word in negative:
            infamousProb[word] = (negative[word] + 1) / (infamousWords + vocab)
    return famousProb, infamousProb, fFileCount, iFileCount




def testNaiveBayes(test, trainedDataF, trainedDataI, fFileCount, iFileCount):
    f = open(test, encoding="ISO-8859-1")
    infamous = math.log(iFileCount / (fFileCount + iFileCount), 2)
    famous = math.log(fFileCount / (fFileCount + iFileCount), 2)
    p = PorterStemmer()
    for line in f:
        words = tokenizeText(line)
        for word in words:
            if word in trainedDataF:
                famous += math.log(trainedDataF[word], 2)
            if word in trainedDataI:
                infamous += math.log(trainedDataI[word], 2)
    if famous >= infamous:
        return "famous"
    return "infamous"




def testConnotated(test, trainedDataF, trainedDataI, fFileCount, iFileCount):
    f = open(test, encoding="ISO-8859-1")
    infamous = math.log(iFileCount / (fFileCount + iFileCount), 2)
    famous = math.log(fFileCount / (fFileCount + iFileCount), 2)
    p = PorterStemmer()
    for line in f:
        tokens = tokenizeText(line)
        words = []
        for token in tokens:
            words.append(p.stem(token, 0, len(token) - 1))
        for word in words:
            if word in trainedDataF:
                famous += math.log(trainedDataF[word], 2)
            if word in trainedDataI:
                infamous += math.log(trainedDataI[word], 2)
    print(famous)
    print(infamous)
    if famous >= infamous:
        return "famous"
    return "infamous"




def fill(connotation, file):
    p = PorterStemmer()
    f = open(file, encoding="ISO-8859-1")
    for line in f:
        tokens = tokenizeText(line)
        line = tokens[0]
        word = p.stem(line, 0, len(line) - 1)
        connotation[word] = 0




if __name__ == "__main__":
    allFiles = []
    with os.scandir(sys.argv[1]) as it:
        for file in it:
            allFiles.append(file)
    mode = sys.argv[2]
    numCorrect = 0
    positive = {}
    negative = {}
    orig_stdout = sys.stdout
    if mode == "all":
        w = open("naivebayes.output", "w")
    else:
        w = open("curatedWords.output", "w")
        fill(positive, "positive.txt")
        fill(negative, "negative.txt")
    sys.stdout = w
    totalsize = 0
    temp = 0
    for file in allFiles:
        fileList = set()
        for files in allFiles:
            if files != file:
                fileList.add(files)
        if mode == "all":
            trainedDataF, trainedDataI, fFileCount, iFileCount = trainNaiveBayes(fileList)
            if temp == 0:
                totalsize = fFileCount + iFileCount
                temp += 1
            result = testNaiveBayes(file, trainedDataF, trainedDataI, fFileCount, iFileCount)
        else:
            tempPositive = positive.copy()
            tempNegative = negative.copy()
            trainedDataF, trainedDataI, fFileCount, iFileCount = trainConnotated(fileList, tempPositive, tempNegative)
            if temp == 0:
                totalsize = fFileCount + iFileCount
                temp += 1
            result = testConnotated(file, trainedDataF, trainedDataI, fFileCount, iFileCount)
        if result[0] == file.name[0]:
            numCorrect += 1
        print(file.name + " " + result)
    sys.stdout = orig_stdout
    w.close()
    print(numCorrect)
    print(totalsize)
    print(numCorrect / (totalsize))

