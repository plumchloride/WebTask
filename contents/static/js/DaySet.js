for(let i = 1; i<8;i++){
  date = new Date()
  date.setDate(date.getDate() + i);
  y = date.getFullYear();
  m = ('00' + (date.getMonth()+1)).slice(-2);
  d = ('00' + date.getDate()).slice(-2);
  console.log(y + '-' + m + '-' + d);
  document.getElementById("task_graph_"+String(i)).innerText = String(y + '-' + m + '-' + d);
}