<!DOCTYPE html>
<html>
    <head>
        <title>Appname</title>
        <link rel="stylesheet" type="text/css" href="/static/css/lib.css">
        <link rel="stylesheet" type="text/css" href="/static/css/appname.css">
    </head>
    <body>
        <div id="appname">
            <div class="navbar navbar-fixed-top">
                <div class="navbar-inner">
                    <div class="container">
                        <a class="brand" href="#">Appname</a>
                        <div id="appnameheader" class="nav-collapse">
                            <ul id="appname-menu" class="nav">
                            </ul>
                        </div><!--/.nav-collapse -->
                    </div>
                </div>
            </div>
            <div id="appnamecontainer" class="container">
                <div id="appnameapp"></div>
            </div>
        </div>
        <script type="application/javascript" src="/static/script/libs.js"></script>
        <script type="application/javascript" src="/static/script/template.js"></script>
        <script type="application/javascript" src="/static/script/appname.js"></script>
        <script type="text/javascript">
        $(function(){
            var appname = new App.Appname.Router
            Backbone.history.start();
            App.Appname.router = appname;
        });
        </script>
    </body>
</html>
