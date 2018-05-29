try
  {
  	console.log('work here');
	var t_out = setTimeout("submit()",3000);
	setTimeout("get_next()", 10000);

	draw_table();
  }
catch(err)
  {
  	console.log(err);
  }
var count=0;
//set_visibale(0);

function get_next()
{
    //alert('nothing...');
    var res=confirm('do you like me?');
    console.log(res);
}
    function submit() 
    {
        clearTimeout(t_out);
    	console.log(count);
    	t_out=setTimeout("submit()",3000);
        //alert("you have cost about 5 seconds...");
        //set_visibale(count);
        draw_table();
    	
    	count++;
        //window.location.href='/next';
        // body...
    }

    function set_visibale(count)
    {
    	if(count %5==0)
        {
        	document.getElementById("right").style.display='None';
        	document.getElementById("left").style.width='100%';
        }
        else
        {
        	document.getElementById("left").style.width='65%';
        	document.getElementById("right").style.display='inline';
        }
    }

    function draw_table()
    {
    	var matrix=[
			    	[1,'abcde',parseInt(5*Math.random()),parseInt(10*Math.random())+1],
			    	[2,'bcdef',parseInt(5*Math.random()),parseInt(10*Math.random())+1],
			    	[3,'cdefg',parseInt(5*Math.random()),parseInt(10*Math.random())+1],
			    	[4,'dfagrt',parseInt(5*Math.random()),parseInt(10*Math.random())+1],
			    	[5,'asdaf',parseInt(5*Math.random()),parseInt(10*Math.random())+1],
			    	[6,'bfd',parseInt(5*Math.random()),parseInt(10*Math.random())+1],
			    	[7,'cer',parseInt(5*Math.random()),parseInt(10*Math.random())+1],
			    	[8,'drt',parseInt(5*Math.random()),parseInt(10*Math.random())+1],
			    	[9,'bf',parseInt(5*Math.random()),parseInt(10*Math.random())+1],
			    	[10,'cew',parseInt(5*Math.random()),parseInt(10*Math.random())+1]
			    	];
		//alert(matrix.length);
    	var row1=10;
    	var col1=4;
    	var div1=document.getElementById("table_rank");
        var tab="<table border='0' cellpadding='0' cellspacing='0' width='100%' height='100%' style='text-align: center;'>";
        //var tab="<table border='1' width='100%' height='100%' style='text-align: center;'>";
        //循环行
        tab+="<tr>";
	        tab+="<td class='table_meta'><b>Rank</b></td>";
	        tab+="<td class='table_meta'><b>User</b></td>";
	        tab+="<td class='table_meta'><b>Number</b></td>";
	        tab+="<td class='table_meta'><b>Total Number</b></td>";
        tab+="</tr>";
        tab+="<hr/>";
        for (var row=0;row<matrix.length;row++)
        {
        	tab+="<tr>";
        	for (var col=0;col<matrix[row].length; col++)
        	{
        		tab+="<td class='table_cell'";
                if(row%2==0)
                {
                    tab+=" bgcolor='#cde6c7' ";
                }
                tab+=">"+matrix[row][col]+"</td>";
        	}
        	tab+="</tr>";
        }
        //tab+="<hr/>";

        tab+="</table>"
         div1.innerHTML=tab;
    }