document.addEventListener("DOMContentLoaded", () => {
    
    // --- SCROLL ANIMATION LOGIC (from your original setup) ---
    const scrollElements = document.querySelectorAll(".animate-on-scroll");

    const elementInView = (el, dividend = 1) => {
        const elementTop = el.getBoundingClientRect().top;
        return (
            elementTop <= (window.innerHeight || document.documentElement.clientHeight) / dividend
        );
    };
    const displayScrollElement = (element) => element.classList.add("is-visible");
    
    const handleScrollAnimation = () => {
        scrollElements.forEach((el) => {
            if (elementInView(el, 1.25)) {
                displayScrollElement(el);
            }
        });
    };
    window.addEventListener("scroll", handleScrollAnimation);
    handleScrollAnimation(); // Initial check on load


    // --- 3D TILT EFFECT LOGIC (NEW) ---
    const tiltContainer = document.querySelector(".tilt-container");

    if (tiltContainer) {
        const tiltImage = tiltContainer.querySelector(".tilt-image");
        const tiltIntensity = 15; // Controls the amount of tilt.

        // Event listener for mouse movement over the container
        tiltContainer.addEventListener("mousemove", (e) => {
            const { offsetWidth: width, offsetHeight: height } = tiltContainer;
            const { offsetX: x, offsetY: y } = e;

            // Calculate rotation values based on mouse position from the center
            const rotateY = tiltIntensity * (x / width - 0.5);
            const rotateX = -1 * tiltIntensity * (y / height - 0.5);

            // Apply the CSS transform to the image, making it tilt and scale up slightly
            tiltImage.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.05, 1.05, 1.05)`;
        });

        // Event listener for when the mouse leaves the container
        tiltContainer.addEventListener("mouseleave", () => {
            // Reset the image to its original state with a smooth, slow transition
            tiltImage.style.transition = 'transform 0.5s ease-in-out';
            tiltImage.style.transform = `perspective(1000px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)`;

            // After the reset animation is done, set the transition back to fast for the next hover
            setTimeout(() => {
                tiltImage.style.transition = 'transform 0.1s ease-out';
            }, 500);
        });
    }
});