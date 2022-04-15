

    function onloadeve(){
        var class_div2 = 0;
        var class_div3 = 0;
        var class_div4 = 0;

        

        $.get("http://localhost:5000/FX5U_SQL ", function (data) {
            if(data != 'None'){
                if(data[0].PLC2[0].IP_address != "undefined"){
                    class_div2 = 1;
                    var div1 = document.getElementsByClassName('plc_area_1')[1];
                    div1.style.background = null;
                    var d = document.getElementsByClassName('plc_area_1')[0].cloneNode(true);
                    for(var lend = 0;lend<d.childNodes.length;lend ++){
                        //在div中生成元素
                        div1.appendChild(d.childNodes[lend].cloneNode(true));
                    }
                    //在div內容都生成完成後，在餵入資料

                    //=============================================================     Ajax 資料內容    ======================================
                    var jaon_data =  data[0].PLC2[0];
                    div1.querySelector('#plc_address').value = jaon_data.IP_address;
                    //1.先生成jSON格式中 Single數量
                    for(var single = 0;single <jaon_data.single_num;single++ ){
                        div1.querySelector('#add_single').click();
                    }
                    //2.生成jSON格式中 Double數量
                    for(var single = 0;single <jaon_data.single_num;single++ ){
                        div1.querySelector('#add_double').click();
                    }
                    //3.將jSON格式中的Single位址UPDATE上去
                    for(var single =0;single <jaon_data.single_num;single++ ){
                        var div_single_set =div1.querySelector('#single_set').querySelector('#panel_sin'+(single+1));
                        div_single_set.querySelector('input').value= jaon_data.single_address[single].split(":")[0];
                        div_single_set.querySelector('select').value = jaon_data.single_address[single].split(":")[1];
                        console.log( div_single_set.querySelector('select').value);
                        
                    }
                    //4.將jSON格式中的Double位址UPDATE上去
                    for(var double =0;double <jaon_data.double_num;double++ ){
                        var div_double_set = div1.querySelector('#double_set').querySelector('#panel_dou'+(double+1));
                        div_double_set.querySelector('input').value= jaon_data.double_address[double].split(":")[0];
                        div_double_set.querySelector('select').value = jaon_data.double_address[double].split(":")[1];
                        console.log( div_double_set.querySelector('select').value);
                        
                    } 
                }
                if(data[0].PLC3[0].IP_address != "undefined"){
                    class_div3 = 1;
                    var div1 = document.getElementsByClassName('plc_area_1')[2];
                    div1.style.background = null;
                    var d = document.getElementsByClassName('plc_area_1')[0].cloneNode(true);

                    for(var lend = 0;lend<d.childNodes.length;lend ++){
                        //在div中生成元素
                        div1.appendChild(d.childNodes[lend].cloneNode(true));
                    }

                    //=============================================================     Ajax 資料內容    ======================================
                    var jaon_data =  data[0].PLC3[0];
                    div1.querySelector('#plc_address').value = jaon_data.IP_address;
                    //1.先生成jSON格式中 Single數量
                    for(var single = 0;single <jaon_data.single_num;single++ ){
                        div1.querySelector('#add_single').click();
                    }
                    //2.生成jSON格式中 Double數量
                    for(var single = 0;single <jaon_data.single_num;single++ ){
                        div1.querySelector('#add_double').click();
                    }
                    //3.將jSON格式中的Single位址UPDATE上去
                    for(var single =0;single <jaon_data.single_num;single++ ){
                        var div_single_set =div1.querySelector('#single_set').querySelector('#panel_sin'+(single+1));
                        div_single_set.querySelector('input').value= jaon_data.single_address[single].split(":")[0];
                        div_single_set.querySelector('select').value = jaon_data.single_address[single].split(":")[1];
                        console.log( div_single_set.querySelector('select').value);
                        
                    }
                    //4.將jSON格式中的Double位址UPDATE上去
                    for(var double =0;double <jaon_data.double_num;double++ ){
                        var div_double_set = div1.querySelector('#double_set').querySelector('#panel_dou'+(double+1));
                        div_double_set.querySelector('input').value= jaon_data.double_address[double].split(":")[0];
                        div_double_set.querySelector('select').value = jaon_data.double_address[double].split(":")[1];
                        console.log( div_double_set.querySelector('select').value);
                        
                    } 
                }
                if(data[0].PLC4[0].IP_address != "undefined"){
                    class_div4 = 1;
                    var div1 = document.getElementsByClassName('plc_area_1')[3];
                    div1.style.background = null;
                    var d = document.getElementsByClassName('plc_area_1')[0].cloneNode(true);
                    for(var lend = 0;lend<d.childNodes.length;lend ++){
                        //在div中生成元素
                        div1.appendChild(d.childNodes[lend].cloneNode(true));
                    }

                    //=============================================================     Ajax 資料內容    ======================================
                    var jaon_data =  data[0].PLC4[0];
                    div1.querySelector('#plc_address').value = jaon_data.IP_address;
                    //1.先生成jSON格式中 Single數量
                    for(var single = 0;single <jaon_data.single_num;single++ ){
                        div1.querySelector('#add_single').click();
                    }
                    //2.生成jSON格式中 Double數量
                    for(var single = 0;single <jaon_data.single_num;single++ ){
                        div1.querySelector('#add_double').click();
                    }
                    //3.將jSON格式中的Single位址UPDATE上去
                    for(var single =0;single <jaon_data.single_num;single++ ){
                        var div_single_set =div1.querySelector('#single_set').querySelector('#panel_sin'+(single+1));
                        div_single_set.querySelector('input').value= jaon_data.single_address[single].split(":")[0];
                        div_single_set.querySelector('select').value = jaon_data.single_address[single].split(":")[1];
                        console.log( div_single_set.querySelector('select').value);
                        
                    }
                    //4.將jSON格式中的Double位址UPDATE上去
                    for(var double =0;double <jaon_data.double_num;double++ ){
                        var div_double_set = div1.querySelector('#double_set').querySelector('#panel_dou'+(double+1));
                        div_double_set.querySelector('input').value= jaon_data.double_address[double].split(":")[0];
                        div_double_set.querySelector('select').value = jaon_data.double_address[double].split(":")[1];
                        console.log( div_double_set.querySelector('select').value);
                        
                    } 

                }

                if(data[0].PLC1[0].IP_address != "undefined"){
                    var jaon_data =  data[0].PLC1[0];
                    document.getElementsByClassName('plc_area_1')[0].querySelector('#plc_address').value = data[0].PLC1[0].IP_address;
                    //1.先生成jSON格式中 Single數量
                    for(var single = 0;single <jaon_data.single_num;single++ ){
                        document.getElementsByClassName('plc_area_1')[0].querySelector('#add_single').click();
                    }
                    //2.生成jSON格式中 Double數量
                    for(var single = 0;single <jaon_data.single_num;single++ ){
                        document.getElementsByClassName('plc_area_1')[0].querySelector('#add_double').click();
                    }
                    //3.將jSON格式中的Single位址UPDATE上去
                    for(var single =0;single <jaon_data.single_num;single++ ){
                        var div_single_set = document.getElementsByClassName('plc_area_1')[0].querySelector('#single_set').querySelector('#panel_sin'+(single+1));
                        div_single_set.querySelector('input').value= jaon_data.single_address[single].split(":")[0];
                        div_single_set.querySelector('select').value = jaon_data.single_address[single].split(":")[1];
                        console.log( div_single_set.querySelector('select').value);
                        
                    }
                    //4.將jSON格式中的Double位址UPDATE上去
                    for(var double =0;double <jaon_data.double_num;double++ ){
                        var div_double_set = document.getElementsByClassName('plc_area_1')[0].querySelector('#double_set').querySelector('#panel_dou'+(double+1));
                        div_double_set.querySelector('input').value= jaon_data.double_address[double].split(":")[0];
                        div_double_set.querySelector('select').value = jaon_data.double_address[double].split(":")[1];
                        console.log( div_double_set.querySelector('select').value);
                        
                    } 
                }

                

            }

            // console.log(data[0]['PLC1'][0].IP_address);

            // console.log(data[0].PLC1[0].IP_address);
           
           // console.log(document.getElementsByClassName('plc_area_1')[1].querySelector('#add_single'));

        });


       
     
        var class_div = document.getElementsByClassName('plc_area_1').length;
        for(var divnum = 0;divnum < class_div;divnum++){
            var divincon = document.getElementsByClassName('plc_area_1')[divnum];
            if(divincon.childNodes.length < 5){
                divincon.style.background = "url(static/add.png)";
                divincon.style.backgroundSize = "30%";
                divincon.style.backgroundAttachment = "scroll";
                divincon.style.backgroundRepeat ="no-repeat";
                divincon.style.backgroundPosition = "center"
                


            }else{
                divincon.style.background = (0,142,23);
            }
           
            //console.log(divincon.style);
            
        }
        document.getElementsByClassName('plc_area_1')[1].addEventListener("click",function(e){
            if(class_div2 == 0){
                var d = document.getElementsByClassName('plc_area_1')[0].cloneNode(true);
                //console.log(d.childNodes.length);
                for(var lend = 0;lend<d.childNodes.length;lend ++){
                   
                    this.appendChild(d.childNodes[lend].cloneNode(true));
                    console.log(d.childNodes[lend].id)
                }
                //this.appendChild(d);
                class_div2 = 1;
                this.style.background = null;
            }                   
            
        })
        document.getElementsByClassName('plc_area_1')[2].addEventListener("click",function(e){
            if(class_div3 == 0){
                var d = document.getElementsByClassName('plc_area_1')[0].cloneNode(true);
                //console.log(d.childNodes.length);
                for(var lend = 0;lend<d.childNodes.length;lend ++){
                   
                    this.appendChild(d.childNodes[lend].cloneNode(true));
                    console.log(d.childNodes[lend].id)
                }
                //this.appendChild(d);
                class_div3 = 1;
                this.style.background = null;
            }                   
            
        })
        document.getElementsByClassName('plc_area_1')[3].addEventListener("click",function(e){       
            if(class_div4 == 0){           
                var d = document.getElementsByClassName('plc_area_1')[0].cloneNode(true);
                for(var lend = 0;lend<d.childNodes.length;lend ++){
                   
                    this.appendChild(d.childNodes[lend].cloneNode(true));
                    console.log(d.childNodes[lend].id)
                }
                
                class_div4 = 1;
                this.style.background = null;
            }
        })
    }

    
	function text_pub(){
		var plc_num_json = "";

        //plc_num_json.filter()
        //var FX5U_address = document.querySelector('.plc_area_1 #plc_address').value;
        var class_div = document.getElementsByClassName('plc_area_1').length;//使用plc_area_1 class的數量

        var FX5U_address_array = new Array(4);
        var single_num_array = new Array(4);
        var single_input_array_2 = new Array(4);
        var double_num_array = new Array(4);
        var double_input_array_2 = new Array(4);
        for(var divnum = 0;divnum < class_div;divnum++){
            if(document.getElementById(document.getElementsByClassName('plc_area_1')[divnum].id).childNodes.length > 1)
            {
                var FX5U_address = document.getElementById(document.getElementsByClassName('plc_area_1')[divnum].id).querySelector('#plc_address').value;
                if(FX5U_address == ''){
                    return alert('請填入PLC IP位址');
                }
                var single_num =document.getElementById(document.getElementsByClassName('plc_area_1')[divnum].id).querySelector('#txt_1').value;
                var double_num = document.getElementById(document.getElementsByClassName('plc_area_1')[divnum].id).querySelector('#txt_2').value;
                //var single_node_num = document.querySelector('.plc_area_1 #single_set').childNodes.length;
                //var double_node_num = document.querySelector('.plc_area_1 #double_set').childNodes.length;
                var single_node_num = document.getElementById(document.getElementsByClassName('plc_area_1')[divnum].id).querySelector('#single_set').childNodes;
                var double_node_num = document.getElementById(document.getElementsByClassName('plc_area_1')[divnum].id).querySelector('#double_set').childNodes;
                //var single_text = document.querySelector('#single_set').childNodes[3].nodeName;
                var single_input_array = new Array(single_node_num.length);
                var double_input_array = new Array(double_node_num.length);
                var  single_input_count = 0;
                var  double_input_count = 0;

                for(var i =0;i<single_node_num.length;i++)
                {
                    if( single_node_num[i].nodeName == "DIV"){
                        var input_val = single_node_num[i].childNodes[2].value;
                        var select_val = single_node_num[i].childNodes[3].value;
                        single_input_array[single_input_count] = input_val+':'+select_val;
                        single_input_count ++;
                    
                    }
                }
                for(var i =0;i<double_node_num.length;i++)
                {
                    if( double_node_num[i].nodeName == "DIV"){
                        var input_val = double_node_num[i].childNodes[2].value;
                        var select_val = double_node_num[i].childNodes[3].value;
                        double_input_array[double_input_count] = input_val+':'+select_val;
                        double_input_count ++;
                    
                    }
                }
                

                
                FX5U_address_array[divnum] = FX5U_address;
                single_num_array[divnum] = single_num;
                single_input_array_2[divnum] = single_input_array.filter(d => d);
                double_num_array[divnum] = double_num;
                double_input_array_2[divnum] = double_input_array.filter(d => d);
                   

                
            
            }
          
        } 
        
       
        $.ajax({
             
            type: 'POST',
            url: " http://localhost:5000/FX5U_SQL" ,
            contentType: "application/json;charset=UTF-8",
            data: 
                JSON.stringify(
                    {      
                        "PLC1":[ 
                            {
                                "IP_address" : ''+FX5U_address_array[0]+'',
                                "single_num":single_num_array[0],
                                "single_address":single_input_array_2[0],
                                "double_num":double_num_array[0],
                                "double_address":double_input_array_2[0],
                            }
                        ],
                        "PLC2":[ 
                            {
                                "IP_address" : ''+FX5U_address_array[1]+'',
                                "single_num":single_num_array[1],
                                "single_address":single_input_array_2[1],
                                "double_num":double_num_array[1],
                                "double_address":double_input_array_2[1],
                            }
                        ],
                        "PLC3":[ 
                            {
                                "IP_address" : ''+FX5U_address_array[2]+'',
                                "single_num":single_num_array[2],
                                "single_address":single_input_array_2[2],
                                "double_num":double_num_array[2],
                                "double_address":double_input_array_2[2],
                            }
                        ],
                        "PLC4":[ 
                            {
                                "IP_address" : ''+FX5U_address_array[3]+'',
                                "single_num":single_num_array[3],
                                "single_address":single_input_array_2[3],
                                "double_num":double_num_array[3],
                                "double_address":double_input_array_2[3],
                            }
                        ],
                    }
                )
                
                ,
            dataType: 'json',

            success: function(data){
            // console.log('ajax result:')
            console.log(data)
            //console.log(plc_num_json.filter(d =>d));
            }

        });

	}
    var sin_count = 0;
    var dou_count = 0;
	function add_sin(e)
	{
        console.log(e.parentElement.getAttribute('id'));
        sin_count  = e.parentElement.querySelector('#txt_1').value;
        sin_count ++;
        var panel1 = document.createElement('div');
        var texts = document.createElement('input');
        var pxt = document.createElement('p');
        var select_box = document.createElement('select');
        var select_val = document.createElement('option');
        select_val.value = "M";
        select_val.text = "M";
        select_box.add(select_val);
        select_val = document.createElement('option');
        select_val.value = "D";
        select_val.text = "D";
        select_box.add(select_val);
        
        select_val = document.createElement('option');
        select_val.value = "X";
        select_val.text = "X";
        select_box.add(select_val);

        pxt.id = "Single";
        pxt.style.display = "inline";
        pxt.innerHTML = "Single位址 : ";
        panel1.appendChild(document.createElement('br'));
        panel1.appendChild(pxt);
        panel1.appendChild(texts);
        panel1.appendChild(select_box);
        panel1.id = 'panel_sin'+sin_count;

        e.parentElement.querySelector('#single_set').appendChild(panel1);
        e.parentElement.querySelector('#txt_1').value = sin_count;

        
	}

	function add_dou(e)
	{
        dou_count  = e.parentElement.querySelector('#txt_2').value;
        dou_count ++;
        var panel1 = document.createElement('div');
        var texts = document.createElement('input');
        var pxt = document.createElement('p');
        var select_box = document.createElement('select');
        var select_val = document.createElement('option');
        select_val.value = "M";
        select_val.text = "M";
        select_box.add(select_val);

        select_val = document.createElement('option');
        select_val.value = "D";
        select_val.text = "D";
        select_box.add(select_val);
  
        select_val = document.createElement('option');
        select_val.value = "X";
        select_val.text = "X";
        select_box.add(select_val);

        pxt.id = "Single";
        pxt.style.display = "inline";
        pxt.innerHTML = "Double位址 : ";
        panel1.appendChild(document.createElement('br'));
        panel1.appendChild(pxt);
        panel1.appendChild(texts);
        panel1.appendChild(select_box);
        panel1.id = 'panel_dou'+dou_count;
        e.parentElement.querySelector('#double_set').appendChild(panel1);
        e.parentElement.querySelector('#txt_2').value = dou_count;
 
        

	}



