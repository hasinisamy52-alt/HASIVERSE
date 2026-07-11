/* ====================================
   HASIVERSE SCRIPT
==================================== */

document.addEventListener("DOMContentLoaded", function () {

    /* ===========================
       Smooth Scroll
    =========================== */

    document.querySelectorAll('a[href^="#"]').forEach(anchor => {

        anchor.addEventListener("click", function (e) {

            e.preventDefault();

            const target = document.querySelector(this.getAttribute("href"));

            if (target) {

                target.scrollIntoView({

                    behavior: "smooth"

                });

            }

        });

    });


    /* ===========================
       Scroll Reveal Animation
    =========================== */

    const observer = new IntersectionObserver((entries) => {

        entries.forEach(entry => {

            if (entry.isIntersecting) {

                entry.target.classList.add("show");

            }

        });

    }, {

        threshold: 0.2

    });

    document.querySelectorAll(
        ".feature-card, .stat-card, .testimonial-card, .why-card"
    ).forEach(el => {

        observer.observe(el);

    });


    /* ===========================
       Animated Counter
    =========================== */

    const counters = document.querySelectorAll(".stat-card h2");

    counters.forEach(counter => {

        const targetText = counter.innerText;

        const target = parseInt(targetText.replace(/\D/g, ""));

        if (isNaN(target)) return;

        let count = 0;

        const increment = Math.ceil(target / 100);

        const updateCounter = () => {

            if (count < target) {

                count += increment;

                counter.innerText = count;

                requestAnimationFrame(updateCounter);

            } else {

                counter.innerText = targetText;

            }

        };

        updateCounter();

    });

});