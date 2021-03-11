
    
  function show() { 
    // document.getElementById("active").disabled = true;
    
    var rowId =  event.target.parentNode.parentNode.id; 
            //this gives id of tr whose button was clicked 
              var data_name = document.getElementById(rowId).querySelectorAll(".dta");  
              // var data_mob = document.getElementById(rowId).querySelectorAll(".dta"); 
            // /*returns array of all elements with  
            // "row-data" class within the row with given id*/ 

              var name = data_name[0].innerHTML; 
              var mob = data_name[4].innerHTML
              // var date = data[1]; 
              document.getElementById("name_text").value=name;
              document.getElementById("mob_text").value=mob;
              document.getElementById("row_id").value=rowId;

              alert("rowid: " + rowId + "name:" + name +" mob: " + mob); 
              
              // document.getElementById("warning").disabled = false;
              // document.getElementById('warning').removeAttribute('disabled');
              return true;
          }
function selectoption()
{
  select = document.getElementById('appointment_date');
  var opt = document.createElement('option');
  opt.value = date_today;
  opt.innerHTML = "Today";
  var ppt = document.createElement('option');
  ppt.value = date_tomorrow;
  ppt.innerHTML = "Tomorrow";
  select.appendChild(opt);
  select.appendChild(ppt);
}

var options = { year: 'numeric', month: 'long', day: 'numeric' };
var today  = new Date();
var year   = today.getFullYear();
var month  = today.toLocaleString('default', { month: 'long' });
var date   = ("0" + today.getDate()).slice(-2);
var z = parseInt(date) +1
var date1  = ("0" + (z)).slice(-2);
var date_today = month + " " + date + " " + "," + " " + year;
var date_tomorrow = month + " " + date1 + " " + "," + " " + year;
var today1 = today.toLocaleDateString("en-US", options);




function searchdata()
{
var input,table,tr,td,filter,displaydate;
input=document.getElementById("appointment_date");
filter = input.value;
console.log(filter);
table = document.getElementById("table1");
tr = table.getElementsByTagName("tr");
for(i=0;i<tr.length;i++)
{
td=tr[i].getElementsByTagName("td")[1];
if(td)
{

displaydate=td.innerText;
console.log(displaydate);
console.log(date_today);
if(displaydate.localeCompare(filter)==0)

{
  tr[i].style.display="";
}
else
{
  tr[i].style.display="none";
}

}

} 
}   