//     <script>

//     function onloadeve(){
//         var class_div3 = 0;
//         var class_div4 = 0;

//         var plc_num_json = new Array(4);
//         var class_div = document.getElementsByClassName('plc_area_1').length;
//         for(var divnum = 0;divnum < class_div;divnum++){
//             var divincon = document.getElementsByClassName('plc_area_1')[divnum];
//             if(divincon.childNodes.length < 5){
//                 divincon.style.background = "url(static/add.png)";
//                 divincon.style.backgroundSize = "30%";
//                 divincon.style.backgroundAttachment = "scroll";
//                 divincon.style.backgroundRepeat ="no-repeat";
//                 divincon.style.backgroundPosition = "center"
                


//             }else{
//                 divincon.style.background = (0,142,23);
//             }
           
//             //console.log(divincon.style);
            
//         }

//         document.getElementsByClassName('plc_area_1')[2].addEventListener("click",function(e){
//             if(class_div3 == 0){
//                 var d = document.getElementsByClassName('plc_area_1')[0].cloneNode(true);
//                 this.appendChild(d);
//                 class_div3 = 1;
//                 this.style.background = null;
//             }                   
            
//         })
//         document.getElementsByClassName('plc_area_1')[3].addEventListener("click",function(e){       
//             if(class_div4 == 0){           
//                 var d = document.getElementsByClassName('plc_area_1')[0].cloneNode(true);
//                 this.appendChild(d);
//                 class_div4 = 1;
//                 this.style.background = null;
//             }
//         })
//     }

    
// 	function text_pub(){
// 		var plc_num_json = new Array(4);
//         //plc_num_json.filter()
//         //var FX5U_address = document.querySelector('.plc_area_1 #plc_address').value;
//         var class_div = document.getElementsByClassName('plc_area_1').length;//使用plc_area_1 class的數量

