function myFunction(){
    
    var data={};
    var sno = document.getElementsByName("sno")[0].value;
    data["sno"] = sno
    var firstname = document.getElementsByName("firstname")[0].value;
    data["firstname"] = firstname
    var lastname = document.getElementsByName("lastname")[0].value;
    data["lastname"] = lastname
    var coursesSelected = [];
    var courses = document.getElementsByName("courses");
    for(i=0; i<courses.length; i++){
        if(courses[i].checked == true){
            coursesSelected.push(courses[i].value)
        }
    }
    data["courses"] = coursesSelected;
    var status = document.getElementsByName("status")[0];
    var statusSelected = status.options[status.selectedIndex].value;
    data["status"] = statusSelected;
    var semester = document.getElementsByName("semester");
    for(i=0; i<semester.length; i++){
        if(semester[i].checked == true){
            data["semester"] = semester[i].value;
        }
    }
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