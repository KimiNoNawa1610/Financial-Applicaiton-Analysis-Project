const Animation = () => {

    const mobile = document.querySelector('.mobile-view');

    const links = document.querySelector('.links');

    const mobilelinks= document.querySelectorAll('.links li');

    

    mobile.addEventListener('click',()=>{

        //toggle Links

        links.classList.toggle('active');

        //Mobile Links Appears

        mobilelinks.forEach((links, indexes) => {

            if (links.style.animation) {

                links.style.animation = "";

            }
            else {

                links.style.animation = `linksFaded 0.5s ease forwards ${indexes / 5 + 0.5}s`;

            }

        });

        //Mobile Lines Animation

        mobile.classList.toggle('transform');

    });

}

Animation();
