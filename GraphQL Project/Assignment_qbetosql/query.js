var app = angular.module('myApp', []);
app.controller('myController', function($scope) {
	
	var tableData = {};
	var skeletonIds = [];
	
	$scope.IsVisible = false;
	$scope.isConBoxVisible = false;
	
	
	$scope.getTables = function() {
	
		uname = $scope.userName;
		password = $scope.password;
		database = $scope.database;
		//$scope.tableList = [];
		var url = 'http://localhost:5000/?query={authen(uname:" '+uname+'",upass:"'+password+'",databaseName:"'+database+'"){tableNames}}';
		$.ajax({
			url: url,
			type: 'GET',
			success: function(response){
				$scope.tableList = response.data.authen;
				console.log($scope.tableList);
				$scope.IsVisible = !$scope.IsVisible;
				$scope.$digest(); //hey AngularJS, look for changes to update the scope!
			},
			error:function(error){
				alert(error);
				//console.log(error);
			}
		});
	
	}

	
	// Creating QBE Interface
	var tableColumn;
	var columnValidation = {};
	$scope.readTables = function(){
		var dbTable=document.getElementById('databaseTables');
		var totalTablesInQbeInterface = 0;
		// Reading Data from Database Tables Section
		//console.log(totalTablesInQbeInterface);
		for(i=0; i<dbTable.rows.length;i++){
			var objs = dbTable.rows.item(i).cells;
			var data1 = objs.item(0).innerHTML;
			var data2 = objs.item(1).childNodes[0].value;
			totalTablesInQbeInterface=totalTablesInQbeInterface+parseInt(data2);
			tableData[data1] = data2;
		}


		// Creating tables in QBE interface section
		var h2 = document.getElementById('qbeInterfacechilds');
		var errorFlag = false;
		//console.log(totalTablesInQbeInterface);
		if(totalTablesInQbeInterface>0 && totalTablesInQbeInterface<4){
			for(var key in tableData){
				if(tableData[key]>0){
					console.log(tableData[key]);
					var url = 'http://localhost:5000/?query={tables(uname:" '+uname+'",upass:"'+password+'",databaseName:"'+database+'",tableName:"'+key+'"){colname, coltype}}';
					$.ajax({
						url: url,
						type: 'GET',
						async: false,
						success: function(response){
							
							tableColumn = response.data.tables;
							
							console.log(key);
							
							for(j=0; j<tableData[key]; j++){
								//console.log(key + tableData[key] + j);
								var skeletonTable = document.createElement('table');
								skeletonTable.setAttribute('id', key+'_'+j);
								//storing Id's in a list
								skeletonIds.push(key+'_'+j);
								var tr1 = document.createElement('tr');
								var tr2 = document.createElement('tr');
								
								var td = document.createElement('td');
								var text = document.createTextNode(key);
								td.appendChild(text);
								tr1.appendChild(td);

								var td3 = document.createElement('td');
								var inputElement = document.createElement('input');
								inputElement.setAttribute('type', 'text');
								inputElement.setAttribute('value', '');
								td3.appendChild(inputElement);
								tr2.appendChild(td3);
								
								for (var i = 0; i < tableColumn.length; i++){
									var td1 = document.createElement('td');
									var text1 = document.createTextNode(tableColumn[i].colname+"("+tableColumn[i].coltype+")");
									td1.appendChild(text1);
									tr1.appendChild(td1);
									var td2 = document.createElement('td');
									var inputElement = document.createElement('input');
									inputElement.setAttribute('id', key+'_'+j+'.'+tableColumn[i].colname);
									inputElement.setAttribute('type', 'text');
									inputElement.setAttribute('value', '');
									columnValidation[key+'_'+j+'.'+tableColumn[i].colname]=tableColumn[i].coltype;
									td2.appendChild(inputElement);
									tr2.appendChild(td2);
								}
								
								skeletonTable.appendChild(tr1);
								skeletonTable.appendChild(tr2);
								document.body.appendChild(skeletonTable);
								//console.log("table "+i);
								h2.appendChild(skeletonTable);
							}
					},
						error:function(error){
							alert(error);
							//console.log(error);
						}
					});


				}
			}if($scope.isConBoxVisible==false){
				$scope.isConBoxVisible = !$scope.isConBoxVisible;
			}
		}else{
			alert('You should select atleast 1 table or atmost 3 table skeletons');
		}

		console.log(skeletonIds)
	}

	var queryParams = '';
	var queryCondParams = '';
	var qbeToSql;
	var finalResult = {};
	$scope.runQuery = function(){

		console.log(skeletonIds.length)
		queryParams = '';
		queryCondParams = '';
		errorFlag = false;
		//Reading QBE data from QBE interface
		nullTables=[];
		for(i=0; i<skeletonIds.length; i++){
			var tablenull=true;
			var sTable = document.getElementById(skeletonIds[i]);
			console.log(skeletonIds[i]);
			for(j=1;j<sTable.rows.length;j++){
				
				var row = sTable.rows.item(j).cells;
				console.log(row);
				console.log(row.length);
				for(k=0;k<row.length;k++){
				 	if(k==0){	 
						var cellData = row.item(0).childNodes[0].value;
						console.log(cellData);
						if(cellData == 'P.' || cellData == 'P.UNQ'){
							queryParams+=skeletonIds[i]+'='+cellData+',';
							tablenull = false;
						}else if(cellData == ''){
							queryParams+=skeletonIds[i]+'='+null+',';
						}else{
							alert("Wrong data is passed under "+skeletonIds[i]+". Only P. or P.UNQ is expected in that column");
							errorFlag = true;
						}
					}else if(k==row.length-1 && i== skeletonIds.length-1 && errorFlag==false){
						var inputId = row.item(k).childNodes[0].getAttribute('id');
						//console.log(inputId);
						var cellData = row.item(k).childNodes[0].value;
						console.log(columnValidation[inputId]);
						if(columnValidation[inputId]=='int' || columnValidation[inputId]=='INTEGER'){
							var pat = /['][\s\S]+[']/;	
							if(cellData != ''){
								if(!pat.test(cellData)){
									console.log("validation passed"+cellData);
									queryParams+=inputId+'='+cellData;
									tablenull = false;
								}else{
									alert("Data type mismatch at "+inputId+". String is not expected");
									errorFlag=true;
								}
							}else{
								queryParams+=inputId+'='+null;
							}
						}else{
							if(cellData != ''){
								queryParams+=inputId+'='+cellData;
								tablenull = false;
							}else{
								queryParams+=inputId+'='+null;
							}
						}
					}else if(errorFlag==false){
						var inputId = row.item(k).childNodes[0].getAttribute('id');
						//console.log(inputId);
						var cellData = row.item(k).childNodes[0].value;
						if(columnValidation[inputId]=='int' || columnValidation[inputId]=='INTEGER'){
							var pat = /['][\s\S]+[']/;	
							if(cellData != ''){
								if(!pat.test(cellData)){
									console.log("validation passed"+cellData);
									queryParams+=inputId+'='+cellData+',';
									tablenull=false;
								}else{
									alert("Data type mismatch at "+inputId+". String is not expected");
									errorFlag=true;
								}
							}else{
								queryParams+=inputId+'='+null+',';
							}

						}else{
							if(cellData != ''){
								queryParams+=inputId+'='+cellData+',';
								tablenull=false;
							}else{
								queryParams+=inputId+'='+null+',';
							}
						} 
					}else{

					}
				}

			}
			nullTables.push(tablenull);
		}
		if($scope.conditions==undefined){
			queryCondParams = '';
		}else{
			queryCondParams = $scope.conditions;
		}


		var count = 0;
		console.log(nullTables);
		for(i=0; i<nullTables.length;i++){
			if(nullTables[i]==true){
				count++;
			}

		}

		console.log(queryParams);
		console.log(queryCondParams);
		if(nullTables.length==3 && count==2){
			alert("Please Check Data. Either it is not valid or there might be more tables with null values")
		}else{
			if(errorFlag==false){
				var url = 'http://localhost:5000/?query={qbetomysql(uname:" '+uname+'",upass:"'+password+'",databaseName:"'+database+'",queryParams:"'+queryParams+'",queryCondParams:"'+queryCondParams+'"){resultquery, qbetosqlquery}}';
				$.ajax({
					url: url,
					type: 'GET',
					success: function(response){
						finalResult={};
						console.log(response.data);
						if(response.data.qbetomysql==null || response.data.qbetomysql.length==0){
							alert("Unexpected Error, Please check your inputs");
						}else{
							qbeToSql = response.data.qbetomysql[0].qbetosqlquery;
							
							var s = response.data.qbetomysql;
							for(i=0; i<s.length; i++){
								finalResult[i]=s[i].resultquery;
							}

							//console.log(finalResult);
							
							populateResutlData();
						}
					},
					error:function(error){
						alert(error);
						//console.log(error);
					}
				});
			}
		}

	}
	
	var childNodesExist = false;

	function populateResutlData(){
		
		if(childNodesExist){
			function removeAllChildNodes1(parent) {
				while (parent.firstChild) {
					parent.removeChild(parent.firstChild);
				}
			}
			const container = document.querySelector('#resultchildren');
			removeAllChildNodes1(container);
		}
		var h2Result = document.getElementById('resultchildren');

		var p = document.createElement('p');
		p.innerHTML = qbeToSql;

		document.body.appendChild(p);
		h2Result.append(p);

		var pos = qbeToSql.indexOf("SELECT");
		var pos2 = qbeToSql.indexOf("FROM");

		var res = qbeToSql.slice(7, pos2-1);
		var list=[]
		var strt =0;
		while(res.search(',')!==-1){
			var cpos = res.search(',');
			list.push(res.slice(strt, cpos));
			res = res.substr(cpos+1);
		}
		list.push(res);

		//Creating result table
		var resultTable = document.createElement('table');
		var tr1 = document.createElement('tr');
		for(i=0;i<list.length;i++){
			var td = document.createElement('td');
			var text = document.createTextNode(list[i])
			td.appendChild(text);
			tr1.appendChild(td);
		}
		resultTable.appendChild(tr1);

		//console.log(finalResult.size);

		for(key in finalResult){
			var tr = document.createElement('tr');
			var l = finalResult[key];
			console.log(finalResult[key]);
			for(j=0; j<l.length;j++){
				var td = document.createElement('td');
				console.log(l[j])
				var text = document.createTextNode(l[j]);
				td.appendChild(text);
				tr.appendChild(td);
			}
			resultTable.appendChild(tr)
		}	
		document.body.appendChild(resultTable);
		p.appendChild(resultTable);
		childNodesExist = true;
	}


	$scope.resetSkeletons = function(){
		function removeAllChildNodes(parent) {
    		while (parent.firstChild) {
        		parent.removeChild(parent.firstChild);
   			}
		}
		const container = document.querySelector('#qbeInterfacechilds');
		removeAllChildNodes(container);
		$scope.isConBoxVisible = !$scope.isConBoxVisible;

		const container2 = document.querySelector('#resultchildren');
		removeAllChildNodes(container2);

		skeletonIds=[];
		$scope.conditions = '';
	}


});