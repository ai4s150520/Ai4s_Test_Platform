document.addEventListener("DOMContentLoaded", function() {

    const scrollElements = document.querySelectorAll(".animate-on-scroll");

    const elementInView = (el, dividend = 1) => {
        const elementTop = el.getBoundingClientRect().top;
        return (
            elementTop <= (window.innerHeight || document.documentElement.clientHeight) / dividend
        );
    };

    const displayScrollElement = (element) => {
        element.classList.add("is-visible");
    };

    const hideScrollElement = (element) => {
        element.classList.remove("is-visible");
    };

    const handleScrollAnimation = () => {
        scrollElements.forEach((el) => {
            if (elementInView(el, 1.25)) {
                displayScrollElement(el);
            } else {
                // Optional: To re-animate every time it's scrolled to
                // hideScrollElement(el);
            }
        });
    };

    // Initial check on page load
    handleScrollAnimation();

    window.addEventListener("scroll", () => {
        handleScrollAnimation();
    });

});