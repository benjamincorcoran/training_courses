"""
Created on Tue Feb  8 16:40:26 2022

Alter the two strings (string1 and string2 on lines 21 and 22) and run the script to return 
Jaro, Jaro-Winkler, Levenshtein, standardised Levenshtein and bigram comparison
scores for the two input strings. It also returns the Soundex and double 
metaphone phonetic encodings of the two input strings.

@author: edwara5
"""
# install required packages
!pip install -r  requirements.txt --trusted-host art-p-01 --index-url http://sccm_functional:1qazxsw23edcvfr4@art-p-01/artifactory/api/pypi/yr-python/simple

# load required packages
import jellyfish
from metaphone import doublemetaphone
import logging

# strings to alter
string1 = "niamh"
string2 = "nieve"

# soundex phonetic encoding
soundex1 = jellyfish.soundex(string1)
soundex2 = jellyfish.soundex(string2)

metaphone1 = doublemetaphone(string1)
metaphone2 = doublemetaphone(string2)

# levenshtein edit distance
lev_distance = jellyfish.levenshtein_distance(string1, string2)

# standardised levenshtein edit distance
standardised_lev = round((1 - ((jellyfish.levenshtein_distance(string1, string2))/max(len(string1), len(string2)))),3)

# jaro similarity score
jaro = round(jellyfish.jaro_distance(string1, string2),3)

# jaro-winkler similarity score
jaro_winkler = round(jellyfish.jaro_winkler_similarity(string1, string2),3)

# bigram string comparison (brace yourself for lots of code)
QGRAM_END_CHAR =   chr(2)
QGRAM_START_CHAR = chr(1)

def qgram(str1, str2, q=2, common_divisor = 'average', min_threshold = None,
          padded=True):
  """Return approximate string comparator measure (between 0.0 and 1.0)
     using q-grams (with default bigrams: q = 2).
  USAGE:
    score = qgram(str1, str2, q, common_divisor, min_threshold, padded)
  ARGUMENTS:
    str1            The first string
    str2            The second string
    q               The length of the q-grams to be used. Must be at least 1.
    common_divisor  Method of how to calculate the divisor, it can be set to
                    'average','shortest', or 'longest' , and is calculated
                    according to the lengths of the two input strings
    min_threshold   Minimum threshold between 0 and 1
    padded          If set to True (default), the beginnng and end of the
                    strings will be padded with (q-1) special characters, if
                    False no padding will be done.
  DESCRIPTION:
    q-grams are q-character sub-strings contained in a string. For example,
    'peter' contains the bigrams (q=2): ['pe','et','te','er'].
    Padding will result in specific q-grams at the beginning and end of a
    string, for example 'peter' converted into padded bigrams (q=2) will result
    in the following 2-gram list: ['*p','pe','et','te','er','r@'], with '*'
    illustrating the start and '@' the end character.
    This routine counts the number of common q-grams and divides by the
    average number of q-grams. The resulting number is returned.
  """

  if (q < 1):
    logging.exception('Illegal value for q: %d (must be at least 1)' % (q))
    raise Exception

  # Quick check if the strings are empty or the same - - - - - - - - - - - - -
  #
  if (str1 == '') or (str2 == ''):
    return 0.0
  elif (str1 == str2):
    return 1.0

  # Calculate number of q-grams in strings (plus start and end characters) - -
  #
  if (padded == True):
    num_qgram1 = len(str1)+q-1
    num_qgram2 = len(str2)+q-1
  else:
    num_qgram1 = max(len(str1)-(q-1),0)  # Make sure its not negative
    num_qgram2 = max(len(str2)-(q-1),0)

  # Check if there are q-grams at all from both strings - - - - - - - - - - - -
  # (no q-grams if length of a string is less than q)
  #
  if ((padded == False) and (min(num_qgram1, num_qgram2) == 0)):
    return 0.0

  # Calculate the divisor - - - - - - - - - - - - - - - - - - - - - - - - - - -
  #
  if (common_divisor not in ['average','shortest','longest']):
    logging.exception('Illegal value for common divisor: %s' % \
                      (common_divisor))
    raise Exception

  if (common_divisor == 'average'):
    divisor = 0.5*(num_qgram1+num_qgram2)  # Compute average number of q-grams
  elif (common_divisor == 'shortest'):
    divisor = min(num_qgram1,num_qgram2)
  else:  # Longest
    divisor = max(num_qgram1,num_qgram2)

  # Use number of q-grams to quickly check for minimum threshold - - - - - - -
  #
  if (min_threshold != None):
    if (isinstance(min_threshold, float)) and (min_threshold > 0.0) and \
       (min_threshold > 0.0):

      max_common_qgram = min(num_qgram1,num_qgram2)

      w = float(max_common_qgram) / float(divisor)

      if (w  < min_threshold):
        return 0.0  # Similariy is smaller than minimum threshold

    else:
      logging.exception('Illegal value for minimum threshold (not between' + \
                        ' 0 and 1): %f' % (min_threshold))
      raise Exception

  # Add start and end characters (padding) - - - - - - - - - - - - - - - - - -
  #
  if (padded == True):
    qgram_str1 = (q-1)*QGRAM_START_CHAR+str1+(q-1)*QGRAM_END_CHAR
    qgram_str2 = (q-1)*QGRAM_START_CHAR+str2+(q-1)*QGRAM_END_CHAR
  else:
    qgram_str1 = str1
    qgram_str2 = str2

  # Make a list of q-grams for both strings - - - - - - - - - - - - - - - - - -
  #
  qgram_list1 = [qgram_str1[i:i+q] for i in range(len(qgram_str1) - (q-1))]
  qgram_list2 = [qgram_str2[i:i+q] for i in range(len(qgram_str2) - (q-1))]

  # Get common q-grams  - - - - - - - - - - - - - - - - - - - - - - - - - - - -
  #
  common = 0

  if (num_qgram1 < num_qgram2):  # Count using the shorter q-gram list
    short_qgram_list = qgram_list1
    long_qgram_list =  qgram_list2
  else:
    short_qgram_list = qgram_list2
    long_qgram_list =  qgram_list1

  for q_gram in short_qgram_list:
    if (q_gram in long_qgram_list):
      common += 1
      long_qgram_list.remove(q_gram)  # Remove the counted q-gram

  w = float(common) / float(divisor)

  assert (w >= 0.0) and (w <= 1.0), 'Similarity weight outside 0-1: %f' % (w)

  # A log message - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
  #
  logging.debug('%d-gram comparator string "%s" with "%s" value: %.3f' % \
                (q, str1, str2, w))
  return round(w,3)

# =============================================================================

def bigram(str1, str2, min_threshold = None):
  """For backwards compatibility.
  """

  return qgram(str1, str2, 2, 'average', min_threshold)
    
print("\nString distance metrics for " + string1 + " and " + string2 + ": \n\n\n  Levenshtein edit distance: " + str(lev_distance) + "\n\n  standardised levenshtein score: " + str(
        standardised_lev) + "\n\n  bigram score: " +str(qgram(string1, string2)) + "\n\n  Jaro similarity score: " + str(jaro)
      + "\n\n  jaro-winkler similarity score: " + str(jaro_winkler) + "\n\n\nPhonetic encodings: \n\n\n  soundex encoding of string 1: " + str(soundex1) + 
      " \n\n  soundex encoding of string 2: " + str(soundex2) + "\n\n  double metaphone encoding of string 1: " + str(metaphone1) +
      "\n\n  double metaphone encoding of string 2: " + str(metaphone2))
