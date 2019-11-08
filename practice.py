def majority_vote(lst): 
  for i in set(lst):
    if lst.count(i)>len(lst)//2:
      return i
  return None

print(majority_vote([]))


