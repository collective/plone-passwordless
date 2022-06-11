require([
    'jquery'
  ], function($){
  
    var cycle = function(){
      $('h1').animate({
        left: '250px',
        opacity: '0.5',
        'font-size': '30px'
      }, function(){
        $('h1').animate({
          left: '0',
          opacity: '1',
          'font-size': '20px'
        }, function(){
          setTimeout(function(){
            cycle();
          }, 2000);
        });
      });
    };
  
    $(document).ready(function(){
        console.log('it works');
    //   cycle();
    });
});