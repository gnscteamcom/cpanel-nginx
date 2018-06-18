<?php 
    $lang = $data['lang'];
?>
<link rel="stylesheet" href="css/ionicons.min.css">
<link rel="stylesheet" href="css/dataTables.bootstrap.css">
<link rel="stylesheet" href="css/responsive.dataTables.min.css">
<link rel="stylesheet" href="css/AdminLTE.css">
<link rel="stylesheet" href="css/style.css">
<link rel="stylesheet" href="css/skin-green.css">

<script src="js/jquery-3.2.1.min.js"></script>
<script src="../3rdparty/bootstrap/optimized/js/bootstrap.min.js"></script>

<script src="js/jquery.dataTables.min.js"></script>
<script src="js/dataTables.bootstrap.min.js"></script>
<script src="js/dataTables.responsive.min.js"></script>
<script src="js/responsive.bootstrap.min.js"></script>

<div id="cpnginx" class="header" >
  <nav class="nav navbar navbar-static-top nav2">
    <div class="container-fluid">
    <div class="navbar-header">
      
      <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar-collapse">
        <i class="fa fa-bars"></i>
      </button>
    </div>

    
    <div class="collapse navbar-collapse" id="navbar-collapse">
      <ul class="nav navbar-nav">
     <li>
         <a href="index.live.php"> <i class="fa fa-dashboard"></i> <?php echo $lang['home']; ?></a>
        </li>  
        
          <li>
            
             <a href="#" class="dropdown-toggle" data-toggle="dropdown" aria-expanded="false"><?php echo $lang['domain']; ?> <span class="caret"></span></a>
             
             <ul class="dropdown-menu" role="menu">
                 <li><a href="listdomain.live.php"><?php echo $lang['domain_sub1']; ?></a></li>
                 <li><a href="listredirection.live.php"> <?php echo $lang['domain_sub2']; ?></a></li>
                 <li><a href="listdirectorylisting.live.php"><?php echo $lang['domain_sub3']; ?></a></li>
                 <li><a href="listhotlink.live.php"><?php echo $lang['domain_sub4']; ?></a></li>
                 
             </ul>           
        </li>
          
        <li class="dropdown">
                      <a href="#" class="dropdown-toggle" data-toggle="dropdown" aria-expanded="false"><?php echo $lang['web_server']; ?><span class="caret"></span></a>
                      <ul class="dropdown-menu" role="menu">
                          
                          <li><a href="listnginxsite.live.php"><?php echo $lang['web_server_sub1']; ?></a></li>
                          <li><a href="switchwebserver.live.php"><?php echo $lang['web_server_sub2']; ?></a></li>
                        
                      </ul>
        </li>
        
                  
        <li class="dropdown">
                      <a href="#" class="dropdown-toggle" data-toggle="dropdown" aria-expanded="false"><?php echo $lang['php']; ?><span class="caret"></span></a>
                      <ul class="dropdown-menu" role="menu">
                          <li><a href="listphpversion.live.php"><?php echo $lang['php_sub1']; ?></a></li>
                          <li><a href="switchphpversion.live.php"><?php echo $lang['php_sub2']; ?></a></li>
                        
                      </ul>
        </li>
        
        
      
        
        
        <li>
            
             <a href="#" class="dropdown-toggle" data-toggle="dropdown" aria-expanded="false"><?php echo $lang['templates']; ?><span class="caret"></span></a>
             
             <ul class="dropdown-menu" role="menu">
                 <li><a href="listwebsiteapp.live.php"><?php echo $lang['templates_sub1']; ?></a></li>
                 <li><a href="viewwebsiteapp.live.php"><?php echo $lang['templates_sub2']; ?></a></li>
                 <li><a href="changewebsiteapp.live.php"><?php echo $lang['templates_sub3']; ?></a></li>
                
             </ul>           
        </li>
        
   
        
        <li class="dropdown">
          
        <a href="#" class="dropdown-toggle" data-toggle="dropdown" aria-expanded="false"><?php echo $lang['firewall']; ?><span class="caret"></span></a>
                  <ul class="dropdown-menu" role="menu">
                      <li><a href="domainfirewall.live.php"><?php echo $lang['firewall_sub1']; ?></a></li>
                    <li><a href="changefirewallsettings.live.php"><?php echo $lang['firewall_sub2']; ?></a></li>
                   
                  </ul>
        </li> 
        
        
        
        
        <li class="dropdown">
          
        <a href="#" class="dropdown-toggle" data-toggle="dropdown" aria-expanded="false"><?php echo $lang['cache']; ?><span class="caret"></span></a>
                  <ul class="dropdown-menu" role="menu">
                    <li><a href="listcachedomain.live.php"><?php echo $lang['cache_sub1']; ?></a></li>                   
                    <li><a href="changecachedomain.live.php"><?php echo $lang['cache_sub2']; ?></a></li>
                  </ul>
        </li> 
        

    
        <li class="dropdown">
                      <a href="#" class="dropdown-toggle" data-toggle="dropdown" aria-expanded="false"><?php echo $lang['help']; ?> <span class="caret"></span></a>
                      <ul class="dropdown-menu" role="menu">
                          <li><a href="https://cpnginx.com/documentation/"><?php echo $lang['help_sub1']; ?></a></li>           
                       
                      </ul>
        </li>
        
      </ul>
   
    </div>
    </div>
  </nav>
</div>