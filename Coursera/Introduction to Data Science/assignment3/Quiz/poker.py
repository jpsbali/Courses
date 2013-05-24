import MapReduce, sys 

mr = MapReduce.MapReduce()
all_hands = []

# Python Kernel() : Generate all 5-card poker hands as csv string. 
# e.g. : '3S,QC,AD,AC,7H'  (5 cards in each emitted data line) 
def Kernel(print_results): 
  global all_hands
  faces = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
  suits = [ 'S', 'C', 'D', 'H' ] # Spades, Clubs, Diamonds, Hearts  

  # Make a list of all 52 cards in the deck; e.g. '3S' or 'QH'. 
  all_cards = [];  
  for f in range(0, len(faces)): 
    for s in range(0, len(suits)): 
      card = faces[f] + suits[s];  # construct e.g. 'QH' for Q of Hearts 
      all_cards.append(card) 

  # Generate and EMIT all unique 5-card combinations (poker hands). 
  all_cards_len = len(all_cards)  # 52 
  for i1 in range(0, all_cards_len): 
    for i2 in range(i1+1, all_cards_len): 
      for i3 in range(i2+1, all_cards_len): 
        for i4 in range(i3+1, all_cards_len): 
          for i5 in range(i4+1, all_cards_len): 
            hand = ('["%s","%s","%s","%s","%s"]' % (all_cards[i1], all_cards[i2], all_cards[i3], all_cards[i4], all_cards[i5])) 
            #print hand
            all_hands.append(hand)

  if (print_results):
    for hand in all_hands:
      print hand

# Python Mapper() : Given unique 5-card hand (csv string), return the made hand.
# e.g. 'flush', 'straight', etc  
def mapper(cards):
  #cards = dataline.split(',')  # 5 cards like 'QH' (for Q of hearts) 

  # Get counts of all faces and suits. 
  counts = ({ 
    '2':0, '3':0, '4':0, '5':0, '6':0, '7':0, '8':0, '9':0, 'T':0, 
    'J':0, 'Q':0, 'K':0, 'A':0, 
    'S':0, 'C':0, 'D':0, 'H':0 
  }) 
  for card in cards: 
    face = card[0] 
    suit = card[1] 
    counts[face] += 1 
    counts[suit] += 1 

  is_flush = ( 
    (counts['S'] == 5) or 
    (counts['C'] == 5) or 
    (counts['D'] == 5) or 
    (counts['H'] == 5)) 

  is_straight = False 
  straightrunfaces = 'A23456789TJQKA';  # note: ace ('A') appears twice
  for i in range(0, 10): 
    if (counts[straightrunfaces[i]] and 
      counts[straightrunfaces[i+1]] and 
      counts[straightrunfaces[i+2]] and 
      counts[straightrunfaces[i+3]] and 
      counts[straightrunfaces[i+4]]): 
      is_straight = True 
      break 

  is_4cardstraight = False
  for i in range(0, 11): 
    if (counts[straightrunfaces[i]] and 
      counts[straightrunfaces[i+1]] and 
      counts[straightrunfaces[i+2]] and 
      counts[straightrunfaces[i+3]]): 
      is_4cardstraight = True 
      break 

  is_quad, is_trip, is_pair, is_two_pair = False, False, False, False 
  faces = 'A23456789TJQK' 
  for i in range(0, len(faces)): 
    face_count = counts[faces[i]] 
    if face_count == 4: 
      is_quad = True 
    elif face_count == 3: 
      is_trip = True 
    elif face_count == 2: 
      if is_pair:  # saw another pair before? 
        is_two_pair = True 
      is_pair = True 

  # Emit output: a (stringized) count of '1' for the detected hand.
  if is_straight and is_flush: 
    mr.emit_intermediate('straightflush', '1') 
  elif is_quad: 
    mr.emit_intermediate('4ofakind', '1') 
  elif is_trip and is_pair: 
    mr.emit_intermediate('fullhouse', '1') 
  elif is_flush: 
    mr.emit_intermediate('flush', '1') 
  elif is_4cardstraight and is_straight: 
    mr.emit_intermediate('straight', '1') 
  elif is_4cardstraight: 
    mr.emit_intermediate('4cardstraight', '1') 
  elif is_trip: 
    mr.emit_intermediate('3ofakind', '1') 
  elif is_two_pair: 
    mr.emit_intermediate('2pair', '1') 
  elif is_pair: 
    mr.emit_intermediate('pair', '1') 
  else: 
    mr.emit_intermediate('highcard', '1') 


# Python Reducer() : key is a made hand, e.g. 'flush' .
# Count up how many unique hands make e.g. a flush.
def reducer(key, values): 
  sum = 0; 
  for value in values:
    count = int(value)
    sum += count 

  output_str = '%s:%d' % (key, sum) 
  mr.emit(output_str) 


if __name__ == '__main__':
  try:
    if (sys.argv[1] == 'runkernel'):
      # used to generate a file to be fed to MapReduce
      print 'Running Kernel'
      Kernel(True)
    else:
      # Run MapReduce on the data file
      print 'Running MapReduce'
      inputdata = open(sys.argv[1])
      mr.execute(inputdata, mapper, reducer)
      inputdata.close()
  except Exception, e:
    # No arguments were given. Run Kernel and store data in memory and then invoke MapReduce
    print 'No Args'
    print 'Running Kernel'
    Kernel(False)
    print 'Running MapReduce'
    mr.execute(all_hands, mapper, reducer)
    