//         for(var divnum = 0;divnum < class_div;divnum++){
//             if(document.getElementById(document.getElementsByClassName('plc_area_1')[divnum].id).childNodes.length > 5)
//             {
//                 var FX5U_address = document.getElementById(document.getElementsByClassName('plc_area_1')[divnum].id).querySelector('#plc_address').value;
//                 if(FX5U_address == ''){
//                     return alert('請填入PLC IP位址');
//                 }
//                 var single_num =document.getElementById(document.getElementsByClassName('plc_area_1')[divnum].id).querySelector('#txt_1').value;
//                 var double_num = document.getElementById(document.getElementsByClassName('plc_area_1')[divnum].id).querySelector('#txt_2').value;
//                 //var single_node_num = document.querySelector('.plc_area_1 #single_set').childNodes.length;
//                 //var double_node_num = document.querySelector('.plc_area_1 #double_set').childNodes.length;
//                 var single_node_num = document.getElementById(document.getElementsByClassName('plc_area_1')[divnum].id).querySelector('#single_set').childNodes;
//                 var double_node_num = document.getElementById(document.getElementsByClassName('plc_area_1')[divnum].id).querySelector('#double_set').childNodes;
//                 //var single_text = document.querySelector('#single_set').childNodes[3].nodeName;
//                 var single_input_array = new Array(single_node_num.length);
//                 var double_input_array = new Array(double_node_num.length);
//                 var  single_input_count = 0;
//                 var  double_input_count = 0;

