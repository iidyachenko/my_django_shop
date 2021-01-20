$( document ).on( 'click', '.details a', function(event) {
   if (event.target.hasAttribute('href')) {
       var link = event.target.href + 'ajax/';
       var link_array = link.split('/');
       console.log(link_array)
       console.log(link_array[4])
       if (link_array[3] === 'products') {
           $.ajax({
               url: link,
               success: function (data) {
                   $('.details').html(data.result);
               }
           });

           event.preventDefault();
       }
   }
});