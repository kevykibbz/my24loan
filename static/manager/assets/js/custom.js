/*proloader*/
function load()
{
  document.querySelector('.placeholder').style.display="none";
  document.querySelector('.main-display').style.display="block";
}

/*insection observer API */
function observerImages()
{
    var images=document.querySelectorAll('[data-src]'),
    imgOpts={},
    observer=new IntersectionObserver((entries,observer)=>
    {
        entries.forEach((entry)=>
        {
            if(!entry.isIntersecting) return;
            const img=entry.target;
            const newUrl=img.getAttribute('data-src');
            img.src=newUrl;
            observer.unobserve(img);
        });
    },imgOpts);
  
    images.forEach((image)=>
    {
      observer.observe(image)
    });
}

$(document).ready(function()
{
  observerImages();
});

/*submit register form*/
$(document).on('submit','.ContactForm',function()
{
  var el=$(this),
  btn_text=el.find('button:last').text(),
  form_data=new FormData(this);
  el.find("input,textarea,select").attr('aria-invalid',false).parents('.form-group').removeClass('error').find('.help-block').html('');
  el.children().find('.is-invalid').removeClass('is-invalid');
  el.parents('.form-wrapper').find('.load-overlay .loader-container').html(`<div class="loader"><svg class="circular" viewBox="25 25 50 50"><circle class="path" cx="50" cy="50" r="10" fill="none" stroke-width="2" stroke-miterlimit="10"/></svg></div>`);
  $.ajax(
    {
      url:el.attr('action'),
      method:el.attr('method'),
      dataType:'json',
      data:form_data,
      contentType:false,
      cache:false,
      processData:false,
      beforeSend:function()
      {
        el.parents('.form-wrapper').find('.load-overlay').show();
        el.find('button:last').attr('disabled',true).html('<i class="spinner-border spinner-border-sm" role="status"></i> Please wait...');
        el.parents('.form-wrapper').find('.overlay-close').removeClass('btn-remove');
      },
      success:function(callback)
      {
        el.parents('.form-wrapper').find('.overlay-close').addClass('btn-remove');
        el.parents('.form-wrapper').find('.load-overlay').hide();
        el.find('button:last').attr('disabled',false).text(btn_text);
        if(callback.valid)
        {
            el[0].reset();
            $('.small-model').modal({show:true});
            $('.small-model').find('.modal-title').text('Success');
            $('.small-model').find('.modal-body').html('<div class="text-success text-center"><i class="fa fa-check-circle"></i> '+callback.message+'</div>');
            if(callback.email)
            {
              window.location='/'+callback.email;
            }
            if(callback.login)
            {
              window.location='/accounts/login';
            }
            if(callback.home)
            {
              window.location='/onboarding';
            }
        }
        else
        {
            $.each(callback.form_errors,function(key,value)
            {
                el.find("input[aria-label='"+key+"']").attr('aria-invalid',true).parents('.form-group').addClass('error').find('.help-block').html('<ul role="alert"><li>'+value+'</li></ul>');
            });
        }
      },
      error:function(err)
      {
        el.parents('.form-wrapper').find('.overlay-close').addClass('btn-remove');
        el.find('button:last').attr('disabled',false).text(btn_text);
        el.parents('.form-wrapper').find('.load-overlay .loader-container').html('<span class="text-danger font-weight-bold"> <i class="zmdi zmdi-alert-triangle"></i> '+err.status+' :'+err.statusText+'</span>.');
      }
    });
  return false;
});