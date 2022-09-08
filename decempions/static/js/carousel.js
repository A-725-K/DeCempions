let cardsIndex = 0;

const showCard = (n) => {
	const cards = Array
		.from(document.getElementsByClassName('carousel-card'))
		.reverse();

	if (!cards.length) return;

	cardsIndex = n;
	
	if (cardsIndex > cards.length-1) cardsIndex = 0;
	if (cardsIndex < 0) cardsIndex = cards.length-1;

	cards.map((card) => card.style.display = 'none');
	cards[cardsIndex].style.display = 'flex';
};

const nextNthCard = (n) => { showCard(cardsIndex += n); };
const prevtNthCard = (n) => { showCard(cardsIndex -= n); };
