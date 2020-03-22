function edit_row(no) {
    document.getElementById("edit_button"+no).style.display="none";
    document.getElementById("save_button"+no).style.display="block";

    let sort=document.getElementById("sort_row"+no);
    let description = document.getElementById("description_row"+no);
    let availability = document.getElementById("availability_row"+no);
    let amount = document.getElementById("amount_row"+no);
    let price = document.getElementById("price_row"+no);

    let sort_data = sort.innerHTML;
    let description_data = description.innerHTML;
    let availability_data = availability.innerHTML;
    let amount_data = amount.innerHTML.slice(0, -4);
    let price_data = price.innerHTML.slice(0, -4);

    sort.innerHTML="<input type='text' id='sort_text"+no+"' value='"+sort_data+"'>";
    sort.style.background = "white";
    description.innerHTML="<input type='text' id='description_text"+no+"' value='"+description_data+"'>";
    description.style.background = "white";
    availability.innerHTML="<input type='text' id='availability_text"+no+"' value='"+availability_data+"'>";
    availability.style.background = "white";
    amount.innerHTML="<input type='text' id='amount_text"+no+"' value='"+amount_data+"'>";
    amount.style.background = "white";
    price.innerHTML="<input type='text' id='price_text"+no+"' value='"+price_data+"'>";
    price.style.background = "white";
}

function save_row(no) {
    let elementIds = ["sort_text"+no, "description_text"+no, "availability_text"+no, "amount_text"+no, "price_text"+no];
    let JSONtoSend = {};
    let isOkayToSend = true;
    for (const elementName of elementIds){
        let element = document.getElementById(elementName);
        if ((element.value.length < 1) ||
            ((elementName === "amount_text"+no || elementName === "price_text"+no || elementName === "availability_text"+no)
                && isNaN(element.value))) {
            element.classList.add("warning_cell");
            isOkayToSend = false;
            element.oninput = function(){
                element.classList.remove("warning_cell");
            };
        }
        else {
            JSONtoSend[elementName] = element.value;
        }
    }

    if (isOkayToSend){
        let xhttp = new XMLHttpRequest();
        xhttp.open("PATCH", "/sql"+
                                        "?article_id="+no+
                                        "&sort="+JSONtoSend['sort_text'+no]+
                                        "&description="+JSONtoSend['description_text'+no]+
                                        "&availability="+JSONtoSend['availability_text'+no]+
                                        "&amount="+JSONtoSend['amount_text'+no]+
                                        "&price="+JSONtoSend['price_text'+no], true);
        xhttp.onreadystatechange = function () {
            if(xhttp.readyState === 4) {
                switch (xhttp.status) {
                    case 200:
                        document.getElementById("sort_row" + no).innerHTML = JSONtoSend['sort_text'+no];
                        document.getElementById("sort_row" + no).style.background = "#dff8c2";

                        document.getElementById("description_row" + no).innerHTML = JSONtoSend['description_text'+no];
                        document.getElementById("description_row" + no).style.background = "#dff8c2";

                        document.getElementById("availability_row" + no).innerHTML = JSONtoSend['availability_text'+no];
                        document.getElementById("availability_row" + no).style.background = "#dff8c2";

                        document.getElementById("amount_row" + no).innerHTML = JSONtoSend['amount_text'+no] + " шт.";
                        document.getElementById("amount_row" + no).style.background = "#dff8c2";

                        document.getElementById("price_row" + no).innerHTML = JSONtoSend['price_text'+no] + " грн";
                        document.getElementById("price_row" + no).style.background = "#dff8c2";

                        document.getElementById("edit_button" + no).style.display = "block";
                        document.getElementById("save_button" + no).style.display = "none";
                        break;
                    case 500:
                        let error = JSON.parse(xhttp.response);
                        alert("Ошибка в заполнении базы данных!\n"+error.error);
                        break;
                    default:
                        alert("Произошла ошибка, попробуйте ещё раз!")
                }
            }
        };
        xhttp.send();
    }
}

function delete_row(no) {

    let xhttp = new XMLHttpRequest();
        xhttp.open("DELETE", "/sql?article_id="+no, true);
        xhttp.onreadystatechange = function (){
            if(xhttp.readyState === 4) {
                let error = JSON.parse(xhttp.response);
                switch (xhttp.status) {
                    case 200:
                        document.getElementById("row"+no+"").outerHTML="";
                        break;
                    case 500:
                        alert("Ошибка в работе с базой данных!\n"+error.error);
                        break;
                    default:
                        alert("Произошла ошибка, попробуйте ещё раз!\n"+error.error)
                }
            }
        };
        xhttp.send();
}

function add_row() {
    let elementIds = ["new_sort", "new_description", "new_availability", "new_amount", "new_price"];
    let JSONtoSend = {};
    let isOkayToSend = true;
    for (const elementName of elementIds){
        let element = document.getElementById(elementName);
        if ((element.value.length < 1) ||
            ((elementName === "new_amount" || elementName === "new_price" || elementName === "new_availability")
                && isNaN(element.value))) {
            element.classList.add("warning_cell");
            isOkayToSend = false;
            element.oninput = function(){
                element.classList.remove("warning_cell");
            }
        }
        else {
            JSONtoSend[elementName] = element.value;
        }
    }

    if (isOkayToSend) {
        let table = document.getElementById("data_table");
        let table_len = (table.rows.length)-1;

        let xhttp = new XMLHttpRequest();
        xhttp.open("POST", "/sql"+
                                        "?article_id="+table_len+
                                        "&sort="+JSONtoSend['new_sort']+
                                        "&description="+JSONtoSend['new_description']+
                                        "&availability="+JSONtoSend['new_availability']+
                                        "&amount="+JSONtoSend['new_amount']+
                                        "&price="+JSONtoSend['new_price'], true);
        xhttp.onreadystatechange = function (){
            if(xhttp.readyState === 4) {
                switch (xhttp.status) {
                    case 200:
                        let new_row = table.insertRow(table_len).outerHTML=
                        "<tr id='row"+table_len+"'>" +
                        "<td id='sort_row"+table_len+"'>"+JSONtoSend['new_sort']+"</td>" +
                        "<td id='description_row"+table_len+"'>"+JSONtoSend['new_description']+"</td>" +
                        "<td id='availability_row"+table_len+"'>"+JSONtoSend['new_availability']+"</td>" +
                        "<td id='amount_row"+table_len+"'>"+JSONtoSend['new_amount']+" шт.</td>" +
                        "<td id='price_row"+table_len+"'>"+JSONtoSend['new_price']+" грн</td>" +
                        "<td class='hidden' style='display: grid'>" +
                        "<input type='button' id='edit_button"+table_len+"' value='Редактировать' class='edit_button' onclick='edit_row("+table_len+")'>" +
                        "<input type='button' id='save_button"+table_len+"' value='Сохранить' class='save_button' onclick='save_row("+table_len+")'>" +
                        "<input type='button' value='Удалить' class='delete_button' onclick='delete_row("+table_len+")'>" +
                        "</td>" +
                        "</tr>";
                        break;
                    case 500:
                        let error = JSON.parse(xhttp.response);
                        alert("Ошибка в заполнении базы данных!\nПроверьте уникальность артикула!\n"+error.error);
                        break;
                    default:
                        alert("Произошла ошибка, попробуйте ещё раз!")
                }
            }
        };
        xhttp.send();
    }
}