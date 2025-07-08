const timerElement = document.getElementById('timer');
const interviewDate = timerElement.getAttribute('data-interview-date');
const startTime = timerElement.getAttribute('data-start-time');
const endTime = timerElement.getAttribute('data-end-time');

const startDateTime = new Date(`${interviewDate}T${startTime}`);


const updateTimer = () => {
	const now = new Date();
	const timeLeft = countdown(now, startDateTime, countdown.DAYS | countdown.HOURS | countdown.MINUTES | countdown.SECONDS);

	document.getElementById('timer').innerHTML = `${timeLeft.days}d 
												  ${timeLeft.hours}h 
												  ${timeLeft.minutes}m 
											      ${timeLeft.seconds}s`;
}

setInterval(updateTimer, 1000);


/*if (now < startDateTime) {
	updateTimer();
	setInterval(updateTimer, 1000);
}else {
	document.getElementById('timer').innerHTML = "Interview started or concluded."
}*/