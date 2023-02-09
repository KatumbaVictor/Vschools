const form=document.getElementById('form');form.addEventListener('submit',()=>{var button=form.lastElementChild;button.innerHTML="Submiting....";button.setAttribute('disabled','');button.style.color='rgba(255, 255, 255, 0.889)';})
function submit(){document.getElementById('form').lastElementChild.click();}
function back(){window.open('/login/','_self');};