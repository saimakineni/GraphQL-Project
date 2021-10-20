function myFunction() {
  
  
  
	var select1 = document.getElementsByName("hobbies")[0];
    var selected1 = [];
    for (var i = 0; i < select1.length; i++) {
        if (select1.options[i].selected) 
			selected1.push(select1.options[i].value);
    }
    console.log(selected1);
}