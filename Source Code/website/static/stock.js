let bottom = JSON.parse({{ dates | tojson }})
let income = JSON.parse({{ money | tojson }})

const data = {
    labels: bottom,
    datasets: [{
        label: 'My First dataset',
        backgroundColor: 'rgb(255, 99, 132)',
        borderColor: 'rgb(255, 99, 132)',
        data:income,
    }]
};
const config = {
    type: 'line',
    data: data,
    options: {}
};

var ctx = document.getElementById("myChart");
var newmychart = new Chart(ctx,config);

let mo3=document.getElementById("mo3")



mo3.addEventListener("click",()=>{
    console.log('hello1')
    let xhr = new XMLHttpRequest();
    xhr.open('GET','http://127.0.0.1:5000/data',true);
    xhr.onload= function(){
        if(this.status == 200){
        let information = JSON.parse(this.responseText);
        dates =[]
        for(let num =0;num< information.length;num++)
        {
            dates.push(num)
        }
        newmychart.data.labels=dates;
        newmychart.data.datasets[0].data=information;
        newmychart.update();
        }
    }
    xhr.send();
});

let mo6=document.getElementById("mo6")

mo6.addEventListener("click",()=>{
    $.get("http://127.0.0.1:5000/data",function(data){
        alert(data)
        });
    });