$(document).ready(function(){
    // initialize form by hiding the result box
    $("#results_section").hide();

    var systemSelect = $("select[name='system']");
    var routeSelect = $("select[name='route']");
    var directionSelect = $("select[name='direction']");

    routeSelect.change(function () {
            directionSelect.empty();
            for (var i = 0; i < directionArray[routeSelect.val()].length; i++) {
                directionSelect.append($("<option />").val(directionArray[routeSelect.val()][i]).text(directionArray[routeSelect.val()][i]));
            }
    });

    systemSelect.change(function () {
        $.getJSON("/busschedule/routes", "system="+systemSelect.val(), function(json) {
            directionArray=[]
            routeSelect.empty();
            for (var i = 0; i < json.length; i++) {
                routeSelect.append($("<option />").val(json[i].route_short_name).text(json[i].route_short_name + " " + json[i].route_long_name));
                directionArray[json[i].route_short_name]= new Array(json[i].direction1, json[i].direction2);
            }
            routeSelect.change();
        });
    });

    $.getJSON("/busschedule/systems", function(json) {
        for (var i = 0; i < json.length; i++) {
            systemSelect.append($("<option />").val(json[i].agency_id).text(json[i].system_name));
        }
        systemSelect.change();
    });

    // if the form has already been used, and result box is visible
    //    briefly hide it
    $("#submit").click(function() {
        $("#results_section").hide();
        //if ($('#schedule > tbody').val() == null && $('#schedule > tbody').val() != null){}
        //else {
        //    $('#schedule').empty();
        //}
        var query='';
        query +='system='+$('#system').val();
        query +='&route='+$('#route').val();
        query +='&direction='+$('#direction').val();
        query +='&date='+$('#date').val();
        //alert(query);
        request_schedule(query);
    });
});

function request_schedule(query) {
    $.getJSON("/busschedule/stops", query, function(json) {
        //alert( "stops received: " + json.direction );
        build_table(json);
        showTable();
    });
}

function build_table(data) {
  var system = data['system'];
  var route = data['route'];
  var direction = data['direction'];
  var routeDisplayName = data['route_display_name'];
  var num_trips = data['trips'].length;
  var resultsSection = $('#results_section');
  resultsSection.empty();
  
  var html = '<h2>' + routeDisplayName +' (' + direction + ' )</h2>\n';
  html += '<table class="nicetable" id="schedule">';
  html += '<colgroup><col><col>';
  for (trip in data['trips']){
    html += '<col>'
  }
  html += '</colgroup>'
  html += '<tr><th>Stop ID</th><th>Stop Name</th>';
  for (trip in data['trips']){
    html+= '<th>'+data["trips"][trip]["run_number"]+'</th>';
  }
  html+= '</tr>'
  for (stop in data['trips'][0]['stops']){
    html+='<tr><td>'+data['trips'][0]['stops'][stop]['stop_id']+'</td>'
    html+='<td>'+data['trips'][0]['stops'][stop]['stop_short_name']+'</td>'
    for (trip in data['trips']){
      html+='<td>'+data['trips'][trip]['stops'][stop]['departure_time']+'</td>'
    }
    html+='</tr>'
  }
  html+='</table>'
  resultsSection.append(html);

}

function showTable() {
    $("#results_section").slideDown("fast");
}

