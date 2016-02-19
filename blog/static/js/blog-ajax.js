
$( document ).ready(function() {
    $("button").click(function(event){
        var searchstring = $('#searchin');
        obj = searchstring.focus();
        var csrftoken = $.cookie('csrftoken');

        function csrfSafeMethod(method) {
            // these HTTP methods do not require CSRF protection
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });
        event.preventDefault();
        $.ajax({
        url: "http://localhost:8000/Anime/new/",
        type: 'post', 
        dataType: "json",
        data: {name: obj.val()},
        success: function(data) {
            var left = 2;
            var top = 5;
            
            //Delete results from last results
            var test = document.getElementById('cards');
            while (test.firstChild){
                test.removeChild(test.firstChild);
            }
            var x = 0;
            while (x < data.length){
               var places = [];
               var show = data[x];
               // Add fields to array, later add icons to bottom of show
               if (show.fields.netflix == true){
                  console.log("netflix");
                  places.push("netflix");
                }
               if (show.fields.crunchy == true){
                  places.push("crunchyroll");
               }
               if (show.fields.hulu == true){
                  places.push("hulu");
                }
               if (show.fields.funimation == true){
                  places.push("funimation");
               }
                // create div that is card for each show
               var div = document.createElement('div');
               $(div).hide();
               var parent = document.getElementById('cards');
               parent.appendChild(div);
               div.style.backgroundColor = 'rgba(50,50,50,0.2)';
               if (left > 100){
                    left = 2;
                    top+= 25;
               }
               // Styling and spacing of card
               div.style.height = "45%";
               div.style.width = "15%";
               div.style.marginLeft = left + "%";
               div.style.marginRight = "2%";
               div.style.marginTop = top + "%";
               div.style.position = "absolute";
               left += 20;
               $(div).css({"border-color": "rgb(255,179,56",
                            "border-width": "3%",
                            "border-style": "solid"});
               console.log(show.fields.image);
               var name = document.createElement('h2');
               var pic = document.createElement('div');
               
               div.appendChild(pic);
               //Setting up picture of show
               pic.style.position = "absolute";
               test2 = "http://localhost:8000/blog/media/" + show.fields.image;
               console.log(test2);
               $(pic).append('<img src="' + test2 +'"height = "80%" width = "130%"">');
               $(pic).children().css({"margin-top": "15%",
                                      "margin-left": "10%"})
             
               div.appendChild(name);
               $(name).text(show.fields.title);
               name.style.position = "absolute";
               name.style.textAlign = "center";
               name.style.fontSize = '175%';
               name.style.color = 'rgb(255,179,56)';
               name.style.marginLeft = "10%";
               name.style.marginTop = "0%";
               var siteLeft = 0;
               //Adding the company images to the shows
               for (i = 0; i < places.length; i++){
                  var site = document.createElement('div');
                  div.appendChild(site);
                  console.log(places[i] + places.length)
                  var netpic = "http://localhost:8000/blog/media/logos/" + places[i] + ".png";
                  $(site).append('<img src="' + netpic +'"height = "15%" width = "25%"">');
                  $(site).children().css({"margin-top": "130%",
                                          "margin-left": siteLeft + "%",
                                           "position": "absolute"})
                   siteLeft += 30;
               }
              
               x += 1;
               $(div).fadeIn(1800);
            }

            
        },
        failure: function(data) { 
            alert('Got an error dude');
        }
    });
    });
}); 