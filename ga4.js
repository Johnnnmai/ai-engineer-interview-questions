/* GA4 loader + key-event hooks (MPBX, 2026-11-27) */
(function(){var id='G-6JZKGJWRWP';var s=document.createElement('script');s.async=1;s.src='https://www.googletagmanager.com/gtag/js?id='+id;document.head.appendChild(s);
window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}window.gtag=window.gtag||gtag;gtag('js',new Date());gtag('config',id);
var CK=/gumroad\.com|buy\.stripe\.com|checkout\.stripe\.com|\/go\/|[#?&]pro\b|#pro|ad-free|\/success|\/checkout|\/buy/i;
document.addEventListener('click',function(e){var a=e.target&&e.target.closest&&e.target.closest('a[href],button[data-checkout]');if(!a)return;var h=a.href||a.getAttribute('data-checkout')||'';if(CK.test(h)){gtag('event','checkout_click',{link_url:h,link_text:(a.textContent||'').trim().slice(0,80),transport_type:'beacon'})}},true);
document.addEventListener('submit',function(e){var f=e.target;if(f&&f.querySelector&&f.querySelector('input[type=email]')){gtag('event','generate_lead',{form_id:f.id||f.getAttribute('action')||''})}},true);
})();
