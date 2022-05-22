let cardsIndex = 0;

const showCard = (n) => {
	let cards = document.getElementsByClassName('carousel-card');

	if (n > cards.length-1) cardsIndex = 0;
	if (n < 0) cardsIndex = cards.length-1;

	for (let i=0; i<cards.length; i++) cards[i].style.display = 'none';
	cards[cardsIndex].style.display = 'flex';
};

const changeCard = (n) => { showCard(cardsIndex += n); };

showCard(cardsIndex);
