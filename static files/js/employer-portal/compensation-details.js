var tagify = new Tagify(document.getElementById('benefits_and_incentives'));

document.getElementById('form').addEventListener('submit', () => {
	var tags = tagify.getCleanValue().map(tag => tag.value);
	document.getElementById('id_compensation-details-benefits_and_incentives').value = JSON.stringify(tags.join(','));
})