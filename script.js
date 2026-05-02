document.addEventListener('DOMContentLoaded', () => {
    const slides = document.querySelectorAll('.slide');
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    const currentSlideNum = document.getElementById('currentSlideNum');
    const progressBar = document.getElementById('progressBar');
    
    let currentIndex = 0;
    const totalSlides = slides.length;

    function updatePresentation() {
        // Update slides classes
        slides.forEach((slide, index) => {
            if (index === currentIndex) {
                slide.classList.add('slide-active');
            } else {
                slide.classList.remove('slide-active');
            }
        });

        // Update progress text
        currentSlideNum.innerText = currentIndex + 1;

        // Update progress bar width
        const progressPercentage = ((currentIndex + 1) / totalSlides) * 100;
        progressBar.style.width = `${progressPercentage}%`;

        // Update Button States
        prevBtn.disabled = currentIndex === 0;
        nextBtn.disabled = currentIndex === totalSlides - 1;
    }

    function goToSlide(index) {
        if (index >= 0 && index < totalSlides) {
            currentIndex = index;
            updatePresentation();
        }
    }

    prevBtn.addEventListener('click', () => goToSlide(currentIndex - 1));
    nextBtn.addEventListener('click', () => goToSlide(currentIndex + 1));

    // Keyboard navigation
    document.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowRight' || e.key === 'Space' || e.key === ' ') {
            goToSlide(currentIndex + 1);
        } else if (e.key === 'ArrowLeft') {
            goToSlide(currentIndex - 1);
        }
    });

    // Initialize state
    updatePresentation();
});
