
  $(document).ready(function(){

    //contact form handeler
    var contactForm=$(".contact-form")
    var contactFormMethod=contactForm.attr("method")
    var contactFormEndpoint=contactForm.attr("action")

    function displaySubmitting(submitBtn,defaultText,doSubmit){
      if (doSubmit){
        submitBtn.addClass("disabled")
        submitBtn.html("<i class='fa fa-spin fa-spinner'></i> Sending...")
      }else{
        submitBtn.removeClass("disabled")
        submitBtn.html(defaultText)
      }

    }
    contactForm.submit(function(event){
      event.preventDefault()

      var contactFormSubmitBtn=contactForm.find("[type='submit']")
      var contactFormSubmitBtnText=contactFormSubmitBtn.text()

      var contactFormData=contactForm.serialize()
      var thisForm=$(this)
      displaySubmitting(contactFormSubmitBtn,"",true)
      $.ajax({
        method:contactFormMethod,
        url:contactFormEndpoint,
        data:contactFormData,
        success:function(data){
          contactForm[0].reset()
          $.alert({
            title:"Success!",
            content:data.message,
            theme:"modern",
          })
          setTimeout(function(){
            displaySubmitting(contactFormSubmitBtn,contactFormSubmitBtnText,false)
          },2000)
        },
        error:function(error){
          console.log(error)

          var jsonData=error.responseJSON
          var msg=""
          $.each(jsonData,function(key,value){
            msg += key+":"+value[0].message+"</br>"
          })
          $.alert({
            title:"Oops!",
            content:msg,
             theme:"modern",
          })
          setTimeout(function(){
            displaySubmitting(contactFormSubmitBtn,contactFormSubmitBtnText,false)
          },2000)
        }
      })
    })


    //Auto search

    var searchForm=$(".search-form")
    var searchInput=searchForm.find("[name='q']")
    var typingTimer;
    var typingInterval=1500
    var searchBtn=searchForm.find("[type='submit']")

    searchInput.keyup(function(event){
      console.log(searchInput.val())
      clearTimeout(typingTimer)
      typingTimer=setTimeout(perfomSearch,typingInterval)

    })
    searchInput.keydown(function(event){
      clearTimeout(typingTimer)
    })
    function displaySearching(){
      searchBtn.addClass("disabled")
      searchBtn.html("<i class='fa fa-spin fa-spinner'></i> Searching...")
    }
    function perfomSearch(){
      displaySearching()
      var query=searchInput.val()
      setTimeout(function(){
        window.location.href='/search/?q='+query
      },1000)

    }








    //Cart +add products









    var productForm=$(".form-product-ajax")
    productForm.submit(function(event){
      event.preventDefault();
      var thisForm=$(this)
      //var actionEndpoint=thisForm.attr("action");
      var actionEndpoint=thisForm.attr("data-endpoint");
      var httpMethod=thisForm.attr("method");
      var formData=thisForm.serialize();


     $.ajax({
          url:actionEndpoint,
          method:httpMethod,
          data:formData,
          //type : 'POST',
          success: function(data){
            //  console.log(data)
           var submitSpan = thisForm.find(".submit-span")
           console.log(submitSpan.html())
           if(data.added){
             submitSpan.html('<button type="submit" class="btn btn-danger" name="button">Remove?</button>')
           }else{
            submitSpan.html('<button type="submit" class="btn btn-success" name="button">Add to cart</button>')
          }
          var navbarcount=$(".navbar_cart-count")
          navbarcount.text(data.cartItemsCount)
          if(window.location.href.indexOf("cart") != -1){
            refreshCart()
          }

         },
        error: function(errorData){
          $.alert({
            title:"Oops!",
            content:"An error occured",
            theme:"modern",
          })
     // //
      }
      })

      })
      function refreshCart(){
        console.log("cart")
        var cartTable=$(".cart-table")
        var cartBody=cartTable.find(".cart-body")
        //cartBody.html("<h1>Changed</h1>")
        var productRows=cartBody.find(".cart-products")
        var currentUrl=window.location.href


        var refreshCartUrl='/api/cart/';
        var refreshCartMethod="GET";
        var data={};
        $.ajax({
          url:refreshCartUrl,
          method:refreshCartMethod,
          data:data,
          success: function(data){
            console.log("success")
            console.log(data)
            var hiddenCartItemRemoveForm=$(".cart-item-remove-form")
            if(data.products.length > 0 ){
              productRows.html(" ")
              i=data.products.length
              $.each(data.products,function(index,value){
                var newCartItemRemove=hiddenCartItemRemoveForm.clone()
                newCartItemRemove.css("display","block")
                newCartItemRemove.find(".cart-item-product-id").val(value.id)
                cartBody.prepend("<tr><th scope=\"row\">"+i+"</th><td><a href='" +value.url+ "'>"+value.name+"</a>"+newCartItemRemove.html() + "</td><td>"+value.price+"</td></tr>")
                i--
              })
              cartBody.find(".card-subtotal").text(data.subtotal)
              cartBody.find(".card-total").text(data.total)
            }else{
              window.location.href=currentUrl
            }
          },
          error: function(errorData){
            $.alert({
              title:"Oops!",
              content:"An error occured",
              theme:"modern",
            })
          }
        })
      }

    });