//                 for(var i =0;i<single_node_num.length;i++)
//                 {
//                     if( single_node_num[i].nodeName == "DIV"){
//                         var input_val = single_node_num[i].childNodes[2].value;
//                         var select_val = single_node_num[i].childNodes[3].value;
//                         single_input_array[single_input_count] = input_val+':'+select_val;
//                         single_input_count ++;
                    
//                     }
//                 }
//                 for(var i =0;i<double_node_num.length;i++)
//                 {
//                     if( double_node_num[i].nodeName == "DIV"){
//                         var input_val = double_node_num[i].childNodes[2].value;
//                         var select_val = double_node_num[i].childNodes[3].value;
//                         double_input_array[double_input_count] = input_val+':'+select_val;
//                         double_input_count ++;
                    
//                     }
//                 }


//                 $.ajax({
             
//                     type: 'POST',
//                     url: " http://localhost:5000/FX5U_SQL" ,
//                     contentType: "application/json;charset=UTF-8",
//                     data: 
//                         JSON.stringify(
//                             {      
                                
//                             "IP_address" : ''+FX5U_address+'',
//                             "single_num":single_num,
//                             "single_address":single_input_array.filter(d => d),
//                             "double_num":double_num,
//                             "double_address":double_input_array.filter(d => d),

//                             }
//                         ),
//                     dataType: 'json',

