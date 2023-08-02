var main = document.getElementsByTagName('main')[0]
var url = new URL(`${window.location.protocol}//${window.location.host}/getUser`);

let getUser = (self) => {
	var name = self.value;
	console.log(name)
	url.searchParams.append('name',name)

	if (name.length > 0) {
		document.getElementById('divtwo').style.display = 'none'
		Array.from(document.getElementsByClassName('user')).forEach((item) => {
			item.remove()
		})

		fetch(url,{
        	method: 'GET'
	    }).then((response) => {
	        return response.json().then((data) => {
	            console.log(data);
	            data.forEach((item) => {
	            	var container = document.createElement('div')
	            	container.setAttribute('class','user');
	            	container.innerHTML = `
		                <img src = "${item.profile_picture}" class = "profile_picture" alt = "profile photo"/>
		                <p style = "margin-bottom: 0;" class = "username">${item.username} <a href = "/dialogue/${item.user_token}">join chatroom</a></p>
	            	`
	            	main.appendChild(container)
	            })
	        })
	    })
	}else {
		document.getElementById('divtwo').style.display = 'flex'

		Array.from(document.getElementsByClassName('user')).forEach((item) => {
			item.remove()
		})
	}
}