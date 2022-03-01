let mo6=document.getElementById("mo6")

mo6.addEventListener("click",()=>{
    $.get("http://127.0.0.1:5000/data",function(data){
        alert(data)
        });
    });