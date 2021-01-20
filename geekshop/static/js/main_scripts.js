$( document ).on( 'click', '.details a', function(event) {
   if (event.target.hasAttribute('href')) {
       var link = event.target.href + 'ajax/';
           $.ajax({
               url: link,
               success: function (data) {
                   $('.details').html(data.result);
               }
           });

   }
});