//                     success: function(data){
//                     // console.log('ajax result:')
//                     console.log(data)
//                     //console.log(plc_num_json.filter(d =>d));
//                     }

//                 });
                   

                
            
//             }
          
//         } 

// 		// for(var i =0;i<single_node_num;i++)
// 		// {
//         //     if( document.querySelector('.plc_area_1 #single_set').childNodes[i].nodeName == "DIV"){
//         //         var input_val = document.querySelector('#single_set').childNodes[i].childNodes[2].value;
//         //         var select_val = document.querySelector('#single_set').childNodes[i].childNodes[3].value;
//         //         single_input_array[single_input_count] = input_val+':'+select_val;
//         //         single_input_count ++;
               
//         //     }

		    
// 		// }
//         // for(var i =0;i<double_node_num;i++)
// 		// {
//         //     if( document.querySelector('.plc_area_1 #double_set').childNodes[i].nodeName == "DIV"){
//         //         var input_val = document.querySelector('.plc_area_1 #double_set').childNodes[i].childNodes[2].value;
//         //         var select_val = document.querySelector('.plc_area_1 #double_set').childNodes[i].childNodes[3].value;
//         //         double_input_array[double_input_count] = input_val+':'+select_val;
//         //         double_input_count ++;
               
//         //     }

		    
// 		// }
//         // console.log(input_array );
//         // console.log(select_array );
// 	}
//     var sin_count = 0;
//     var dou_count = 0;
// 	function add_sin(e)
// 	{
//         console.log(e.parentElement.getAttribute('id'));
//         sin_count  = e.parentElement.querySelector('#txt_1').value;
//         sin_count ++;
//         var panel1 = document.createElement('div');
//         var texts = document.createElement('input');
//         var pxt = document.createElement('p');
//         var select_box = document.createElement('select');
//         var select_val = document.createElement('option');
//         select_val.value = "D";
//         select_val.text = "D";
//         select_box.add(select_val);
//         select_val = document.createElement('option');
//         select_val.value = "M";
//         select_val.text = "M";
//         select_box.add(select_val);
//         select_val = document.createElement('option');
//         select_val.value = "X";
//         select_val.text = "X";
//         select_box.add(select_val);

