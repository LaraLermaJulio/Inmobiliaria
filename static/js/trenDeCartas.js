// Carousel functionality
const carousel = document.querySelector('.properties-carousel');
const prevButton = document.querySelector('.carousel-button.prev');
const nextButton = document.querySelector('.carousel-button.next');
const propertyCards = document.querySelectorAll('.property-card');
let currentIndex = 0;
const cardsToShow = 3; 

function setupCarousel() {
     propertyCards.forEach(card => {
        card.style.flex = `0 0 ${100 / cardsToShow}%`;
    });
    
    if (propertyCards.length <= cardsToShow) {
        prevButton.style.display = 'none';
        nextButton.style.display = 'none';
    }
}

function updateCarousel() {
     const cardWidth = 100 / cardsToShow;
    const offset = -currentIndex * cardWidth;
    
    carousel.style.transition = 'transform 0.5s ease';
    carousel.style.transform = `translateX(${offset}%)`;
}

prevButton.addEventListener('click', () => {
    if (currentIndex > 0) {
        currentIndex--;
    } else {
        carousel.style.transition = 'none';
        currentIndex = propertyCards.length - cardsToShow;
        setTimeout(() => {
            carousel.style.transition = 'transform 0.5s ease';
            updateCarousel();
        }, 10);
    }
    updateCarousel();
});

nextButton.addEventListener('click', () => {
    if (currentIndex < propertyCards.length - cardsToShow) {
        currentIndex++;
    } else {
        currentIndex = 0;
    }
    updateCarousel();
});

window.addEventListener('DOMContentLoaded', setupCarousel);