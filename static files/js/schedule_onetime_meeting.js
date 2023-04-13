const form = document.getElementById("form");

form.addEventListener('submit',(ev) => {
	ev.preventDefault();
})

let getDate = (self) => {
	var time = new Date(self.value);
	var year = time.getFullYear();
	var month = time.getMonth();
	var date = time.getDate();
}

let getTime = (self) => {
	var time = new Date(self.value);
	console.log(time)
	var hour = time.getHours();
	var minutes = time.getMinutes();
	var seconds = 0;

	console.log(hour)
	console.log(minutes)
}