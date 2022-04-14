function deleteStock(stock_id){
    fetch('/delete-stock',{
        method: 'POST',
        body: JSON.stringify({stock_id: stock_id})
    }).then((_res) =>{
        window.location.href = "/profile"
    })
}

