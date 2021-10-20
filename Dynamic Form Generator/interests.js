function myFunction(){
    
    var data={};
    var sid = document.getElementsByName("sid")[0].value;
    data["sid"] = sid
    var sname = document.getElementsByName("sname")[0].value;
    data["sname"] = sname
    var plsSelected = [];
    var pls = document.getElementsByName("pls");
    for(i=0; i<pls.length; i++){
        if(pls[i].checked == true){
            plsSelected.push(pls[i].value)
        }
    }
    data["pls"] = plsSelected;
    var degree = document.getElementsByName("degree")[0];
    var degreeSelected = degree.options[degree.selectedIndex].value;
    data["degree"] = degreeSelected; 
    var hobbies = document.getElementsByName("hobbies")[0];
    var hobbiesSelected = [];
    for(var i=0; i<hobbies.length; i++){
        if(hobbies.options[i].selected){
            hobbiesSelected.push(hobbies.options[i].value);
        }  
    }
    data["hobbies"] = hobbiesSelected;
    console.log(data);

    var url = http://localhost:5000/webforms/
    $.ajax({
        url: url,
        type: 'POST',
        data: JSON.stringify(data),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function(response) {
        if (response.ok) {
            alert("Insert Sucessful")
        },
        error: function(error) {
            alert("ERROR");
            console.log(error);
        }
    });
}

function reload(){
    window.location.reload();
}