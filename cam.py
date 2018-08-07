#!/usr/bin/python3
import cgi
import cgitb
cgitb.enable()

print("Content-Type: text/html\n\n")

print("""
<html><head><title>CatCam</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>


<script>
window.setInterval(function(){
        var newImage = new Image();
        newImage.src = "cam.jpg?"+new Date().getTime();
        jQuery("#cam").attr("src",newImage.src);

},1000);
</script>

</head>
<body>
<div class="container">

<h1>CatCam</h1>

<div class="alert alert-success"></div>

<div class="jumbotron">
<img class="img-fluid" alt="Responsive Webcam image" src="cam.jpg" id="cam">
</div>

</div>
</body>
</html>
""")
