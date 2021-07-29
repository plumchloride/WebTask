def rank(time,min,lists):
  cal_list = [0,0,0,0,0,0,0]
  values = False
  for i in range(len(time)):
    for z in range(len(lists)):
      if time[i][:10] == lists[z]:
        cal_list[z] += min[i]
        values = True
  if not(values):
    return [0,0,0,0,0,0,0]
  sum_val = sum(cal_list)
  rank_list = [0,0,0,0,0,0,0]
  for i in range(len(cal_list)):
    rank_list[i] = int((cal_list[i]/sum_val)*100)
  return rank_list