//         pxt.id = "Single";
//         pxt.style.display = "inline";
//         pxt.innerHTML = "Single位址 : ";
//         panel1.appendChild(document.createElement('br'));
//         panel1.appendChild(pxt);
//         panel1.appendChild(texts);
//         panel1.appendChild(select_box);
//         panel1.id = 'panel_sin'+sin_count;
//         // document.querySelector('.plc_area #single_set').appendChild( document.createElement('br'));
//         // document.querySelector('.plc_area #single_set').appendChild(pxt);
//         // document.querySelector('.plc_area #single_set').appendChild(texts);
//         // document.querySelector('.plc_area #single_set').appendChild(select_box);
//         //document.querySelector('.plc_area_1 #single_set').appendChild(panel1);
//         e.parentElement.querySelector('#single_set').appendChild(panel1);
//         //console.log( e.parentElement.querySelector('#txt_1'));
//         e.parentElement.querySelector('#txt_1').value = sin_count;
// 	    //console.log(document.querySelector('.plc_area'));
        
// 	}

// 	function add_dou(e)
// 	{
//         dou_count  = e.parentElement.querySelector('#txt_2').value;
//         dou_count ++;
//         var panel1 = document.createElement('div');
//         var texts = document.createElement('input');
//         var pxt = document.createElement('p');
//         var select_box = document.createElement('select');
//         var select_val = document.createElement('option');
//         select_val.value = "D";
//         select_val.text = "D";
//         select_box.add(select_val);
//         select_val = document.createElement('option');
//         select_val.value = "M";
//         select_val.text = "M";
//         select_box.add(select_val);
//         select_val = document.createElement('option');
//         select_val.value = "X";
//         select_val.text = "X";
//         select_box.add(select_val);

//         pxt.id = "Single";
//         pxt.style.display = "inline";
//         pxt.innerHTML = "Double位址 : ";
//         panel1.appendChild(document.createElement('br'));
//         panel1.appendChild(pxt);
//         panel1.appendChild(texts);
//         panel1.appendChild(select_box);
//         panel1.id = 'panel_dou'+dou_count;
//         //document.querySelector('.plc_area #double_set').appendChild( document.createElement('br'));
//         //document.querySelector('.plc_area #double_set').appendChild(pxt);
//         //document.querySelector('.plc_area #double_set').appendChild(texts);
//         //document.querySelector('.plc_area #double_set').appendChild(select_box);
//         e.parentElement.querySelector('#double_set').appendChild(panel1);
//         e.parentElement.querySelector('#txt_2').value = dou_count;
//         //document.querySelector('.plc_area_1 #double_set').appendChild(panel1);
//         //document.getElementById('txt_2').value = dou_count;
        

// 	}
// </script>